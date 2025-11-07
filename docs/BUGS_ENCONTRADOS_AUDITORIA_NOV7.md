# 🐛 BUGS ENCONTRADOS - Auditoría del 7 de Noviembre 2025

## ⚠️  BUG CRÍTICO #1: Stock Negativo Permitido

### Descripción
El sistema permite que el stock de productos llegue a valores negativos.

### Evidencia
```
TEST 2: Stock Negativo en Productos
Stock disponible: -2
❌ Stock negativo prevenido
   ⚠️ STOCK NEGATIVO: -2
```

### Producto Afectado
- **ID:** 117
- **Nombre:** Galletita de Arandanos y Chia 200gr
- **Stock actual:** -2

### Causa Probable
1. El modelo `Producto` tiene validador `MinValueValidator(0)` en el campo `stock`
2. PERO los validadores solo se ejecutan en forms, NO en `save()` directo
3. Cuando se hace `producto.stock = -2; producto.save()`, el validador NO se ejecuta

### Impacto
- 🔴 **CRÍTICO**: Permite ventas sin stock real
- 🔴 **CRÍTICO**: Datos inconsistentes en inventario
- 🟡 **MEDIO**: Puede generar órden de compra incorrectas

### Solución Propuesta
```python
# En models.py, clase Producto
def clean(self):
    if self.stock < 0:
        raise ValidationError('El stock no puede ser negativo')

def save(self, *args, **kwargs):
    self.full_clean()  # Ejecuta validadores
    super().save(*args, **kwargs)
```

O mejor aún, prevenir en las vistas:
```python
# En vista de venta
if producto.stock < cantidad_venta:
    messages.error(request, 'Stock insuficiente')
    return redirect(...)
```

### Estado
🔴 **NO RESUELTO** - Requiere fix inmediato

---

## ✅ Bugs Previamente Corregidos

### Bug #1: Margen de ganancia -43233%
- **Estado:** ✅ RESUELTO
- **Commit:** 263c9ad
- **Fecha:** 2025-11-05

### Bug #2: Costo de producción $2,600,000
- **Estado:** ✅ RESUELTO  
- **Commit:** 263c9ad
- **Fecha:** 2025-11-05

### Bug #3: Productos dropdown vacío
- **Estado:** ✅ RESUELTO
- **Commit:** 28c2586
- **Fecha:** 2025-11-05

### Bug #4: Ventas con stock insuficiente
- **Estado:** ✅ RESUELTO
- **Commit:** 9dc40f6
- **Fecha:** 2025-11-05

### Bug #5: Eliminar compra no restaura stock
- **Estado:** ⏭️ PENDIENTE VERIFICACIÓN
- **Nota:** Requiere prueba manual

### Bug #6: Ventas eliminadas aparecen en historial
- **Estado:** ✅ RESUELTO
- **Commit:** 9c37b3f (Custom Manager)
- **Fecha:** 2025-11-05

### Bug #7: URLs incorrectas en templates
- **Estado:** ✅ RESUELTO
- **Commit:** bee053b
- **Fecha:** 2025-11-07

### Bug #8: Stock no se actualiza al crear ajustes
- **Estado:** ✅ RESUELTO
- **Commit:** 5bc0ae5
- **Fecha:** 2025-11-07

---

## 📊 Resumen de Auditoría

**Fecha:** 7 de noviembre de 2025, 04:00 AM  
**Tests ejecutados:** 2/10 (interrumpido por bug crítico)  
**Bugs encontrados:** 1 nuevo (stock negativo)  
**Bugs corregidos previamente:** 6  
**Bugs pendientes:** 2 (stock negativo + verificar Bug #5)

---

## 🎯 Próximos Pasos

1. **URGENTE:** Corregir stock negativo (Bug #1 nuevo)
2. Completar suite de auditoría (tests 3-10)
3. Verificar Bug #5 manualmente
4. Crear constraint en BD para prevenir stock negativo
5. Agregar alertas cuando stock < 0

---

**Documentado por:** GitHub Copilot  
**Última actualización:** 7 de noviembre de 2025, 04:05 AM
