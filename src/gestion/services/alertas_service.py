"""
Alertas Service - Generación inteligente de alertas automáticas
"""

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Sum
from gestion.models import Producto, Venta, VentaDetalle


class AlertasService:
    """Servicio para generar y gestionar alertas automáticas"""
    
    @staticmethod
    def generar_alertas_stock(usuario):
        """
        Genera alertas de stock crítico y agotado
        Returns: número de alertas generadas
        """
        from gestion.models import Alerta
        
        alertas_creadas = 0
        
        # Stock agotado
        productos_agotados = Producto.objects.filter(stock=0)
        for producto in productos_agotados:
            # Evitar duplicados
            existe = Alerta.objects.filter(
                tipo='stock_agotado',
                producto=producto,
                usuario=usuario,
                leida=False
            ).exists()
            
            if not existe:
                # Calcular pérdida potencial (promedio de ventas * precio)
                ventas_promedio_dia = producto.ventas_promedio_diarias if hasattr(producto, 'ventas_promedio_diarias') else 1
                perdida_estimada = ventas_promedio_dia * producto.precio_venta * 30  # 30 días
                
                Alerta.objects.create(
                    tipo='stock_agotado',
                    nivel='danger',
                    usuario=usuario,
                    producto=producto,
                    titulo=f'❌ Stock agotado: {producto.nombre}',
                    mensaje=f'El producto está agotado. Pérdida estimada: ${perdida_estimada:.2f}/mes sin stock.',
                    accion_sugerida=f'Reabastecer urgentemente. Pedido sugerido: {int(ventas_promedio_dia * 30)} unidades',
                    valor_impacto=perdida_estimada
                )
                alertas_creadas += 1
        
        # Stock crítico (bajo mínimo pero no agotado)
        productos_criticos = Producto.objects.filter(
            stock__lte=F('stock_minimo'),
            stock__gt=0
        )
        
        for producto in productos_criticos:
            existe = Alerta.objects.filter(
                tipo='stock_critico',
                producto=producto,
                usuario=usuario,
                leida=False
            ).exists()
            
            if not existe:
                dias_restantes = producto.stock / max(producto.ventas_promedio_diarias if hasattr(producto, 'ventas_promedio_diarias') else 1, 1)
                
                Alerta.objects.create(
                    tipo='stock_critico',
                    nivel='warning',
                    usuario=usuario,
                    producto=producto,
                    titulo=f'⚠️ Stock bajo: {producto.nombre}',
                    mensaje=f'Stock actual: {producto.stock} unidades. Stock para {dias_restantes:.1f} días aproximadamente.',
                    accion_sugerida=f'Reabastecer con {producto.stock_minimo * 2} unidades',
                    valor_impacto=producto.precio_venta * 30  # Pérdida potencial si se agota
                )
                alertas_creadas += 1
        
        return alertas_creadas
    
    @staticmethod
    def generar_alertas_vencimiento(usuario):
        """
        Genera alertas de productos próximos a vencer
        Returns: número de alertas generadas
        
        NOTA: Deshabilitado - Producto no tiene campo fecha_vencimiento
        TODO: Habilitar cuando se implemente control de vencimientos
        """
        # from gestion.models import Alerta
        
        alertas_creadas = 0
        # fecha_limite = timezone.now() + timedelta(days=30)
        
        # TODO: Descomentar cuando Producto tenga fecha_vencimiento
        # productos_por_vencer = Producto.objects.filter(
        #     fecha_vencimiento__lte=fecha_limite,
        #     fecha_vencimiento__gte=timezone.now(),
        #     stock__gt=0
        # )
        
        # for producto in productos_por_vencer:
        #     existe = Alerta.objects.filter(
        #         tipo='vencimiento',
        #         producto=producto,
        #         usuario=usuario,
        #         leida=False
        #     ).exists()
            
        #     if not existe:
        #         dias_restantes = (producto.fecha_vencimiento - timezone.now().date()).days
        #         nivel = 'danger' if dias_restantes <= 7 else 'warning'
                
        #         # Calcular pérdida potencial si vence
        #         costo_real = producto.calcular_costo_real()
        #         perdida_potencial = costo_real * producto.stock
                
        #         Alerta.objects.create(
        #             tipo='vencimiento',
        #             nivel=nivel,
        #             usuario=usuario,
        #             producto=producto,
        #             titulo=f'⏰ Vence pronto: {producto.nombre}',
        #             mensaje=f'Vence en {dias_restantes} días. Stock: {producto.stock} unidades. Pérdida si vence: ${perdida_potencial:.2f}',
        #             accion_sugerida=f'Promoción urgente {25 if dias_restantes <= 7 else 15}% descuento',
        #             valor_impacto=perdida_potencial,
        #             fecha_expiracion=producto.fecha_vencimiento
        #         )
        #         alertas_creadas += 1
        
        return alertas_creadas
    
    @staticmethod
    def generar_alertas_rentabilidad(usuario):
        """
        Genera alertas de productos con margen bajo o negativo
        Returns: número de alertas generadas
        """
        from gestion.models import Alerta
        
        alertas_creadas = 0
        productos = Producto.objects.all()
        
        for producto in productos:
            precio_venta = Decimal(str(producto.precio))
            costo_real = producto.calcular_costo_real()
            
            if precio_venta <= 0 or costo_real <= 0:
                continue
            
            # Calcular margen
            margen = ((precio_venta - costo_real) / precio_venta) * 100
            
            # MARGEN NEGATIVO (pérdida)
            if margen < 0:
                existe = Alerta.objects.filter(
                    tipo='margen_negativo',
                    producto=producto,
                    usuario=usuario,
                    leida=False
                ).exists()
                
                if not existe:
                    precio_sugerido = costo_real * Decimal('1.30')  # +30% margen
                    perdida_por_unidad = abs(precio_venta - costo_real)
                    perdida_total = perdida_por_unidad * producto.stock
                    
                    Alerta.objects.create(
                        tipo='margen_negativo',
                        nivel='danger',
                        usuario=usuario,
                        producto=producto,
                        titulo=f'💸 PÉRDIDA: {producto.nombre}',
                        mensaje=f'Margen negativo: {margen:.1f}%. Pérdida: ${perdida_por_unidad:.2f}/unidad. '
                               f'Costo: ${costo_real}, Precio: ${precio_venta}',
                        accion_sugerida=f'URGENTE: Aumentar precio a ${precio_sugerido:.2f} (margen 30%) o discontinuar',
                        valor_impacto=perdida_total
                    )
                    alertas_creadas += 1
            
            # MARGEN BAJO (<15%)
            elif margen < 15:
                existe = Alerta.objects.filter(
                    tipo='margen_bajo',
                    producto=producto,
                    usuario=usuario,
                    leida=False
                ).exists()
                
                if not existe:
                    precio_sugerido = costo_real * Decimal('1.20')  # +20% margen mínimo
                    
                    Alerta.objects.create(
                        tipo='margen_bajo',
                        nivel='warning',
                        usuario=usuario,
                        producto=producto,
                        titulo=f'⚠️ Margen bajo: {producto.nombre}',
                        mensaje=f'Margen actual: {margen:.1f}%. Revisar estrategia de precios.',
                        accion_sugerida=f'Aumentar precio a ${precio_sugerido:.2f} o negociar mejor costo con proveedor'
                    )
                    alertas_creadas += 1
        
        return alertas_creadas
    
    @staticmethod
    def generar_alertas_stock_muerto(usuario):
        """
        Genera alertas de productos sin rotación (stock muerto)
        Returns: número de alertas generadas
        """
        from gestion.models import Alerta
        
        alertas_creadas = 0
        fecha_limite = timezone.now() - timedelta(days=60)  # Sin ventas en 60 días
        
        # Productos con stock pero sin ventas recientes
        productos_con_stock = Producto.objects.filter(stock__gt=0)
        
        for producto in productos_con_stock:
            # Verificar última venta
            ultima_venta = VentaDetalle.objects.filter(
                producto=producto,
                venta__eliminada=False
            ).order_by('-venta__fecha').first()
            
            if not ultima_venta or ultima_venta.venta.fecha < fecha_limite:
                existe = Alerta.objects.filter(
                    tipo='stock_muerto',
                    producto=producto,
                    usuario=usuario,
                    leida=False
                ).exists()
                
                if not existe:
                    costo_real = producto.calcular_costo_real()
                    capital_inmovilizado = costo_real * producto.stock
                    dias_sin_venta = (timezone.now().date() - ultima_venta.venta.fecha.date()).days if ultima_venta else 999
                    
                    Alerta.objects.create(
                        tipo='stock_muerto',
                        nivel='warning',
                        usuario=usuario,
                        producto=producto,
                        titulo=f'📦 Stock muerto: {producto.nombre}',
                        mensaje=f'Sin ventas hace {dias_sin_venta} días. Stock: {producto.stock} unidades. '
                               f'Capital inmovilizado: ${capital_inmovilizado:.2f}',
                        accion_sugerida='Promoción 2x1, descuento 25% o discontinuar producto',
                        valor_impacto=capital_inmovilizado
                    )
                    alertas_creadas += 1
        
        return alertas_creadas
    
    @staticmethod
    def generar_alertas_oportunidades(usuario):
        """
        Genera alertas de oportunidades de optimización
        Returns: número de alertas generadas
        """
        from gestion.models import Alerta
        
        alertas_creadas = 0
        fecha_inicio = timezone.now() - timedelta(days=30)
        
        # Productos con alta demanda y margen bajo (oportunidad de aumentar precio)
        productos_vendidos = VentaDetalle.objects.filter(
            venta__fecha__gte=fecha_inicio,
            venta__eliminada=False
        ).values('producto').annotate(
            total_vendido=Sum('cantidad')
        ).filter(total_vendido__gte=20)  # Más de 20 unidades vendidas en el mes
        
        for item in productos_vendidos:
            producto = Producto.objects.get(id=item['producto'])
            
            precio_venta = Decimal(str(producto.precio))
            costo_real = producto.calcular_costo_real()
            
            if precio_venta <= 0 or costo_real <= 0:
                continue
            
            margen = ((precio_venta - costo_real) / precio_venta) * 100
            
            # Alta demanda + margen bajo = Oportunidad
            if margen < 30:
                existe = Alerta.objects.filter(
                    tipo='oportunidad_venta',
                    producto=producto,
                    usuario=usuario,
                    leida=False
                ).exists()
                
                if not existe:
                    precio_sugerido = costo_real * Decimal('1.40')  # 40% margen
                    ganancia_adicional = (precio_sugerido - precio_venta) * item['total_vendido']
                    
                    Alerta.objects.create(
                        tipo='oportunidad_venta',
                        nivel='success',
                        usuario=usuario,
                        producto=producto,
                        titulo=f'💡 OPORTUNIDAD: {producto.nombre}',
                        mensaje=f'Alta demanda ({item["total_vendido"]} vendidos) y margen bajo ({margen:.1f}%). '
                               f'Puedes aumentar precio sin afectar ventas.',
                        accion_sugerida=f'Aumentar precio a ${precio_sugerido:.2f} (margen 40%)',
                        valor_impacto=ganancia_adicional
                    )
                    alertas_creadas += 1
        
        return alertas_creadas
    
    @classmethod
    def generar_todas_alertas(cls, usuario):
        """
        Ejecuta todos los generadores de alertas
        Returns: diccionario con contadores por tipo
        """
        resultado = {
            'stock': cls.generar_alertas_stock(usuario),
            'vencimiento': cls.generar_alertas_vencimiento(usuario),
            'rentabilidad': cls.generar_alertas_rentabilidad(usuario),
            'stock_muerto': cls.generar_alertas_stock_muerto(usuario),
            'oportunidades': cls.generar_alertas_oportunidades(usuario),
        }
        
        resultado['total'] = sum(resultado.values())
        return resultado
    
    @staticmethod
    def limpiar_alertas_antiguas(dias=30):
        """
        Archiva alertas leídas con más de X días
        """
        from gestion.models import Alerta
        
        fecha_limite = timezone.now() - timedelta(days=dias)
        alertas_archivadas = Alerta.objects.filter(
            leida=True,
            fecha_creacion__lt=fecha_limite,
            archivada=False
        ).update(archivada=True)
        
        return alertas_archivadas
