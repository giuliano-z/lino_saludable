# 🧪 Plan de Testing Completo - LINO SYS

**Fecha:** 28 de Octubre de 2025  
**Objetivo:** Validar funcionalidad completa del sistema después de consolidación

---

## 📊 Estado Actual del Sistema

### ✅ Módulos Completados (LINO V3)
- Dashboard
- Productos
- Materias Primas (recién consolidado)
- Inventario
- Reportes

### ⚠️ Módulos Pendientes
- Ventas (40% - CRÍTICO)
- Compras (35% - CRÍTICO)
- Recetas (25% - CRÍTICO)

---

## 🔍 Plan de Testing por Prioridad

### FASE 1: Validación de Materias Primas (10 min)

**Estado:** RECIÉN CONSOLIDADO - Requiere validación completa

**Tests a realizar:**

1. **✅ Lista de Materias Primas**
   - URL: `http://127.0.0.1:8000/gestion/materias-primas/`
   - Verificar:
     - [ ] KPIs se cargan correctamente
     - [ ] Tabla muestra todas las materias primas
     - [ ] Filtros funcionan (búsqueda, proveedor, estado stock)
     - [ ] Botón "Nueva Materia Prima" funciona
     - [ ] Acciones (Ver, Editar) funcionan
     - [ ] Alertas de stock crítico aparecen

2. **✅ Crear Materia Prima**
   - URL: `http://127.0.0.1:8000/gestion/materias-primas/crear/`
   - Verificar:
     - [ ] Formulario se carga sin errores
     - [ ] Campos requeridos funcionan
     - [ ] Validación de stock funciona
     - [ ] Guardar crea registro correctamente
     - [ ] Redirige a lista tras guardar

3. **✅ Editar Materia Prima**
   - URL: `http://127.0.0.1:8000/gestion/materias-primas/{id}/editar/`
   - Verificar:
     - [ ] Formulario carga datos existentes
     - [ ] Campos se pueden modificar
     - [ ] Guardar actualiza correctamente
     - [ ] Navegación breadcrumb funciona

4. **✅ Detalle Materia Prima**
   - URL: `http://127.0.0.1:8000/gestion/materias-primas/{id}/detalle/`
   - Verificar:
     - [ ] Información completa se muestra
     - [ ] KPIs calculan correctamente
     - [ ] Tabla de lotes aparece (si hay)
     - [ ] Botones de acción funcionan

5. **✅ Movimientos**
   - URL: `http://127.0.0.1:8000/gestion/materias-primas/{id}/movimiento/`
   - Verificar:
     - [ ] Formulario de movimiento funciona
     - [ ] Ingreso actualiza stock
     - [ ] Salida reduce stock
     - [ ] Historial se registra

**Resultado Esperado:** 0 errores, navegación fluida

---

### FASE 2: Validación de Productos (5 min)

**Estado:** OPTIMIZADO - Validación de regresión

**Tests a realizar:**

1. **✅ Lista de Productos**
   - URL: `http://127.0.0.1:8000/gestion/productos/`
   - Verificar:
     - [ ] Lista carga sin errores
     - [ ] Filtros funcionan
     - [ ] CRUD completo funciona

2. **✅ Recetas de Productos**
   - Verificar:
     - [ ] Asignación de recetas funciona
     - [ ] Cálculo de costos correcto

**Resultado Esperado:** Sin regresiones

---

### FASE 3: Validación de Dashboard (5 min)

**Estado:** OPTIMIZADO

**Tests a realizar:**

1. **✅ Dashboard Principal**
   - URL: `http://127.0.0.1:8000/gestion/`
   - Verificar:
     - [ ] KPIs se cargan
     - [ ] Gráficos renderizan
     - [ ] Alertas críticas aparecen
     - [ ] Links de navegación funcionan

**Resultado Esperado:** Dashboard funcional

---

### FASE 4: Testing de Módulos Críticos (20 min)

#### 4.1 Ventas (CRÍTICO - 40% completado)

**Tests prioritarios:**

1. **✅ Lista de Ventas**
   - URL: `http://127.0.0.1:8000/gestion/ventas/`
   - Verificar:
     - [ ] Lista carga
     - [ ] Filtros funcionan
     - [ ] Total calculado correctamente

2. **✅ Nueva Venta**
   - Verificar:
     - [ ] Formulario funciona
     - [ ] Selección de productos
     - [ ] Cálculo de totales
     - [ ] Descuenta stock al guardar

3. **⚠️ Problemas conocidos:**
   - Formulario puede tener diseño antiguo
   - Validaciones incompletas

#### 4.2 Compras (CRÍTICO - 35% completado)

**Tests prioritarios:**

1. **✅ Lista de Compras**
   - URL: `http://127.0.0.1:8000/gestion/compras/`
   - Verificar:
     - [ ] Lista carga
     - [ ] Filtros funcionan

2. **✅ Nueva Compra**
   - Verificar:
     - [ ] Formulario funciona
     - [ ] Selección de materias primas
     - [ ] Actualiza stock al guardar

3. **⚠️ Problemas conocidos:**
   - Diseño inconsistente con LINO V3
   - Puede tener formularios viejos

#### 4.3 Recetas (CRÍTICO - 25% completado)

**Tests prioritarios:**

1. **✅ Lista de Recetas**
   - URL: `http://127.0.0.1:8000/gestion/recetas/`
   - Verificar:
     - [ ] Lista carga
     - [ ] Relación con productos visible

2. **✅ Crear/Editar Receta**
   - Verificar:
     - [ ] Asignación de ingredientes
     - [ ] Cálculo de costos
     - [ ] Cantidades correctas

3. **⚠️ Problemas conocidos:**
   - Necesita refactorización completa
   - UI muy básica

---

### FASE 5: Testing de Inventario (5 min)

**Estado:** OPTIMIZADO

**Tests a realizar:**

1. **✅ Inventario General**
   - URL: `http://127.0.0.1:8000/gestion/inventario/`
   - Verificar:
     - [ ] Vista consolidada funciona
     - [ ] Stock actualizado
     - [ ] Alertas correctas

---

### FASE 6: Testing de Reportes (5 min)

**Estado:** OPTIMIZADO

**Tests a realizar:**

1. **✅ Reportes**
   - URL: `http://127.0.0.1:8000/gestion/reportes/`
   - Verificar:
     - [ ] Generación de reportes
     - [ ] Exportación a Excel
     - [ ] Filtros de fecha

---

## 🎯 Prioridades de Corrección

Basado en el testing, priorizaremos correcciones en este orden:

### ALTA PRIORIDAD
1. **Materias Primas** - Completar cualquier bug encontrado
2. **Ventas** - Módulo crítico para operación
3. **Compras** - Integración con materias primas

### MEDIA PRIORIDAD
4. **Recetas** - Cálculo de costos importante
5. **Productos** - Regresiones menores

### BAJA PRIORIDAD
6. **Dashboard** - Refinamientos visuales
7. **Reportes** - Funcionalidad adicional

---

## 📝 Registro de Bugs Encontrados

### Durante Testing:

| # | Módulo | Descripción | Severidad | Estado |
|---|--------|-------------|-----------|--------|
| 1 | Materias Primas | Template lista_materias_primas.html corrupto | 🔴 CRÍTICO | ✅ RESUELTO |
| 2 | Materias Primas | form.html usaba object en vez de materia_prima | 🔴 CRÍTICO | 🔧 EN PROGRESO |
| 3 | - | - | - | - |

---

## ✅ Checklist de Validación Final

Antes de considerar el sistema listo:

- [ ] Todos los módulos cargan sin errores 500
- [ ] No hay errores de template syntax
- [ ] Navegación fluida entre vistas
- [ ] CRUD completo funciona en todos los módulos
- [ ] Cálculos de stock/costos correctos
- [ ] Diseño LINO V3 consistente en módulos principales
- [ ] Sin regresiones en funcionalidad existente

---

## 🚀 Siguiente Fase: Optimización

Una vez completado el testing y corregidos los bugs:

1. **Módulo Ventas** - Actualizar a LINO V3
2. **Módulo Compras** - Actualizar a LINO V3
3. **Módulo Recetas** - Refactorización completa

---

**Autor:** Claude (GitHub Copilot)  
**Actualizado:** 28 de Octubre de 2025, 19:45
