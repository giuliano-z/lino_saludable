#!/usr/bin/env python
"""
Script para limpiar datos de prueba del sistema LINO
Mantiene: Usuarios, Configuración
Elimina: Productos, Ventas, Compras, Recetas, Materias Primas
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import (
    Producto, MateriaPrima, Compra, Venta, VentaDetalle,
    Receta, RecetaMateriaPrima, MovimientoMateriaPrima
)
from django.contrib.auth import get_user_model

User = get_user_model()

def limpiar_datos():
    """Limpia todos los datos de prueba manteniendo usuarios y configuración"""
    
    print("\n" + "="*60)
    print("🧹 LIMPIEZA DE DATOS DE PRUEBA - LINO SALUDABLE")
    print("="*60 + "\n")
    
    # Contar datos antes
    print("📊 Datos actuales:")
    print(f"   - Productos: {Producto.objects.count()}")
    print(f"   - Materias Primas: {MateriaPrima.objects.count()}")
    print(f"   - Compras: {Compra.objects.count()}")
    print(f"   - Ventas: {Venta.objects.count()}")
    print(f"   - Recetas: {Receta.objects.count()}")
    print(f"   - Usuarios: {User.objects.count()} (NO se borrarán)")
    
    # Confirmar
    print("\n" + "⚠️  " + "="*56)
    print("⚠️  ADVERTENCIA: Esta acción eliminará TODOS los datos")
    print("⚠️  Mantiene: Usuarios y Configuración")
    print("⚠️  " + "="*56)
    
    confirmacion = input("\n¿Continuar? (escribir 'SI' para confirmar): ")
    
    if confirmacion != 'SI':
        print("\n❌ Operación cancelada")
        return
    
    print("\n🔄 Eliminando datos...")
    
    try:
        # Orden importante por dependencias
        print("   → Eliminando detalles de ventas...")
        count = VentaDetalle.objects.all().delete()[0]
        print(f"      ✅ {count} detalles eliminados")
        
        print("   → Eliminando ventas...")
        count = Venta.objects.all().delete()[0]
        print(f"      ✅ {count} ventas eliminadas")
        
        print("   → Eliminando ingredientes de recetas...")
        count = RecetaMateriaPrima.objects.all().delete()[0]
        print(f"      ✅ {count} ingredientes eliminados")
        
        print("   → Eliminando recetas...")
        count = Receta.objects.all().delete()[0]
        print(f"      ✅ {count} recetas eliminadas")
        
        print("   → Eliminando movimientos de materias primas...")
        count = MovimientoMateriaPrima.objects.all().delete()[0]
        print(f"      ✅ {count} movimientos eliminados")
        
        print("   → Eliminando compras...")
        count = Compra.objects.all().delete()[0]
        print(f"      ✅ {count} compras eliminadas")
        
        print("   → Eliminando productos...")
        count = Producto.objects.all().delete()[0]
        print(f"      ✅ {count} productos eliminados")
        
        print("   → Eliminando materias primas...")
        count = MateriaPrima.objects.all().delete()[0]
        print(f"      ✅ {count} materias primas eliminadas")
        
        print("\n" + "="*60)
        print("✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("="*60)
        
        print("\n📊 Estado final:")
        print(f"   - Productos: {Producto.objects.count()}")
        print(f"   - Materias Primas: {MateriaPrima.objects.count()}")
        print(f"   - Compras: {Compra.objects.count()}")
        print(f"   - Ventas: {Venta.objects.count()}")
        print(f"   - Recetas: {Receta.objects.count()}")
        print(f"   - Usuarios: {User.objects.count()} ✅ (mantenidos)")
        
        print("\n🎯 El sistema está listo para cargar datos reales")
        print("   Puedes usar el admin: http://127.0.0.1:8000/admin/")
        print("   O crear un script de carga personalizado\n")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la limpieza: {str(e)}")
        print("   Algunos datos pueden haber quedado parcialmente eliminados")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    limpiar_datos()
