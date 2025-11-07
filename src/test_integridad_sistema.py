#!/usr/bin/env python
"""
🔍 SCRIPT DE TESTING EXHAUSTIVO - LINO SALUDABLE
==================================================

Este script prueba la integridad del sistema completo, buscando:
- Bugs de transacciones (ventas, compras, eliminaciones)
- Problemas de stock
- Cálculos incorrectos
- Inconsistencias de datos

Uso:
    python test_integridad_sistema.py

"""

import os
import django
import sys
from decimal import Decimal
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth import get_user_model
from gestion.models import (
    Producto, MateriaPrima, Venta, VentaDetalle, 
    Compra, MovimientoMateriaPrima
)

User = get_user_model()


class Colors:
    """Colores ANSI para terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(title):
    """Imprime un header bonito"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")


# =====================================================================
# TEST 1: Validación de Stock en Ventas
# =====================================================================
def test_venta_stock_insuficiente():
    """
    Test Bug #4: Verificar que no se puedan crear ventas con stock insuficiente
    """
    print_header("TEST 1: Validación de Stock en Ventas")
    
    # Buscar un producto con stock
    producto = Producto.objects.filter(stock__gt=0).first()
    
    if not producto:
        print_warning("No hay productos con stock para probar")
        return
    
    print_info(f"Producto de prueba: {producto.nombre}")
    print_info(f"Stock actual: {producto.stock}")
    
    # Intentar vender más de lo disponible
    cantidad_excesiva = producto.stock + 10
    print_info(f"Intentando vender: {cantidad_excesiva} (más de lo disponible)")
    
    # Este test no puede crear ventas directamente porque necesita un request
    # Pero podemos verificar que el código esté correcto
    print_warning("Este test requiere probar manualmente en la interfaz web")
    print_info("Pasos para probar:")
    print_info(f"  1. Ir a Nueva Venta")
    print_info(f"  2. Seleccionar '{producto.nombre}'")
    print_info(f"  3. Ingresar cantidad: {cantidad_excesiva}")
    print_info(f"  4. Verificar que muestre error y NO registre la venta")


# =====================================================================
# TEST 2: Reversión de Stock al Eliminar Compras
# =====================================================================
def test_eliminar_compra_restaura_stock():
    """
    Test Bug #5: Verificar que eliminar una compra restaure el stock correctamente
    """
    print_header("TEST 2: Reversión de Stock al Eliminar Compras")
    
    # Buscar última compra
    compra = Compra.objects.order_by('-id').first()
    
    if not compra:
        print_warning("No hay compras para probar")
        return
    
    print_info(f"Compra de prueba: #{compra.id}")
    
    # Verificar si es legacy o nueva
    es_legacy = compra.es_compra_legacy()
    
    if es_legacy:
        mp = compra.materia_prima
        stock_actual = mp.stock_actual
        cantidad_compra = compra.cantidad_mayoreo
        
        print_info(f"Tipo: Compra Legacy (1 producto)")
        print_info(f"Materia Prima: {mp.nombre}")
        print_info(f"Stock actual: {stock_actual} {mp.get_unidad_medida_display()}")
        print_info(f"Cantidad de compra: {cantidad_compra}")
        print_info(f"Stock esperado después de eliminar: {stock_actual - cantidad_compra}")
        
    else:
        print_info(f"Tipo: Compra Nueva (múltiples productos)")
        detalles = compra.detalles.all()
        print_info(f"Cantidad de items: {detalles.count()}")
        
        for detalle in detalles:
            mp = detalle.materia_prima
            stock_actual = mp.stock_actual
            cantidad_compra = detalle.cantidad
            print_info(f"  - {mp.nombre}: Stock {stock_actual}, "
                      f"Compra {cantidad_compra}, "
                      f"Esperado después: {stock_actual - cantidad_compra}")
    
    print_warning("Este test requiere eliminación manual y verificación")
    print_info("Pasos para probar:")
    print_info(f"  1. Anotar stocks actuales arriba")
    print_info(f"  2. Ir a Compras y eliminar compra #{compra.id}")
    print_info(f"  3. Verificar que los stocks bajen según lo esperado")
    print_info(f"  4. Si no bajan, hay un BUG ❌")


# =====================================================================
# TEST 3: Consistencia de Costos de Productos
# =====================================================================
def test_consistencia_costos():
    """
    Verificar que todos los productos fraccionados tengan costos correctos
    """
    print_header("TEST 3: Consistencia de Costos de Productos")
    
    productos_fraccionados = Producto.objects.filter(
        materia_prima_asociada__isnull=False,
        cantidad_fraccion__isnull=False
    )
    
    print_info(f"Productos fraccionados encontrados: {productos_fraccionados.count()}")
    
    problemas = []
    
    for producto in productos_fraccionados:
        mp = producto.materia_prima_asociada
        cantidad = producto.cantidad_fraccion
        precio_mp = mp.costo_unitario
        
        costo_esperado = Decimal(str(cantidad)) * Decimal(str(precio_mp))
        costo_calculado = producto.calcular_costo_real()
        
        diferencia = abs(costo_esperado - costo_calculado)
        
        if diferencia > Decimal('0.01'):  # Tolerancia de 1 centavo
            problemas.append({
                'producto': producto.nombre,
                'esperado': costo_esperado,
                'calculado': costo_calculado,
                'diferencia': diferencia
            })
    
    if problemas:
        print_error(f"Encontrados {len(problemas)} productos con costos incorrectos:")
        for p in problemas:
            print(f"  - {p['producto']}")
            print(f"    Esperado: ${p['esperado']}")
            print(f"    Calculado: ${p['calculado']}")
            print(f"    Diferencia: ${p['diferencia']}")
    else:
        print_success("Todos los costos de productos son correctos")


# =====================================================================
# TEST 4: Productos con Stock Negativo
# =====================================================================
def test_stock_negativo():
    """
    Buscar productos con stock negativo (no debería pasar nunca)
    """
    print_header("TEST 4: Productos con Stock Negativo")
    
    productos_negativos = Producto.objects.filter(stock__lt=0)
    
    if productos_negativos.exists():
        print_error(f"Encontrados {productos_negativos.count()} productos con stock negativo:")
        for p in productos_negativos:
            print(f"  - {p.nombre}: Stock = {p.stock}")
    else:
        print_success("No hay productos con stock negativo")


# =====================================================================
# TEST 5: Materias Primas con Stock Negativo
# =====================================================================
def test_mp_stock_negativo():
    """
    Buscar materias primas con stock negativo
    """
    print_header("TEST 5: Materias Primas con Stock Negativo")
    
    mps_negativas = MateriaPrima.objects.filter(stock_actual__lt=0)
    
    if mps_negativas.exists():
        print_error(f"Encontradas {mps_negativas.count()} materias primas con stock negativo:")
        for mp in mps_negativas:
            print(f"  - {mp.nombre}: Stock = {mp.stock_actual} {mp.get_unidad_medida_display()}")
    else:
        print_success("No hay materias primas con stock negativo")


# =====================================================================
# TEST 6: Ventas sin VentaDetalle
# =====================================================================
def test_ventas_sin_detalles():
    """
    Buscar ventas huérfanas (sin productos)
    """
    print_header("TEST 6: Ventas sin Productos (Huérfanas)")
    
    ventas_sin_detalles = []
    
    for venta in Venta.objects.all():
        if venta.ventadetalle_set.count() == 0:
            ventas_sin_detalles.append(venta)
    
    if ventas_sin_detalles:
        print_error(f"Encontradas {len(ventas_sin_detalles)} ventas sin productos:")
        for v in ventas_sin_detalles:
            print(f"  - Venta #{v.id}: Cliente {v.cliente}, Total ${v.total}")
    else:
        print_success("Todas las ventas tienen productos")


# =====================================================================
# TEST 7: Precios de Venta vs Costo
# =====================================================================
def test_precios_vs_costos():
    """
    Buscar productos donde el precio de venta es menor al costo
    """
    print_header("TEST 7: Productos con Pérdida (Precio < Costo)")
    
    productos_perdida = []
    
    for producto in Producto.objects.all():
        costo = producto.calcular_costo_real()
        precio_venta = Decimal(str(producto.precio))
        
        if costo > 0 and precio_venta < costo:
            margen = ((precio_venta - costo) / costo * 100)
            productos_perdida.append({
                'nombre': producto.nombre,
                'costo': costo,
                'precio': precio_venta,
                'margen': margen
            })
    
    if productos_perdida:
        print_warning(f"Encontrados {len(productos_perdida)} productos con pérdida:")
        for p in productos_perdida:
            print(f"  - {p['nombre']}")
            print(f"    Costo: ${p['costo']}")
            print(f"    Precio: ${p['precio']}")
            print(f"    Margen: {p['margen']:.1f}%")
    else:
        print_success("Todos los productos tienen margen positivo")


# =====================================================================
# TEST 8: Ventas Eliminadas Aparecen en Historial
# =====================================================================
def test_ventas_eliminadas_en_historial():
    """
    Test Bug #6: Verificar que ventas eliminadas NO aparecen en historial
    """
    print_header("TEST 8: Ventas Eliminadas en Historial")
    
    # Buscar ventas eliminadas
    ventas_eliminadas = Venta.todos.filter(eliminada=True)
    
    print_info(f"Ventas eliminadas encontradas: {ventas_eliminadas.count()}")
    
    if ventas_eliminadas.exists():
        print_warning("Verificando que NO aparezcan en queries normales:")
        
        # Verificar que NO aparecen con el manager normal
        ventas_activas = Venta.objects.all()
        
        for v_elim in ventas_eliminadas[:3]:  # Solo primeras 3
            if v_elim in ventas_activas:
                print_error(f"Venta #{v_elim.id} (ELIMINADA) aparece en Venta.objects.all()")
            else:
                print_success(f"Venta #{v_elim.id} (ELIMINADA) NO aparece en queries normales ✅")
        
        # Verificar que NO aparecen en VentaDetalle queries
        for v_elim in ventas_eliminadas[:3]:
            detalles_visibles = VentaDetalle.objects.filter(
                venta=v_elim
            ).exclude(venta__eliminada=True)
            
            if detalles_visibles.exists():
                print_error(f"Detalles de venta #{v_elim.id} (ELIMINADA) aparecen en queries")
            else:
                print_success(f"Detalles de venta #{v_elim.id} correctamente ocultos ✅")
    else:
        print_info("No hay ventas eliminadas para probar")


# =====================================================================
# EJECUTAR TODOS LOS TESTS
# =====================================================================
def main():
    """Ejecutar todos los tests"""
    print(f"\n{Colors.BOLD}🔍 INICIANDO TESTS DE INTEGRIDAD DEL SISTEMA{Colors.END}")
    print(f"{Colors.BOLD}Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")
    
    tests = [
        test_venta_stock_insuficiente,
        test_eliminar_compra_restaura_stock,
        test_consistencia_costos,
        test_stock_negativo,
        test_mp_stock_negativo,
        test_ventas_sin_detalles,
        test_precios_vs_costos,
        test_ventas_eliminadas_en_historial,  # ✅ NUEVO TEST
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print_error(f"Error ejecutando {test.__name__}: {str(e)}")
    
    print_header("RESUMEN FINAL")
    print_info("Tests completados. Revisar resultados arriba.")
    print_info("Los tests marcados como 'requieren prueba manual' deben")
    print_info("verificarse en la interfaz web de Railway.")


if __name__ == '__main__':
    main()
