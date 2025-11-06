"""
Signals para LINO Saludable
============================

Manejo automático de inventario y costos:
- Descuento automático de inventario al crear/reabastecer productos
- Promedio ponderado en compras de materias primas
- Actualización de ventas y stock al agregar/eliminar detalles
"""

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import Producto, Compra, MateriaPrima, VentaDetalle


# ==================== SIGNALS PARA PRODUCTOS ====================
# 
# NOTA: Los signals de Producto están DESACTIVADOS porque ahora usamos
# control manual explícito en las vistas:
# - crear_producto: usa descontar_materias_primas() al crear con stock inicial
# - editar_producto: usa campo cantidad_a_producir para re-stockeo
#
# El signal automático causaba problemas:
# 1. Asumía que cantidad_fraccion siempre está en gramos (divide /1000)
# 2. Causaba doble descuento con el control manual
# 3. No diferenciaba entre ajuste manual vs producción real
#
# Si se reactiva, eliminar la lógica manual de las vistas para evitar duplicación.

# @receiver(pre_save, sender=Producto)
# def guardar_stock_anterior_producto(sender, instance, **kwargs):
#     """DESACTIVADO - Ver nota arriba"""
#     pass

# @receiver(post_save, sender=Producto)
# def descontar_inventario_al_cambiar_stock(sender, instance, created, **kwargs):
#     """DESACTIVADO - Ver nota arriba"""
#     pass


# ==================== SIGNALS PARA COMPRAS ====================

# NOTA: El signal de Compra está DESACTIVADO porque el modelo Compra
# ya tiene un método save() que actualiza el stock y calcula el promedio ponderado
# Ver gestion/models.py línea ~676
#
# Si se reactiva este signal, eliminar la lógica de save() en el modelo Compra
# para evitar duplicación de stock.

# @receiver(post_save, sender=Compra)
# def actualizar_inventario_con_promedio_ponderado(sender, instance, created, **kwargs):
#     """Signal desactivado - ver nota arriba"""
#     pass


# ==================== SIGNALS PARA VENTAS ====================

@receiver(post_save, sender=VentaDetalle)
def actualizar_venta_al_agregar_detalle(sender, instance, created, **kwargs):
    """
    Al crear o modificar un detalle de venta:
    1. Descuenta stock del producto (solo al crear)
    2. Recalcula el total de la venta
    """
    if created:
        # Descontar stock del producto
        producto = instance.producto
        producto.stock -= instance.cantidad
        producto.save()
    
    # Recalcular total de la venta
    instance.venta.calcular_total()


@receiver(post_delete, sender=VentaDetalle)
def actualizar_venta_al_eliminar_detalle(sender, instance, **kwargs):
    """
    Al eliminar un detalle de venta:
    1. Devuelve stock al producto
    2. Recalcula el total de la venta
    """
    # Devolver stock al producto
    producto = instance.producto
    producto.stock += instance.cantidad
    producto.save()
    
    # Recalcular total de la venta
    instance.venta.calcular_total()
