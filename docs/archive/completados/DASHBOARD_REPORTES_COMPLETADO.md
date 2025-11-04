# ✅ Dashboard de Reportes - COMPLETADO

## 📊 Vista Implementada

**URL:** `/gestion/reportes/`  
**Template:** `modules/reportes/dashboard.html`  
**Vista:** `reportes_lino()` en views.py

---

## 🎯 Funcionalidades

### 1. KPIs Financieros Principales (4 Cards)

#### 💰 Ingresos Totales
- **Color:** Verde (#28a745)
- **Icono:** bi-cash-stack
- **Cálculo:** Suma total de ventas
- **Badge:** "Ingresos"

#### 📉 Gastos Totales  
- **Color:** Rojo (#dc3545)
- **Icono:** bi-cart-dash
- **Cálculo:** Suma total de compras
- **Badge:** "Gastos"

#### 🏆 Ganancia Neta
- **Color:** Verde oliva (ganancia) / Rojo (pérdida)
- **Icono:** bi-trophy
- **Cálculo:** `ingresos_totales - gastos_totales`
- **Badge Dinámico:** "Ganancia" o "Pérdida"

#### 📈 ROI (Return on Investment)
- **Color:** Azul (#17a2b8)
- **Icono:** bi-percent
- **Cálculo:** `(ganancia_neta / gastos_totales) * 100`
- **Badge:** "ROI"

---

### 2. Sistema de Alertas

**Alertas Automáticas:**

#### ⚠️ Stock Crítico
- **Condición:** Productos con stock <= stock_minimo
- **Tipo:** warning (amarillo)
- **Icono:** bi-exclamation-circle-fill

#### 🚨 Pérdidas Detectadas
- **Condición:** ganancia_neta < 0
- **Tipo:** danger (rojo)  
- **Icono:** bi-exclamation-triangle-fill

---

### 3. Métricas Operativas (2 Secciones)

#### 📊 Métricas de Ventas
- **Total Ventas:** Cantidad de operaciones
- **Ticket Promedio:** `ingresos_totales / total_ventas`
- **Margen Bruto:** Porcentaje con colores:
  - ✅ Verde: >= 20%
  - ⚠️ Amarillo: 10-20%
  - 🔴 Rojo: < 10%
- **Compras Realizadas:** Total de compras

#### 📦 Inventario y Productos
- **Total Productos:** Cantidad en catálogo
- **Stock Crítico:** Productos bajo stock mínimo
  - ✅ Verde: 0 productos críticos
  - 🔴 Rojo: > 0 productos críticos
- **Valor Inventario:** Valorización total
- **Proveedores:** Proveedores activos

---

### 4. Reportes Detallados (6 Cards)

#### 📈 Ventas Detalladas
- **Icono:** bi-graph-up (verde)
- **Link:** Lista de ventas
- **Descripción:** Análisis completo de ventas, productos y tendencias

#### 🛒 Compras y Costos
- **Icono:** bi-cart-check (rojo)
- **Link:** Lista de compras
- **Descripción:** Histórico de compras e inversiones en materia prima

#### 📦 Estado de Inventario
- **Icono:** bi-boxes (verde oliva)
- **Link:** Inventario
- **Descripción:** Stock actual, críticos y valorización de inventario

#### 💹 Análisis de Rentabilidad
- **Icono:** bi-graph-up-arrow (amarillo)
- **Link:** Dashboard Rentabilidad
- **Descripción:** Márgenes, costos vs precios y alertas de rentabilidad

#### 🛍️ Catálogo de Productos
- **Icono:** bi-bag-check (azul)
- **Link:** Lista productos
- **Descripción:** Listado completo, precios y disponibilidad

#### 📚 Recetas y Costos
- **Icono:** bi-book (morado)
- **Link:** Lista recetas
- **Descripción:** Recetas, ingredientes y costeo de producción

---

## 🎨 Diseño Visual

### Colores Principales
```css
--lino-primary: #4a5c3a (verde oliva)
--success: #28a745 (verde)
--danger: #dc3545 (rojo)
--warning: #ffc107 (amarillo)
--info: #17a2b8 (azul)
```

### Efectos Visuales
- **Hover en Cards:** Border color + transform translateY(-4px)
- **Sombras:** Sutiles con color del tema (rgba)
- **Border Radius:** 12px-16px
- **Gradientes:** Linear en iconos de cards

---

## 📋 Variables de Contexto

### Desde `reportes_lino()` View:
```python
{
    'ingresos_totales': Decimal,
    'gastos_totales': Decimal,
    'ganancia_neta': Decimal,
    'margen_porcentaje': float,
    'roi': float,
    'total_ventas': int,
    'total_compras': int,
    'ticket_promedio': Decimal,
    'productos_criticos': int,
    'valor_inventario': Decimal,
    'total_productos': int,
    'proveedores_activos': int,
    'alertas': [
        {
            'tipo': 'warning' | 'danger',
            'titulo': str,
            'descripcion': str
        }
    ],
    'tiene_datos': bool
}
```

---

## 🔗 URLs Relacionadas

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/gestion/reportes/` | `reportes_lino` | Dashboard principal |
| `/gestion/ventas/` | `lista_ventas` | Detalle ventas |
| `/gestion/compras/` | `lista_compras` | Detalle compras |
| `/gestion/inventario/` | `inventario` | Estado stock |
| `/gestion/rentabilidad/` | `dashboard_rentabilidad` | Análisis rentabilidad |
| `/gestion/productos/` | `lista_productos` | Catálogo productos |
| `/gestion/recetas/` | `lista_recetas` | Listado recetas |

---

## ✨ Características Especiales

### 1. Responsividad
- **XL (≥1200px):** 4 columnas para KPIs
- **MD (768-1199px):** 2 columnas
- **SM (<768px):** 1 columna

### 2. Impresión
- **Botón Print:** window.print() en navbar
- **Optimizado:** Para reportes en papel

### 3. Consistencia
- Usa `lino-wizard-ventas.css` (patrón establecido)
- Clases `.lino-card`, `.lino-btn` consistentes
- Bootstrap Icons en todos los elementos

---

## 🚀 Acceso

**Desde Sidebar:**
```
Panel de Control
  └─ Centro de Reportes
```

**URL Directa:**
```
http://127.0.0.1:8000/gestion/reportes/
```

---

## 📊 Estado: COMPLETADO ✅

**Fecha:** 30 octubre 2025  
**Diseño:** Verde Oliva v3  
**Template:** 336 líneas  
**Integración:** Vista `reportes_lino` actualizada

**Progreso Total:** 7/19 vistas (37%)
