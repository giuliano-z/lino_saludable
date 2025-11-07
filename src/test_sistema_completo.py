#!/usr/bin/env python
"""
Script de Testing Completo para LINO Saludable
Diagnostica problemas en productos, materias primas y ventas
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import Producto, MateriaPrima, Venta, VentaDetalle
from decimal import Decimal
import json


def print_header(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)


def test_materias_primas():
    """Test 1: Verificar materias primas"""
    print_header("TEST 1: MATERIAS PRIMAS")
    
    materias = MateriaPrima.objects.all()
    print(f"\nTotal materias primas: {materias.count()}")
    
    problemas = []
    
    for mp in materias:
        print(f"\n📦 {mp.nombre} (ID: {mp.id})")
        print(f"   Unidad: {mp.get_unidad_medida_display()}")
        print(f"   Costo: ${mp.costo_unitario}/unidad")
        print(f"   Stock: {mp.stock_actual}")
        
        # Verificar problemas
        if mp.costo_unitario <= 0:
            problemas.append(f"❌ {mp.nombre}: Costo unitario = 0")
        
        if mp.stock_actual < 0:
            problemas.append(f"❌ {mp.nombre}: Stock negativo")
    
    if problemas:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(f"   {p}")
    else:
        print("\n✅ Todas las materias primas están correctas")
    
    return len(problemas) == 0


def test_productos():
    """Test 2: Verificar productos y sus costos"""
    print_header("TEST 2: PRODUCTOS Y COSTOS")
    
    productos = Producto.objects.all()
    print(f"\nTotal productos: {productos.count()}")
    
    problemas = []
    
    for p in productos:
        print(f"\n🍪 {p.nombre} (ID: {p.id})")
        print(f"   Precio venta: ${p.precio}")
        print(f"   Stock: {p.stock}")
        print(f"   Tipo: {p.tipo_producto}")
        
        if p.materia_prima_asociada:
            print(f"   Materia prima: {p.materia_prima_asociada.nombre}")
            print(f"   Cantidad fracción: {p.cantidad_fraccion}")
            
            # Calcular costo
            costo = p.calcular_costo_real()
            margen = p.calcular_margen_real()
            
            print(f"   Costo calculado: ${costo}")
            print(f"   Margen: {margen}%")
            
            # Verificar problemas
            if costo <= 0 and p.materia_prima_asociada:
                problemas.append(f"❌ {p.nombre}: Costo calculado = 0")
            
            if margen < 0:
                problemas.append(f"❌ {p.nombre}: Margen negativo ({margen}%)")
            
            # Problema sospechoso: cantidad_fraccion muy grande
            if p.cantidad_fraccion and p.cantidad_fraccion > 100:
                problemas.append(
                    f"⚠️  {p.nombre}: cantidad_fraccion sospechosa = {p.cantidad_fraccion} "
                    f"(MP en {p.materia_prima_asociada.get_unidad_medida_display()})"
                )
            
            # Debug detallado
            debug = p.debug_costo()
            print(f"\n   🔍 DEBUG:")
            print(f"      Formula: {debug.get('formula', 'N/A')}")
            
        elif p.tiene_receta and p.receta:
            print(f"   Receta: {p.receta.nombre}")
            costo = p.calcular_costo_real()
            margen = p.calcular_margen_real()
            print(f"   Costo receta: ${costo}")
            print(f"   Margen: {margen}%")
    
    if problemas:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(f"   {p}")
    else:
        print("\n✅ Todos los productos están correctos")
    
    return len(problemas) == 0


def test_ventas():
    """Test 3: Verificar que se puedan crear ventas"""
    print_header("TEST 3: SISTEMA DE VENTAS")
    
    # Productos disponibles para venta (con stock)
    productos_disponibles = Producto.objects.filter(stock__gt=0)
    
    print(f"\nProductos disponibles para venta: {productos_disponibles.count()}")
    
    if productos_disponibles.count() == 0:
        print("❌ NO HAY PRODUCTOS CON STOCK PARA VENDER")
        return False
    
    print("\n✅ Productos con stock:")
    for p in productos_disponibles:
        print(f"   • {p.nombre} - Stock: {p.stock} - Precio: ${p.precio}")
    
    # Verificar ventas existentes
    ventas = Venta.objects.all()
    print(f"\nVentas registradas: {ventas.count()}")
    
    if ventas.exists():
        print("\nÚltimas 5 ventas:")
        for v in ventas[:5]:
            print(f"   Venta #{v.id} - {v.fecha} - Total: ${v.total}")
    
    return True


def test_calculos_especificos():
    """Test 4: Verificar cálculos específicos problemáticos"""
    print_header("TEST 4: VERIFICACIÓN DE CÁLCULOS PROBLEMÁTICOS")
    
    # Buscar producto "Harina de Almendras" que tiene el problema
    try:
        producto = Producto.objects.get(nombre__icontains="Harina de Almendras")
        
        print(f"\n🔍 Análisis detallado: {producto.nombre}")
        print("-" * 80)
        
        if producto.materia_prima_asociada:
            mp = producto.materia_prima_asociada
            
            print(f"Materia Prima: {mp.nombre}")
            print(f"  • Unidad: {mp.get_unidad_medida_display()}")
            print(f"  • Costo unitario: ${mp.costo_unitario}")
            
            print(f"\nProducto:")
            print(f"  • Cantidad fracción: {producto.cantidad_fraccion}")
            print(f"  • Precio venta: ${producto.precio}")
            
            costo_calculado = mp.costo_unitario * producto.cantidad_fraccion
            print(f"\nCálculo manual:")
            print(f"  {producto.cantidad_fraccion} × ${mp.costo_unitario} = ${costo_calculado}")
            
            costo_sistema = producto.calcular_costo_real()
            margen_sistema = producto.calcular_margen_real()
            
            print(f"\nCálculo del sistema:")
            print(f"  Costo: ${costo_sistema}")
            print(f"  Margen: {margen_sistema}%")
            
            # Verificar si hay discrepancia
            if abs(float(costo_calculado) - float(costo_sistema)) > 0.01:
                print(f"\n❌ DISCREPANCIA ENCONTRADA:")
                print(f"   Manual: ${costo_calculado}")
                print(f"   Sistema: ${costo_sistema}")
                return False
            else:
                print(f"\n✅ Cálculos coinciden")
                
                # Verificar si la cantidad_fraccion es sospechosa
                if producto.cantidad_fraccion > 100:
                    print(f"\n⚠️  WARNING: cantidad_fraccion = {producto.cantidad_fraccion}")
                    print(f"   Para MP en {mp.get_unidad_medida_display()}, esto parece incorrecto")
                    print(f"   ¿Debería ser {producto.cantidad_fraccion/1000} en vez de {producto.cantidad_fraccion}?")
                    
                    # Calcular cómo debería ser
                    cantidad_corregida = producto.cantidad_fraccion / 1000
                    costo_corregido = mp.costo_unitario * Decimal(str(cantidad_corregida))
                    margen_corregido = ((Decimal(str(producto.precio)) - costo_corregido) / Decimal(str(producto.precio))) * 100
                    
                    print(f"\n   Si corregimos a {cantidad_corregida}:")
                    print(f"   Costo: ${costo_corregido}")
                    print(f"   Margen: {margen_corregido}%")
                    
                    return False
        
        return True
        
    except Producto.DoesNotExist:
        print("\n❌ No se encontró el producto 'Harina de Almendras'")
        return False


def generar_reporte_completo():
    """Genera reporte completo del estado del sistema"""
    print("\n" + "="*80)
    print(" REPORTE COMPLETO DEL SISTEMA LINO")
    print("="*80)
    
    resultados = {
        'materias_primas': test_materias_primas(),
        'productos': test_productos(),
        'ventas': test_ventas(),
        'calculos': test_calculos_especificos()
    }
    
    print_header("RESUMEN FINAL")
    print()
    
    total_tests = len(resultados)
    tests_pasados = sum(resultados.values())
    
    for test, resultado in resultados.items():
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{status} - {test.replace('_', ' ').title()}")
    
    print(f"\nTests pasados: {tests_pasados}/{total_tests}")
    
    if tests_pasados == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return 0
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON - Revisar problemas arriba")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(generar_reporte_completo())
