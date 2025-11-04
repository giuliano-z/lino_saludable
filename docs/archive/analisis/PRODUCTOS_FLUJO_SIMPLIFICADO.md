# ✅ PRODUCTOS - FORMULARIO SIMPLIFICADO

## 🎯 OBJETIVO:
Simplificar el formulario de productos para que refleje el flujo real:
1. Productos SIN receta → Fraccionados de 1 materia prima
2. Productos CON receta → Elaborados con múltiples materias primas

---

## 📝 CAMPOS DEL FORMULARIO:

### **SECCIÓN 1: Información Básica**
- Nombre del Producto ✏️
- Descripción ✏️ (opcional)
- Categoría ✏️
- Marca ✏️ (opcional)
- Código de Barras ✏️ (opcional)

### **SECCIÓN 2: Tipo de Producto**
- ☑️ **"Este producto usa una receta"** (checkbox)

**SI NO USA RECETA (fraccionado):**
- Materia Prima Base: [Select de MateriaPrima]
- Cantidad por unidad: [500] [g/kg/ml/l]

**SI USA RECETA:**
- Receta: [Select de Receta]

### **SECCIÓN 3: Precio y Margen**
- **Costo Calculado:** $660 (readonly, verde/rojo según margen)
- **Precio de Venta:** [$400] ✏️ (TÚ lo defines)
- **Margen Real:** -39% ⚠️ (readonly, alerta si negativo)

### **SECCIÓN 4: Stock**
- **Stock Actual:** [10] unidades ✏️
- **Stock Mínimo:** [5] unidades ✏️

---

## 🔧 LÓGICA DEL FORMULARIO:

### **Al CREAR producto:**
```python
1. Usuario marca checkbox "Usa receta": NO
2. Selecciona Materia Prima: "Maní sin sal"
3. Ingresa cantidad: 500g
4. Ingresa stock inicial: 10 unidades
5. Ingresa precio venta: $400

# SISTEMA (automático):
- Calcula costo: (1320 $/kg) × 0.5kg = $660
- Calcula margen: (400-660)/660 = -39% ⚠️
- Descuenta inventario: 25kg - 5kg = 20kg
- Crea producto con stock = 10
```

### **Al EDITAR stock de producto:**
```python
1. Usuario cambia stock de 10 → 15 (+5 unidades)

# SISTEMA (automático):
- Si es SIN receta: Descuenta 5×500g = 2.5kg de inventario
- Si es CON receta: Descuenta según receta × 5 unidades
- Actualiza stock producto a 15
```

---

## ⚙️ CAMBIOS NECESARIOS:

### **1. FormularioProducto simplificado:**
- Eliminar: tipo_producto, costo_base, precio_venta_calculado
- Usar: tiene_receta (checkbox simple)
- Agregar: cantidad_materia_prima_gramos (para fraccionados)

### **2. Cálculo automático en views.py:**
```python
def calcular_costo_producto(producto):
    if producto.tiene_receta and producto.receta:
        # CON receta
        return producto.receta.costo_total()
    elif producto.materia_prima_asociada:
        # SIN receta (fraccionado)
        cantidad_kg = producto.cantidad_fraccion / 1000
        return materia_prima.precio_actual * cantidad_kg
    return 0

def calcular_margen(precio_venta, costo):
    if costo > 0:
        return ((precio_venta - costo) / costo) * 100
    return 0
```

### **3. Signal para descontar inventario:**
```python
@receiver(post_save, sender=Producto)
def actualizar_inventario_al_crear_producto(sender, instance, created, **kwargs):
    if created or instance.stock != instance._stock_anterior:
        diferencia_stock = instance.stock - (instance._stock_anterior or 0)
        
        if instance.tiene_receta and instance.receta:
            # Descontar según receta
            for ingrediente in instance.receta.ingredientes.all():
                materia = ingrediente.materia_prima
                cantidad_descontar = ingrediente.cantidad * diferencia_stock
                materia.stock_actual -= cantidad_descontar
                materia.save()
        
        elif instance.materia_prima_asociada:
            # Descontar cantidad_fraccion
            cantidad_kg = instance.cantidad_fraccion / 1000 * diferencia_stock
            instance.materia_prima_asociada.stock_actual -= cantidad_kg
            instance.materia_prima_asociada.save()
```

---

## 📊 COMPRAS - Solución Promedio Ponderado:

```python
# Modelo Compra
class Compra:
    materia_prima = FK(MateriaPrima)
    cantidad = 20  # kg
    precio_unitario = 1400  # $/kg
    total = 28000  # $ (cantidad × precio)
    proveedor = "Proveedor XYZ"
    fecha = datetime.now()

# Al guardar Compra:
@receiver(post_save, sender=Compra)
def actualizar_inventario_compra(sender, instance, created, **kwargs):
    if created:
        materia = instance.materia_prima
        
        # Promedio Ponderado
        stock_anterior = materia.stock_actual
        precio_anterior = materia.precio_actual
        
        valor_anterior = stock_anterior * precio_anterior
        valor_nuevo = instance.cantidad * instance.precio_unitario
        
        stock_total = stock_anterior + instance.cantidad
        precio_promedio = (valor_anterior + valor_nuevo) / stock_total
        
        materia.stock_actual = stock_total
        materia.precio_actual = precio_promedio
        materia.save()

# Ejemplo:
# Stock: 5kg × $1000 = $5,000
# Compra: 20kg × $1400 = $28,000
# ────────────────────────────
# Total: 25kg × $1,320/kg ✅
```

---

## 🎯 RESUMEN DE ACCIONES:

1. ✅ **Simplificar form.html** de productos
2. ✅ **Eliminar campos** tipo_producto (confuso)
3. ✅ **Usar checkbox** "Usa receta" (claro y simple)
4. ✅ **Mostrar costo/margen** calculados automáticamente
5. ✅ **Implementar** promedio ponderado en Compras
6. ✅ **Signal** para descontar inventario al crear/editar producto

¿Procedo a implementar estos cambios? 🚀
