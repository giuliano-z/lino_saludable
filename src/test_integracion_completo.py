#!/usr/bin/env python
"""
Test de Integración Completo - Sistema de Ajustes
Verifica que todo el flujo funcione correctamente antes de deploy
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from gestion.models import Producto, MateriaPrima, AjusteInventario
from decimal import Decimal

User = get_user_model()

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_test(name, success, details=""):
    emoji = "✅" if success else "❌"
    print(f"{emoji} {name}")
    if details:
        print(f"   {details}")

def test_urls_existen():
    """Test 1: Verificar que todas las URLs están configuradas"""
    print_header("TEST 1: Configuración de URLs")
    
    from django.urls import reverse
    
    try:
        # URLs sin parámetros
        url = reverse('gestion:lista_ajustes')
        print_test("URL lista_ajustes", True, url)
        
        url = reverse('gestion:crear_ajuste_producto')
        print_test("URL crear_ajuste_producto", True, url)
        
        url = reverse('gestion:crear_ajuste_materia_prima')
        print_test("URL crear_ajuste_materia_prima", True, url)
        
        # URLs con parámetros
        producto = Producto.objects.first()
        if producto:
            url = reverse('gestion:crear_ajuste_producto_directo', args=[producto.id])
            print_test("URL crear_ajuste_producto_directo", True, url)
        
        mp = MateriaPrima.objects.first()
        if mp:
            url = reverse('gestion:crear_ajuste_mp_directo', args=[mp.id])
            print_test("URL crear_ajuste_mp_directo", True, url)
        
        ajuste = AjusteInventario.objects.first()
        if ajuste:
            url = reverse('gestion:detalle_ajuste', args=[ajuste.id])
            print_test("URL detalle_ajuste", True, url)
        
        return True
    except Exception as e:
        print_test("Error en URLs", False, str(e))
        return False

def test_vistas_cargan():
    """Test 2: Verificar que las vistas cargan sin errores"""
    print_header("TEST 2: Carga de Vistas")
    
    user = User.objects.first()
    client = Client()
    client.force_login(user)
    
    tests_passed = 0
    tests_total = 0
    
    # Test lista de ajustes
    tests_total += 1
    response = client.get('/gestion/ajustes/')
    if response.status_code == 200:
        print_test("GET /gestion/ajustes/", True, "Lista carga correctamente")
        tests_passed += 1
    else:
        print_test("GET /gestion/ajustes/", False, f"Status: {response.status_code}")
    
    # Test formulario producto
    tests_total += 1
    response = client.get('/gestion/ajustes/productos/crear/')
    if response.status_code == 200:
        print_test("GET /gestion/ajustes/productos/crear/", True, "Formulario carga")
        tests_passed += 1
    else:
        print_test("GET /gestion/ajustes/productos/crear/", False, f"Status: {response.status_code}")
    
    # Test formulario MP
    tests_total += 1
    response = client.get('/gestion/ajustes/materias-primas/crear/')
    if response.status_code == 200:
        print_test("GET /gestion/ajustes/materias-primas/crear/", True, "Formulario carga")
        tests_passed += 1
    else:
        print_test("GET /gestion/ajustes/materias-primas/crear/", False, f"Status: {response.status_code}")
    
    # Test formulario pre-llenado producto
    producto = Producto.objects.first()
    if producto:
        tests_total += 1
        response = client.get(f'/gestion/ajustes/productos/{producto.id}/crear/')
        if response.status_code == 200:
            print_test(f"GET /gestion/ajustes/productos/{producto.id}/crear/", True, "Pre-llenado funciona")
            tests_passed += 1
        else:
            print_test(f"GET /gestion/ajustes/productos/{producto.id}/crear/", False, f"Status: {response.status_code}")
    
    # Test formulario pre-llenado MP
    mp = MateriaPrima.objects.first()
    if mp:
        tests_total += 1
        response = client.get(f'/gestion/ajustes/materias-primas/{mp.id}/crear/')
        if response.status_code == 200:
            print_test(f"GET /gestion/ajustes/materias-primas/{mp.id}/crear/", True, "Pre-llenado funciona")
            tests_passed += 1
        else:
            print_test(f"GET /gestion/ajustes/materias-primas/{mp.id}/crear/", False, f"Status: {response.status_code}")
    
    print(f"\nResultado: {tests_passed}/{tests_total} tests pasaron")
    return tests_passed == tests_total

def test_crear_ajuste_producto():
    """Test 3: Crear un ajuste de producto completo"""
    print_header("TEST 3: Crear Ajuste de Producto (con actualización de stock)")
    
    user = User.objects.first()
    client = Client()
    client.force_login(user)
    
    producto = Producto.objects.first()
    
    if not producto:
        print_test("Error", False, "No hay productos en la BD")
        return False
    
    stock_original = producto.stock
    nuevo_stock = stock_original + 10
    
    print(f"Producto: {producto.nombre}")
    print(f"Stock ANTES del ajuste: {stock_original}")
    
    # Hacer POST al formulario
    response = client.post(f'/gestion/ajustes/productos/{producto.id}/crear/', {
        'producto': producto.id,
        'stock_nuevo': nuevo_stock,
        'tipo': 'INVENTARIO_FISICO',
        'razon': 'Test automatizado de integración'
    })
    
    # Verificar que redirigió correctamente
    print_test("POST exitoso", response.status_code in [200, 302], f"Status: {response.status_code}")
    
    # Refrescar producto de la BD
    producto.refresh_from_db()
    
    print(f"Stock DESPUÉS del ajuste: {producto.stock}")
    
    # Verificar que el stock SÍ cambió
    stock_cambio = producto.stock == nuevo_stock
    print_test("Stock actualizado en BD", stock_cambio, 
               f"Esperado: {nuevo_stock}, Real: {producto.stock}")
    
    # Verificar que se creó el ajuste
    ultimo_ajuste = AjusteInventario.objects.filter(producto=producto).order_by('-id').first()
    if ultimo_ajuste:
        print_test("Ajuste creado", True, f"ID: {ultimo_ajuste.id}, Diferencia: {ultimo_ajuste.diferencia}")
    else:
        print_test("Ajuste creado", False, "No se encontró el ajuste en BD")
    
    # Restaurar stock original
    producto.stock = stock_original
    producto.save()
    if ultimo_ajuste:
        ultimo_ajuste.delete()
    
    return stock_cambio

def test_crear_ajuste_mp():
    """Test 4: Crear un ajuste de materia prima completo"""
    print_header("TEST 4: Crear Ajuste de Materia Prima (con actualización de stock)")
    
    user = User.objects.first()
    client = Client()
    client.force_login(user)
    
    mp = MateriaPrima.objects.first()
    
    if not mp:
        print_test("Error", False, "No hay MPs en la BD")
        return False
    
    stock_original = mp.stock_actual
    nuevo_stock = stock_original + Decimal('15.5')
    
    print(f"Materia Prima: {mp.nombre}")
    print(f"Stock ANTES del ajuste: {stock_original}")
    
    # Hacer POST al formulario
    response = client.post(f'/gestion/ajustes/materias-primas/{mp.id}/crear/', {
        'materia_prima': mp.id,
        'stock_nuevo': str(nuevo_stock),
        'tipo': 'CORRECCION',
        'razon': 'Test automatizado de integración - MP'
    })
    
    # Verificar que redirigió correctamente
    print_test("POST exitoso", response.status_code in [200, 302], f"Status: {response.status_code}")
    
    # Refrescar MP de la BD
    mp.refresh_from_db()
    
    print(f"Stock DESPUÉS del ajuste: {mp.stock_actual}")
    
    # Verificar que el stock SÍ cambió
    stock_cambio = mp.stock_actual == nuevo_stock
    print_test("Stock actualizado en BD", stock_cambio,
               f"Esperado: {nuevo_stock}, Real: {mp.stock_actual}")
    
    # Verificar que se creó el ajuste
    ultimo_ajuste = AjusteInventario.objects.filter(materia_prima=mp).order_by('-id').first()
    if ultimo_ajuste:
        print_test("Ajuste creado", True, f"ID: {ultimo_ajuste.id}, Diferencia: {ultimo_ajuste.diferencia}")
    else:
        print_test("Ajuste creado", False, "No se encontró el ajuste en BD")
    
    # Restaurar stock original
    mp.stock_actual = stock_original
    mp.save()
    if ultimo_ajuste:
        ultimo_ajuste.delete()
    
    return stock_cambio

def test_detalle_templates():
    """Test 5: Verificar que los botones están en los templates de detalle"""
    print_header("TEST 5: Botones en Templates de Detalle")
    
    # Verificar producto detalle
    with open('gestion/templates/modules/productos/detalle.html', 'r') as f:
        content = f.read()
        tiene_boton = 'crear_ajuste_producto_directo' in content
        print_test("Botón en detalle de producto", tiene_boton, 
                   "URL correcta en template" if tiene_boton else "URL NO encontrada")
    
    # Verificar MP detalle
    with open('gestion/templates/modules/materias_primas/materias_primas/detalle.html', 'r') as f:
        content = f.read()
        tiene_boton = 'crear_ajuste_mp_directo' in content
        print_test("Botón en detalle de MP", tiene_boton,
                   "URL correcta en template" if tiene_boton else "URL NO encontrada")
    
    return True

def main():
    print("\n" + "="*70)
    print("  TEST DE INTEGRACIÓN COMPLETO - SISTEMA DE AJUSTES")
    print("="*70)
    
    results = []
    
    results.append(test_urls_existen())
    results.append(test_vistas_cargan())
    results.append(test_crear_ajuste_producto())
    results.append(test_crear_ajuste_mp())
    results.append(test_detalle_templates())
    
    print_header("RESUMEN FINAL")
    
    tests_passed = sum(results)
    tests_total = len(results)
    
    print(f"\nTests exitosos: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 TODOS LOS TESTS PASARON - LISTO PARA DEPLOY")
        return 0
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON - REVISAR ANTES DE DEPLOY")
        return 1

if __name__ == '__main__':
    exit(main())
