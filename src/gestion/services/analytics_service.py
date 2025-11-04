"""
Analytics Service - Cálculos financieros avanzados
ROI, Punto de Equilibrio, Flujo de Caja, Rotación de Inventario
"""

from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, Avg, F, Q
from django.utils import timezone
from gestion.models import Producto, Venta, VentaDetalle, Compra


class AnalyticsService:
    """Servicio para cálculos financieros y analíticos avanzados"""
    
    def __init__(self):
        self.hoy = timezone.now().date()
        self.inicio_mes = self.hoy.replace(day=1)
    
    def calcular_roi(self, periodo_dias=30):
        """
        ROI (Return on Investment)
        ROI = (Ganancia Neta / Inversión) * 100
        
        Args:
            periodo_dias: Días a analizar (default 30)
        Returns:
            dict con roi, ganancia, inversion
        """
        fecha_inicio = self.hoy - timedelta(days=periodo_dias)
        
        # Ingresos del período
        ingresos = Venta.objects.filter(
            fecha__date__gte=fecha_inicio,
            eliminada=False
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Costos de productos vendidos
        costos_vendidos = VentaDetalle.objects.filter(
            venta__fecha__date__gte=fecha_inicio,
            venta__eliminada=False
        ).aggregate(
            total=Sum(F('cantidad') * F('producto__costo_base'))
        )['total'] or Decimal('0')
        
        # Inversión en inventario actual
        inversion_inventario = Producto.objects.filter(
            stock__gt=0
        ).aggregate(
            total=Sum(F('stock') * F('costo_base'))
        )['total'] or Decimal('1')  # Evitar división por 0
        
        ganancia_neta = ingresos - costos_vendidos
        roi = (ganancia_neta / inversion_inventario * 100) if inversion_inventario > 0 else Decimal('0')
        
        return {
            'roi': float(roi),
            'ganancia_neta': float(ganancia_neta),
            'inversion': float(inversion_inventario),
            'ingresos': float(ingresos),
            'periodo_dias': periodo_dias
        }
    
    def calcular_punto_equilibrio(self):
        """
        Punto de Equilibrio
        BE = Costos Fijos / (Precio Promedio - Costo Variable Promedio)
        
        Returns:
            dict con unidades_equilibrio, ventas_equilibrio
        """
        # Costos fijos estimados (podrías tener un modelo de Gastos)
        # Por ahora lo estimamos como un % de las ventas
        ventas_mes = Venta.objects.filter(
            fecha__date__gte=self.inicio_mes,
            eliminada=False
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        costos_fijos_estimados = ventas_mes * Decimal('0.15')  # 15% de ventas
        
        # Precio promedio y costo variable promedio
        productos_activos = Producto.objects.filter(stock__gt=0)
        
        if productos_activos.exists():
            precio_promedio = productos_activos.aggregate(
                promedio=Avg('precio_venta')
            )['promedio'] or Decimal('0')
            
            costo_promedio = productos_activos.aggregate(
                promedio=Avg('costo')
            )['promedio'] or Decimal('0')
            
            margen_contribucion = precio_promedio - costo_promedio
            
            if margen_contribucion > 0:
                unidades_equilibrio = costos_fijos_estimados / margen_contribucion
                ventas_equilibrio = unidades_equilibrio * precio_promedio
            else:
                unidades_equilibrio = Decimal('0')
                ventas_equilibrio = Decimal('0')
        else:
            unidades_equilibrio = Decimal('0')
            ventas_equilibrio = Decimal('0')
            precio_promedio = Decimal('0')
            costo_promedio = Decimal('0')
        
        return {
            'unidades_equilibrio': float(unidades_equilibrio),
            'ventas_equilibrio': float(ventas_equilibrio),
            'costos_fijos': float(costos_fijos_estimados),
            'precio_promedio': float(precio_promedio),
            'costo_promedio': float(costo_promedio)
        }
    
    def calcular_flujo_caja_proyectado(self, dias=30):
        """
        Flujo de Caja Proyectado
        Proyección basada en promedio de ventas y costos
        
        Args:
            dias: Días a proyectar (default 30)
        Returns:
            dict con flujo_proyectado, ingresos_esperados, egresos_esperados
        """
        # Promedio diario de ventas (últimos 30 días)
        hace_30_dias = self.hoy - timedelta(days=30)
        
        ventas_30d = Venta.objects.filter(
            fecha__date__gte=hace_30_dias,
            eliminada=False
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        promedio_ventas_diarias = ventas_30d / 30 if ventas_30d > 0 else Decimal('0')
        
        # Promedio diario de compras (últimos 30 días)
        compras_30d = Compra.objects.filter(
            fecha_compra__gte=hace_30_dias
        ).aggregate(total=Sum('precio_mayoreo'))['total'] or Decimal('0')
        
        promedio_compras_diarias = compras_30d / 30 if compras_30d > 0 else Decimal('0')
        
        # Proyección
        ingresos_proyectados = promedio_ventas_diarias * dias
        egresos_proyectados = promedio_compras_diarias * dias
        flujo_neto = ingresos_proyectados - egresos_proyectados
        
        return {
            'flujo_proyectado': float(flujo_neto),
            'ingresos_esperados': float(ingresos_proyectados),
            'egresos_esperados': float(egresos_proyectados),
            'promedio_diario_ventas': float(promedio_ventas_diarias),
            'promedio_diario_compras': float(promedio_compras_diarias),
            'dias': dias
        }
    
    def calcular_rotacion_inventario(self):
        """
        Rotación de Inventario
        Rotación = Costo de Ventas del Período / Inventario Promedio
        Días de Inventario = 30 / Rotación
        
        Returns:
            dict con rotacion, dias_inventario, costo_ventas, inventario_promedio
        """
        # Costo de ventas del mes
        costo_ventas_mes = VentaDetalle.objects.filter(
            venta__fecha__date__gte=self.inicio_mes,
            venta__eliminada=False
        ).aggregate(
            total=Sum(F('cantidad') * F('producto__costo_base'))
        )['total'] or Decimal('0')
        
        # Inventario actual
        inventario_actual = Producto.objects.filter(
            stock__gt=0
        ).aggregate(
            total=Sum(F('stock') * F('costo_base'))
        )['total'] or Decimal('1')
        
        # Inventario promedio (simplificado, usamos inventario actual)
        # TODO: Implementar histórico de inventario para promedio real
        inventario_promedio = inventario_actual
        
        # Rotación
        if inventario_promedio > 0:
            rotacion = costo_ventas_mes / inventario_promedio
            dias_inventario = 30 / rotacion if rotacion > 0 else 999
        else:
            rotacion = Decimal('0')
            dias_inventario = 999
        
        # Clasificación
        if dias_inventario < 15:
            clasificacion = 'excelente'
        elif dias_inventario < 30:
            clasificacion = 'buena'
        elif dias_inventario < 60:
            clasificacion = 'regular'
        else:
            clasificacion = 'mala'
        
        return {
            'rotacion': float(rotacion),
            'dias_inventario': float(dias_inventario),
            'costo_ventas_mes': float(costo_ventas_mes),
            'inventario_promedio': float(inventario_promedio),
            'clasificacion': clasificacion
        }
    
    def calcular_salud_financiera(self):
        """
        Widget "Salud Financiera"
        Combina múltiples métricas en un score de 0-100
        
        Returns:
            dict con score_total y métricas individuales
        """
        roi = self.calcular_roi(30)
        rotacion = self.calcular_rotacion_inventario()
        flujo = self.calcular_flujo_caja_proyectado(30)
        
        # Productos con stock bajo (riesgo)
        total_productos = Producto.objects.count()
        productos_riesgo = Producto.objects.filter(
            Q(stock__lte=F('stock_minimo')) | Q(stock=0)
        ).count()
        
        # Score Liquidez (basado en flujo de caja)
        if flujo['flujo_proyectado'] >= 10000:
            score_liquidez = 100
        elif flujo['flujo_proyectado'] >= 5000:
            score_liquidez = 80
        elif flujo['flujo_proyectado'] >= 0:
            score_liquidez = 60
        else:
            score_liquidez = 30
        
        # Score Rentabilidad (basado en ROI)
        if roi['roi'] >= 30:
            score_rentabilidad = 100
        elif roi['roi'] >= 20:
            score_rentabilidad = 80
        elif roi['roi'] >= 10:
            score_rentabilidad = 60
        else:
            score_rentabilidad = 30
        
        # Score Eficiencia (basado en rotación)
        if rotacion['clasificacion'] == 'excelente':
            score_eficiencia = 100
        elif rotacion['clasificacion'] == 'buena':
            score_eficiencia = 80
        elif rotacion['clasificacion'] == 'regular':
            score_eficiencia = 60
        else:
            score_eficiencia = 30
        
        # Score Crecimiento (basado en % productos con stock saludable)
        pct_stock_saludable = ((total_productos - productos_riesgo) / total_productos * 100) if total_productos > 0 else 0
        
        if pct_stock_saludable >= 90:
            score_crecimiento = 100
        elif pct_stock_saludable >= 75:
            score_crecimiento = 80
        elif pct_stock_saludable >= 60:
            score_crecimiento = 60
        else:
            score_crecimiento = 30
        
        # Score total (promedio ponderado)
        score_total = (
            score_liquidez * 0.30 +
            score_rentabilidad * 0.35 +
            score_eficiencia * 0.20 +
            score_crecimiento * 0.15
        )
        
        # Clasificación general
        if score_total >= 85:
            clasificacion = 'excelente'
            emoji = '💚'
        elif score_total >= 70:
            clasificacion = 'buena'
            emoji = '💙'
        elif score_total >= 50:
            clasificacion = 'regular'
            emoji = '💛'
        else:
            clasificacion = 'mala'
            emoji = '❤️'
        
        return {
            'score_total': round(score_total, 1),
            'clasificacion': clasificacion,
            'emoji': emoji,
            'liquidez': {
                'score': score_liquidez,
                'valor': flujo['flujo_proyectado']
            },
            'rentabilidad': {
                'score': score_rentabilidad,
                'valor': roi['roi']
            },
            'eficiencia': {
                'score': score_eficiencia,
                'valor': rotacion['dias_inventario']
            },
            'crecimiento': {
                'score': score_crecimiento,
                'valor': pct_stock_saludable
            }
        }
