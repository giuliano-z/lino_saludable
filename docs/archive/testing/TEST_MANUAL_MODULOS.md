# 🧪 TEST MANUAL DE MÓDULOS - LINO V3

## 📅 Fecha: 18/01/2025
## 🎯 Objetivo: Verificar funcionamiento completo de Ventas, Productos y Compras

---

## 🌐 Servidor
**URL Base:** `http://127.0.0.1:8000`

**Estado:** ✅ Corriendo (puerto 8000 en uso)

---

## ✅ CHECKLIST DE TESTING

### 1. **MÓDULO VENTAS** 🛒

#### Lista de Ventas
- [ ] **URL:** `/ventas/`
- [ ] Header verde oliva visible ✅
- [ ] Breadcrumbs: Inicio → Ventas ✅
- [ ] KPIs mostrando datos correctos
- [ ] Tabla con ventas (Fecha, Cliente, Total, Productos, Estado)
- [ ] Botón "Nueva Venta" funcional
- [ ] Filtros por fecha funcionando
- [ ] Paginación operativa
- [ ] Botón "Ver Detalle" (ojo) navegando correctamente

#### Crear Venta (Wizard)
- [ ] **URL:** `/ventas/crear/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Ventas → Nueva Venta ✅
- [ ] **Paso 1:** Selección de cliente funcional
- [ ] **Paso 2:** Agregar productos con cantidades
- [ ] **Paso 3:** Preview del total
- [ ] Cálculo automático de subtotal/total
- [ ] Botón "Finalizar Venta" creando venta correctamente
- [ ] Stock de productos decrementando ✅

#### Detalle de Venta
- [ ] **URL:** `/ventas/<id>/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Ventas → Venta #ID ✅
- [ ] Información del cliente
- [ ] Tabla de productos vendidos
- [ ] Total calculado correctamente
- [ ] Botón "Eliminar Venta" visible
- [ ] Botón "Volver" funcional

#### Eliminar Venta
- [ ] **URL:** `/ventas/<id>/eliminar/`
- [ ] Modal de confirmación rojo ⚠️
- [ ] Advertencia clara
- [ ] Botones Confirmar/Cancelar
- [ ] Al confirmar: Venta eliminada ✅
- [ ] Stock de productos restaurado ✅
- [ ] Redirección a lista de ventas

---

### 2. **MÓDULO PRODUCTOS** 📦

#### Lista de Productos
- [ ] **URL:** `/productos/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Productos ✅
- [ ] KPIs: Total productos, Stock total, Valor inventario
- [ ] Tabla con: Nombre, Categoría, Stock, Precio, Margen
- [ ] Filtros por categoría/origen
- [ ] Botón "Nuevo Producto" funcional
- [ ] Iconos de margen (✅ positivo, ⚠️ negativo)
- [ ] Botón "Ver Detalle" navegando

#### Crear/Editar Producto
- [ ] **URL:** `/productos/crear/` o `/productos/<id>/editar/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs correctos ✅
- [ ] **Checkbox "¿Usa receta?"** visible
- [ ] Al marcar checkbox:
  - [ ] Campo "Receta" aparece
  - [ ] Campos "Materia Prima" + "Cantidad Fracción" desaparecen
- [ ] Al desmarcar checkbox:
  - [ ] Campo "Receta" desaparece
  - [ ] Campos "Materia Prima" + "Cantidad Fracción" aparecen
- [ ] Preview de costo calculado en tiempo real
- [ ] Preview de margen real (% con color verde/rojo)
- [ ] Alerta si margen es negativo ⚠️
- [ ] Formulario reducido a 13 campos ✅
- [ ] Botón "Guardar" creando producto
- [ ] **Inventario descontado automáticamente** ✅

#### Detalle de Producto
- [ ] **URL:** `/productos/<id>/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Productos → [Nombre] ✅
- [ ] Layout 2 columnas (8+4)
- [ ] Columna izquierda: Info completa
- [ ] Columna derecha: Stats + Acciones
- [ ] Costo real calculado y visible
- [ ] Margen real con color correcto
- [ ] Botones: Editar, Eliminar, Volver

#### Eliminar Producto
- [ ] **URL:** `/productos/<id>/eliminar/`
- [ ] Modal de confirmación
- [ ] Advertencia clara
- [ ] Al confirmar: Producto eliminado
- [ ] **Inventario NO se restaura** (comportamiento esperado)

---

### 3. **MÓDULO COMPRAS** 🚚

#### Lista de Compras
- [ ] **URL:** `/compras/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Compras ✅
- [ ] KPIs: Total compras mes, Gasto total, Promedio
- [ ] Tabla: Fecha, Proveedor, Materia Prima, Cantidad, Total
- [ ] Campos correctos: `cantidad_mayoreo`, `precio_mayoreo` ✅
- [ ] Filtros por proveedor/materia/fecha
- [ ] Botón "Nueva Compra" funcional
- [ ] Botón "Ver Detalle" (ojo) navegando

#### Crear Compra
- [ ] **URL:** `/compras/crear/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Compras → Nueva Compra ✅
- [ ] Formulario 6 campos:
  - [ ] Proveedor (texto)
  - [ ] Fecha (date picker)
  - [ ] Materia Prima (select)
  - [ ] Cantidad (número)
  - [ ] Precio Mayoreo (número)
  - [ ] Notas (textarea opcional)
- [ ] Al seleccionar materia prima:
  - [ ] Info card aparece con stock actual
  - [ ] Unidad de medida mostrada
  - [ ] Último costo visible
- [ ] **Cálculo automático del total** (cantidad × precio)
- [ ] Preview de stock nuevo en panel lateral
- [ ] Preview de precio unitario
- [ ] Botón "Registrar Compra" funcional
- [ ] **Stock actualizado con promedio ponderado** ✅

#### Detalle de Compra ⭐ NUEVA
- [ ] **URL:** `/compras/<id>/`
- [ ] Header verde oliva ✅
- [ ] Breadcrumbs: Inicio → Compras → Compra #ID ✅
- [ ] **Sección Información:**
  - [ ] Materia Prima con stock actual
  - [ ] Proveedor
  - [ ] Fecha de compra
  - [ ] Cantidad comprada
- [ ] **Sección Desglose Económico:**
  - [ ] Tabla con precio total, precio unitario, cantidad
  - [ ] Total pagado destacado
  - [ ] Fórmula del cálculo mostrada ✅
- [ ] **Panel Lateral Resumen:**
  - [ ] Card Total Invertido (rojo) 💰
  - [ ] Card Precio Unitario (amarillo) 🏷️
  - [ ] Card Cantidad (azul) 📦
- [ ] **Acciones Rápidas:**
  - [ ] Botón "Nueva Compra"
  - [ ] Botón "Ver Todas"
  - [ ] Botón "Imprimir"
- [ ] **Información Adicional:**
  - [ ] 3 ítems con iconos ✅
- [ ] Función de impresión (Ctrl+P oculta header/botones)

---

## 🧪 TESTS AUTOMATIZADOS

### Test de Flujo de Inventario
**Archivo:** `/src/test_flujo_inventario.py`

**Ejecución:**
```bash
cd /Users/giulianozulatto/Proyectos/lino_saludable/src
/Users/giulianozulatto/Proyectos/lino_saludable/venv/bin/python test_flujo_inventario.py
```

**Resultado Esperado:**
```
✅ Exitosas: 21
❌ Fallidas: 0
🎉 ¡TODOS LOS TESTS PASARON! 🎉
```

**Estado:** ✅ **PASSING (100%)**

---

## 📊 VERIFICACIÓN DE LÓGICA DE NEGOCIO

### 1. **Promedio Ponderado** (Compras)
**Escenario:**
1. Comprar 5kg de Almendras a $1,000 → Stock: 5kg, Costo: $1,000/kg
2. Comprar 20kg de Almendras a $1,400 → Stock: 25kg, Costo: ?

**Fórmula:**
```
Nuevo Costo = (Stock_Ant × Costo_Ant + Cant_Nueva × Precio_Nuevo) / Stock_Total
Nuevo Costo = (5 × 1000 + 20 × 1400) / 25
Nuevo Costo = (5000 + 28000) / 25
Nuevo Costo = 33000 / 25
Nuevo Costo = $1,320/kg ✅
```

**Test:** Crear 2 compras y verificar que costo unitario de la materia prima sea $1,320

---

### 2. **Descuento de Inventario - SIN Receta** (Productos)
**Escenario:**
1. Materia Prima: Maní con 100kg en stock
2. Crear Producto: "Maní sin sal 500g"
   - Materia Prima: Maní
   - Cantidad Fracción: 500g
   - Stock: 10 unidades

**Cálculo:**
```
Descuento = (Cantidad_Fraccion / 1000) × Stock
Descuento = (500 / 1000) × 10
Descuento = 0.5kg × 10
Descuento = 5kg ✅
```

**Test:** Verificar que stock de Maní sea 95kg después de crear producto

---

### 3. **Descuento de Inventario - CON Receta** (Productos)
**Escenario:**
1. Receta "Mix Frutos Secos" por cada 1kg:
   - 0.6kg Almendras
   - 0.4kg Nueces
2. Crear Producto: "Mix 250g" con 8 unidades
   - Cantidad Fracción: 250g

**Cálculo:**
```
Peso_Unidad = 250 / 1000 = 0.25kg
Kg_Totales = 0.25kg × 8 unidades = 2kg

Descuento_Almendras = 0.6kg/kg × 2kg = 1.2kg ✅
Descuento_Nueces = 0.4kg/kg × 2kg = 0.8kg ✅
```

**Test:** Verificar que Almendras -1.2kg y Nueces -0.8kg

---

### 4. **Margen Negativo** (Productos)
**Escenario:**
1. Producto con costo real $700
2. Precio de venta $400

**Cálculo:**
```
Margen = ((Precio - Costo) / Costo) × 100
Margen = ((400 - 700) / 700) × 100
Margen = (-300 / 700) × 100
Margen = -42.86% ⚠️
```

**Test:** Verificar que alerta de margen negativo aparezca en form + detalle

---

## 🎨 VERIFICACIÓN DE DISEÑO

### Paleta de Colores
- [ ] Header: `#4a5c3a` (verde oliva) ✅
- [ ] Gradiente: `#4a5c3a` → `#5d7247` ✅
- [ ] Botones blancos sobre verde ✅
- [ ] Cards con borde sutil ✅
- [ ] Stats cards con colores semánticos (rojo, amarillo, azul, verde) ✅

### Consistencia Visual
- [ ] Todos los módulos tienen header idéntico ✅
- [ ] Breadcrumbs con mismo formato ✅
- [ ] Iconos Bootstrap Icons ✅
- [ ] Mismos estilos de botones (`.lino-btn--white`, `.lino-btn--primary`) ✅
- [ ] Tablas con `.lino-table` ✅
- [ ] Cards con `.lino-card` ✅

### Responsive
- [ ] Vista móvil: Columnas se apilan correctamente
- [ ] Tabla: Scroll horizontal en pantallas pequeñas
- [ ] Header: Título y botón se adaptan
- [ ] Forms: Inputs ocupan 100% en móvil

---

## 🐛 PROBLEMAS CONOCIDOS

### ❌ Errores a Verificar
1. **Campo `compra.total` no existe** → Usar `compra.precio_mayoreo` ✅ CORREGIDO
2. **Campo `compra.cantidad` no existe** → Usar `compra.cantidad_mayoreo` ✅ CORREGIDO
3. **Vista `detalle_compra` no existía** → Creada ✅ CORREGIDO
4. **URL `/compras/<id>/` no existía** → Agregada ✅ CORREGIDO

### ⚠️ Pendientes de Verificar
1. **Navegación desde lista de compras** al detalle
2. **Impresión de detalle de compra** (CSS @media print)
3. **Filtros en lista de compras** por proveedor/materia
4. **Validaciones JavaScript** en form de compras

---

## 📝 NOTAS PARA TESTING

### Datos de Prueba Necesarios
Para testear completamente, necesitas:

1. **Materias Primas:** Al menos 5 (Almendras, Nueces, Avena, Maní, Miel)
2. **Recetas:** Al menos 2 (Mix Frutos Secos, Granola Casera)
3. **Productos:** Al menos 10 (5 con receta, 5 sin receta)
4. **Compras:** Al menos 10 (diferentes proveedores y materias)
5. **Ventas:** Al menos 5 (diferentes clientes y productos)

### Scripts de Población
Si no tienes datos, ejecutar:
```bash
cd /Users/giulianozulatto/Proyectos/lino_saludable/src
/Users/giulianozulatto/Proyectos/lino_saludable/venv/bin/python poblar_lino_real.py
```

---

## ✅ CHECKLIST FINAL

- [ ] **Ventas:** 4 vistas funcionando (lista, crear, detalle, eliminar)
- [ ] **Productos:** 4 vistas funcionando (lista, crear/editar, detalle, eliminar)
- [ ] **Compras:** 3 vistas funcionando (lista, crear, detalle)
- [ ] **Diseño:** Verde oliva consistente en todos los módulos
- [ ] **Lógica:** Promedio ponderado + Descuento inventario funcionando
- [ ] **Tests:** 21/21 tests automatizados pasando
- [ ] **Responsive:** Funciona en móvil/tablet/desktop
- [ ] **Navegación:** Breadcrumbs y botones navegando correctamente

---

## 🚀 SIGUIENTE PASO

Una vez verificado todo:
### **MÓDULO RECETAS** 🍳
- Lista de recetas (cards con ingredientes)
- Crear receta (wizard multi-paso)
- Detalle receta (tabla ingredientes + costo total)
- Editar receta (modificar ingredientes)

**Estimado:** 2-3 horas

---

**Testing realizado por:** _________________  
**Fecha:** ___/___/2025  
**Resultado:** ⬜ APROBADO  ⬜ CON OBSERVACIONES  ⬜ RECHAZADO
