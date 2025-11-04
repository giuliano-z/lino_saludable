# 📏 GUÍA DE UNIDADES DE MEDIDA - LINO

## 🎯 **REGLA DE ORO:**

> **La cantidad que ingresas en "Cantidad por unidad" debe estar EN LA MISMA UNIDAD que la materia prima**

---

## 📦 **EJEMPLOS PRÁCTICOS:**

### **Caso 1: Materia Prima en GRAMOS**
```
Materia Prima: Almendras (Gramos)
Costo Unitario: $10.00 por gramo

Producto: Bolsita de Almendras 500g
Cantidad por unidad: 500 (gramos)

✅ Costo calculado: 500g × $10.00/g = $5,000.00
```

---

### **Caso 2: Materia Prima en KILOGRAMOS**
```
Materia Prima: Harina de Avena (Kilogramos)
Costo Unitario: $1,500.00 por kilogramo

Producto: Paquete de Harina 1kg
Cantidad por unidad: 1 (kilogramo)

✅ Costo calculado: 1kg × $1,500.00/kg = $1,500.00
```

---

### **Caso 3: Materia Prima en MILILITROS** ⭐
```
Materia Prima: Aceite de Coco (Mililitros)
Costo Unitario: $5.00 por mililitro

Producto: Frasco de Aceite 250ml
Cantidad por unidad: 250 (mililitros)

✅ Costo calculado: 250ml × $5.00/ml = $1,250.00
```

**❗IMPORTANTE:** NO ingreses 250 gramos si la materia prima está en mililitros!

---

### **Caso 4: Materia Prima en LITROS**
```
Materia Prima: Leche de Almendras (Litros)
Costo Unitario: $800.00 por litro

Producto: Botella de Leche 1L
Cantidad por unidad: 1 (litro)

✅ Costo calculado: 1L × $800.00/L = $800.00
```

---

## 🔧 **CÓMO FUNCIONA EL SISTEMA:**

### **1. El Label se Actualiza Automáticamente** ✨

Cuando seleccionas una materia prima, el formulario muestra:

```
Cantidad por unidad (Gramos)  ← Si la MP está en gramos
Cantidad por unidad (Mililitros)  ← Si la MP está en mililitros
Cantidad por unidad (Kilogramos)  ← Si la MP está en kilogramos
```

### **2. El Costo se Calcula en Tiempo Real** 💰

El sistema hace el cálculo automáticamente:

```javascript
Costo del Producto = Cantidad × Costo Unitario de la Materia Prima
```

### **3. Conversión Automática de Unidades** 🔄

Si la materia prima está en una escala y el producto en otra:

```
Materia Prima: Harina (Kilogramos) - $1,500/kg
Producto: Bolsita (Gramos) - 500g

El sistema convierte:
500g ÷ 1000 = 0.5kg
0.5kg × $1,500/kg = $750.00
```

---

## ⚠️ **ERRORES COMUNES:**

### **Error 1: Mezclar Unidades**
❌ **INCORRECTO:**
```
Materia Prima: Aceite de Coco (Mililitros)
Cantidad ingresada: 500 (pensando en gramos)
```

✅ **CORRECTO:**
```
Materia Prima: Aceite de Coco (Mililitros)
Cantidad ingresada: 500 (mililitros)
```

---

### **Error 2: No Verificar el Label**
❌ **INCORRECTO:**
```
Ingresar "500" sin leer que dice "(Kilogramos)"
```

✅ **CORRECTO:**
```
Leer el label: "Cantidad por unidad (Kilogramos)"
Si tu producto es de 500 gramos:
500g = 0.5kg
Ingresar: 0.5
```

---

## 📊 **TABLA DE CONVERSIONES:**

| De | A | Fórmula |
|----|---|---------|
| Gramos | Kilogramos | Dividir ÷ 1000 |
| Kilogramos | Gramos | Multiplicar × 1000 |
| Mililitros | Litros | Dividir ÷ 1000 |
| Litros | Mililitros | Multiplicar × 1000 |

### **Ejemplos:**
- 500 gramos = 0.5 kilogramos
- 1.5 kilogramos = 1500 gramos
- 250 mililitros = 0.25 litros
- 2 litros = 2000 mililitros

---

## 🎨 **MEJORAS IMPLEMENTADAS:**

### **✅ Label Dinámico**
El campo ahora muestra:
```html
Cantidad por unidad (Gramos)
              ↑
    Se actualiza según la MP seleccionada
```

### **✅ Cálculo en Tiempo Real**
No necesitas guardar para ver el costo:
- Seleccionas materia prima
- Ingresas cantidad
- **¡El costo aparece automáticamente!**

### **✅ Helper Text Inteligente**
```
📌 Cantidad en Gramos de la materia prima por unidad de producto
           ↑
    Se adapta a la unidad de la MP
```

---

## 🧪 **TESTING:**

### **Prueba 1: Producto Fraccionado (Sin Receta)**
1. Marcar: "¿Este producto usa una receta?" → **NO**
2. Seleccionar: Materia Prima Base
3. Ver cómo cambia el label de unidad
4. Ingresar cantidad
5. Verificar que el costo se calcula correctamente

### **Prueba 2: Producto con Receta**
1. Marcar: "¿Este producto usa una receta?" → **SÍ**
2. Seleccionar: Receta
3. Verificar que el costo total de la receta se muestre
4. Ingresar precio de venta
5. Ver el margen de ganancia calculado

---

## 💡 **TIPS PRO:**

1. **Siempre verifica el label** antes de ingresar la cantidad
2. **Usa la misma unidad** que la materia prima
3. **El costo se actualiza en tiempo real** - no guardes innecesariamente
4. **Revisa el margen** antes de guardar el producto
5. **Si ves "Se calculará al guardar"** es porque falta seleccionar la MP o Receta

---

## 🆘 **FAQ:**

### **P: ¿Por qué no aparece el costo?**
**R:** Porque no has seleccionado una materia prima o receta, o la cantidad está en 0.

### **P: ¿Puedo usar gramos si la MP está en kilogramos?**
**R:** Sí, pero debes convertir: 500g = 0.5kg

### **P: ¿El sistema convierte automáticamente?**
**R:** SÍ, internamente el sistema maneja las conversiones, pero para evitar confusiones, el label te indica la unidad correcta.

### **P: ¿Qué pasa si me equivoco?**
**R:** Puedes editar el producto después y corregir la cantidad. El sistema recalculará el costo.

---

**Última actualización:** 30 de octubre de 2025
**Versión:** LINO v3.0
