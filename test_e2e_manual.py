#!/usr/bin/env python
"""
Tests E2E Simplificados - Sistema LINO
Tests manuales con Playwright (sin pytest) para evitar problemas de async/sync
"""

import os
import sys
from playwright.sync_api import sync_playwright, expect
import time

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Configuración
BASE_URL = "http://127.0.0.1:8000"  # Asegúrate de tener el servidor corriendo
USERNAME = "testuser_e2e_manual"
PASSWORD = "testpass123E2E"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}")

def print_test(name, passed, details=""):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")
    return passed

def setup_test_user():
    """Crear usuario de test."""
    print_header("SETUP: Creando Usuario de Test")
    
    # Eliminar si existe
    User.objects.filter(username=USERNAME).delete()
    
    # Crear nuevo
    user = User.objects.create_user(
        username=USERNAME,
        email='test_e2e_manual@lino.com',
        password=PASSWORD,
        is_staff=True,
        is_superuser=True
    )
    print(f"✅ Usuario creado: {USERNAME}")
    return user

def cleanup_test_user():
    """Limpiar usuario de test."""
    User.objects.filter(username=USERNAME).delete()
    print(f"🧹 Usuario eliminado: {USERNAME}")

def test_login(page):
    """TEST 1: Login exitoso."""
    print_header("TEST 1: Login Exitoso")
    
    try:
        # Ir a login
        page.goto(f"{BASE_URL}/admin/login/")
        page.wait_for_load_state('networkidle')
        
        # Verificar que estamos en login
        assert "login" in page.url.lower() or "Log in" in page.content()
        
        # Llenar formulario
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        
        # Submit
        page.click('input[type="submit"]')
        page.wait_for_load_state('networkidle')
        
        # Verificar redirección
        success = "/admin/" in page.url
        print_test("Login y redirección", success, f"URL: {page.url}")
        
        return success
    except Exception as e:
        print_test("Login exitoso", False, f"Error: {str(e)}")
        return False

def test_dashboard(page):
    """TEST 2: Dashboard carga."""
    print_header("TEST 2: Dashboard Principal")
    
    try:
        page.goto(f"{BASE_URL}/gestion/")
        page.wait_for_load_state('networkidle')
        
        # Verificar que no hay errores
        title = page.title()
        success = "error" not in title.lower() and "404" not in title
        
        print_test("Dashboard carga", success, f"Título: {title}")
        return success
    except Exception as e:
        print_test("Dashboard carga", False, f"Error: {str(e)}")
        return False

def test_productos_lista(page):
    """TEST 3: Lista de productos."""
    print_header("TEST 3: Lista de Productos")
    
    try:
        page.goto(f"{BASE_URL}/gestion/productos/")
        page.wait_for_load_state('networkidle')
        
        title = page.title()
        content = page.content()
        
        success = ("producto" in content.lower() and 
                   "error" not in title.lower())
        
        print_test("Lista productos accesible", success)
        return success
    except Exception as e:
        print_test("Lista productos", False, f"Error: {str(e)}")
        return False

def test_materias_primas_lista(page):
    """TEST 4: Lista de materias primas."""
    print_header("TEST 4: Lista de Materias Primas")
    
    try:
        page.goto(f"{BASE_URL}/gestion/materias-primas/")
        page.wait_for_load_state('networkidle')
        
        title = page.title()
        success = "error" not in title.lower()
        
        print_test("Lista MPs accesible", success)
        return success
    except Exception as e:
        print_test("Lista MPs", False, f"Error: {str(e)}")
        return False

def test_ventas_lista(page):
    """TEST 5: Lista de ventas."""
    print_header("TEST 5: Lista de Ventas")
    
    try:
        page.goto(f"{BASE_URL}/gestion/ventas/")
        page.wait_for_load_state('networkidle')
        
        title = page.title()
        success = "error" not in title.lower()
        
        print_test("Lista ventas accesible", success)
        return success
    except Exception as e:
        print_test("Lista ventas", False, f"Error: {str(e)}")
        return False

def test_compras_lista(page):
    """TEST 6: Lista de compras."""
    print_header("TEST 6: Lista de Compras")
    
    try:
        page.goto(f"{BASE_URL}/gestion/compras/")
        page.wait_for_load_state('networkidle')
        
        title = page.title()
        success = "error" not in title.lower()
        
        print_test("Lista compras accesible", success)
        return success
    except Exception as e:
        print_test("Lista compras", False, f"Error: {str(e)}")
        return False

def test_ajustes_lista(page):
    """TEST 7: Lista de ajustes."""
    print_header("TEST 7: Lista de Ajustes de Inventario")
    
    try:
        page.goto(f"{BASE_URL}/gestion/ajustes/")
        page.wait_for_load_state('networkidle')
        
        title = page.title()
        success = "error" not in title.lower()
        
        print_test("Lista ajustes accesible", success)
        return success
    except Exception as e:
        print_test("Lista ajustes", False, f"Error: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests E2E."""
    print_header("TESTS E2E - SISTEMA LINO")
    print(f"\n⚠️  IMPORTANTE: Asegúrate de tener el servidor corriendo en {BASE_URL}")
    print(f"   Ejecuta: cd src && python manage.py runserver\n")
    
    input("Presiona ENTER cuando el servidor esté corriendo...")
    
    # Setup
    user = setup_test_user()
    
    resultados = {}
    
    with sync_playwright() as p:
        # Usar chromium en modo headless
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Ejecutar tests
            resultados['Login'] = test_login(page)
            
            if resultados['Login']:
                # Solo continuar si login funcionó
                resultados['Dashboard'] = test_dashboard(page)
                resultados['Productos'] = test_productos_lista(page)
                resultados['Materias Primas'] = test_materias_primas_lista(page)
                resultados['Ventas'] = test_ventas_lista(page)
                resultados['Compras'] = test_compras_lista(page)
                resultados['Ajustes'] = test_ajustes_lista(page)
            else:
                print("\n⚠️  Login falló - tests subsecuentes omitidos")
        
        finally:
            browser.close()
    
    # Cleanup
    cleanup_test_user()
    
    # Resumen
    print_header("RESUMEN FINAL - TESTS E2E")
    total = len(resultados)
    pasados = sum(1 for v in resultados.values() if v)
    
    print(f"\n📊 Tests ejecutados: {total}")
    print(f"✅ Tests pasando: {pasados}")
    print(f"❌ Tests fallando: {total - pasados}")
    print(f"📈 Porcentaje: {(pasados/total*100):.1f}%\n")
    
    for nombre, resultado in resultados.items():
        symbol = "✅" if resultado else "❌"
        print(f"{symbol} {nombre}")
    
    print("\n" + "="*80)
    if all(resultados.values()):
        print("🎉 TODOS LOS TESTS E2E PASARON")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - Revisar arriba")
    print("="*80 + "\n")
    
    return 0 if all(resultados.values()) else 1

if __name__ == "__main__":
    exit(main())
