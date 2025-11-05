#!/usr/bin/env python
"""
🧪 Test de Nuevos KPIs - LINO Dietética
Verifica que los nuevos servicios funcionen correctamente
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.services.dashboard_service import DashboardService
from gestion.services.rentabilidad_service import RentabilidadService
from gestion.services.inventario_service import InventarioService
from decimal import Decimal

def test_dashboard_service():
    """Test del servicio principal del dashboard"""
    print("\n" + "="*80)
    print("🎯 TEST: DashboardService - KPIs Principales")
    print("="*80)
    
    service = DashboardService()
    kpis = service.get_kpis_principales()
    
    print(f"\n📊 KPIs Retornados:")
    for key in kpis.keys():
        print(f"   - {key}")
    
    print(f"\n💰 VENTAS DEL MES:")
    if 'ventas_mes' in kpis:
        print(f"   Total: ${kpis['ventas_mes'].get('total', 0):,.2f}")
        print(f"   Variación: {kpis['ventas_mes'].get('variacion', 0):+.1f}%")
        print(f"   Sparkline: {kpis['ventas_mes'].get('sparkline', [])}")
    
    print(f"\n🛒 COMPRAS DEL MES:")
    if 'compras_mes' in kpis:
        print(f"   Total: ${kpis['compras_mes'].get('total', 0):,.2f}")
        print(f"   Variación: {kpis['compras_mes'].get('variacion', 0):+.1f}%")
        print(f"   Sparkline: {kpis['compras_mes'].get('sparkline', [])}")
    else:
        print(f"   ❌ KPI 'compras_mes' NO ENCONTRADO")
    
    print(f"\n💎 GANANCIA NETA:")
    if 'ganancia_neta' in kpis:
        ganancia = kpis['ganancia_neta'].get('total', 0)
        margen = kpis['ganancia_neta'].get('margen', 0)
        print(f"   Total: ${ganancia:,.2f}")
        print(f"   Margen: {margen:.1f}%")
        print(f"   Estado: {'✅ POSITIVA' if ganancia >= 0 else '⚠️ NEGATIVA'}")
    else:
        print(f"   ❌ KPI 'ganancia_neta' NO ENCONTRADO")
    
    print(f"\n🔔 ALERTAS:")
    if 'alertas' in kpis:
        print(f"   Total: {kpis['alertas'].get('total', 0)}")
        print(f"   Variación: {kpis['alertas'].get('variacion', 0):+.1f}%")
    
    return kpis

def test_rentabilidad_service():
    """Test del servicio de rentabilidad"""
    print("\n" + "="*80)
    print("💰 TEST: RentabilidadService - Análisis de Margen")
    print("="*80)
    
    service = RentabilidadService()
    kpis = service.get_kpis_rentabilidad()
    
    print(f"\n📈 Objetivo de Margen:")
    if 'objetivo_margen' in kpis:
        obj = kpis['objetivo_margen']
        print(f"   Objetivo: {obj.get('objetivo', 0):.1f}%")
        print(f"   Actual: {obj.get('actual', 0):.1f}%")
        print(f"   Gap: {obj.get('gap', 0):+.1f}%")
        print(f"   Estado: {obj.get('estado', 'N/A')}")
    
    print(f"\n🎯 Análisis Detallado:")
    analisis = service.get_objetivo_margen_analisis()
    print(f"   Productos totales: {analisis.get('total_productos', 0)}")
    print(f"   Cumpliendo objetivo: {analisis.get('productos_cumpliendo', 0)}")
    print(f"   Críticos: {len(analisis.get('productos_criticos', []))}")
    
    print(f"\n💡 Recomendaciones:")
    recomendaciones = analisis.get('recomendaciones', [])
    for i, rec in enumerate(recomendaciones[:3], 1):
        print(f"   {i}. {rec.get('titulo', 'N/A')}")
        print(f"      → {rec.get('descripcion', 'N/A')}")
    
    return kpis

def test_inventario_service():
    """Test del servicio de inventario"""
    print("\n" + "="*80)
    print("📦 TEST: InventarioService - Métricas Predictivas")
    print("="*80)
    
    service = InventarioService()
    kpis = service.get_kpis_inventario()
    
    print(f"\n⏱️  Cobertura de Stock:")
    if 'cobertura_dias' in kpis:
        cob = kpis['cobertura_dias']
        print(f"   Días promedio: {cob.get('dias', 0):.1f}")
        print(f"   Estado: {cob.get('estado', 'N/A')}")
        print(f"   Objetivo: {cob.get('objetivo', 0)} días")
        print(f"   Mensaje: {cob.get('mensaje', 'N/A')}")
    else:
        print(f"   ❌ KPI 'cobertura_dias' NO ENCONTRADO")
    
    print(f"\n🔄 Rotación de Inventario:")
    if 'rotacion' in kpis:
        rot = kpis['rotacion']
        print(f"   Rotación: {rot.get('valor', 0):.2f}x/mes")
        print(f"   Estado: {rot.get('estado', 'N/A')}")
        print(f"   Objetivo: {rot.get('objetivo', 0):.0f}x/mes")
        print(f"   Mensaje: {rot.get('mensaje', 'N/A')}")
    else:
        print(f"   ❌ KPI 'rotacion' NO ENCONTRADO")
    
    print(f"\n🛒 Última Compra:")
    if 'ultima_compra' in kpis:
        ult = kpis['ultima_compra']
        print(f"   Días desde última: {ult.get('dias', 0)}")
        print(f"   Frecuencia promedio: {ult.get('frecuencia_promedio', 0):.1f} días")
        print(f"   Estado: {ult.get('estado', 'N/A')}")
        print(f"   Mensaje: {ult.get('mensaje', 'N/A')}")
    else:
        print(f"   ❌ KPI 'ultima_compra' NO ENCONTRADO")
    
    return kpis

def main():
    """Ejecuta todos los tests"""
    print("\n" + "🌿"*40)
    print(" "*20 + "LINO DIETÉTICA")
    print(" "*15 + "Test de Nuevos KPIs")
    print("🌿"*40)
    
    try:
        # Test Dashboard
        dashboard_kpis = test_dashboard_service()
        
        # Test Rentabilidad
        rentabilidad_kpis = test_rentabilidad_service()
        
        # Test Inventario
        inventario_kpis = test_inventario_service()
        
        print("\n" + "="*80)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("="*80)
        print("\n💡 Próximos pasos:")
        print("   1. Verificar que los datos se muestren correctamente en el Dashboard")
        print("   2. Configurar objetivos desde /gestion/configuracion/negocio/")
        print("   3. Revisar recomendaciones automáticas de rentabilidad")
        print("   4. Analizar productos con rotación lenta")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
