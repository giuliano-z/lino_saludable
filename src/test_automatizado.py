#!/usr/bin/env python
"""
🔍 SCRIPT DE TESTING AUTOMATIZADO - LINO SALUDABLE
Automatiza las verificaciones técnicas antes del audit manual
"""
import os
import sys
import django
from pathlib import Path
import time
from decimal import Decimal

# Configurar Django
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root / 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from gestion.models import Producto, MateriaPrima, Venta, VentaDetalle, Compra
from gestion.validators import LinoValidator
import json

class LinoTester:
    """Clase para automatizar tests del sistema LINO"""
    
    def __init__(self):
        self.client = Client()
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'issues': []
        }
        self.admin_user = None
        
        # Colores para terminal
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.END = '\033[0m'
    
    def log_test(self, test_name, status, message="", is_warning=False):
        """Registra resultado de un test"""
        if status:
            print(f"{self.GREEN}✅ {test_name}{self.END}")
            if message:
                print(f"   {message}")
            self.results['passed'] += 1
        else:
            if is_warning:
                print(f"{self.YELLOW}⚠️  {test_name}{self.END}")
                self.results['warnings'] += 1
            else:
                print(f"{self.RED}❌ {test_name}{self.END}")
                self.results['failed'] += 1
            
            if message:
                print(f"   {message}")
                self.results['issues'].append({
                    'test': test_name,
                    'message': message,
                    'type': 'warning' if is_warning else 'error'
                })
    
    def setup_test_user(self):
        """Configura usuario para tests"""
        try:
            self.admin_user = User.objects.filter(is_superuser=True).first()
            if self.admin_user:
                self.client.force_login(self.admin_user)
                self.log_test("Setup usuario admin", True, f"Usuario: {self.admin_user.username}")
                return True
            else:
                self.log_test("Setup usuario admin", False, "No hay superusuarios disponibles")
                return False
        except Exception as e:
            self.log_test("Setup usuario admin", False, f"Error: {str(e)}")
            return False
    
    def test_database_integrity(self):
        """Test de integridad de base de datos"""
        print(f"\n{self.BLUE}🗄️  TESTING DATABASE INTEGRITY{self.END}")
        
        try:
            # Test 1: Contar registros principales
            productos_count = Producto.objects.count()
            materias_count = MateriaPrima.objects.count()
            ventas_count = Venta.objects.count()
            
            self.log_test("Database Connection", True, 
                         f"Productos: {productos_count}, Materias: {materias_count}, Ventas: {ventas_count}")
            
            # Test 2: Verificar productos con datos válidos
            productos_invalidos = Producto.objects.filter(precio__lte=0).count()
            self.log_test("Productos con precios válidos", productos_invalidos == 0,
                         f"Productos con precio inválido: {productos_invalidos}" if productos_invalidos > 0 else "")
            
            # Test 3: Verificar stock no negativos
            productos_stock_negativo = Producto.objects.filter(stock__lt=0).count()
            self.log_test("Productos sin stock negativo", productos_stock_negativo == 0,
                         f"Productos con stock negativo: {productos_stock_negativo}" if productos_stock_negativo > 0 else "")
            
            # Test 4: Verificar materias primas válidas
            materias_invalidas = MateriaPrima.objects.filter(costo_unitario__lt=0).count()
            self.log_test("Materias primas con costos válidos", materias_invalidas == 0,
                         f"Materias con costo inválido: {materias_invalidas}" if materias_invalidas > 0 else "")
            
            return True
        
        except Exception as e:
            self.log_test("Database Integrity", False, f"Error crítico: {str(e)}")
            return False
    
    def test_url_responses(self):
        """Test de URLs principales"""
        print(f"\n{self.BLUE}🌐 TESTING URL RESPONSES{self.END}")
        
        urls_to_test = [
            ('panel_control', 'gestion:panel_control'),
            ('lista_productos', 'gestion:lista_productos'), 
            ('crear_producto', 'gestion:crear_producto'),
            ('lista_ventas', 'gestion:lista_ventas'),
            ('crear_venta', 'gestion:crear_venta'),
            ('lista_compras', 'gestion:lista_compras'),
            ('crear_compra', 'gestion:crear_compra'),
        ]
        
        for name, url_name in urls_to_test:
            try:
                response = self.client.get(reverse(url_name))
                success = response.status_code in [200, 302]  # 302 = redirect válido
                
                if success:
                    if response.status_code == 200:
                        # Verificar que no sea una página de error
                        content = response.content.decode('utf-8')
                        has_error = 'Error 500' in content or 'Server Error' in content
                        self.log_test(f"URL {name}", not has_error,
                                     "Página carga con error 500" if has_error else "")
                    else:
                        self.log_test(f"URL {name}", True, f"Redirect ({response.status_code})")
                else:
                    self.log_test(f"URL {name}", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"URL {name}", False, f"Excepción: {str(e)}")
    
    def test_business_validations(self):
        """Test de validaciones de negocio"""
        print(f"\n{self.BLUE}🛡️  TESTING BUSINESS VALIDATIONS{self.END}")
        
        try:
            # Test 1: Validación de venta con stock insuficiente
            if Producto.objects.exists():
                producto = Producto.objects.first()
                
                # Simular venta con más stock del disponible
                detalles_test = [{
                    'producto_id': producto.id,
                    'cantidad': producto.stock + 100,  # Más del disponible
                    'precio_unitario': producto.precio
                }]
                
                es_valida, errores = LinoValidator.validar_venta_completa(detalles_test)
                self.log_test("Validación stock insuficiente", not es_valida,
                             f"Errores detectados: {len(errores)}" if not es_valida else "No detectó error de stock")
                
                # Test 2: Validación de venta válida
                detalles_validos = [{
                    'producto_id': producto.id,
                    'cantidad': min(1, producto.stock),  # Cantidad válida
                    'precio_unitario': producto.precio
                }]
                
                if producto.stock > 0:
                    es_valida, errores = LinoValidator.validar_venta_completa(detalles_validos)
                    self.log_test("Validación venta válida", es_valida,
                                 "Venta válida correctamente validada" if es_valida else f"Errores: {errores}")
                else:
                    self.log_test("Validación venta válida", True, "Saltado (no hay stock)", True)
            else:
                self.log_test("Validaciones de negocio", False, "No hay productos para testear")
            
            # Test 3: Sistema de alertas
            alertas = LinoValidator.obtener_productos_alertas_stock()
            has_alertas = isinstance(alertas, dict) and 'total_alertas' in alertas
            self.log_test("Sistema de alertas", has_alertas,
                         f"Total alertas: {alertas.get('total_alertas', 0)}" if has_alertas else "Error en sistema de alertas")
        
        except Exception as e:
            self.log_test("Business Validations", False, f"Error: {str(e)}")
    
    def test_forms_rendering(self):
        """Test de renderizado de formularios"""
        print(f"\n{self.BLUE}📝 TESTING FORMS RENDERING{self.END}")
        
        forms_to_test = [
            ('Crear Producto', 'gestion:crear_producto'),
            ('Crear Venta', 'gestion:crear_venta'), 
            ('Crear Compra', 'gestion:crear_compra'),
        ]
        
        for form_name, url_name in forms_to_test:
            try:
                response = self.client.get(reverse(url_name))
                if response.status_code == 200:
                    content = response.content.decode('utf-8')
                    
                    # Verificar elementos básicos de formulario
                    has_form = '<form' in content
                    has_csrf = 'csrfmiddlewaretoken' in content
                    has_submit = 'type="submit"' in content or 'btn' in content
                    
                    form_valid = has_form and has_csrf and has_submit
                    self.log_test(f"Form {form_name}", form_valid,
                                 "Formulario renderiza correctamente" if form_valid else "Faltan elementos del formulario")
                else:
                    self.log_test(f"Form {form_name}", False, f"No carga (status {response.status_code})")
                    
            except Exception as e:
                self.log_test(f"Form {form_name}", False, f"Error: {str(e)}")
    
    def test_static_files(self):
        """Test de archivos estáticos"""
        print(f"\n{self.BLUE}📦 TESTING STATIC FILES{self.END}")
        
        try:
            # Test CSS principal
            response = self.client.get('/static/css/custom.css')
            css_works = response.status_code == 200
            self.log_test("CSS principal", css_works, 
                         "CSS carga correctamente" if css_works else f"Status: {response.status_code}")
            
            # Test página principal para verificar que carga CSS
            response = self.client.get('/')
            if response.status_code in [200, 302]:
                # Si es redirect, seguir el redirect
                if response.status_code == 302:
                    response = self.client.get(response.url)
                
                if response.status_code == 200:
                    content = response.content.decode('utf-8')
                    has_css_links = 'stylesheet' in content
                    has_bootstrap = 'bootstrap' in content
                    
                    self.log_test("CSS en páginas", has_css_links,
                                 "CSS incluido en páginas" if has_css_links else "No se detecta CSS en HTML")
                    self.log_test("Bootstrap incluido", has_bootstrap,
                                 "Bootstrap detectado" if has_bootstrap else "Bootstrap no detectado")
                else:
                    self.log_test("Static Files Test", False, "Página principal no carga")
            else:
                self.log_test("Static Files Test", False, "No se puede acceder a página principal")
                
        except Exception as e:
            self.log_test("Static Files", False, f"Error: {str(e)}")
    
    def test_performance_basic(self):
        """Test básico de performance"""
        print(f"\n{self.BLUE}⚡ TESTING BASIC PERFORMANCE{self.END}")
        
        urls_performance = [
            ('Panel Control', 'gestion:panel_control'),
            ('Lista Productos', 'gestion:lista_productos'),
        ]
        
        for name, url_name in urls_performance:
            try:
                start_time = time.time()
                response = self.client.get(reverse(url_name))
                end_time = time.time()
                
                response_time = end_time - start_time
                is_fast = response_time < 3.0  # Menos de 3 segundos
                
                if response.status_code == 200:
                    self.log_test(f"Performance {name}", is_fast,
                                 f"Tiempo: {response_time:.2f}s {'(OK)' if is_fast else '(LENTO)'}")
                else:
                    self.log_test(f"Performance {name}", False, f"No cargó (status {response.status_code})")
                    
            except Exception as e:
                self.log_test(f"Performance {name}", False, f"Error: {str(e)}")
    
    def generate_report(self):
        """Genera reporte final"""
        print(f"\n{self.BLUE}{'='*70}{self.END}")
        print(f"{self.BLUE} 📊 REPORTE FINAL DE TESTING AUTOMATIZADO{self.END}")
        print(f"{self.BLUE}{'='*70}{self.END}")
        
        total_tests = self.results['passed'] + self.results['failed'] + self.results['warnings']
        success_rate = (self.results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   {self.GREEN}✅ Tests exitosos: {self.results['passed']}{self.END}")
        print(f"   {self.RED}❌ Tests fallidos: {self.results['failed']}{self.END}")
        print(f"   {self.YELLOW}⚠️  Advertencias: {self.results['warnings']}{self.END}")
        print(f"   📊 Tasa de éxito: {success_rate:.1f}%")
        
        if self.results['failed'] == 0:
            print(f"\n{self.GREEN}🎉 ¡TODOS LOS TESTS CRÍTICOS PASARON!{self.END}")
            print(f"{self.GREEN}✅ Sistema listo para testing manual detallado{self.END}")
        else:
            print(f"\n{self.RED}🚨 HAY {self.results['failed']} ISSUES CRÍTICAS{self.END}")
            print(f"{self.RED}❌ Resolver antes del testing manual{self.END}")
        
        if self.results['issues']:
            print(f"\n🔍 ISSUES ENCONTRADAS:")
            for i, issue in enumerate(self.results['issues'], 1):
                icon = "⚠️" if issue['type'] == 'warning' else "❌"
                print(f"   {icon} {i}. {issue['test']}: {issue['message']}")
        
        print(f"\n{self.BLUE}{'='*70}{self.END}")
        print(f"{self.BLUE}🚀 PRÓXIMO PASO: TESTING MANUAL DETALLADO CON AUDIT_PRE_PRODUCCION.md{self.END}")
        print(f"{self.BLUE}{'='*70}{self.END}")
        
        return self.results['failed'] == 0

def main():
    """Función principal"""
    print("🔍 INICIANDO TESTING AUTOMATIZADO DE LINO SALUDABLE...")
    
    tester = LinoTester()
    
    # Configurar usuario
    if not tester.setup_test_user():
        print("❌ No se pudo configurar usuario de prueba. Abortando.")
        return False
    
    # Ejecutar todos los tests
    tester.test_database_integrity()
    tester.test_url_responses() 
    tester.test_business_validations()
    tester.test_forms_rendering()
    tester.test_static_files()
    tester.test_performance_basic()
    
    # Generar reporte
    return tester.generate_report()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
