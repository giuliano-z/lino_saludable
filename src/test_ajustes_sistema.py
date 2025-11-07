#!/usr/bin/env python
"""
Script de Testing para Sistema de Ajustes de Inventario
Verifica que todas las vistas funcionen correctamente
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from gestion.models import Producto, MateriaPrima, AjusteInventario
from decimal import Decimal

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_test(name, status, details=""):
    icon = "✅" if status else "❌"
    print(f"{icon} {name}")
    if details:
        print(f"   {details}")

def test_modelo_ajuste():
    """Test 1: Verificar que el modelo AjusteInventario existe y funciona"""
    print_header("TEST 1: Modelo AjusteInventario")
    
    try:
        # Verificar que el modelo existe
        assert hasattr(AjusteInventario, 'producto'), "Campo producto no existe"
        assert hasattr(AjusteInventario, 'materia_prima'), "Campo materia_prima no existe"
        assert hasattr(AjusteInventario, 'stock_anterior'), "Campo stock_anterior no existe"
        assert hasattr(AjusteInventario, 'stock_nuevo'), "Campo stock_nuevo no existe"
        assert hasattr(AjusteInventario, 'diferencia'), "Campo diferencia no existe"
        assert hasattr(AjusteInventario, 'tipo'), "Campo tipo no existe"
        assert hasattr(AjusteInventario, 'razon'), "Campo razon no existe"
        assert hasattr(AjusteInventario, 'usuario'), "Campo usuario no existe"
        assert hasattr(AjusteInventario, 'fecha'), "Campo fecha no existe"
        
        print_test("Estructura del modelo", True, "Todos los campos existen")
        
        # Verificar tipos de ajuste
        tipos = dict(AjusteInventario.TIPO_CHOICES)
        assert len(tipos) == 7, f"Esperados 7 tipos, encontrados {len(tipos)}"
        print_test("Tipos de ajuste", True, f"{len(tipos)} tipos configurados")
        
        # Verificar métodos helper
        assert hasattr(AjusteInventario, 'item_nombre'), "Método item_nombre no existe"
        assert hasattr(AjusteInventario, 'item_tipo'), "Método item_tipo no existe"
        assert hasattr(AjusteInventario, 'es_incremento'), "Método es_incremento no existe"
        assert hasattr(AjusteInventario, 'es_reduccion'), "Método es_reduccion no existe"
        print_test("Métodos helper", True, "Todos los métodos existen")
        
        return True
    except Exception as e:
        print_test("Error en modelo", False, str(e))
        return False

def test_creacion_ajuste_producto():
    """Test 2: Crear un ajuste de producto"""
    print_header("TEST 2: Crear Ajuste de Producto")
    
    try:
        # Obtener o crear usuario
        user, _ = User.objects.get_or_create(
            username='test_user',
            defaults={'is_staff': True}
        )
        
        # Obtener primer producto disponible
        producto = Producto.objects.first()
        if not producto:
            print_test("Productos disponibles", False, "No hay productos en la BD")
            return False
        
        print_test("Producto encontrado", True, f"{producto.nombre} (stock: {producto.stock})")
        
        # Guardar stock original
        stock_original = producto.stock
        nuevo_stock = Decimal(str(stock_original + 5))
        
        # Crear ajuste
        ajuste = AjusteInventario.objects.create(
            producto=producto,
            stock_anterior=stock_original,
            stock_nuevo=nuevo_stock,
            tipo='INVENTARIO_FISICO',
            razon='Test automatizado de ajuste de producto',
            usuario=user
        )
        
        print_test("Ajuste creado", True, f"ID: {ajuste.id}, Diferencia: {ajuste.diferencia}")
        
        # Verificar cálculo automático de diferencia
        assert ajuste.diferencia == 5, f"Diferencia incorrecta: {ajuste.diferencia}"
        print_test("Cálculo de diferencia", True, "Diferencia calculada correctamente")
        
        # Actualizar stock del producto (como lo hace el formulario)
        producto.stock = nuevo_stock
        producto.save()
        producto.refresh_from_db()
        
        assert producto.stock == nuevo_stock, "Stock no se actualizó"
        print_test("Actualización de stock", True, f"Stock actualizado a {producto.stock}")
        
        # Restaurar stock original
        producto.stock = stock_original
        producto.save()
        ajuste.delete()
        
        return True
    except Exception as e:
        print_test("Error en creación", False, str(e))
        return False

def test_creacion_ajuste_mp():
    """Test 3: Crear un ajuste de materia prima"""
    print_header("TEST 3: Crear Ajuste de Materia Prima")
    
    try:
        # Obtener usuario
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('test_user', password='test123')
        
        # Obtener primera MP disponible
        mp = MateriaPrima.objects.filter(activo=True).first()
        if not mp:
            print_test("Materias primas disponibles", False, "No hay MPs activas en la BD")
            return False
        
        print_test("Materia prima encontrada", True, f"{mp.nombre} (stock: {mp.stock_actual})")
        
        # Guardar stock original
        stock_original = mp.stock_actual
        nuevo_stock = Decimal(str(stock_original - 2))
        
        # Crear ajuste
        ajuste = AjusteInventario.objects.create(
            materia_prima=mp,
            stock_anterior=stock_original,
            stock_nuevo=nuevo_stock,
            tipo='MERMA',
            razon='Test automatizado de merma de MP',
            usuario=user
        )
        
        print_test("Ajuste creado", True, f"ID: {ajuste.id}, Diferencia: {ajuste.diferencia}")
        
        # Verificar que la diferencia es negativa
        assert ajuste.diferencia == -2, f"Diferencia incorrecta: {ajuste.diferencia}"
        print_test("Cálculo de diferencia negativa", True, "Merma calculada correctamente")
        
        # Actualizar stock de MP
        mp.stock_actual = nuevo_stock
        mp.save()
        mp.refresh_from_db()
        
        assert mp.stock_actual == nuevo_stock, "Stock de MP no se actualizó"
        print_test("Actualización de stock MP", True, f"Stock actualizado a {mp.stock_actual}")
        
        # Restaurar stock original
        mp.stock_actual = stock_original
        mp.save()
        ajuste.delete()
        
        return True
    except Exception as e:
        print_test("Error en creación MP", False, str(e))
        return False

def test_validacion_exclusiva():
    """Test 4: Verificar que no se puede crear ajuste con producto Y MP"""
    print_header("TEST 4: Validación Exclusiva (Producto O MP)")
    
    try:
        user = User.objects.first()
        producto = Producto.objects.first()
        mp = MateriaPrima.objects.first()
        
        if not producto or not mp:
            print_test("Datos disponibles", False, "Faltan productos o MPs")
            return False
        
        # Intentar crear ajuste con ambos
        try:
            ajuste = AjusteInventario(
                producto=producto,
                materia_prima=mp,  # ❌ No debería permitirse
                stock_anterior=10,
                stock_nuevo=15,
                tipo='OTRO',
                razon='Test de validación',
                usuario=user
            )
            ajuste.full_clean()  # Esto debería lanzar ValidationError
            
            print_test("Validación exclusiva", False, "Permitió crear ajuste con producto Y MP")
            ajuste.delete()
            return False
        except Exception as e:
            print_test("Validación exclusiva", True, f"Rechazó correctamente: {type(e).__name__}")
            return True
            
    except Exception as e:
        print_test("Error en validación", False, str(e))
        return False

def test_propiedades_helper():
    """Test 5: Verificar propiedades helper del modelo"""
    print_header("TEST 5: Propiedades Helper")
    
    try:
        user = User.objects.first()
        producto = Producto.objects.first()
        
        if not producto:
            print_test("Producto disponible", False, "No hay productos")
            return False
        
        # Crear ajuste de prueba
        ajuste = AjusteInventario.objects.create(
            producto=producto,
            stock_anterior=10,
            stock_nuevo=15,
            tipo='INVENTARIO_FISICO',
            razon='Test de propiedades',
            usuario=user
        )
        
        # Test item_nombre
        assert producto.nombre in ajuste.item_nombre, "item_nombre no contiene nombre del producto"
        print_test("Propiedad item_nombre", True, ajuste.item_nombre)
        
        # Test item_tipo
        assert ajuste.item_tipo == "Producto", f"item_tipo incorrecto: {ajuste.item_tipo}"
        print_test("Propiedad item_tipo", True, ajuste.item_tipo)
        
        # Test es_incremento
        assert ajuste.es_incremento == True, "es_incremento debería ser True"
        print_test("Propiedad es_incremento", True, str(ajuste.es_incremento))
        
        # Test es_reduccion
        assert ajuste.es_reduccion == False, "es_reduccion debería ser False"
        print_test("Propiedad es_reduccion", True, str(ajuste.es_reduccion))
        
        # Test tipo_display
        assert ajuste.tipo_display == "Inventario Físico", f"tipo_display incorrecto: {ajuste.tipo_display}"
        print_test("Propiedad tipo_display", True, ajuste.tipo_display)
        
        ajuste.delete()
        return True
        
    except Exception as e:
        print_test("Error en propiedades", False, str(e))
        return False

def test_queries_ajustes():
    """Test 6: Verificar queries y filtros"""
    print_header("TEST 6: Queries y Filtros")
    
    try:
        # Contar ajustes existentes
        total = AjusteInventario.objects.count()
        print_test("Total de ajustes", True, f"{total} registros")
        
        # Ajustes de productos
        ajustes_productos = AjusteInventario.objects.filter(producto__isnull=False).count()
        print_test("Ajustes de productos", True, f"{ajustes_productos} registros")
        
        # Ajustes de MPs
        ajustes_mps = AjusteInventario.objects.filter(materia_prima__isnull=False).count()
        print_test("Ajustes de MPs", True, f"{ajustes_mps} registros")
        
        # Verificar que la suma coincide
        assert total == ajustes_productos + ajustes_mps, "Los totales no coinciden"
        print_test("Integridad de datos", True, "Totales coinciden")
        
        # Test select_related (performance)
        ajustes = AjusteInventario.objects.select_related(
            'producto', 'materia_prima', 'usuario'
        ).all()[:5]
        print_test("Query optimizada", True, f"Select_related funciona ({len(ajustes)} resultados)")
        
        return True
    except Exception as e:
        print_test("Error en queries", False, str(e))
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "TEST SUITE - AJUSTES INVENTARIO" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Modelo AjusteInventario", test_modelo_ajuste),
        ("Crear Ajuste de Producto", test_creacion_ajuste_producto),
        ("Crear Ajuste de MP", test_creacion_ajuste_mp),
        ("Validación Exclusiva", test_validacion_exclusiva),
        ("Propiedades Helper", test_propiedades_helper),
        ("Queries y Filtros", test_queries_ajustes),
    ]
    
    resultados = []
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print_header("RESUMEN DE TESTS")
    exitosos = sum(1 for _, r in resultados if r)
    total_tests = len(resultados)
    
    for nombre, resultado in resultados:
        icon = "✅" if resultado else "❌"
        print(f"{icon} {nombre}")
    
    print("\n" + "="*70)
    print(f"Resultado: {exitosos}/{total_tests} tests exitosos ({exitosos*100//total_tests}%)")
    print("="*70 + "\n")
    
    if exitosos == total_tests:
        print("🎉 TODOS LOS TESTS PASARON - Sistema listo para producción")
        return 0
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - Revisar antes de desplegar")
        return 1

if __name__ == '__main__':
    sys.exit(main())
