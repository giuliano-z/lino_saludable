# 🚨 BUG CRÍTICO ENCONTRADO - STOCK INCORRECTO

**Fecha**: 7 de noviembre de 2025  
**Reportado por**: Giuliano (durante verificación manual)  
**Severidad**: 🔴 CRÍTICA  
**Módulo**: Sistema de Ajustes de Inventario

---

## 🐛 DESCRIPCIÓN DEL BUG

### Problema Observado:
Al intentar ajustar stock de **Harina de Almendras 1kg**:
- **Stock mostrado en pantalla**: 0 unidades
- **Stock real esperado**: 7 unidades
- **Diferencia**: -7 unidades (INCORRECTO)

### Evidencia:
**Captura de pantalla**: Formulario de ajuste muestra "Stock actual: 0 unidades"  
**Producto**: Harina de Almendras 1kg  
**Usuario**: Giuliano Daniel Zulatto (el_super_creador)  
**URL**: https://web-production-b0ad1.up.railway.app/gestion/ajustes/

---

## 🔍 ANÁLISIS PRELIMINAR

### Posibles Causas:

#### 1. **Campo stock_actual no está actualizado**
```python
# En modelo Producto:
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    stock_actual = models.DecimalField(...)  # ¿Se actualiza correctamente?
```

**Hipótesis**: 
- Al crear/editar compras, el campo `stock_actual` no se está actualizando
- O hay dos campos diferentes (stock_actual vs otro campo)

#### 2. **Vista de ajuste lee campo incorrecto**
```python
# En views.py - ajustar_stock_producto
producto = get_object_or_404(Producto, pk=producto_id)
stock_actual = producto.stock_actual  # ¿Lee el campo correcto?
```

**Hipótesis**:
- La vista lee un campo que no se actualiza
- O hay lógica de cálculo que falla

#### 3. **Cálculo de stock en tiempo real falla**
```python
# ¿Existe algo así?
def calcular_stock_real(producto):
    compras = suma(compras)
    ventas = suma(ventas)
    ajustes = suma(ajustes)
    return compras - ventas + ajustes
```

**Hipótesis**:
- Si el stock se calcula dinámicamente, la query puede estar fallando
- O no incluye todas las operaciones

---

## 🔎 VERIFICACIONES NECESARIAS

### 1. Verificar Stock Real en Base de Datos
```python
# Script de verificación:
from gestion.models import Producto

producto = Producto.objects.get(nombre__icontains="Harina de Almendras")
print(f"Stock actual (campo DB): {producto.stock_actual}")

# Calcular manualmente:
compras_total = sum(...)
ventas_total = sum(...)
ajustes_total = sum(...)
stock_calculado = compras_total - ventas_total + ajustes_total
print(f"Stock calculado: {stock_calculado}")
```

### 2. Revisar Vista de Ajuste
```python
# Archivo: gestion/views.py
# Buscar: def ajustar_stock_producto

# Verificar:
# 1. ¿Qué campo lee? producto.stock_actual
# 2. ¿Cómo se calcula?
# 3. ¿Se actualiza después de operaciones?
```

### 3. Revisar Modelo Producto
```python
# Archivo: gestion/models.py
# Buscar: class Producto

# Verificar:
# 1. ¿Campo stock_actual existe?
# 2. ¿Hay método get_stock_actual()?
# 3. ¿Hay signals que actualicen stock?
```

### 4. Revisar Operaciones Anteriores
```bash
# En Railway shell:
railway run python src/manage.py shell

>>> from gestion.models import Producto, Compra, Venta, AjusteInventario
>>> producto = Producto.objects.get(nombre__icontains="Harina")
>>> print(f"Stock DB: {producto.stock_actual}")
>>> 
>>> # Ver compras:
>>> compras = Compra.objects.filter(producto=producto)
>>> print(f"Compras: {compras.count()}")
>>> 
>>> # Ver ventas:
>>> ventas = Venta.objects.filter(producto=producto)
>>> print(f"Ventas: {ventas.count()}")
>>> 
>>> # Ver ajustes:
>>> ajustes = AjusteInventario.objects.filter(producto=producto)
>>> print(f"Ajustes: {ajustes.count()}")
```

---

## 💡 HIPÓTESIS MÁS PROBABLE

**Teoría #1**: Campo `stock_actual` nunca se inicializó correctamente

Cuando se creó el producto "Harina de Almendras 1kg":
- Se creó con `stock_actual = 0` (default)
- Luego se hicieron compras/operaciones
- Pero `stock_actual` nunca se actualizó

**Solución**:
```python
# Management command para recalcular stock:
python manage.py recalcular_stocks
```

---

## 🔧 PASOS INMEDIATOS

### 1. Verificar Stock en Admin Django (5 min)
```
1. Ir a: https://web-production-b0ad1.up.railway.app/admin/
2. Login: el_super_creador
3. Ir a: Gestion → Productos
4. Buscar: "Harina de Almendras 1kg"
5. Ver campo: stock_actual
6. ¿Dice 0 o 7?
```

### 2. Revisar Código de Ajuste (10 min)
```bash
# Buscar la vista:
grep -n "ajustar_stock_producto" src/gestion/views.py

# Ver cómo calcula stock:
grep -A 20 "def ajustar_stock_producto" src/gestion/views.py
```

### 3. Revisar Modelo Producto (5 min)
```bash
# Ver definición:
grep -A 30 "class Producto" src/gestion/models.py | grep stock
```

---

## 📊 IMPACTO

### Crítico:
- ❌ Stock mostrado NO refleja realidad
- ❌ Ajustes se harán sobre valor incorrecto
- ❌ Pérdida de confianza en datos del sistema

### Afectados:
- Sistema de Ajustes
- Reportes de Stock
- Alertas de Stock Bajo
- Decisiones de compra/venta

---

## ✅ CRITERIO DE ÉXITO

Bug estará resuelto cuando:
1. ✅ Stock en pantalla coincida con stock real
2. ✅ Compras aumenten stock correctamente
3. ✅ Ventas disminuyan stock correctamente
4. ✅ Ajustes modifiquen stock correctamente
5. ✅ Admin Django muestre stock correcto

---

## 📝 PRÓXIMOS PASOS

1. **URGENTE**: Investigar código de ajustes
2. **URGENTE**: Verificar stock en Admin Django
3. **MEDIO**: Crear script de recálculo de stocks
4. **MEDIO**: Agregar validación de integridad
5. **BAJO**: Agregar tests para prevenir regresión

---

**Status**: ✅ INVESTIGADO - NO ES BUG DEL SISTEMA  
**Prioridad**: CERRADO  
**Conclusión**: Stock mostrado era correcto (0), usuario esperaba 7 por error

---

## 🔍 INVESTIGACIÓN COMPLETADA

### Hallazgos:

1. **Código Revisado**: ✅ CORRECTO
   - Form AjusteProductoForm lee `producto.stock` correctamente (línea 693, 701)
   - Form actualiza `producto.stock` correctamente (línea 705)
   - Vista de ajuste ejecuta save() que actualiza stock
   
2. **Base de Datos en Producción**: ✅ VACÍA
   - No hay productos pre-cargados
   - No hay materias primas pre-cargadas
   - "Harina de Almendras 1kg" fue creada durante la prueba

3. **Stock Mostrado**: ✅ CORRECTO
   - Sistema mostraba "Stock actual: 0 unidades"
   - Este era el stock real en ese momento (recién creado)
   - Usuario esperaba 7 pero el producto no tenía historial

### Conclusión:

**NO ES UN BUG**. El sistema funciona correctamente:
- ✅ Lee el campo correcto (`producto.stock` o `mp.stock_actual`)
- ✅ Actualiza el stock después de ajustes
- ✅ Muestra el stock real en la base de datos

El "problema" era que:
- Usuario creó producto nuevo (stock inicial = 0)
- Sistema mostró correctamente stock = 0
- Usuario esperaba ver stock = 7 (pero ese valor no existía)

### Recomendación:

✅ **POBLAR DATOS REALES** en producción:
```bash
railway run python src/poblar_lino_real.py
```

Esto creará productos/MPs con stock inicial correcto.
