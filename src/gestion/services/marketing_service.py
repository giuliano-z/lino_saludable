"""
Marketing Service - Análisis de tendencias y cross-selling
"""

from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, Count, F, Q, Avg
from django.utils import timezone
from gestion.models import Producto, Venta, VentaDetalle
from collections import defaultdict, Counter


class MarketingService:
    """Servicio para análisis de marketing y recomendaciones"""
    
    def __init__(self):
        self.hoy = timezone.now().date()
        self.inicio_mes = self.hoy.replace(day=1)
        self.inicio_semana = self.hoy - timedelta(days=6)
    
    def get_productos_trending(self, limit=5):
        """
        Análisis de tendencias de demanda
        Productos con mayor crecimiento en ventas
        
        Returns:
            list de productos con tendencia positiva
        """
        # Ventas últimos 7 días
        ventas_semana = VentaDetalle.objects.filter(
            venta__fecha__date__gte=self.inicio_semana,
            venta__eliminada=False
        ).values('producto').annotate(
            total_semana=Sum('cantidad')
        )
        
        # Ventas semana anterior
        inicio_semana_anterior = self.inicio_semana - timedelta(days=7)
        fin_semana_anterior = self.inicio_semana - timedelta(days=1)
        
        ventas_semana_anterior = VentaDetalle.objects.filter(
            venta__fecha__date__gte=inicio_semana_anterior,
            venta__fecha__date__lte=fin_semana_anterior,
            venta__eliminada=False
        ).values('producto').annotate(
            total_anterior=Sum('cantidad')
        )
        
        # Crear diccionario de semana anterior
        dict_anterior = {item['producto']: item['total_anterior'] for item in ventas_semana_anterior}
        
        # Calcular tendencias
        trending = []
        for item in ventas_semana:
            producto_id = item['producto']
            total_actual = item['total_semana']
            total_anterior = dict_anterior.get(producto_id, 0)
            
            if total_anterior > 0:
                variacion = ((total_actual - total_anterior) / total_anterior) * 100
            else:
                variacion = 100 if total_actual > 0 else 0
            
            # Solo productos con tendencia positiva significativa
            if variacion >= 10:  # Mínimo 10% de crecimiento
                try:
                    producto = Producto.objects.get(id=producto_id)
                    trending.append({
                        'producto': producto,
                        'producto_id': producto_id,
                        'producto_nombre': producto.nombre,
                        'ventas_semana': total_actual,
                        'ventas_anterior': total_anterior,
                        'variacion': float(variacion),
                        'emoji': '🔥' if variacion >= 50 else '📊'
                    })
                except Producto.DoesNotExist:
                    continue
        
        # Ordenar por variación y limitar
        trending.sort(key=lambda x: x['variacion'], reverse=True)
        return trending[:limit]
    
    def get_hero_products(self, limit=3):
        """
        Productos "héroe" del mes
        Los que más margen de ganancia generan
        
        Returns:
            list de productos más rentables
        """
        # Ventas del mes con margen calculado
        ventas_mes = VentaDetalle.objects.filter(
            venta__fecha__date__gte=self.inicio_mes,
            venta__eliminada=False
        ).values(
            'producto__id',
            'producto__nombre',
            'producto__precio',
            'producto__costo_base',
            'producto__stock'
        ).annotate(
            cantidad_vendida=Sum('cantidad'),
            ingresos=Sum(F('cantidad') * F('precio_unitario'))
        )
        
        # Calcular margen de ganancia total
        hero_products = []
        for item in ventas_mes:
            precio = Decimal(str(item['producto__precio']))
            costo = Decimal(str(item['producto__costo_base'] or 0))
            cantidad = item['cantidad_vendida']
            
            if precio > 0 and costo > 0:
                margen_unitario = precio - costo
                ganancia_total = margen_unitario * cantidad
                margen_porcentaje = ((precio - costo) / precio) * 100
                
                hero_products.append({
                    'producto_id': item['producto__id'],
                    'producto_nombre': item['producto__nombre'],
                    'cantidad_vendida': cantidad,
                    'ingresos': float(item['ingresos']),
                    'ganancia_total': float(ganancia_total),
                    'margen_porcentaje': float(margen_porcentaje),
                    'stock_actual': item['producto__stock'],
                    'ranking': 0  # Se asignará después
                })
        
        # Ordenar por ganancia total
        hero_products.sort(key=lambda x: x['ganancia_total'], reverse=True)
        
        # Asignar ranking y emojis
        for i, producto in enumerate(hero_products[:limit], 1):
            producto['ranking'] = i
            if i == 1:
                producto['emoji'] = '🥇'
                producto['badge'] = 'Top 1'
            elif i == 2:
                producto['emoji'] = '🥈'
                producto['badge'] = 'Top 2'
            elif i == 3:
                producto['emoji'] = '🥉'
                producto['badge'] = 'Top 3'
        
        return hero_products[:limit]
    
    def get_cross_selling_recommendations(self, producto_id=None, limit=5):
        """
        Cross-Selling Inteligente
        Productos que suelen comprarse juntos
        
        Args:
            producto_id: ID del producto base (opcional)
            limit: Número de recomendaciones
        
        Returns:
            list de productos relacionados con % de coincidencia
        """
        if producto_id:
            # Buscar ventas que incluyan este producto
            ventas_con_producto = Venta.objects.filter(
                detalles__producto_id=producto_id,
                eliminada=False
            ).values_list('id', flat=True)
            
            # Otros productos vendidos en las mismas ventas
            productos_relacionados = VentaDetalle.objects.filter(
                venta_id__in=ventas_con_producto
            ).exclude(
                producto_id=producto_id
            ).values(
                'producto__id',
                'producto__nombre'
            ).annotate(
                coincidencias=Count('venta', distinct=True)
            )
            
            total_ventas_base = len(ventas_con_producto)
            
            relaciones = []
            for item in productos_relacionados:
                if total_ventas_base > 0:
                    porcentaje_coincidencia = (item['coincidencias'] / total_ventas_base) * 100
                    
                    if porcentaje_coincidencia >= 30:  # Mínimo 30% coincidencia
                        relaciones.append({
                            'producto_id': item['producto__id'],
                            'producto_nombre': item['producto__nombre'],
                            'coincidencias': item['coincidencias'],
                            'porcentaje': float(porcentaje_coincidencia),
                            'emoji': '⭐' if porcentaje_coincidencia >= 70 else '📦'
                        })
            
            relaciones.sort(key=lambda x: x['porcentaje'], reverse=True)
            return relaciones[:limit]
        
        else:
            # Cross-selling general (pares más comunes)
            return self._get_pares_frecuentes(limit)
    
    def _get_pares_frecuentes(self, limit=5):
        """
        Encuentra los pares de productos que más se venden juntos
        """
        # Obtener todas las ventas con múltiples items
        ventas = Venta.objects.filter(eliminada=False).prefetch_related('detalles')
        
        pares_contador = Counter()
        
        for venta in ventas:
            productos_en_venta = list(venta.detalles.values_list('producto__id', 'producto__nombre'))
            
            # Generar todos los pares posibles
            if len(productos_en_venta) >= 2:
                for i, (id1, nombre1) in enumerate(productos_en_venta):
                    for id2, nombre2 in productos_en_venta[i+1:]:
                        # Ordenar para evitar duplicados (A,B) y (B,A)
                        par = tuple(sorted([(id1, nombre1), (id2, nombre2)], key=lambda x: x[0]))
                        pares_contador[par] += 1
        
        # Convertir a lista ordenada
        pares_frecuentes = []
        for par, frecuencia in pares_contador.most_common(limit):
            (id1, nombre1), (id2, nombre2) = par
            pares_frecuentes.append({
                'producto1_id': id1,
                'producto1_nombre': nombre1,
                'producto2_id': id2,
                'producto2_nombre': nombre2,
                'frecuencia': frecuencia,
                'recomendacion': f'Combo: {nombre1} + {nombre2}'
            })
        
        return pares_frecuentes
    
    def get_productos_baja_rotacion(self, dias_sin_venta=60, limit=10):
        """
        Productos con baja rotación (para promoción)
        
        Args:
            dias_sin_venta: Días sin ventas para considerar baja rotación
            limit: Número de productos a retornar
        
        Returns:
            list de productos con baja rotación
        """
        fecha_limite = timezone.now() - timedelta(days=dias_sin_venta)
        
        # Productos con stock
        productos_con_stock = Producto.objects.filter(stock__gt=0)
        
        baja_rotacion = []
        for producto in productos_con_stock:
            # Última venta del producto
            ultima_venta = VentaDetalle.objects.filter(
                producto=producto,
                venta__eliminada=False
            ).order_by('-venta__fecha').first()
            
            if not ultima_venta or ultima_venta.venta.fecha < fecha_limite:
                dias_sin_venta_real = (timezone.now().date() - ultima_venta.venta.fecha.date()).days if ultima_venta else 999
                costo_real = producto.calcular_costo_real()
                capital_inmovilizado = costo_real * producto.stock
                
                baja_rotacion.append({
                    'producto_id': producto.id,
                    'producto_nombre': producto.nombre,
                    'stock': producto.stock,
                    'dias_sin_venta': dias_sin_venta_real,
                    'capital_inmovilizado': float(capital_inmovilizado),
                    'descuento_sugerido': 25 if dias_sin_venta_real > 90 else 15,
                    'emoji': '💤' if dias_sin_venta_real > 90 else '📦'
                })
        
        # Ordenar por capital inmovilizado (mayor impacto primero)
        baja_rotacion.sort(key=lambda x: x['capital_inmovilizado'], reverse=True)
        return baja_rotacion[:limit]
