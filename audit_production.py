#!/usr/bin/env python3
"""
🔍 AUDITORÍA AUTOMATIZADA DEL SERVIDOR PRODUCCIÓN
Script para verificar que TODO funcione al 100% en Railway

Ejecutar:
    python audit_production.py
"""

import requests
from datetime import datetime
from typing import Dict, List, Tuple
import json


# ==================== CONFIGURACIÓN ====================

BASE_URL = "https://web-production-b0ad1.up.railway.app"
TIMEOUT = 10  # segundos

# Credenciales por defecto (desde createusers.py)
DEFAULT_CREDENTIALS = {
    'username': 'sister_emprendedora',
    'password': 'SisterLino2025!'
}

# ==================== UTILIDADES ====================

class Colors:
    """Colores para terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """Imprime un header bonito"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")


def print_test(name: str, success: bool, detail: str = ""):
    """Imprime resultado de un test"""
    icon = "✅" if success else "❌"
    color = Colors.GREEN if success else Colors.RED
    status = "PASS" if success else "FAIL"
    
    print(f"{icon} {color}{status}{Colors.END} - {name}")
    if detail:
        print(f"   {Colors.YELLOW}→ {detail}{Colors.END}")


def print_warning(text: str):
    """Imprime una advertencia"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text: str):
    """Imprime información"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


# ==================== TESTS DE AUDITORÍA ====================

class ProductionAuditor:
    """Clase para auditar el servidor de producción"""
    
    def __init__(self):
        self.session = requests.Session()
        self.results = {}
        self.logged_in = False
    
    def test_server_online(self) -> bool:
        """TEST 1: Verificar servidor está online"""
        print_header("TEST 1: SERVIDOR ONLINE")
        
        try:
            response = self.session.get(f"{BASE_URL}/", timeout=TIMEOUT)
            success = response.status_code == 200
            
            print_test(
                "Servidor responde",
                success,
                f"Status Code: {response.status_code}"
            )
            
            if success:
                print_info(f"URL: {BASE_URL}")
                print_info(f"Response Time: {response.elapsed.total_seconds():.2f}s")
            
            return success
        except Exception as e:
            print_test("Servidor responde", False, str(e))
            return False
    
    def test_https_enabled(self) -> bool:
        """TEST 2: Verificar HTTPS está activo"""
        print_header("TEST 2: HTTPS HABILITADO")
        
        try:
            success = BASE_URL.startswith('https://')
            print_test("HTTPS activo", success, f"URL: {BASE_URL}")
            return success
        except Exception as e:
            print_test("HTTPS activo", False, str(e))
            return False
    
    def test_admin_accessible(self) -> bool:
        """TEST 3: Verificar admin Django accesible"""
        print_header("TEST 3: ADMIN DJANGO ACCESIBLE")
        
        try:
            response = self.session.get(f"{BASE_URL}/admin/login/", timeout=TIMEOUT)
            success = response.status_code == 200
            
            print_test(
                "Admin login page carga",
                success,
                f"Status: {response.status_code}"
            )
            
            if success:
                has_csrf = 'csrfmiddlewaretoken' in response.text
                print_test("CSRF token presente", has_csrf)
            
            return success
        except Exception as e:
            print_test("Admin login page carga", False, str(e))
            return False
    
    def test_login(self) -> bool:
        """TEST 4: Verificar login funciona"""
        print_header("TEST 4: LOGIN FUNCIONAL")
        
        try:
            # 1. Obtener CSRF token
            response = self.session.get(f"{BASE_URL}/admin/login/", timeout=TIMEOUT)
            
            if 'csrftoken' not in self.session.cookies:
                print_test("Obtener CSRF token", False, "No CSRF cookie")
                return False
            
            csrf_token = self.session.cookies['csrftoken']
            print_test("Obtener CSRF token", True, f"Token: {csrf_token[:20]}...")
            
            # 2. Hacer login
            login_data = {
                'username': DEFAULT_CREDENTIALS['username'],
                'password': DEFAULT_CREDENTIALS['password'],
                'csrfmiddlewaretoken': csrf_token,
                'next': '/admin/'
            }
            
            response = self.session.post(
                f"{BASE_URL}/admin/login/",
                data=login_data,
                headers={'Referer': f"{BASE_URL}/admin/login/"},
                timeout=TIMEOUT,
                allow_redirects=True
            )
            
            # 3. Verificar login exitoso (redirect to /admin/)
            success = response.status_code == 200 and '/admin/' in response.url
            
            print_test(
                "Login exitoso",
                success,
                f"Usuario: {DEFAULT_CREDENTIALS['username']}"
            )
            
            if success:
                self.logged_in = True
                print_info(f"Redirected to: {response.url}")
            
            return success
        except Exception as e:
            print_test("Login exitoso", False, str(e))
            return False
    
    def test_dashboard_loads(self) -> bool:
        """TEST 5: Verificar dashboard principal carga"""
        print_header("TEST 5: DASHBOARD PRINCIPAL")
        
        if not self.logged_in:
            print_warning("Requiere login previo - SKIP")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/gestion/", timeout=TIMEOUT)
            success = response.status_code == 200
            
            print_test(
                "Dashboard carga",
                success,
                f"Status: {response.status_code}"
            )
            
            if success:
                # Verificar elementos clave del dashboard
                checks = {
                    'KPIs presentes': any(kpi in response.text for kpi in ['Ventas', 'Compras', 'Stock']),
                    'Navigation presente': 'Productos' in response.text,
                    'Chart.js loaded': 'chart' in response.text.lower()
                }
                
                for check_name, check_result in checks.items():
                    print_test(check_name, check_result)
            
            return success
        except Exception as e:
            print_test("Dashboard carga", False, str(e))
            return False
    
    def test_module_accessible(self, module_name: str, url_path: str) -> bool:
        """TEST genérico: Verificar módulo accesible"""
        if not self.logged_in:
            print_warning(f"{module_name} - Requiere login - SKIP")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}{url_path}", timeout=TIMEOUT)
            success = response.status_code == 200
            
            print_test(
                f"{module_name} accesible",
                success,
                f"URL: {url_path}"
            )
            
            return success
        except Exception as e:
            print_test(f"{module_name} accesible", False, str(e))
            return False
    
    def test_all_modules(self) -> Dict[str, bool]:
        """TEST 6-11: Verificar todos los módulos"""
        print_header("TESTS 6-11: MÓDULOS DEL SISTEMA")
        
        modules = {
            'Productos': '/gestion/productos/',
            'Materias Primas': '/gestion/materias-primas/',
            'Compras': '/gestion/compras/',
            'Ventas': '/gestion/ventas/',
            'Ajustes': '/gestion/ajustes/',
            'Reportes': '/gestion/reportes/'
        }
        
        results = {}
        for module_name, url_path in modules.items():
            results[module_name] = self.test_module_accessible(module_name, url_path)
        
        return results
    
    def test_static_files(self) -> bool:
        """TEST 12: Verificar archivos estáticos cargan"""
        print_header("TEST 12: ARCHIVOS ESTÁTICOS")
        
        try:
            # Intentar cargar CSS principal (si está servido por WhiteNoise)
            response = self.session.get(
                f"{BASE_URL}/static/css/lino-design-system-v3.css",
                timeout=TIMEOUT
            )
            
            css_loads = response.status_code == 200
            print_test("CSS principal carga", css_loads, f"Status: {response.status_code}")
            
            return css_loads
        except Exception as e:
            print_test("CSS principal carga", False, str(e))
            return False
    
    def test_database_connection(self) -> bool:
        """TEST 13: Verificar conexión a base de datos (indirectamente)"""
        print_header("TEST 13: CONEXIÓN A BASE DE DATOS")
        
        if not self.logged_in:
            print_warning("Requiere login - SKIP")
            return False
        
        try:
            # Si podemos acceder a /gestion/productos/, la DB está funcionando
            response = self.session.get(f"{BASE_URL}/gestion/productos/", timeout=TIMEOUT)
            success = response.status_code == 200
            
            print_test(
                "Database connection OK",
                success,
                "Verificado via /gestion/productos/"
            )
            
            return success
        except Exception as e:
            print_test("Database connection OK", False, str(e))
            return False
    
    def generate_report(self):
        """Genera reporte final de auditoría"""
        print_header("📊 REPORTE FINAL DE AUDITORÍA")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        failed_tests = total_tests - passed_tests
        percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total de tests: {total_tests}")
        print(f"{Colors.GREEN}✅ Tests pasando: {passed_tests}{Colors.END}")
        print(f"{Colors.RED}❌ Tests fallando: {failed_tests}{Colors.END}")
        print(f"{Colors.BOLD}📈 Porcentaje: {percentage:.1f}%{Colors.END}")
        
        print("\n" + "=" * 80)
        
        if percentage >= 90:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 SISTEMA FUNCIONANDO EXCELENTE (90%+){Colors.END}")
        elif percentage >= 70:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SISTEMA FUNCIONAL CON ADVERTENCIAS (70-90%){Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ SISTEMA REQUIERE ATENCIÓN URGENTE (<70%){Colors.END}")
        
        print("=" * 80 + "\n")
        
        # Guardar reporte JSON
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': BASE_URL,
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'percentage': percentage,
            'results': self.results
        }
        
        with open('audit_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print_info(f"Reporte guardado en: audit_report.json")
    
    def run_full_audit(self):
        """Ejecuta auditoría completa"""
        print_header("🔍 AUDITORÍA COMPLETA SERVIDOR PRODUCCIÓN")
        print_info(f"Servidor: {BASE_URL}")
        print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ejecutar todos los tests
        self.results['Servidor Online'] = self.test_server_online()
        self.results['HTTPS Habilitado'] = self.test_https_enabled()
        self.results['Admin Accesible'] = self.test_admin_accessible()
        self.results['Login Funcional'] = self.test_login()
        self.results['Dashboard Carga'] = self.test_dashboard_loads()
        
        # Módulos
        module_results = self.test_all_modules()
        self.results.update(module_results)
        
        # Otros tests
        self.results['Archivos Estáticos'] = self.test_static_files()
        self.results['Database Connection'] = self.test_database_connection()
        
        # Generar reporte
        self.generate_report()


# ==================== MAIN ====================

def main():
    """Función principal"""
    auditor = ProductionAuditor()
    auditor.run_full_audit()


if __name__ == "__main__":
    main()
