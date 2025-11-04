"""
Dashboard Service - Lógica de negocio del dashboard principal
Centraliza todos los cálculos y queries para el dashboard
"""

from datetime import timedelta, datetime
from decimal import Decimal
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from gestion.models import Producto, Venta, VentaDetalle, Compra


class DashboardService:
    """Servicio para obtener datos del dashboard principal"""
    
    def __init__(self, usuario=None):
        self.usuario = usuario
        self.hoy = timezone.now().date()
        self.inicio_mes = self.hoy.replace(day=1)
        self.inicio_semana = self.hoy - timedelta(days=6)  # Últimos 7 días
    
    def get_kpis_principales(self):
        """Obtiene los 4 KPIs principales del dashboard"""
        
        # 💰 Ventas del Mes
        ventas_mes = Venta.objects.filter(
            fecha__date__gte=self.inicio_mes,
            eliminada=False
        )
        total_ventas_mes = ventas_mes.aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Ventas mes anterior para comparación
        inicio_mes_anterior = (self.inicio_mes - timedelta(days=1)).replace(day=1)
        fin_mes_anterior = self.inicio_mes - timedelta(days=1)
        ventas_mes_anterior = Venta.objects.filter(
            fecha__date__gte=inicio_mes_anterior,
            fecha__date__lte=fin_mes_anterior,
            eliminada=False
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Calcular variación
        if ventas_mes_anterior > 0:
            variacion_ventas = ((total_ventas_mes - ventas_mes_anterior) / ventas_mes_anterior) * 100
        else:
            variacion_ventas = 100 if total_ventas_mes > 0 else 0
        
        # 🌱 Productos Activos
        total_productos = Producto.objects.count()
        productos_bajo_stock = Producto.objects.filter(
            stock__lte=F('stock_minimo'),
            stock__gt=0
        ).count()
        
        # 💎 Valor de Inventario y ROI
        productos_con_stock = Producto.objects.filter(stock__gt=0)
        valor_inventario = sum(
            (p.costo_base or Decimal('0')) * p.stock for p in productos_con_stock
        ) if productos_con_stock.exists() else Decimal('0')
        
        # ROI simple: (ganancia_mes / valor_inventario) * 100
        costo_total_ventas = ventas_mes.aggregate(
            costo_total=Sum(F('detalles__cantidad') * F('detalles__producto__costo_base'))
        )['costo_total']
        ganancia_mes = total_ventas_mes - (costo_total_ventas or Decimal('0'))
        
        roi = (ganancia_mes / valor_inventario * 100) if valor_inventario > 0 else Decimal('0')
        
        # 🚨 Alertas Críticas
        from gestion.models import Alerta
        alertas_count = Alerta.objects.filter(
            usuario=self.usuario,
            leida=False,
            archivada=False,
            nivel='danger'
        ).count() if self.usuario else 0
        
        return {
            'ventas_mes': {
                'total': float(total_ventas_mes),
                'variacion': float(variacion_ventas),
                'sparkline': self._get_sparkline_ventas()
            },
            'productos': {
                'total': total_productos,
                'bajo_stock': productos_bajo_stock,
                'sparkline': self._get_sparkline_productos()
            },
            'inventario': {
                'valor': float(valor_inventario),
                'roi': float(roi),
                'sparkline': self._get_sparkline_inventario()
            },
            'alertas': {
                'count': alertas_count,
                'criticas': alertas_count
            }
        }
    
    def _get_sparkline_ventas(self):
        """Ventas de los últimos 7 días para sparkline"""
        sparkline = []
        for i in range(7):
            fecha = self.hoy - timedelta(days=6-i)
            total = Venta.objects.filter(
                fecha__date=fecha,
                eliminada=False
            ).aggregate(total=Sum('total'))['total'] or Decimal('0')
            sparkline.append(float(total))
        return sparkline
    
    def _get_sparkline_productos(self):
        """Productos vendidos últimos 7 días para sparkline"""
        sparkline = []
        for i in range(7):
            fecha = self.hoy - timedelta(days=6-i)
            total = VentaDetalle.objects.filter(
                venta__fecha__date=fecha,
                venta__eliminada=False
            ).aggregate(total=Sum('cantidad'))['total'] or 0
            sparkline.append(total)
        return sparkline
    
    def _get_sparkline_inventario(self):
        """Simulación de valor de inventario últimos 7 días (requiere histórico)"""
        # Por ahora retornamos valores simulados con tendencia
        # TODO: Implementar histórico de inventario
        valor_actual = Producto.objects.filter(stock__gt=0).aggregate(
            total=Sum(F('stock') * F('costo_base'))
        )['total'] or 0
        
        sparkline = []
        for i in range(7):
            # Simulación con pequeñas variaciones
            variacion = (i - 3) * 0.02  # ±6% variación
            sparkline.append(float(valor_actual * (1 + variacion)))
        return sparkline
    
    def get_resumen_hoy(self):
        """Resumen del día actual"""
        ventas_hoy = Venta.objects.filter(
            fecha__date=self.hoy,
            eliminada=False
        )
        
        total_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or Decimal('0')
        cantidad_ventas_hoy = ventas_hoy.count()
        productos_vendidos_hoy = VentaDetalle.objects.filter(
            venta__fecha__date=self.hoy,
            venta__eliminada=False
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        
        # Comparar con ayer
        ayer = self.hoy - timedelta(days=1)
        total_ayer = Venta.objects.filter(
            fecha__date=ayer,
            eliminada=False
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        variacion_dia = ((total_hoy - total_ayer) / total_ayer * 100) if total_ayer > 0 else 0
        
        return {
            'total_ventas': float(total_hoy),
            'cantidad_ventas': cantidad_ventas_hoy,
            'productos_vendidos': productos_vendidos_hoy,
            'variacion': float(variacion_dia)
        }
    
    def get_actividad_reciente(self, limit=10):
        """Actividad reciente: ventas, compras, alertas"""
        actividades = []
        
        # Ventas recientes
        ventas = Venta.objects.filter(eliminada=False).order_by('-fecha')[:limit]
        for venta in ventas:
            actividades.append({
                'tipo': 'venta',
                'icono': 'bi-cart-check',
                'color': 'success',
                'titulo': f'Venta #{venta.id}',
                'descripcion': f'${venta.total:.2f}',
                'fecha': venta.fecha,
                'url': f'/gestion/ventas/{venta.id}/'
            })
        
        # Compras recientes (últimas 5)
        compras = Compra.objects.order_by('-fecha_compra')[:5]
        for compra in compras:
            actividades.append({
                'tipo': 'compra',
                'icono': 'bi-truck',
                'color': 'info',
                'titulo': f'Compra #{compra.id}',
                'descripcion': f'${compra.precio_mayoreo:.2f}',
                'fecha': compra.fecha_compra,
                'url': f'/gestion/compras/{compra.id}/'
            })
        
        # Ordenar por fecha y limitar (normalizar fechas para comparación)
        def normalize_fecha(x):
            fecha = x['fecha']
            if isinstance(fecha, datetime):
                return fecha
            else:
                # Convertir date a datetime aware
                dt = datetime.combine(fecha, datetime.min.time())
                return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        
        actividades.sort(key=normalize_fecha, reverse=True)
        return actividades[:limit]
    
    def get_top_productos(self, limit=5):
        """Top productos más vendidos del mes"""
        inicio_mes = self.hoy.replace(day=1)
        
        top = VentaDetalle.objects.filter(
            venta__fecha__date__gte=inicio_mes,
            venta__eliminada=False
        ).values(
            'producto__id',
            'producto__nombre',
            'producto__stock',
            'producto__precio',
            'producto__costo_base'
        ).annotate(
            total_vendido=Sum('cantidad'),
            ingresos=Sum(F('cantidad') * F('precio_unitario'))
        ).order_by('-ingresos')[:limit]
        
        # Agregar margen calculado
        for item in top:
            precio = Decimal(str(item['producto__precio']))
            costo = Decimal(str(item['producto__costo_base'] or 0))
            if precio > 0:
                margen = ((precio - costo) / precio * 100)
                item['margen'] = float(margen)
            else:
                item['margen'] = 0
            
            # Estado de stock
            stock = item['producto__stock']
            if stock == 0:
                item['estado_stock'] = 'agotado'
            elif stock <= 10:  # Asumimos stock mínimo de 10
                item['estado_stock'] = 'critico'
            else:
                item['estado_stock'] = 'normal'
        
        return list(top)
    
    def get_dashboard_completo(self):
        """Obtiene todos los datos del dashboard en un solo llamado"""
        return {
            'kpis': self.get_kpis_principales(),
            'resumen_hoy': self.get_resumen_hoy(),
            'actividad_reciente': self.get_actividad_reciente(),
            'top_productos': self.get_top_productos(),
            'fecha_actualizacion': timezone.now()
        }
