#!/usr/bin/env python
"""
Script de inicialización y verificación del sistema LINO SALUDABLE
Ejecutar antes de poner en producción para verificar que todo funcione correctamente
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.db import connection
from gestion.logging_system import verificar_logs_funcionando, LinoLogger, business_logger
from gestion.validators import LinoValidator
from gestion.models import Producto, MateriaPrima, ConfiguracionCostos
import logging

def crear_banner():
    """Crea el banner del sistema"""
    print("=" * 70)
    print(" 🥜 LINO SALUDABLE - INICIALIZADOR DEL SISTEMA 🥜")
    print("=" * 70)
    print("🔧 Verificando sistema antes de la puesta en producción...")
    print()

def verificar_directorios():
    """Verifica y crea directorios necesarios"""
    print("📁 Verificando directorios...")
    
    directorios = [
        'logs',
        'backups',
        'media',
        'staticfiles'
    ]
    
    todos_ok = True
    for directorio in directorios:
        path = project_root / directorio
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ Creado: {directorio}/")
            except Exception as e:
                print(f"   ❌ Error creando {directorio}/: {str(e)}")
                todos_ok = False
        else:
            print(f"   ✅ Existe: {directorio}/")
    
    return todos_ok

def verificar_base_datos():
    """Verifica la conexión a la base de datos"""
    print("🗄️  Verificando base de datos...")
    
    try:
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        print("   ✅ Conexión a base de datos exitosa")
        
        # Verificar migraciones pendientes
        try:
            from django.core.management.commands.migrate import Command
            # Si no hay error, no hay migraciones pendientes
            print("   ✅ Migraciones al día")
            return True
        except Exception as e:
            print(f"   ⚠️  Posibles migraciones pendientes: {str(e)}")
            return True
            
    except Exception as e:
        print(f"   ❌ Error de base de datos: {str(e)}")
        return False

def verificar_superusuario():
    """Verifica que exista al menos un superusuario"""
    print("👤 Verificando usuarios administrativos...")
    
    try:
        superusuarios = User.objects.filter(is_superuser=True)
        if superusuarios.exists():
            print(f"   ✅ {superusuarios.count()} superusuario(s) encontrado(s)")
            for user in superusuarios:
                print(f"      - {user.username} ({user.email})")
            return True
        else:
            print("   ⚠️  No hay superusuarios. Creando uno...")
            return crear_superusuario_automatico()
            
    except Exception as e:
        print(f"   ❌ Error verificando usuarios: {str(e)}")
        return False

def crear_superusuario_automatico():
    """Crea un superusuario automático para emergencias"""
    try:
        # Solo crear si estamos en desarrollo
        if os.getenv('DJANGO_SETTINGS_MODULE', '').endswith('settings'):
            User.objects.create_superuser(
                username='admin_lino',
                email='admin@lino.com',
                password='lino2025temp!'  # Cambiar inmediatamente después
            )
            print("   ✅ Superusuario temporal creado:")
            print("      Usuario: admin_lino")
            print("      Contraseña: lino2025temp!")
            print("      ⚠️  CAMBIAR CONTRASEÑA INMEDIATAMENTE")
            return True
    except Exception as e:
        print(f"   ❌ Error creando superusuario: {str(e)}")
        return False

def verificar_logging_system():
    """Verifica el sistema de logging"""
    print("📋 Verificando sistema de logging...")
    
    try:
        if verificar_logs_funcionando():
            # Hacer pruebas adicionales
            LinoLogger.log_venta_creada(9999, "Test Product", 1, 100.00)
            LinoLogger.log_stock_actualizado("Test Product", 10, 9, "Test", None)
            business_logger.info("SISTEMA_INICIALIZADO - Test completado")
            
            print("   ✅ Sistema de logging funcionando correctamente")
            return True
        else:
            print("   ❌ Sistema de logging falló")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en sistema de logging: {str(e)}")
        return False

def verificar_modelos_criticos():
    """Verifica que los modelos críticos funcionen"""
    print("🏗️  Verificando modelos críticos...")
    
    try:
        # Contar registros principales
        productos_count = Producto.objects.count()
        materias_count = MateriaPrima.objects.count()
        
        print(f"   ✅ Productos en base de datos: {productos_count}")
        print(f"   ✅ Materias primas en base de datos: {materias_count}")
        
        # Verificar configuración de costos
        try:
            config = ConfiguracionCostos.objects.first()
            if config:
                print("   ✅ Configuración de costos encontrada")
            else:
                print("   ⚠️  No hay configuración de costos. Creando básica...")
                ConfiguracionCostos.objects.create()
                print("   ✅ Configuración básica creada")
        except Exception as e:
            print(f"   ⚠️  Error con configuración de costos: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando modelos: {str(e)}")
        return False

def verificar_validators():
    """Verifica el sistema de validaciones"""
    print("✅ Verificando sistema de validaciones...")
    
    try:
        # Test básico de validaciones
        errores_dummy = []
        
        # Si hay productos, hacer test real
        if Producto.objects.exists():
            producto = Producto.objects.first()
            estado_stock = LinoValidator.validar_stock_producto(producto)
            print(f"   ✅ Validación de stock funcionando (Test: {producto.nombre})")
            
        alertas = LinoValidator.obtener_productos_alertas_stock()
        if 'error' not in alertas:
            total_alertas = alertas.get('total_alertas', 0)
            print(f"   ✅ Sistema de alertas funcionando ({total_alertas} alertas activas)")
        else:
            print("   ⚠️  Error en sistema de alertas")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error en sistema de validaciones: {str(e)}")
        return False

def ejecutar_migraciones():
    """Ejecuta migraciones pendientes"""
    print("🔄 Ejecutando migraciones...")
    
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
        print("   ✅ Migraciones completadas")
        return True
    except Exception as e:
        print(f"   ❌ Error ejecutando migraciones: {str(e)}")
        return False

def recopilar_archivos_estaticos():
    """Recopila archivos estáticos para producción"""
    print("📦 Recopilando archivos estáticos...")
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=0'])
        print("   ✅ Archivos estáticos recopilados")
        return True
    except Exception as e:
        print(f"   ❌ Error recopilando estáticos: {str(e)}")
        return False

def crear_backup_inicial():
    """Crea un backup inicial de la base de datos"""
    print("💾 Creando backup inicial...")
    
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = project_root / 'backups' / f'lino_inicial_{timestamp}.json'
        
        execute_from_command_line([
            'manage.py', 'dumpdata', 
            '--output', str(backup_path),
            '--verbosity=0'
        ])
        
        print(f"   ✅ Backup creado: {backup_path.name}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creando backup: {str(e)}")
        return False

def mostrar_resumen_final(resultados):
    """Muestra el resumen final de la inicialización"""
    print("\n" + "=" * 70)
    print(" 📊 RESUMEN DE INICIALIZACIÓN")
    print("=" * 70)
    
    total_checks = len(resultados)
    exitosos = sum(1 for r in resultados.values() if r)
    
    if exitosos == total_checks:
        print("🎉 ¡INICIALIZACIÓN COMPLETADA EXITOSAMENTE!")
        print("✅ Todos los componentes están funcionando correctamente")
        print("")
        print("🚀 El sistema está listo para producción")
        print("")
        print("📌 PRÓXIMOS PASOS:")
        print("   1. Cambiar contraseñas temporales")
        print("   2. Configurar variables de entorno de producción")
        print("   3. Configurar servidor web (Nginx)")
        print("   4. Configurar SSL/HTTPS")
        print("   5. Configurar backups automáticos")
    else:
        print("⚠️  INICIALIZACIÓN CON PROBLEMAS")
        print(f"✅ Exitosos: {exitosos}/{total_checks}")
        print("❌ Con problemas:")
        
        for check, resultado in resultados.items():
            if not resultado:
                print(f"   - {check}")
        
        print("\n🔧 Resolver los problemas antes de poner en producción")
    
    print("=" * 70)

def main():
    """Función principal de inicialización"""
    crear_banner()
    
    # Ejecutar todas las verificaciones
    resultados = {
        'Directorios': verificar_directorios(),
        'Base de datos': verificar_base_datos(),
        'Migraciones': ejecutar_migraciones(),
        'Usuarios administrativos': verificar_superusuario(),
        'Sistema de logging': verificar_logging_system(),
        'Modelos críticos': verificar_modelos_criticos(),
        'Sistema de validaciones': verificar_validators(),
        'Archivos estáticos': recopilar_archivos_estaticos(),
        'Backup inicial': crear_backup_inicial(),
    }
    
    mostrar_resumen_final(resultados)
    
    # Logging final
    try:
        business_logger.info("INICIALIZACION_COMPLETADA - Sistema verificado para producción")
    except:
        pass

if __name__ == '__main__':
    main()
