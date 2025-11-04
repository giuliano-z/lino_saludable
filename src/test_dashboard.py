#!/usr/bin/env python
"""
Test Automatizado - Dashboard LINO
Verifica funcionalidad de FASE 1 + FASE 2
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from gestion.models import Producto, Venta, VentaDetalle
from gestion.services.dashboard_service import DashboardService
from gestion.services.alertas_service import AlertasService

User = get_user_model()

class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
        
    def assert_true(self, condition, message):
        """Assert que condición es True"""
        if condition:
            self.tests_passed += 1
            print(f"✅ {message}")
        else:
            self.tests_failed += 1
            self.failures.append(message)
            print(f"❌ {message}")
            
    def assert_equals(self, actual, expected, message):
        """Assert igualdad"""
        if actual == expected:
            self.tests_passed += 1
            print(f"✅ {message}")
        else:
            self.tests_failed += 1
            self.failures.append(f"{message} - Expected: {expected}, Got: {actual}")
            print(f"❌ {message} - Expected: {expected}, Got: {actual}")
            
    def assert_gt(self, actual, threshold, message):
        """Assert mayor que"""
        if actual > threshold:
            self.tests_passed += 1
            print(f"✅ {message} ({actual} > {threshold})")
        else:
            self.tests_failed += 1
            self.failures.append(f"{message} - {actual} <= {threshold}")
            print(f"❌ {message} - {actual} <= {threshold}")
            
    def print_summary(self):
        """Imprimir resumen"""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE TESTS")
        print("="*60)
        print(f"✅ Aprobados: {self.tests_passed}")
        print(f"❌ Fallidos:  {self.tests_failed}")
        print(f"📈 Total:     {total}")
        print(f"🎯 Éxito:     {percentage:.1f}%")
        print("="*60)
        
        if self.failures:
            print("\n⚠️  TESTS FALLIDOS:")
            for i, failure in enumerate(self.failures, 1):
                print(f"{i}. {failure}")
        
        if percentage >= 95:
            print("\n🎉 ¡APROBADO! Sistema funcionando correctamente")
            return 0
        elif percentage >= 80:
            print("\n⚠️  NECESITA AJUSTES - Revisar tests fallidos")
            return 1
        else:
            print("\n❌ REQUIERE CORRECCIONES - Múltiples problemas detectados")
            return 2


def main():
    runner = TestRunner()
    
    print("🧪 INICIANDO TESTS AUTOMATIZADOS")
    print("="*60)
    
    # ==========================================
    # TESTS DE MODELOS
    # ==========================================
    print("\n📦 1. TESTS DE MODELOS")
    print("-"*60)
    
    productos_count = Producto.objects.count()
    runner.assert_gt(productos_count, 0, "Existen productos en BD")
    
    ventas_count = Venta.objects.filter(eliminada=False).count()
    runner.assert_gt(ventas_count, 0, "Existen ventas en BD")
    
    # Verificar producto tiene campo 'precio'
    if productos_count > 0:
        producto = Producto.objects.first()
        runner.assert_true(hasattr(producto, 'precio'), "Producto tiene campo 'precio'")
        runner.assert_true(not hasattr(producto, 'precio_venta'), "Producto NO tiene campo 'precio_venta' directo")
    
    # ==========================================
    # TESTS DE DASHBOARD SERVICE
    # ==========================================
    print("\n📊 2. TESTS DE DASHBOARD SERVICE")
    print("-"*60)
    
    try:
        user = User.objects.first()
        dashboard = DashboardService(usuario=user)
        
        # Test get_kpis_principales
        kpis = dashboard.get_kpis_principales()
        runner.assert_true('ventas_mes' in kpis, "KPIs incluyen 'ventas_mes'")
        runner.assert_true('productos' in kpis, "KPIs incluyen 'productos'")
        runner.assert_true('inventario' in kpis, "KPIs incluyen 'inventario'")
        runner.assert_true('alertas' in kpis, "KPIs incluyen 'alertas'")
        
        # Verificar estructura de ventas_mes
        runner.assert_true('total' in kpis['ventas_mes'], "ventas_mes tiene 'total'")
        runner.assert_true('variacion' in kpis['ventas_mes'], "ventas_mes tiene 'variacion'")
        runner.assert_true('sparkline' in kpis['ventas_mes'], "ventas_mes tiene 'sparkline'")
        
        # Test get_resumen_hoy
        resumen = dashboard.get_resumen_hoy()
        runner.assert_true('total_ventas' in resumen, "resumen_hoy tiene 'total_ventas'")
        runner.assert_true('cantidad_ventas' in resumen, "resumen_hoy tiene 'cantidad_ventas'")
        runner.assert_true('productos_vendidos' in resumen, "resumen_hoy tiene 'productos_vendidos'")
        
        # Test get_ventas_por_periodo (FASE 2)
        ventas_7d = dashboard.get_ventas_por_periodo(dias=7, comparar=False)
        runner.assert_true('labels' in ventas_7d, "ventas_periodo tiene 'labels'")
        runner.assert_true('datos' in ventas_7d, "ventas_periodo tiene 'datos'")
        runner.assert_true('total' in ventas_7d, "ventas_periodo tiene 'total'")
        runner.assert_true('promedio' in ventas_7d, "ventas_periodo tiene 'promedio'")
        
        runner.assert_equals(len(ventas_7d['labels']), 7, "ventas_7d tiene 7 labels")
        runner.assert_equals(len(ventas_7d['datos']), 7, "ventas_7d tiene 7 datos")
        
        # Test comparación
        ventas_comparar = dashboard.get_ventas_por_periodo(dias=7, comparar=True)
        runner.assert_true('datos_anterior' in ventas_comparar, "Con comparar=True incluye 'datos_anterior'")
        runner.assert_true('variacion' in ventas_comparar, "Con comparar=True incluye 'variacion'")
        
        # Test get_top_productos_grafico (FASE 2)
        top5 = dashboard.get_top_productos_grafico(dias=30, limit=5)
        runner.assert_true('labels' in top5, "top_productos tiene 'labels'")
        runner.assert_true('ingresos' in top5, "top_productos tiene 'ingresos'")
        runner.assert_true(len(top5['labels']) <= 5, "top_productos limitado a 5")
        
    except Exception as e:
        runner.assert_true(False, f"DashboardService funciona sin errores: {str(e)}")
    
    # ==========================================
    # TESTS DE ALERTAS SERVICE
    # ==========================================
    print("\n🔔 3. TESTS DE ALERTAS SERVICE")
    print("-"*60)
    
    try:
        # Verificar que no usa precio_venta
        from gestion.services import alertas_service
        import inspect
        
        source = inspect.getsource(alertas_service)
        runner.assert_true(
            'producto.precio_venta' not in source,
            "AlertasService NO usa 'producto.precio_venta'"
        )
        runner.assert_true(
            'producto.precio' in source or 'Decimal(str(producto.precio))' in source,
            "AlertasService usa 'producto.precio' correctamente"
        )
        
    except Exception as e:
        runner.assert_true(False, f"AlertasService se puede inspeccionar: {str(e)}")
    
    # ==========================================
    # TESTS DE INTEGRIDAD DE DATOS
    # ==========================================
    print("\n🔍 4. TESTS DE INTEGRIDAD DE DATOS")
    print("-"*60)
    
    # Verificar que hay ventas de HOY para testing
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha__date=hoy, eliminada=False)
    runner.assert_gt(ventas_hoy.count(), 0, f"Existen ventas HOY ({hoy}) para testing")
    
    if ventas_hoy.exists():
        venta = ventas_hoy.first()
        runner.assert_gt(venta.total, 0, "Venta tiene total > 0")
        
        detalles = VentaDetalle.objects.filter(venta=venta)
        runner.assert_gt(detalles.count(), 0, "Venta tiene detalles")
    
    # ==========================================
    # TESTS DE RENDIMIENTO
    # ==========================================
    print("\n⚡ 5. TESTS DE RENDIMIENTO")
    print("-"*60)
    
    import time
    from django.db import connection
    from django.test.utils import override_settings
    
    # Test velocidad de get_kpis_principales
    start = time.time()
    queries_before = len(connection.queries)
    
    kpis = dashboard.get_kpis_principales()
    
    queries_after = len(connection.queries)
    elapsed = (time.time() - start) * 1000  # ms
    
    queries_count = queries_after - queries_before
    runner.assert_true(elapsed < 500, f"get_kpis_principales < 500ms ({elapsed:.0f}ms)")
    runner.assert_true(queries_count < 15, f"get_kpis_principales < 15 queries ({queries_count} queries)")
    
    # Test velocidad de get_ventas_por_periodo
    start = time.time()
    ventas = dashboard.get_ventas_por_periodo(dias=30)
    elapsed = (time.time() - start) * 1000
    
    runner.assert_true(elapsed < 200, f"get_ventas_por_periodo < 200ms ({elapsed:.0f}ms)")
    
    # ==========================================
    # RESUMEN
    # ==========================================
    return runner.print_summary()


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
