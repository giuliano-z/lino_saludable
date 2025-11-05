"""
Servicio de Rentabilidad - Sistema de Análisis de Márgenes y Objetivos
Proporciona métricas avanzadas de rentabilidad y recomendaciones automáticas
"""

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum, Avg, F, Q
from django.utils import timezone
from datetime import timedelta

from gestion.models import (
    Producto, VentaDetalle, Venta, ConfiguracionCostos
)


class RentabilidadService:
    """
    Servicio centralizado para análisis de rentabilidad del negocio.
    Proporciona KPIs, análisis de objetivos y recomendaciones automáticas.
    """
    
    def __init__(self):
        self.hoy = timezone.now().date()
        self.inicio_mes = self.hoy.replace(day=1)
        self._config = None  # Lazy loading de configuración
    
    @property
    def config(self):
        """Lazy loading de configuración (singleton pattern)"""
        if self._config is None:
            self._config = ConfiguracionCostos.objects.first()
            # Si no existe configuración, crear una con valores por defecto
            if self._config is None:
                self._config = ConfiguracionCostos.objects.create(
                    margen_objetivo=Decimal('35.00'),
                    rotacion_objetivo=Decimal('4.00'),
                    cobertura_objetivo_dias=30
                )
        return self._config
    
    def get_kpis_rentabilidad(self):
        """
        Obtiene los 4 KPIs principales de rentabilidad.
        Optimizado para minimizar queries a la DB.
        
        Returns:
            dict con: objetivo_margen, rentables, en_perdida, margen_promedio
        """
        # Query única para obtener todos los productos con sus datos
        productos = Producto.objects.select_related().all()
        
        total_productos = 0
        productos_rentables = 0
        productos_en_perdida = 0
        suma_margenes_ponderados = Decimal('0')
        suma_ventas_ponderacion = Decimal('0')
        
        for producto in productos:
            total_productos += 1
            
            try:
                costo = producto.calcular_costo_unitario()
                precio = Decimal(str(producto.precio or 0))
                
                # Calcular margen
                if precio > 0:
                    margen = ((precio - costo) / precio) * 100
                else:
                    margen = Decimal('0')
                
                # Clasificar producto
                if costo > precio:
                    productos_en_perdida += 1
                elif margen >= 20:  # Umbral rentable: 20%+
                    productos_rentables += 1
                
                # Obtener ventas del mes para ponderar
                ventas_mes = VentaDetalle.objects.filter(
                    producto=producto,
                    venta__fecha__date__gte=self.inicio_mes,
                    venta__eliminada=False
                ).aggregate(total=Sum('subtotal'))['total'] or Decimal('0')
                
                # Ponderación por ventas
                suma_margenes_ponderados += margen * ventas_mes
                suma_ventas_ponderacion += ventas_mes
                
            except Exception:
                # Si hay error calculando un producto, continuar
                continue
        
        # Calcular porcentajes y margen promedio ponderado
        porcentaje_rentables = (
            Decimal(productos_rentables / total_productos * 100) 
            if total_productos > 0 else Decimal('0')
        )
        
        porcentaje_perdida = (
            Decimal(productos_en_perdida / total_productos * 100)
            if total_productos > 0 else Decimal('0')
        )
        
        margen_promedio = (
            (suma_margenes_ponderados / suma_ventas_ponderacion)
            if suma_ventas_ponderacion > 0 else Decimal('0')
        )
        
        # Obtener objetivo de configuración
        margen_objetivo = self.config.margen_objetivo
        
        return {
            'objetivo_margen': {
                'meta': float(margen_objetivo),
                'actual': float(margen_promedio.quantize(Decimal('0.01'))),
                'gap': float((margen_promedio - margen_objetivo).quantize(Decimal('0.01'))),
                'progreso': float((margen_promedio / margen_objetivo * 100).quantize(Decimal('0.1'))) if margen_objetivo > 0 else 0,
                'alcanzado': margen_promedio >= margen_objetivo
            },
            'rentables': {
                'porcentaje': float(porcentaje_rentables.quantize(Decimal('0.1'))),
                'cantidad': productos_rentables,
                'total': total_productos
            },
            'en_perdida': {
                'porcentaje': float(porcentaje_perdida.quantize(Decimal('0.1'))),
                'cantidad': productos_en_perdida,
                'total': total_productos
            },
            'margen_promedio': {
                'valor': float(margen_promedio.quantize(Decimal('0.01'))),
                'ponderado': True  # Indica que es ponderado por ventas
            }
        }
    
    def get_objetivo_margen_analisis(self):
        """
        Análisis detallado del objetivo de margen con recomendaciones.
        
        Returns:
            dict con análisis completo, productos a ajustar y recomendaciones
        """
        kpis = self.get_kpis_rentabilidad()
        objetivo = kpis['objetivo_margen']
        
        # Contar total de productos
        productos = Producto.objects.all()
        total_productos = productos.count()
        
        # Contar productos que cumplen objetivo
        productos_cumpliendo = 0
        for producto in productos:
            try:
                costo = producto.calcular_costo_unitario()
                precio = Decimal(str(producto.precio or 0))
                if precio > 0:
                    margen = ((precio - costo) / precio) * 100
                    if margen >= self.config.margen_objetivo:
                        productos_cumpliendo += 1
            except Exception:
                continue
        
        # Obtener productos con margen bajo (< 25%)
        productos_bajos = self._obtener_productos_margen_bajo(threshold=25)
        
        # Generar recomendaciones automáticas
        recomendaciones = self._generar_recomendaciones(productos_bajos)
        
        return {
            'total_productos': total_productos,
            'productos_cumpliendo': productos_cumpliendo,
            'meta': objetivo['meta'],
            'actual': objetivo['actual'],
            'gap': objetivo['gap'],
            'progreso': objetivo['progreso'],
            'alcanzado': objetivo['alcanzado'],
            'productos_a_ajustar': len(productos_bajos),
            'productos_criticos': productos_bajos[:5],  # Top 5 más urgentes
            'recomendaciones': recomendaciones[:3]  # Top 3 recomendaciones
        }
    
    def _obtener_productos_margen_bajo(self, threshold=25):
        """
        Obtiene productos con margen por debajo del threshold.
        Ordenados por impacto (ventas * gap de margen).
        
        Args:
            threshold: Margen mínimo aceptable (default 25%)
        
        Returns:
            list de dict con datos del producto y recomendaciones
        """
        productos = Producto.objects.all()
        productos_bajos = []
        
        for producto in productos:
            try:
                costo = producto.calcular_costo_unitario()
                precio = Decimal(str(producto.precio or 0))
                
                if precio == 0:
                    continue
                
                margen = ((precio - costo) / precio) * 100
                
                # Solo productos con margen bajo
                if margen < threshold:
                    # Ventas del mes para calcular impacto
                    ventas_mes = VentaDetalle.objects.filter(
                        producto=producto,
                        venta__fecha__date__gte=self.inicio_mes,
                        venta__eliminada=False
                    ).aggregate(
                        cantidad=Sum('cantidad'),
                        total=Sum('subtotal')
                    )
                    
                    cantidad_vendida = ventas_mes['cantidad'] or 0
                    total_vendido = ventas_mes['total'] or Decimal('0')
                    
                    # Calcular precio sugerido para margen objetivo
                    precio_sugerido = self._calcular_precio_sugerido(
                        costo, 
                        self.config.margen_objetivo
                    )
                    
                    # Impacto = cuánto más ganaríamos con el nuevo precio
                    impacto = (precio_sugerido - precio) * cantidad_vendida
                    
                    productos_bajos.append({
                        'producto': producto,
                        'nombre': producto.nombre,
                        'margen_actual': float(margen.quantize(Decimal('0.01'))),
                        'precio_actual': float(precio),
                        'costo': float(costo),
                        'precio_sugerido': float(precio_sugerido),
                        'cantidad_vendida_mes': cantidad_vendida,
                        'impacto_estimado': float(impacto.quantize(Decimal('0.01'))),
                        'es_top_seller': cantidad_vendida >= 10  # Threshold configurable
                    })
            
            except Exception:
                continue
        
        # Ordenar por impacto (productos más vendidos primero)
        return sorted(
            productos_bajos, 
            key=lambda x: x['impacto_estimado'], 
            reverse=True
        )
    
    def _calcular_precio_sugerido(self, costo, margen_objetivo):
        """
        Calcula el precio de venta necesario para alcanzar margen objetivo.
        
        Fórmula: Precio = Costo / (1 - Margen/100)
        
        Args:
            costo: Costo unitario del producto
            margen_objetivo: Margen deseado en porcentaje
        
        Returns:
            Decimal con precio sugerido
        """
        if margen_objetivo >= 100:
            # Margen 100% no es alcanzable
            return costo * 2
        
        margen_decimal = margen_objetivo / 100
        precio = costo / (1 - margen_decimal)
        
        # Redondear a decenas (ej: 2485 -> 2490)
        if self.config.redondear_precios:
            precio = (precio / 10).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * 10
        
        return precio.quantize(Decimal('0.01'))
    
    def _generar_recomendaciones(self, productos_bajos):
        """
        Genera recomendaciones automáticas basadas en análisis de productos.
        
        Args:
            productos_bajos: Lista de productos con margen bajo
        
        Returns:
            list de dict con recomendaciones accionables
        """
        recomendaciones = []
        
        # Recomendación 1: Ajustar precios de top sellers
        top_sellers_bajos = [
            p for p in productos_bajos 
            if p['es_top_seller'] and p['margen_actual'] < 30
        ]
        
        if top_sellers_bajos:
            impacto_total = sum(p['impacto_estimado'] for p in top_sellers_bajos)
            recomendaciones.append({
                'tipo': 'ajuste_precio_top_sellers',
                'titulo': 'Ajustar precios de productos más vendidos',
                'descripcion': f"Hay {len(top_sellers_bajos)} productos top con margen bajo. Ajustar sus precios tendría alto impacto.",
                'impacto_estimado': float(impacto_total),
                'productos_afectados': len(top_sellers_bajos),
                'accion': 'Revisar precios de productos más vendidos',
                'prioridad': 'alta'
            })
        
        # Recomendación 2: Productos en pérdida
        en_perdida = [p for p in productos_bajos if p['margen_actual'] < 0]
        
        if en_perdida:
            recomendaciones.append({
                'tipo': 'productos_en_perdida',
                'titulo': 'Corregir productos en pérdida URGENTE',
                'descripcion': f"{len(en_perdida)} productos tienen precio menor al costo. Esto genera pérdidas directas.",
                'impacto_estimado': sum(p['impacto_estimado'] for p in en_perdida),
                'productos_afectados': len(en_perdida),
                'accion': 'Ajustar precios inmediatamente',
                'prioridad': 'critica'
            })
        
        # Recomendación 3: Renegociar con proveedores
        productos_alto_costo = [
            p for p in productos_bajos
            if p['costo'] > Decimal(str(p['precio_actual'])) * Decimal('0.6')  # Costo > 60% del precio
        ]
        
        if productos_alto_costo:
            recomendaciones.append({
                'tipo': 'renegociar_costos',
                'titulo': 'Buscar mejores precios de proveedores',
                'descripcion': f"{len(productos_alto_costo)} productos tienen costos muy altos. Considera renegociar o cambiar de proveedor.",
                'impacto_estimado': 0,  # Difícil estimar sin datos de proveedores
                'productos_afectados': len(productos_alto_costo),
                'accion': 'Contactar proveedores',
                'prioridad': 'media'
            })
        
        # Ordenar por prioridad
        orden_prioridad = {'critica': 0, 'alta': 1, 'media': 2, 'baja': 3}
        return sorted(
            recomendaciones,
            key=lambda x: orden_prioridad.get(x['prioridad'], 99)
        )
    
    def get_productos_criticos(self, limit=10):
        """
        Obtiene los productos más críticos que requieren atención.
        Combina margen bajo + alto volumen de ventas.
        
        Args:
            limit: Número máximo de productos a retornar
        
        Returns:
            list de productos ordenados por criticidad
        """
        productos_bajos = self._obtener_productos_margen_bajo(threshold=30)
        return productos_bajos[:limit]
    
    def get_productos_rentabilidad(self):
        """
        Obtiene todos los productos con su información de rentabilidad.
        Usado para tablas completas y análisis detallados.
        
        Returns:
            list: Lista de productos con: nombre, costo, precio_actual, margen,
                  en_perdida, cumple_objetivo, ventas_mes
        """
        from decimal import Decimal
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import timedelta
        
        objetivo_margen = float(self.config.margen_objetivo)
        productos = Producto.objects.all()
        
        # Calcular ventas del mes actual para cada producto
        fecha_inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        lista_productos = []
        for producto in productos:
            costo = producto.calcular_costo_unitario()
            precio_actual = Decimal(str(producto.precio or 0))
            
            if precio_actual > 0:
                margen = float(((precio_actual - costo) / precio_actual * 100))
            else:
                margen = 0.0
            
            # Calcular ventas del mes
            ventas_mes = VentaDetalle.objects.filter(
                producto=producto,
                venta__fecha__gte=fecha_inicio_mes
            ).aggregate(
                total=Sum('cantidad')
            )['total'] or 0
            
            lista_productos.append({
                'nombre': producto.nombre,
                'costo': float(costo),
                'precio_actual': float(precio_actual),
                'margen': margen,
                'en_perdida': margen < 0,
                'cumple_objetivo': margen >= objetivo_margen,
                'ventas_mes': int(ventas_mes)
            })
        
        return lista_productos
