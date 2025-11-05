"""
Servicio de Inventario - Métricas Predictivas y Análisis de Stock
Proporciona indicadores avanzados de gestión de inventario
"""

from decimal import Decimal
from django.db.models import Sum, Avg, Count, F, Q
from django.utils import timezone
from datetime import timedelta
import statistics

from gestion.models import (
    Producto, VentaDetalle, Compra, ConfiguracionCostos
)


class InventarioService:
    """
    Servicio centralizado para análisis de inventario.
    Métricas predictivas: rotación, cobertura, valor, etc.
    """
    
    def __init__(self):
        self.hoy = timezone.now().date()
        self.inicio_mes = self.hoy.replace(day=1)
        self._config = None
    
    @property
    def config(self):
        """Lazy loading de configuración"""
        if self._config is None:
            self._config = ConfiguracionCostos.objects.first()
            if self._config is None:
                self._config = ConfiguracionCostos.objects.create()
        return self._config
    
    def get_kpis_inventario(self):
        """
        Obtiene los 4 KPIs principales de inventario.
        Optimizado con queries eficientes.
        
        Returns:
            dict con: cobertura_dias, stock_critico, ultima_compra, valor_total
        """
        return {
            'cobertura_dias': self._calcular_cobertura_dias(),
            'stock_critico': self._contar_stock_critico(),
            'ultima_compra': self._dias_desde_ultima_compra(),
            'valor_total': self._calcular_valor_inventario(),
            'rotacion': self._calcular_rotacion_inventario()
        }
    
    def _calcular_cobertura_dias(self):
        """
        Calcula la cobertura promedio del inventario en días.
        
        Cobertura = Stock_Actual / Ventas_Diarias_Promedio
        
        Indica cuántos días durará el stock actual al ritmo de ventas actual.
        Usa la mediana para ser robusto ante outliers.
        
        Returns:
            dict con días promedio, estado y detalle
        """
        productos = Producto.objects.filter(stock__gt=0).select_related()
        
        if not productos.exists():
            return {
                'dias': 0,
                'estado': 'sin_stock',
                'mensaje': 'No hay productos en stock'
            }
        
        coberturas = []
        productos_criticos = 0
        
        for producto in productos:
            # Calcular ventas diarias promedio del último mes
            ventas_diarias = self._calcular_ventas_diarias_promedio(producto)
            
            if ventas_diarias > 0:
                cobertura = producto.stock / ventas_diarias
                coberturas.append(cobertura)
                
                # Contar productos con poca cobertura (< objetivo)
                if cobertura < self.config.cobertura_objetivo_dias:
                    productos_criticos += 1
        
        if not coberturas:
            # Hay stock pero no hay ventas históricas
            return {
                'dias': 999,  # Infinito prácticamente
                'estado': 'sin_ventas',
                'mensaje': 'Stock disponible sin historial de ventas'
            }
        
        # Usar mediana (más robusta que promedio)
        cobertura_promedio = statistics.median(coberturas)
        objetivo = self.config.cobertura_objetivo_dias
        
        # Determinar estado
        if cobertura_promedio < objetivo * 0.5:
            estado = 'critico'
            mensaje = 'Stock muy bajo'
        elif cobertura_promedio < objetivo:
            estado = 'bajo'
            mensaje = 'Stock por debajo del objetivo'
        elif cobertura_promedio > objetivo * 2:
            estado = 'exceso'
            mensaje = 'Posible exceso de stock'
        else:
            estado = 'saludable'
            mensaje = 'Cobertura óptima'
        
        return {
            'dias': round(cobertura_promedio, 1),
            'objetivo': objetivo,
            'estado': estado,
            'mensaje': mensaje,
            'productos_criticos': productos_criticos,
            'sparkline': self._get_sparkline_cobertura()
        }
    
    def _calcular_ventas_diarias_promedio(self, producto, dias=30):
        """
        Calcula el promedio de ventas diarias de un producto.
        
        Args:
            producto: Instancia de Producto
            dias: Días hacia atrás para el cálculo (default 30)
        
        Returns:
            float con unidades vendidas por día
        """
        desde = self.hoy - timedelta(days=dias)
        
        total_vendido = VentaDetalle.objects.filter(
            producto=producto,
            venta__fecha__date__gte=desde,
            venta__fecha__date__lte=self.hoy,
            venta__eliminada=False
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        
        # Dividir por días reales del período
        return float(total_vendido) / dias if dias > 0 else 0
    
    def _contar_stock_critico(self):
        """
        Cuenta productos con stock crítico (≤ stock_minimo).
        
        Returns:
            dict con cantidad, lista de productos y estado
        """
        criticos = Producto.objects.filter(
            stock__lte=F('stock_minimo'),
            stock__gt=0  # Excluir agotados
        ).select_related()
        
        cantidad = criticos.count()
        
        # Calcular impacto (son top sellers?)
        criticos_importantes = criticos.annotate(
            ventas_mes=Sum(
                'ventadetalle__cantidad',
                filter=Q(
                    ventadetalle__venta__fecha__date__gte=self.inicio_mes,
                    ventadetalle__venta__eliminada=False
                )
            )
        ).filter(ventas_mes__gt=0).count()
        
        return {
            'cantidad': cantidad,
            'importantes': criticos_importantes,
            'productos': list(criticos[:5]),  # Top 5 para mostrar
            'estado': 'critico' if criticos_importantes > 0 else 'normal'
        }
    
    def _dias_desde_ultima_compra(self):
        """
        Calcula días transcurridos desde la última compra.
        Incluye frecuencia de compra y próxima compra estimada.
        
        Returns:
            dict con días, frecuencia y predicción
        """
        ultima_compra = Compra.objects.order_by('-fecha_compra').first()
        
        if not ultima_compra:
            return {
                'dias': None,
                'fecha': None,
                'frecuencia': None,
                'proxima_estimada': None,
                'estado': 'sin_datos'
            }
        
        dias = (self.hoy - ultima_compra.fecha_compra).days
        
        # Calcular frecuencia de compras (últimos 3 meses)
        hace_3_meses = self.hoy - timedelta(days=90)
        total_compras = Compra.objects.filter(
            fecha_compra__gte=hace_3_meses
        ).count()
        
        frecuencia_dias = 90 / total_compras if total_compras > 0 else None
        
        # Estimar próxima compra
        proxima_estimada = None
        if frecuencia_dias:
            proxima_estimada = dias - frecuencia_dias
            proxima_estimada = round(proxima_estimada)
        
        # Determinar estado
        if frecuencia_dias:
            if dias > frecuencia_dias * 1.5:
                estado = 'retrasada'
            elif dias > frecuencia_dias:
                estado = 'proxima'
            else:
                estado = 'normal'
        else:
            estado = 'normal'
        
        return {
            'dias': dias,
            'fecha': ultima_compra.fecha_compra,
            'frecuencia': round(frecuencia_dias, 1) if frecuencia_dias else None,
            'proxima_estimada': proxima_estimada,
            'estado': estado
        }
    
    def _calcular_valor_inventario(self):
        """
        Calcula el valor total del inventario usando costos reales.
        
        Returns:
            dict con valor total, cantidad de productos y desglose
        """
        productos = Producto.objects.filter(stock__gt=0).select_related()
        
        valor_total = Decimal('0')
        cantidad_productos = 0
        valor_por_categoria = {}  # Para futuro
        
        for producto in productos:
            try:
                costo = producto.calcular_costo_unitario()
                valor_producto = costo * producto.stock
                valor_total += valor_producto
                cantidad_productos += 1
            except Exception:
                continue
        
        return {
            'total': float(valor_total.quantize(Decimal('0.01'))),
            'cantidad_productos': cantidad_productos,
            'promedio_por_producto': float(
                (valor_total / cantidad_productos).quantize(Decimal('0.01'))
            ) if cantidad_productos > 0 else 0
        }
    
    def _calcular_rotacion_inventario(self):
        """
        Calcula la rotación de inventario del mes.
        
        Rotación = Costo_Productos_Vendidos / Valor_Inventario_Promedio
        
        Indica cuántas veces se vendió el inventario en el período.
        Valores típicos: 3-5x por mes es saludable para dietética.
        
        Returns:
            dict con rotación, objetivo y estado
        """
        # Valor de inventario actual
        inventario_actual = self._calcular_valor_inventario()['total']
        
        # Costo de productos vendidos este mes
        productos_vendidos = VentaDetalle.objects.filter(
            venta__fecha__date__gte=self.inicio_mes,
            venta__eliminada=False
        ).select_related('producto')
        
        costo_vendido = Decimal('0')
        for detalle in productos_vendidos:
            try:
                costo = detalle.producto.calcular_costo_unitario()
                costo_vendido += costo * detalle.cantidad
            except Exception:
                continue
        
        # Calcular rotación (simplificado: inventario actual como promedio)
        # TODO: Mejorar usando inventario inicial + final / 2
        rotacion = (
            float((costo_vendido / Decimal(str(inventario_actual))).quantize(Decimal('0.01')))
            if inventario_actual > 0 else 0
        )
        
        objetivo = float(self.config.rotacion_objetivo)
        
        # Determinar estado
        if rotacion < objetivo * 0.5:
            estado = 'muy_bajo'
            mensaje = 'Rotación muy baja - stock muerto'
        elif rotacion < objetivo:
            estado = 'bajo'
            mensaje = 'Rotación por debajo del objetivo'
        elif rotacion > objetivo * 1.5:
            estado = 'alto'
            mensaje = 'Rotación muy alta - revisar stock'
        else:
            estado = 'optimo'
            mensaje = 'Rotación saludable'
        
        return {
            'valor': rotacion,
            'objetivo': objetivo,
            'estado': estado,
            'mensaje': mensaje,
            'costo_vendido_mes': float(costo_vendido.quantize(Decimal('0.01')))
        }
    
    def _get_sparkline_cobertura(self):
        """
        Genera datos de sparkline para cobertura de últimos 7 días.
        Útil para mostrar tendencia en la KPI card.
        
        Returns:
            list de valores de cobertura
        """
        # Implementación simplificada - puede mejorarse
        # Por ahora retorna valores simulados basados en promedio
        cobertura_actual = self._calcular_cobertura_dias()['dias']
        
        sparkline = []
        for i in range(7):
            # Pequeña variación ±10%
            variacion = (i - 3) * 0.03
            valor = cobertura_actual * (1 + variacion)
            sparkline.append(round(valor, 1))
        
        return sparkline
    
    def get_productos_rotacion_lenta(self, limit=10):
        """
        Identifica productos con rotación lenta (poco vendidos).
        Útil para identificar stock muerto.
        
        Args:
            limit: Número máximo de productos a retornar
        
        Returns:
            list de productos con baja rotación
        """
        hace_60_dias = self.hoy - timedelta(days=60)
        
        # Productos con stock pero sin ventas en 60 días
        productos = Producto.objects.filter(
            stock__gt=0
        ).annotate(
            ventas_60d=Sum(
                'ventadetalle__cantidad',
                filter=Q(
                    ventadetalle__venta__fecha__date__gte=hace_60_dias,
                    ventadetalle__venta__eliminada=False
                )
            )
        ).filter(
            Q(ventas_60d__isnull=True) | Q(ventas_60d=0)
        ).select_related()
        
        resultado = []
        for producto in productos[:limit]:
            costo = producto.calcular_costo_unitario()
            valor_inmovilizado = costo * producto.stock
            
            resultado.append({
                'producto': producto,
                'stock': producto.stock,
                'dias_sin_venta': 60,  # Simplificado
                'valor_inmovilizado': float(valor_inmovilizado.quantize(Decimal('0.01')))
            })
        
        return resultado
