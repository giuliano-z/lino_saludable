#!/usr/bin/env python3
"""
Test completo de todos los dashboards y servicios
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
django.setup()

from decimal import Decimal
from django.utils import timezone
from gestion.models import Producto, Venta, VentaDetalle, ConfiguracionCostos, Compra
from gestion.services.dashboard_service import DashboardService
from gestion.services.rentabilidad_service import RentabilidadService
from gestion.services.inventario_service import InventarioService

def print_separator():
    print("\n" + "="*70)

def test_dashboard_principal():
    """Test del Dashboard Principal"""
    print_separator()
    print("🎯 TEST 1: DASHBOARD PRINCIPAL")
    print_separator()
    
    try:
        service = DashboardService()
        kpis = service.get_kpis_principales()
        
        print("\n✅ Dashboard Principal - KPIs:")
        print(f"   Ventas del Mes: ${kpis['ventas_mes']['total']:,.2f}")
        print(f"   Variación: {kpis['ventas_mes']['variacion']:+.1f}%")
        
        print(f"\n   Compras del Mes: ${kpis['compras_mes']['total']:,.2f}")
        print(f"   Variación: {kpis['compras_mes']['variacion']:+.1f}%")
        
        print(f"\n   Ganancia Neta: ${kpis['ganancia_neta']['total']:,.2f}")
        print(f"   Margen: {kpis['ganancia_neta']['margen']:.1f}%")
        
        print(f"\n   Alertas: {kpis['alertas']['count']}")
        
        # Validaciones
        assert 'ventas_mes' in kpis
        assert 'compras_mes' in kpis
        assert 'ganancia_neta' in kpis
        assert 'alertas' in kpis
        
        print("\n✅ TEST PASADO: Dashboard Principal")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en Dashboard Principal: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_rentabilidad():
    """Test del Dashboard de Rentabilidad"""
    print_separator()
    print("💰 TEST 2: DASHBOARD DE RENTABILIDAD")
    print_separator()
    
    try:
        service = RentabilidadService()
        
        # Test 1: KPIs Rentabilidad
        print("\n📊 Test 2.1: KPIs de Rentabilidad")
        kpis = service.get_kpis_rentabilidad()
        
        print(f"\n   Objetivo de Margen:")
        print(f"   - Meta: {kpis['objetivo_margen']['meta']:.1f}%")
        print(f"   - Actual: {kpis['objetivo_margen']['actual']:.1f}%")
        print(f"   - Gap: {kpis['objetivo_margen']['gap']:.1f}%")
        print(f"   - Progreso: {kpis['objetivo_margen']['progreso']:.1f}%")
        print(f"   - Alcanzado: {kpis['objetivo_margen']['alcanzado']}")
        
        print(f"\n   Productos Rentables: {kpis['rentables']['porcentaje']:.1f}%")
        print(f"   ({kpis['rentables']['cantidad']}/{kpis['rentables']['total']} productos)")
        
        print(f"\n   Productos en Pérdida: {kpis['en_perdida']['porcentaje']:.1f}%")
        print(f"   ({kpis['en_perdida']['cantidad']}/{kpis['en_perdida']['total']} productos)")
        
        print(f"\n   Margen Promedio: {kpis['margen_promedio']['valor']:.1f}%")
        print(f"   Ponderado: {kpis['margen_promedio']['ponderado']}")
        
        # Validaciones
        assert 'objetivo_margen' in kpis
        assert 'rentables' in kpis
        assert 'en_perdida' in kpis
        assert 'margen_promedio' in kpis
        
        # Test 2: Análisis de Objetivo
        print("\n📊 Test 2.2: Análisis de Objetivo de Margen")
        analisis = service.get_objetivo_margen_analisis()
        
        print(f"\n   Total Productos: {analisis['total_productos']}")
        print(f"   Productos Cumpliendo: {analisis['productos_cumpliendo']}")
        print(f"   Productos Críticos: {len(analisis['productos_criticos'])}")
        print(f"   Recomendaciones: {len(analisis['recomendaciones'])}")
        
        if analisis['recomendaciones']:
            print("\n   Top 3 Recomendaciones:")
            for i, rec in enumerate(analisis['recomendaciones'][:3], 1):
                print(f"   {i}. [{rec['prioridad'].upper()}] {rec['titulo']}")
                print(f"      Impacto: +{rec['impacto_estimado']:.1f}%")
                print(f"      Productos: {rec['productos_afectados']}")
        
        # Validaciones
        assert 'total_productos' in analisis
        assert 'recomendaciones' in analisis
        assert isinstance(analisis['productos_criticos'], list)
        
        # Test 3: Productos Rentabilidad
        print("\n📊 Test 2.3: Lista de Productos con Rentabilidad")
        productos = service.get_productos_rentabilidad()
        
        print(f"\n   Total Productos: {len(productos)}")
        if productos:
            print(f"\n   Ejemplo (primeros 3):")
            for i, p in enumerate(productos[:3], 1):
                print(f"   {i}. {p['nombre']}")
                print(f"      Costo: ${p['costo']:.2f}")
                print(f"      Precio: ${p['precio_actual']:.2f}")
                print(f"      Margen: {p['margen']:.1f}%")
                print(f"      En Pérdida: {p['en_perdida']}")
                print(f"      Cumple Objetivo: {p['cumple_objetivo']}")
                print(f"      Ventas Mes: {p['ventas_mes']}")
        
        # Validaciones
        assert isinstance(productos, list)
        if productos:
            assert 'nombre' in productos[0]
            assert 'margen' in productos[0]
            assert 'ventas_mes' in productos[0]
        
        print("\n✅ TEST PASADO: Dashboard de Rentabilidad")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en Dashboard de Rentabilidad: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_inventario():
    """Test del Dashboard de Inventario"""
    print_separator()
    print("📦 TEST 3: DASHBOARD DE INVENTARIO")
    print_separator()
    
    try:
        service = InventarioService()
        kpis = service.get_kpis_inventario()
        
        print("\n✅ Dashboard Inventario - KPIs:")
        
        # Cobertura
        print(f"\n   Cobertura de Stock:")
        print(f"   - Días: {kpis['cobertura_dias']['dias']:.0f}")
        print(f"   - Estado: {kpis['cobertura_dias']['estado']}")
        print(f"   - Mensaje: {kpis['cobertura_dias']['mensaje']}")
        print(f"   - Productos Críticos: {kpis['cobertura_dias']['productos_criticos']}")
        
        # Stock Crítico
        print(f"\n   Stock Crítico:")
        print(f"   - Cantidad: {kpis['stock_critico']['cantidad']}")
        print(f"   - Porcentaje: {kpis['stock_critico']['porcentaje']:.1f}%")
        print(f"   - Productos: {len(kpis['stock_critico']['productos'])}")
        
        # Última Compra
        print(f"\n   Última Compra:")
        print(f"   - Días Desde: {kpis['ultima_compra']['dias_desde']}")
        print(f"   - Fecha: {kpis['ultima_compra']['fecha']}")
        
        # Valor Total
        print(f"\n   Valor Total:")
        print(f"   - Valor: ${kpis['valor_total']['valor']:,.2f}")
        print(f"   - Total (alias): ${kpis['valor_total']['total']:,.2f}")
        print(f"   - Productos: {kpis['valor_total']['productos']}")
        print(f"   - Cantidad Productos (alias): {kpis['valor_total']['cantidad_productos']}")
        
        # Rotación
        print(f"\n   Rotación de Inventario:")
        print(f"   - Veces/Mes: {kpis['rotacion']['veces']:.2f}x")
        print(f"   - Estado: {kpis['rotacion']['estado']}")
        print(f"   - Mensaje: {kpis['rotacion']['mensaje']}")
        print(f"   - Productos Rotación Lenta: {len(kpis['rotacion']['productos_rotacion_lenta'])}")
        
        # Validaciones
        assert 'cobertura_dias' in kpis
        assert 'stock_critico' in kpis
        assert 'ultima_compra' in kpis
        assert 'valor_total' in kpis
        assert 'rotacion' in kpis
        
        # Validar estructura valor_total
        assert 'valor' in kpis['valor_total']
        assert 'total' in kpis['valor_total']  # Alias
        assert 'productos' in kpis['valor_total']
        assert 'cantidad_productos' in kpis['valor_total']  # Alias
        
        print("\n✅ TEST PASADO: Dashboard de Inventario")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en Dashboard de Inventario: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_configuracion():
    """Test de Configuración de Objetivos"""
    print_separator()
    print("⚙️ TEST 4: CONFIGURACIÓN DE OBJETIVOS")
    print_separator()
    
    try:
        config = ConfiguracionCostos.get_config()
        
        print("\n✅ Configuración Actual:")
        print(f"   Margen Objetivo: {config.margen_objetivo}%")
        print(f"   Rotación Objetivo: {config.rotacion_objetivo}x/mes")
        print(f"   Cobertura Objetivo: {config.cobertura_objetivo_dias} días")
        
        # Validaciones
        assert hasattr(config, 'margen_objetivo')
        assert hasattr(config, 'rotacion_objetivo')
        assert hasattr(config, 'cobertura_objetivo_dias')
        
        print("\n✅ TEST PASADO: Configuración")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en Configuración: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_datos_existentes():
    """Verificar datos en base de datos"""
    print_separator()
    print("📊 VERIFICACIÓN DE DATOS")
    print_separator()
    
    print(f"\n   Productos: {Producto.objects.count()}")
    print(f"   Ventas: {Venta.objects.count()}")
    print(f"   Ventas Detalle: {VentaDetalle.objects.count()}")
    print(f"   Compras: {Compra.objects.count()}")
    
    if Producto.objects.count() == 0:
        print("\n   ⚠️ ADVERTENCIA: No hay productos. Los KPIs pueden estar vacíos.")

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print(" "*15 + "🧪 SUITE COMPLETA DE TESTS")
    print(" "*15 + "DASHBOARDS CON MÉTRICAS INTELIGENTES")
    print("="*70)
    
    # Verificar datos
    test_datos_existentes()
    
    # Ejecutar tests
    results = {
        'Dashboard Principal': test_dashboard_principal(),
        'Rentabilidad': test_rentabilidad(),
        'Inventario': test_inventario(),
        'Configuración': test_configuracion(),
    }
    
    # Resumen
    print_separator()
    print("📋 RESUMEN DE TESTS")
    print_separator()
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    for name, result in results.items():
        status = "✅ PASADO" if result else "❌ FALLADO"
        print(f"   {name}: {status}")
    
    print(f"\n   Total: {total}")
    print(f"   Pasados: {passed} ✅")
    print(f"   Fallados: {failed} {'❌' if failed > 0 else ''}")
    
    if failed == 0:
        print("\n" + "="*70)
        print(" "*20 + "🎉 TODOS LOS TESTS PASARON! 🎉")
        print("="*70)
        return True
    else:
        print("\n" + "="*70)
        print(" "*15 + f"⚠️ {failed} TEST(S) FALLARON")
        print("="*70)
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
