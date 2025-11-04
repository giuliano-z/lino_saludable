"""
Signals para LINO Saludable
============================

Manejo automático de inventario y costos:
- Descuento automático de inventario al crear/reabastecer productos
- Promedio ponderado en compras de materias primas
"""

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Producto, Compra, MateriaPrima


# ==================== SIGNALS PARA PRODUCTOS ====================

@receiver(pre_save, sender=Producto)
def guardar_stock_anterior_producto(sender, instance, **kwargs):
    """
    Guarda el stock anterior del producto para detectar cambios.
    Necesario para saber cuánto inventario descontar.
    """
    if instance.pk:  # Si el producto ya existe
        try:
            producto_anterior = Producto.objects.get(pk=instance.pk)
            instance._stock_anterior = producto_anterior.stock
        except Producto.DoesNotExist:
            instance._stock_anterior = 0
    else:  # Si es un producto nuevo
        instance._stock_anterior = 0


@receiver(post_save, sender=Producto)
def descontar_inventario_al_cambiar_stock(sender, instance, created, **kwargs):
    """
    Descuenta inventario automáticamente cuando aumenta el stock de un producto.
    
    Casos:
    1. Crear producto con stock inicial → descuenta inventario
    2. Editar producto aumentando stock → descuenta la diferencia
    3. Vender producto (disminuir stock) → NO descuenta inventario (ya se descontó antes)
    """
    stock_anterior = getattr(instance, '_stock_anterior', 0)
    stock_nuevo = instance.stock
    diferencia = stock_nuevo - stock_anterior
    
    # Solo procesar si AUMENTÓ el stock (producción/reabastecimiento)
    if diferencia > 0:
        
        if instance.tiene_receta and instance.receta:
            # ========== PRODUCTO CON RECETA ==========
            # Descuenta múltiples materias primas según la receta
            
            try:
                # Obtener peso de cada unidad del producto
                # Si tiene cantidad_fraccion, usarlo (ej: 250g por bolsita)
                # Si no, asumir que la receta es para 1kg y cada unidad es 1kg
                if instance.cantidad_fraccion:
                    # cantidad_fraccion está en gramos, convertir a kg
                    peso_unidad_kg = Decimal(str(instance.cantidad_fraccion)) / Decimal('1000')
                else:
                    # Asumir 1kg por unidad si no está especificado
                    peso_unidad_kg = Decimal('1.0')
                
                # Total de kg a producir
                kg_totales_a_producir = peso_unidad_kg * Decimal(str(diferencia))
                
                for ingrediente in instance.receta.recetamateriaprima_set.all():
                    materia = ingrediente.materia_prima
                    # Las cantidades en la receta son para 1kg de producto final
                    # Multiplicar por los kg totales que vamos a producir
                    cantidad_necesaria = ingrediente.cantidad * kg_totales_a_producir
                    
                    # Validar que haya stock suficiente
                    if materia.stock_actual < cantidad_necesaria:
                        # TODO: Manejar error (podría lanzar excepción o enviar alerta)
                        print(f"⚠️ WARNING: Stock insuficiente de {materia.nombre}")
                        print(f"   Necesario: {cantidad_necesaria} {materia.get_unidad_medida_display()}")
                        print(f"   Disponible: {materia.stock_actual} {materia.get_unidad_medida_display()}")
                        continue
                    
                    # Descontar inventario
                    materia.stock_actual -= cantidad_necesaria
                    materia.save()
                    
                    print(f"✅ Descontado {cantidad_necesaria} {materia.get_unidad_medida_display()} de {materia.nombre}")
            
            except Exception as e:
                print(f"❌ Error al descontar inventario (receta): {e}")
        
        elif instance.materia_prima_asociada and instance.cantidad_fraccion:
            # ========== PRODUCTO SIN RECETA (Fraccionado) ==========
            # Descuenta solo 1 materia prima
            
            try:
                materia = instance.materia_prima_asociada
                # Convertir gramos a kg (mantener como Decimal)
                cantidad_kg = (Decimal(str(instance.cantidad_fraccion)) / Decimal('1000')) * Decimal(str(diferencia))
                
                # Validar stock suficiente
                if materia.stock_actual < cantidad_kg:
                    print(f"⚠️ WARNING: Stock insuficiente de {materia.nombre}")
                    print(f"   Necesario: {cantidad_kg} kg")
                    print(f"   Disponible: {materia.stock_actual} kg")
                else:
                    # Descontar inventario
                    materia.stock_actual -= cantidad_kg
                    materia.save()
                    
                    print(f"✅ Descontado {cantidad_kg} kg de {materia.nombre}")
            
            except Exception as e:
                print(f"❌ Error al descontar inventario (fraccionado): {e}")


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

