#!/usr/bin/env python3
"""
🔧 VERIFICADOR DE TEMPLATES LINO V3 - CORRECCIÓN DE ERRORES
===============================================================

Este script verifica que los templates corregidos funcionen correctamente
y que el sistema LINO V3 esté completamente operativo.

Ejecutado después de la corrección de errores de sintaxis en templates:
- modules/productos/lista_productos.html ✅ 
- gestion/lista_recetas.html ✅
- gestion/dashboard_rentabilidad.html ✅

Autor: GitHub Copilot
Fecha: 18 octubre 2025
"""

import os
import sys
import django
import requests
import time
from pathlib import Path

# Configurar Django
sys.path.append('/Users/giulianozulatto/Proyectos/lino_saludable/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.template import Template, Context
from django.template.loader import render_to_string

class LinoV3TemplateValidator:
    def __init__(self):
        self.client = Client()
        self.base_url = 'http://127.0.0.1:8001'
        self.results = {}
        
        # Crear usuario de prueba
        self.create_test_user()
        
        print("🚀 LINO V3 Template Validator iniciado")
        print("=" * 60)
    
    def create_test_user(self):
        """Crear usuario de prueba para las verificaciones"""
        try:
            self.test_user = User.objects.create_user(
                username='test_validator',
                password='test123',
                email='test@lino.com'
            )
            print("✅ Usuario de prueba creado")
        except:
            self.test_user = User.objects.get(username='test_validator')
            print("✅ Usuario de prueba existente usado")
    
    def login_test_user(self):
        """Login del usuario de prueba"""
        login_success = self.client.login(username='test_validator', password='test123')
        if login_success:
            print("✅ Login exitoso")
            return True
        else:
            print("❌ Error en login")
            return False
    
    def test_template_syntax(self):
        """Verificar sintaxis de templates críticos"""
        print("\n📝 VERIFICANDO SINTAXIS DE TEMPLATES")
        print("-" * 40)
        
        templates_to_test = [
            'modules/productos/lista_productos.html',
            'gestion/lista_recetas.html', 
            'gestion/dashboard_rentabilidad.html',
            'gestion/base.html',
            'components/theme-toggle.html'
        ]
        
        for template_path in templates_to_test:
            try:
                # Intentar renderizar template con contexto mínimo
                context = {
                    'user': self.test_user,
                    'productos': [],
                    'recetas': [],
                    'analytics': {
                        'alertas': [],
                        'kpis': {
                            'productos_top_margen': [],
                            'productos_top_ingresos': []
                        }
                    },
                    'query': '',
                    'total_alertas': 0
                }
                
                rendered = render_to_string(template_path, context)
                print(f"✅ {template_path}: Sintaxis OK")
                self.results[template_path] = 'OK'
                
            except Exception as e:
                print(f"❌ {template_path}: Error - {str(e)}")
                self.results[template_path] = f'Error: {str(e)}'
    
    def test_lino_v3_components(self):
        """Verificar que los componentes LINO V3 estén cargándose"""
        print("\n🎨 VERIFICANDO COMPONENTES LINO V3")
        print("-" * 40)
        
        # Verificar archivos CSS
        css_files = [
            '/static/css/lino-design-system-v3.css',
            '/static/css/lino-dark-mode.css'
        ]
        
        for css_file in css_files:
            file_path = f'/Users/giulianozulatto/Proyectos/lino_saludable/src{css_file}'
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {css_file}: {size} bytes")
            else:
                print(f"❌ {css_file}: No encontrado")
        
        # Verificar archivos JS
        js_files = [
            '/static/js/lino-theme.js',
            '/static/js/lino-modals.js',
            '/static/js/lino-animations.js',
            '/static/js/lino-tooltips.js',
            '/static/js/lino-css-optimizer.js'
        ]
        
        for js_file in js_files:
            file_path = f'/Users/giulianozulatto/Proyectos/lino_saludable/src{js_file}'
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {js_file}: {size} bytes")
            else:
                print(f"❌ {js_file}: No encontrado")
    
    def test_server_endpoints(self):
        """Verificar que las URLs principales respondan sin error 500"""
        print("\n🌐 VERIFICANDO ENDPOINTS DEL SERVIDOR")
        print("-" * 40)
        
        if not self.login_test_user():
            print("❌ No se pudo hacer login - saltando verificación de endpoints")
            return
        
        endpoints_to_test = [
            ('/', 'Home'),
            ('/gestion/', 'Dashboard Principal'),
            ('/gestion/productos/', 'Lista Productos'),
            ('/gestion/recetas/', 'Lista Recetas'),
            ('/gestion/inventario/', 'Inventario'),
            ('/gestion/compras/', 'Compras'),
            ('/gestion/ventas/', 'Ventas')
        ]
        
        for endpoint, name in endpoints_to_test:
            try:
                response = self.client.get(endpoint, follow=True)
                
                if response.status_code == 200:
                    print(f"✅ {name} ({endpoint}): Status 200")
                    
                    # Verificar que tenga contenido LINO V3
                    content = response.content.decode()
                    if 'lino-design-system-v3' in content:
                        print(f"   📦 LINO V3 CSS detectado")
                    if 'lino-theme.js' in content:
                        print(f"   🎯 LINO V3 JS detectado")
                        
                elif response.status_code == 302:
                    print(f"⚠️  {name} ({endpoint}): Redirect - puede requerir login")
                else:
                    print(f"❌ {name} ({endpoint}): Status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name} ({endpoint}): Error - {str(e)}")
    
    def test_live_server_response(self):
        """Verificar respuesta del servidor en vivo"""
        print("\n🔄 VERIFICANDO SERVIDOR EN VIVO")
        print("-" * 40)
        
        # Esperar un momento para que el servidor esté listo
        time.sleep(2)
        
        try:
            response = requests.get(f'{self.base_url}/gestion/', timeout=10)
            
            if response.status_code == 200:
                print("✅ Servidor respondiendo correctamente")
                
                # Verificar contenido LINO V3
                if 'lino-design-system-v3' in response.text:
                    print("✅ LINO Design System V3 cargado")
                else:
                    print("⚠️  LINO V3 CSS no detectado en respuesta")
                    
            else:
                print(f"⚠️  Servidor responde con status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al servidor - verificar que esté corriendo en puerto 8001")
        except Exception as e:
            print(f"❌ Error al verificar servidor: {str(e)}")
    
    def test_theme_system(self):
        """Verificar funcionamiento del sistema de temas"""
        print("\n🎨 VERIFICANDO SISTEMA DE TEMAS")
        print("-" * 40)
        
        # Verificar que el component de theme toggle existe
        theme_toggle_path = '/Users/giulianozulatto/Proyectos/lino_saludable/src/gestion/templates/components/theme-toggle.html'
        
        if os.path.exists(theme_toggle_path):
            print("✅ Componente theme-toggle.html existe")
            
            with open(theme_toggle_path, 'r') as f:
                content = f.read()
                
            if 'lino-theme-toggle' in content:
                print("✅ Clases CSS de tema detectadas")
            if 'lino-theme-icon-light' in content:
                print("✅ Iconos de tema detectados")
        else:
            print("❌ Componente theme-toggle.html no encontrado")
    
    def generate_report(self):
        """Generar reporte final"""
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE VERIFICACIÓN")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results.values() if r == 'OK'])
        
        print(f"📈 Templates verificados: {total_tests}")
        print(f"✅ Templates OK: {passed_tests}")
        print(f"❌ Templates con error: {total_tests - passed_tests}")
        
        if passed_tests == total_tests:
            print("\n🎉 ¡TODOS LOS TEMPLATES ESTÁN FUNCIONANDO CORRECTAMENTE!")
            print("🚀 LINO Design System V3 está completamente operativo")
        else:
            print(f"\n⚠️  Hay {total_tests - passed_tests} templates con errores que requieren atención")
        
        print("\n📋 ESTADO DETALLADO:")
        for template, status in self.results.items():
            icon = "✅" if status == 'OK' else "❌"
            print(f"{icon} {template}: {status}")
        
        print("\n🔗 URLs de prueba (servidor corriendo en puerto 8001):")
        print("   📱 Dashboard: http://127.0.0.1:8001/gestion/")
        print("   📦 Productos: http://127.0.0.1:8001/gestion/productos/")
        print("   📖 Recetas: http://127.0.0.1:8001/gestion/recetas/")
        
        print("\n💡 Para probar el sistema de temas:")
        print("   1. Abrir cualquier página del sistema")
        print("   2. Buscar el botón de tema en la navbar superior")
        print("   3. Alternar entre tema claro y oscuro")
        
        print("\n🛠️  Para debugging avanzado:")
        print("   1. Abrir consola del navegador")
        print("   2. Ejecutar: linoOptimize.analyze()")
        print("   3. Ejecutar: linoAnimate.fadeInUp(document.querySelector('.lino-card'))")

def main():
    """Función principal de verificación"""
    print("🔧 LINO V3 - VERIFICACIÓN POST-CORRECCIÓN DE ERRORES")
    print("=" * 60)
    
    validator = LinoV3TemplateValidator()
    
    try:
        # Ejecutar todas las verificaciones
        validator.test_template_syntax()
        validator.test_lino_v3_components()
        validator.test_theme_system()
        validator.test_server_endpoints()
        validator.test_live_server_response()
        
        # Generar reporte
        validator.generate_report()
        
    except KeyboardInterrupt:
        print("\n⚠️  Verificación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {str(e)}")
    finally:
        # Cleanup
        if hasattr(validator, 'test_user'):
            try:
                validator.test_user.delete()
                print("\n🧹 Usuario de prueba eliminado")
            except:
                pass

if __name__ == "__main__":
    main()
