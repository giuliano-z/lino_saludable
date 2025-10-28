# -*- coding: utf-8 -*-
"""
Sistema de Analytics y Control de Rentabilidad para LINO Saludable
Análisis avanzado de costos vs precios, márgenes y rentabilidad
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from django.db.models import Sum, F, Q, Avg, Max, Min, Count
from django.utils import timezone
from .models import Producto, VentaDetalle, Venta, MateriaPrima, Compra
import json


class AnalyticsRentabilidad:
    """
    Clase para análisis avanzado de rentabilidad del negocio
    """
    
    def __init__(self):
        self.hoy = timezone.now().date()
        self.mes_actual = self.hoy.replace(day=1)
        self.mes_anterior = (self.mes_actual - timedelta(days=1)).replace(day=1)
    
    def get_productos_rentabilidad(self):
        """
        Analiza la rentabilidad de cada producto
        """
        productos = Producto.objects.all()
        datos_rentabilidad = []
        
        for producto in productos:
            # Verificar que el producto tenga ID válido
            if not producto.id:
                continue
                
            try:
                # Calcular costo actual
                costo_actual = producto.calcular_costo_unitario()
                precio_actual = Decimal(str(producto.precio))
                
                # Ventas del último mes
                ventas_mes = VentaDetalle.objects.filter(
                    producto=producto,
                    venta__fecha__date__gte=self.mes_actual
                ).aggregate(
                    cantidad_vendida=Sum('cantidad'),
                    ingresos=Sum('subtotal'),
                    precio_promedio=Avg('precio_unitario')
                )
                
                # Asegurar valores por defecto para evitar None
                ventas_mes['cantidad_vendida'] = ventas_mes['cantidad_vendida'] or 0
                ventas_mes['ingresos'] = ventas_mes['ingresos'] or Decimal('0')
                ventas_mes['precio_promedio'] = ventas_mes['precio_promedio'] or Decimal('0')
                
                # Calcular márgenes
                if precio_actual > 0:
                    margen_actual = ((precio_actual - costo_actual) / precio_actual * 100)
                else:
                    margen_actual = Decimal('0')
                
                # Determinar estado de rentabilidad
                if margen_actual < 10:
                    estado = 'critico'
                    alerta = 'Margen muy bajo'
                elif margen_actual < 20:
                    estado = 'bajo'
                    alerta = 'Margen bajo'
                elif margen_actual < 30:
                    estado = 'aceptable'
                    alerta = None
                else:
                    estado = 'optimo'
                    alerta = None
                
                # ¿Hay pérdida?
                en_perdida = costo_actual > precio_actual
                
                datos_rentabilidad.append({
                    'producto': producto,
                    'costo_actual': float(costo_actual),
                    'precio_actual': float(precio_actual),
                    'margen_porcentaje': float(margen_actual.quantize(Decimal('0.01'))),
                    'margen_absoluto': float((precio_actual - costo_actual).quantize(Decimal('0.01'))),
                    'cantidad_vendida': ventas_mes['cantidad_vendida'],
                    'ingresos_mes': float(ventas_mes['ingresos']),
                    'precio_promedio_venta': float(ventas_mes['precio_promedio']),
                    'estado': estado,
                    'alerta': alerta,
                    'en_perdida': en_perdida,
                    'impacto_rentabilidad': float((ventas_mes['ingresos'] - (costo_actual * ventas_mes['cantidad_vendida'])) if ventas_mes['cantidad_vendida'] else Decimal('0'))
                })
                
            except Exception as e:
                # Si hay error con un producto específico, continuar con el siguiente
                print(f"Error procesando producto {producto.nombre}: {e}")
                continue
        
        # Ordenar por margen porcentual
        return sorted(datos_rentabilidad, key=lambda x: x['margen_porcentaje'])
    
    def get_alertas_rentabilidad(self):
        """
        Genera alertas críticas de rentabilidad
        """
        productos_data = self.get_productos_rentabilidad()
        alertas = []
        
        # Productos en pérdida
        productos_perdida = [p for p in productos_data if p['en_perdida']]
        if productos_perdida:
            alertas.append({
                'tipo': 'perdida',
                'severidad': 'critica',
                'titulo': f'{len(productos_perdida)} productos en PÉRDIDA',
                'descripcion': 'Productos vendidos por debajo del costo',
                'productos': productos_perdida[:5],  # Top 5
                'accion': 'Ajustar precios urgentemente'
            })
        
        # Productos con margen muy bajo
        productos_margen_bajo = [p for p in productos_data if p['estado'] == 'critico' and not p['en_perdida']]
        if productos_margen_bajo:
            alertas.append({
                'tipo': 'margen_bajo',
                'severidad': 'alta',
                'titulo': f'{len(productos_margen_bajo)} productos con margen crítico',
                'descripcion': 'Margen menor al 10%',
                'productos': productos_margen_bajo[:5],
                'accion': 'Revisar estrategia de precios'
            })
        
        # Productos sin ventas pero con stock
        productos_sin_ventas = Producto.objects.filter(
            stock__gt=0
        ).exclude(
            id__in=VentaDetalle.objects.filter(
                venta__fecha__date__gte=self.mes_actual
            ).values_list('producto_id', flat=True)
        )
        
        if productos_sin_ventas.exists():
            alertas.append({
                'tipo': 'sin_rotacion',
                'severidad': 'media',
                'titulo': f'{productos_sin_ventas.count()} productos sin rotación',
                'descripcion': 'Productos con stock pero sin ventas este mes',
                'productos': list(productos_sin_ventas[:5]),
                'accion': 'Revisar demanda y promociones'
            })
        
        return alertas
    
    def get_evolucion_costos(self, producto_id=None, dias=30):
        """
        Analiza la evolución de costos vs precios en el tiempo
        """
        # Por simplicidad, comparamos mes actual vs anterior
        # En el futuro se podría implementar un histórico más detallado
        
        if producto_id:
            productos = Producto.objects.filter(id=producto_id)
        else:
            productos = Producto.objects.all()
        
        evolucion = []
        
        for producto in productos:
            # Costo actual
            costo_actual = producto.calcular_costo_unitario()
            precio_actual = Decimal(str(producto.precio))
            
            # Ventas mes actual
            ventas_actual = VentaDetalle.objects.filter(
                producto=producto,
                venta__fecha__date__gte=self.mes_actual
            ).aggregate(
                precio_promedio=Avg('precio_unitario'),
                cantidad=Sum('cantidad')
            )
            
            # Asegurar valores por defecto
            ventas_actual['precio_promedio'] = ventas_actual['precio_promedio'] or Decimal('0')
            ventas_actual['cantidad'] = ventas_actual['cantidad'] or 0
            
            # Ventas mes anterior
            ventas_anterior = VentaDetalle.objects.filter(
                producto=producto,
                venta__fecha__date__gte=self.mes_anterior,
                venta__fecha__date__lt=self.mes_actual
            ).aggregate(
                precio_promedio=Avg('precio_unitario'),
                cantidad=Sum('cantidad')
            )
            
            # Asegurar valores por defecto
            ventas_anterior['precio_promedio'] = ventas_anterior['precio_promedio'] or Decimal('0')
            ventas_anterior['cantidad'] = ventas_anterior['cantidad'] or 0
            
            # Calcular variaciones
            if ventas_anterior['precio_promedio'] > 0:
                variacion_precio = ((ventas_actual['precio_promedio'] - ventas_anterior['precio_promedio']) / ventas_anterior['precio_promedio'] * 100)
            else:
                variacion_precio = Decimal('0')
            
            evolucion.append({
                'producto': producto,
                'costo_actual': float(costo_actual),
                'precio_actual': float(precio_actual),
                'precio_promedio_mes_actual': float(ventas_actual['precio_promedio']),
                'precio_promedio_mes_anterior': float(ventas_anterior['precio_promedio']),
                'variacion_precio_porcentaje': float(variacion_precio.quantize(Decimal('0.01'))),
                'ventas_mes_actual': ventas_actual['cantidad'],
                'ventas_mes_anterior': ventas_anterior['cantidad']
            })
        
        return evolucion
    
    def get_kpis_rentabilidad(self):
        """
        Genera KPIs principales de rentabilidad
        """
        productos_data = self.get_productos_rentabilidad()
        
        # Cálculos agregados
        total_productos = len(productos_data)
        productos_rentables = len([p for p in productos_data if p['margen_porcentaje'] >= 20])
        productos_en_perdida = len([p for p in productos_data if p['en_perdida']])
        productos_criticos = len([p for p in productos_data if p['estado'] == 'critico'])
        
        # Margen promedio ponderado por ventas
        total_ingresos = sum(p['ingresos_mes'] for p in productos_data)
        if total_ingresos > 0:
            margen_promedio_ponderado = sum(
                (p['margen_porcentaje'] * p['ingresos_mes']) for p in productos_data
            ) / total_ingresos
        else:
            margen_promedio_ponderado = 0
        
        # Impacto total en rentabilidad
        impacto_total = sum(p['impacto_rentabilidad'] for p in productos_data)
        
        return {
            'total_productos': total_productos,
            'productos_rentables': productos_rentables,
            'productos_en_perdida': productos_en_perdida,
            'productos_criticos': productos_criticos,
            'porcentaje_rentables': round((productos_rentables / max(total_productos, 1)) * 100, 1),
            'porcentaje_perdida': round((productos_en_perdida / max(total_productos, 1)) * 100, 1),
            'margen_promedio_ponderado': round(margen_promedio_ponderado, 1),
            'impacto_rentabilidad_mes': round(impacto_total, 2),
            'productos_top_margen': sorted(productos_data, key=lambda x: x['margen_porcentaje'], reverse=True)[:5],
            'productos_top_ingresos': sorted(productos_data, key=lambda x: x['ingresos_mes'], reverse=True)[:5]
        }
    
    def get_recomendaciones_precios(self):
        """
        Genera recomendaciones automáticas de ajuste de precios
        """
        productos_data = self.get_productos_rentabilidad()
        recomendaciones = []
        
        for producto_data in productos_data:
            producto = producto_data['producto']
            
            # Recomendaciones basadas en margen
            if producto_data['en_perdida']:
                precio_sugerido = producto_data['costo_actual'] * 1.15  # 15% mínimo
                recomendaciones.append({
                    'producto': producto,
                    'tipo': 'urgente',
                    'problema': 'Producto en pérdida',
                    'precio_actual': producto_data['precio_actual'],
                    'precio_sugerido': round(precio_sugerido, 2),
                    'incremento_porcentaje': round(((precio_sugerido / producto_data['precio_actual']) - 1) * 100, 1),
                    'justificacion': 'Mínimo 15% de margen para cubrir gastos operativos'
                })
            
            elif producto_data['estado'] == 'critico':
                precio_sugerido = producto_data['costo_actual'] * 1.25  # 25% objetivo
                recomendaciones.append({
                    'producto': producto,
                    'tipo': 'recomendado',
                    'problema': 'Margen muy bajo',
                    'precio_actual': producto_data['precio_actual'],
                    'precio_sugerido': round(precio_sugerido, 2),
                    'incremento_porcentaje': round(((precio_sugerido / producto_data['precio_actual']) - 1) * 100, 1),
                    'justificacion': '25% de margen para rentabilidad saludable'
                })
        
        return sorted(recomendaciones, key=lambda x: x['tipo'] == 'urgente', reverse=True)


# Función auxiliar para vistas
def get_analytics_dashboard():
    """
    Función principal para obtener todos los datos del dashboard de analytics
    """
    analytics = AnalyticsRentabilidad()
    
    return {
        'kpis': analytics.get_kpis_rentabilidad(),
        'alertas': analytics.get_alertas_rentabilidad(),
        'productos_rentabilidad': analytics.get_productos_rentabilidad(),
        'evolucion_costos': analytics.get_evolucion_costos(),
        'recomendaciones': analytics.get_recomendaciones_precios()
    }
