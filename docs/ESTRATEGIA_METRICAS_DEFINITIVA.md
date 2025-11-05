# 🎯 ESTRATEGIA DE MÉTRICAS DEFINITIVA - Sistema LINO

**Fecha:** 5 de Noviembre 2025  
**Objetivo:** Diseñar un sistema de métricas inteligente, accionable y visualmente óptimo  
**Filosofía:** "Cada métrica debe responder: ¿Qué debo hacer ahora?"

---

## 🧠 FRAMEWORK: Las 5 Categorías de Métricas de Negocio

### **📊 Modelo LINO de Inteligencia de Negocio**

```
┌─────────────────────────────────────────────────────────────┐
│                   PIRÁMIDE DE MÉTRICAS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│         🎯 ESTRATÉGICAS (Qué tan bien va el negocio)       │
│              - Ganancia Neta                                │
│              - Margen de Rentabilidad                       │
│              - ROI                                          │
│                                                             │
│         📈 OPERACIONALES (Qué está pasando ahora)          │
│              - Ventas del Mes                               │
│              - Compras del Mes                              │
│              - Cash Flow                                    │
│                                                             │
│         🔄 EFICIENCIA (Qué tan bien opero)                 │
│              - Rotación de Inventario                       │
│              - Cobertura en Días                            │
│              - Conversión de Stock a Venta                  │
│                                                             │
│         ⚠️ RIESGOS (Qué podría salir mal)                  │
│              - Stock Crítico                                │
│              - Productos en Pérdida                         │
│              - Alertas de Vencimiento                       │
│                                                             │
│         💡 OPORTUNIDADES (Qué puedo mejorar)               │
│              - Productos Top Sin Stock                      │
│              - Margen vs Objetivo                           │
│              - Tendencias de Demanda                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 CATÁLOGO COMPLETO DE MÉTRICAS DISPONIBLES

### **1️⃣ CATEGORÍA: VENTAS Y REVENUE**

| # | Métrica | Fórmula | Datos Necesarios | Accionable | Prioridad |
|---|---------|---------|------------------|------------|-----------|
| 1.1 | Ventas Totales Mes | SUM(ventas.total) WHERE mes_actual | Venta.total | ⭐⭐⭐⭐⭐ Alta | CORE |
| 1.2 | Variación vs Mes Anterior | ((mes_actual - mes_anterior) / mes_anterior) * 100 | Ventas mes actual y anterior | ⭐⭐⭐⭐ Media | CORE |
| 1.3 | Ticket Promedio | Ventas_Totales / Cantidad_Ventas | Venta.total, COUNT(ventas) | ⭐⭐⭐ Media | ÚTIL |
| 1.4 | Ventas por Día Promedio | Ventas_Mes / Días_Transcurridos | Ventas + fecha | ⭐⭐⭐⭐ Alta | ÚTIL |
| 1.5 | Proyección Fin de Mes | (Ventas_Actual / Días_Trans) * Días_Totales | Ventas + calendario | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 1.6 | Ventas por Cliente Frecuente | GROUP BY cliente, SUM(total) | Venta.cliente | ⭐⭐ Baja | NICE |
| 1.7 | Mejor Día de la Semana | GROUP BY day_of_week, AVG(ventas) | Venta.fecha | ⭐⭐⭐ Media | INSIGHT |
| 1.8 | Hora Pico de Ventas | GROUP BY hour, COUNT(ventas) | Venta.fecha (hora) | ⭐⭐ Baja | INSIGHT |

**🎯 Recomendación:** Priorizar 1.1, 1.2, 1.4, 1.5

---

### **2️⃣ CATEGORÍA: COMPRAS Y COSTOS**

| # | Métrica | Fórmula | Datos Necesarios | Accionable | Prioridad |
|---|---------|---------|------------------|------------|-----------|
| 2.1 | Compras Totales Mes | SUM(compra.precio_mayoreo) WHERE mes | Compra.precio_mayoreo | ⭐⭐⭐⭐⭐ Alta | CORE |
| 2.2 | Variación vs Mes Anterior | ((mes_actual - mes_anterior) / mes_anterior) * 100 | Compras mes actual y anterior | ⭐⭐⭐⭐ Alta | CORE |
| 2.3 | Última Compra (días) | DAYS(hoy - MAX(compra.fecha)) | Compra.fecha_compra | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 2.4 | Frecuencia de Compra | COUNT(compras) / Días_Periodo | Compras + fechas | ⭐⭐⭐ Media | ÚTIL |
| 2.5 | Proveedor Más Activo | GROUP BY proveedor, COUNT(*) | Compra.proveedor | ⭐⭐ Baja | NICE |
| 2.6 | Costo Promedio por Compra | AVG(compra.precio_mayoreo) | Compra.precio_mayoreo | ⭐⭐⭐ Media | ÚTIL |
| 2.7 | Materias Primas Más Compradas | GROUP BY materia_prima, SUM(cantidad) | Compra.materia_prima | ⭐⭐⭐ Media | INSIGHT |
| 2.8 | Ahorro por Compra al Mayoreo | (Precio_Minorista - Precio_Mayoreo) | MateriaPrima + Compra | ⭐⭐ Baja | NICE |

**🎯 Recomendación:** Priorizar 2.1, 2.2, 2.3

---

### **3️⃣ CATEGORÍA: RENTABILIDAD Y MARGEN**

| # | Métrica | Fórmula | Datos Necesarios | Accionable | Prioridad |
|---|---------|---------|------------------|------------|-----------|
| 3.1 | Ganancia Neta | Ventas_Totales - Costos_Totales | Ventas + Compras | ⭐⭐⭐⭐⭐ Alta | CORE |
| 3.2 | Margen de Rentabilidad % | (Ganancia / Ventas) * 100 | Ganancia + Ventas | ⭐⭐⭐⭐⭐ Alta | CORE |
| 3.3 | ROI % | (Ganancia / Inversión) * 100 | Ganancia + Compras | ⭐⭐⭐⭐ Alta | CORE |
| 3.4 | Productos Rentables % | (Rentables / Total) * 100 | Producto.precio, costo | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 3.5 | Productos en Pérdida % | (En_Pérdida / Total) * 100 | Producto.precio, costo | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 3.6 | Margen Promedio Ponderado | Weighted_Avg(margen, ventas) | Ventas + márgenes | ⭐⭐⭐⭐ Alta | PREMIUM |
| 3.7 | Objetivo de Margen | Meta_Margen - Margen_Real | Configuración + cálculo | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 3.8 | Producto Más Rentable | MAX(margen_porcentaje) | Análisis productos | ⭐⭐⭐ Media | INSIGHT |
| 3.9 | Producto Menos Rentable | MIN(margen_porcentaje) WHERE >0 | Análisis productos | ⭐⭐⭐⭐ Alta | INSIGHT |
| 3.10 | Break-Even Point | Costos_Fijos / Margen_Contribución | Costos + margen | ⭐⭐ Baja | AVANZADO |

**🎯 Recomendación:** Priorizar 3.1, 3.2, 3.4, 3.5, 3.7

---

### **4️⃣ CATEGORÍA: INVENTARIO Y STOCK**

| # | Métrica | Fórmula | Datos Necesarios | Accionable | Prioridad |
|---|---------|---------|------------------|------------|-----------|
| 4.1 | Valor Total Inventario | SUM(producto.precio * stock) | Producto.precio, stock | ⭐⭐⭐⭐ Alta | CORE |
| 4.2 | Stock Crítico (cantidad) | COUNT WHERE stock <= stock_minimo | Producto.stock, stock_minimo | ⭐⭐⭐⭐⭐ Alta | CORE |
| 4.3 | Rotación de Inventario | Ventas_Mes / Valor_Inventario_Promedio | Ventas + inventario | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 4.4 | Cobertura en Días | (Stock_Actual / Ventas_Diarias_Promedio) | Stock + ventas históricas | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 4.5 | Stock Muerto (sin ventas) | COUNT WHERE ventas_ultimo_mes = 0 | VentaDetalle + Producto | ⭐⭐⭐⭐ Alta | ÚTIL |
| 4.6 | Productos Agotados | COUNT WHERE stock = 0 | Producto.stock | ⭐⭐⭐⭐ Alta | CORE |
| 4.7 | Tasa de Agotamiento | Agotados / Total_Productos * 100 | Count agotados vs total | ⭐⭐⭐ Media | ÚTIL |
| 4.8 | Inversión Inmovilizada | SUM(costo * stock) WHERE sin_ventas_30d | Costo + stock + ventas | ⭐⭐⭐ Media | INSIGHT |
| 4.9 | Productos Sin Stock Mínimo | COUNT WHERE stock_minimo IS NULL | Producto.stock_minimo | ⭐⭐⭐ Media | CONFIG |
| 4.10 | Inventario ABC (Pareto) | Clasificar por valor (A=80%, B=15%, C=5%) | Valor inventario por producto | ⭐⭐⭐ Media | AVANZADO |

**🎯 Recomendación:** Priorizar 4.2, 4.3, 4.4, 4.5

---

### **5️⃣ CATEGORÍA: ALERTAS Y RIESGOS**

| # | Métrica | Fórmula | Datos Necesarios | Accionable | Prioridad |
|---|---------|---------|------------------|------------|-----------|
| 5.1 | Alertas Críticas | COUNT WHERE nivel='danger' AND !leida | Alerta.nivel | ⭐⭐⭐⭐⭐ Alta | CORE |
| 5.2 | Productos Próximos a Vencer | COUNT WHERE días_vencimiento <= 7 | Producto.fecha_vencimiento | ⭐⭐⭐⭐ Alta | ÚTIL |
| 5.3 | Margen Negativo (cantidad) | COUNT WHERE precio < costo | Producto precio/costo | ⭐⭐⭐⭐⭐ Alta | CRÍTICO |
| 5.4 | Stock Crítico Top Sellers | Críticos AND en_top_10_ventas | Stock + análisis ventas | ⭐⭐⭐⭐⭐ Alta | PREMIUM |
| 5.5 | Días Sin Compras | DAYS(hoy - última_compra) | Compra.fecha_compra | ⭐⭐⭐⭐ Alta | ÚTIL |
| 5.6 | Días Sin Ventas | DAYS(hoy - última_venta) | Venta.fecha | ⭐⭐⭐ Media | INSIGHT |
| 5.7 | Tendencia Negativa Ventas | Comparar últimas 4 semanas | Ventas semanales | ⭐⭐⭐⭐ Alta | PREMIUM |
| 5.8 | Cash Flow Negativo | Compras_Mes > Ventas_Mes * 0.7 | Compras + ventas | ⭐⭐⭐⭐ Alta | CRÍTICO |

**🎯 Recomendación:** Priorizar 5.1, 5.3, 5.4, 5.8

---

## 🎨 VISUALIZACIÓN ÓPTIMA POR TIPO DE MÉTRICA

### **KPI Card (Número Grande + Badge + Trend)**
**Cuándo usar:** Métrica única, importante, que necesita destacar  
**Ejemplos:** Ventas Totales, Ganancia Neta, Stock Crítico, Alertas  
**Ventaja:** Impacto visual inmediato, fácil de escanear  
**Tamaño ideal:** 4 KPIs por fila en desktop (col-xl-3)

```
┌─────────────────┐
│ 💰 Ventas Mes   │
│ $125,450        │ ← Número grande
│ +12.5% ↑        │ ← Tendencia
│ [Este Mes]      │ ← Badge contexto
└─────────────────┘
```

---

### **Gráfico de Línea (Tendencia Temporal)**
**Cuándo usar:** Ver evolución en el tiempo, detectar patrones  
**Ejemplos:** Ventas últimos 7/30 días, Evolución de stock, Margen mensual  
**Ventaja:** Detecta tendencias, picos, caídas  
**Tamaño ideal:** 6-12 columnas (col-lg-6 o col-lg-12)

```
Ventas Últimos 7 Días
  $
  │     ╱╲
  │    ╱  ╲    ╱
  │   ╱    ╲  ╱
  │  ╱      ╲╱
  └──────────────► días
```

---

### **Gráfico de Barras (Comparación)**
**Cuándo usar:** Comparar productos, categorías, períodos  
**Ejemplos:** Top 5 productos, Ventas por categoría, Compras por proveedor  
**Ventaja:** Fácil comparación visual  
**Tamaño ideal:** 6-8 columnas (col-lg-6 o col-lg-8)

```
Top 5 Productos Vendidos
  ████████████████ Producto A ($5,200)
  ███████████      Producto B ($3,800)
  █████████        Producto C ($3,200)
  ███████          Producto D ($2,400)
  █████            Producto E ($1,800)
```

---

### **Gráfico de Donut/Pie (Distribución)**
**Cuándo usar:** Mostrar porcentajes, composición de un todo  
**Ejemplos:** Distribución de márgenes, Productos por categoría  
**Ventaja:** Porcentajes visuales intuitivos  
**Tamaño ideal:** 4-6 columnas (col-lg-4 o col-lg-6)

```
Distribución de Rentabilidad
      ╭──────╮
    ╱          ╲     78% Rentables (verde)
   │ 78%  12%   │    12% En pérdida (rojo)
   │  10%       │    10% Margen bajo (amarillo)
    ╲          ╱
      ╰──────╯
```

---

### **Tabla de Datos (Detalle Granular)**
**Cuándo usar:** Necesitas ver múltiples atributos de múltiples items  
**Ejemplos:** Lista de productos, Historial de compras, Ranking completo  
**Ventaja:** Información completa, ordenable, filtrable  
**Tamaño ideal:** 12 columnas (col-12), paginada

```
┌──────────────┬──────────┬─────────┬──────────┬────────┐
│ Producto     │ Stock    │ Precio  │ Vendidos │ Margen │
├──────────────┼──────────┼─────────┼──────────┼────────┤
│ Granola      │ 45 und   │ $2,500  │ 120 und  │ 35%    │
│ Pasta        │ 12 und ⚠️│ $1,800  │ 95 und   │ 28%    │
│ Aceite       │ 0 und ❌ │ $3,200  │ 75 und   │ 42%    │
└──────────────┴──────────┴─────────┴──────────┴────────┘
```

---

### **Panel de Información (Contexto + Acción)**
**Cuándo usar:** Mostrar métrica + explicación + acción recomendada  
**Ejemplos:** Objetivo vs Real, Predicción + contexto, Insight + sugerencia  
**Ventaja:** No solo muestra datos, sugiere acciones  
**Tamaño ideal:** 4-6 columnas (col-lg-4 a col-lg-6)

```
┌─────────────────────────────────────┐
│ 🎯 Objetivo de Margen               │
├─────────────────────────────────────┤
│ Meta:    35%                        │
│ Actual:  32.5%                      │
│ ━━━━━━━━━━━━━━━━━━━━━░░░ 93%      │
│                                     │
│ 💡 Faltan 2.5 puntos porcentuales  │
│    Revisa productos con margen <30% │
│    [Ver Productos] 🔍               │
└─────────────────────────────────────┘
```

---

### **Lista de Alertas/Notificaciones**
**Cuándo usar:** Acciones urgentes, problemas que requieren atención  
**Ejemplos:** Stock crítico, Márgenes negativos, Vencimientos  
**Ventaja:** Prioriza lo urgente, accionable  
**Tamaño ideal:** 12 columnas o sidebar (col-12 o col-lg-4)

```
┌─────────────────────────────────────┐
│ 🔔 Alertas Críticas                 │
├─────────────────────────────────────┤
│ ⚠️ Stock crítico - Granola (3 und) │
│    [Crear Compra] 🛒                │
├─────────────────────────────────────┤
│ ❌ Margen negativo - Pasta Integral │
│    [Ajustar Precio] 💰              │
├─────────────────────────────────────┤
│ ⏰ Vence en 5 días - Aceite Coco    │
│    [Ver Detalles] 🔍                │
└─────────────────────────────────────┘
```

---

### **Sparkline (Micro-gráfico)**
**Cuándo usar:** Mostrar tendencia SIN eje, como contexto de una KPI  
**Ejemplos:** Tendencia de ventas 7 días dentro de KPI card  
**Ventaja:** Ahorra espacio, muestra patrón rápido  
**Tamaño ideal:** Dentro de KPI card

```
💰 Ventas Totales
$125,450 +12% ↑
_/‾\__/‾ (últimos 7 días)
```

---

## 🏗️ DISEÑO DE VISTAS: Propuesta Definitiva

### **🏠 DASHBOARD PRINCIPAL** (Vista General del Negocio)
**Objetivo:** Responder "¿Cómo va mi negocio HOY?"  
**Audiencia:** Dueño/Gerente - Vista diaria

#### **KPIs Principales (4)**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 💰 Ventas Mes   │ 🛒 Compras Mes  │ 💎 Ganancia Neta│ 🔔 Alertas      │
│ $125,450        │ $45,200         │ $80,250         │ 3 críticas      │
│ +12.5% ↑        │ +8.2% ↑         │ +15.8% ↑        │ Requieren       │
│ [Este Mes]      │ [Este Mes]      │ [Margen 64%]    │ atención        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**✅ Justificación:**
- **Ventas Mes**: Métrica #1 de revenue (1.1)
- **Compras Mes**: Contexto de costos (2.1) - DATO REAL, no estimación
- **Ganancia Neta**: Bottom line del negocio (3.1)
- **Alertas**: Acciones urgentes (5.1)

#### **Gráficos (2)**
```
┌──────────────────────────────────┬──────────────────────────────┐
│ 📈 Ventas Últimos 30 Días        │ 🏆 Top 5 Productos del Mes   │
│ (Gráfico de línea con área)      │ (Gráfico de barras)          │
│                                  │                              │
│ Permite ver tendencia, picos     │ Qué productos impulsan ventas│
└──────────────────────────────────┴──────────────────────────────┘
```

#### **Métricas Secundarias (Panel Compacto)**
```
┌────────────────────────────────────────────────────────────────┐
│ Resumen del Día                                                │
├───────────────────┬───────────────────┬───────────────────────┤
│ Ventas Hoy        │ Ticket Promedio   │ Proyección Mes        │
│ $4,250            │ $850              │ $142,000              │
│ +5% vs ayer       │ +2% vs promedio   │ +13% vs mes anterior  │
└───────────────────┴───────────────────┴───────────────────────┘
```

#### **Actividad Reciente (Timeline)**
```
┌─────────────────────────────────────────────────────────────┐
│ 🕐 Actividad Reciente                                       │
├─────────────────────────────────────────────────────────────┤
│ 14:32 ✅ Venta #145 - $2,400                               │
│ 12:15 🛒 Compra #89 - Aceite Coco (50 und)                 │
│ 10:45 ✅ Venta #144 - $1,850                               │
│ 09:20 ⚠️ Alerta - Stock crítico: Granola                   │
└─────────────────────────────────────────────────────────────┘
```

---

### **📈 RENTABILIDAD** (Análisis de Márgenes y Costos)
**Objetivo:** Responder "¿Qué productos son rentables? ¿Dónde gano/pierdo?"  
**Audiencia:** Análisis semanal/mensual

#### **KPIs Principales (4)**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 🎯 Objetivo     │ ✅ Rentables    │ ⚠️ En Pérdida   │ 💰 Margen Prom. │
│ Meta: 35%       │ 78%             │ 12%             │ 32.5%           │
│ Real: 32.5%     │ 156 productos   │ 24 productos    │ Ponderado       │
│ ━━━━━░░ 93%     │ Muy bien ✅     │ Revisar ⚠️      │ -2.5pp vs meta  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**✅ Justificación:**
- **Objetivo Margen**: Muestra si cumples metas (3.7) - ACCIONABLE
- **Rentables %**: Salud general del catálogo (3.4)
- **En Pérdida %**: Problemas que resolver (3.5)
- **Margen Promedio**: Contexto ponderado (3.6)

#### **Panel de Objetivo (Nuevo Componente)**
```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 Desglose de Objetivo de Margen                           │
├─────────────────────────────────────────────────────────────┤
│ Meta:        35.0%  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│ Actual:      32.5%  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░   │
│                                                             │
│ Gap: -2.5 puntos porcentuales                               │
│                                                             │
│ 💡 Para alcanzar meta:                                      │
│    • Ajustar precios en 8 productos de margen <25%          │
│    • Reducir costos en 4 productos clave                    │
│    • Enfocarte en top sellers (ya tienen buen margen)       │
│                                                             │
│ [Ver Productos Críticos] 🔍  [Simular Ajustes] 🎲          │
└─────────────────────────────────────────────────────────────┘
```

#### **Gráficos (2)**
```
┌─────────────────────────────────┬──────────────────────────────┐
│ 🍩 Distribución de Rentabilidad │ 🏆 Top 10 Productos          │
│ (Gráfico Donut)                 │ por Margen %                 │
│                                 │ (Gráfico de barras)          │
│ Verde:    78% Rentables         │                              │
│ Rojo:     12% En pérdida        │ Granola: 45%  ████████████   │
│ Amarillo: 10% Margen bajo       │ Pasta:   38%  ████████       │
└─────────────────────────────────┴──────────────────────────────┘
```

#### **Alertas de Rentabilidad (Lista)**
```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ Productos Que Requieren Atención                         │
├─────────────────────────────────────────────────────────────┤
│ ❌ Pasta Integral - Margen: -5% (precio $1,800 < costo)    │
│    💡 Sugerencia: Subir precio a $2,100 (margen 15%)        │
│    [Ajustar Precio] 💰                                      │
├─────────────────────────────────────────────────────────────┤
│ ⚠️ Aceite Oliva - Margen: 8% (muy bajo)                    │
│    💡 Sugerencia: Renegociar con proveedor o subir precio   │
│    [Ver Proveedores] 🏭  [Ajustar Precio] 💰               │
├─────────────────────────────────────────────────────────────┤
│ 📊 Granola Coco - Margen: 25% (bajo para top seller)       │
│    💡 Sugerencia: Es best seller, puede subir a $2,800      │
│    [Simular Ajuste] 🎲                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### **💼 REPORTES** (Análisis Financiero Temporal)
**Objetivo:** Responder "¿Cómo fue el período X? ¿Mejoramos o empeoramos?"  
**Audiencia:** Análisis mensual/trimestral

#### **KPIs Principales (4)** - SIN CAMBIOS, ya perfecto
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 💵 Ingresos     │ 🛒 Gastos       │ 💰 Ganancia     │ 📊 Margen       │
│ $125,450        │ $45,200         │ $80,250         │ 64.0%           │
│ +12% vs ant.    │ +8% vs ant.     │ +15.8% vs ant.  │ ROI: 177%       │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### **Métricas Secundarias (Grid de Stats)**
```
┌───────────────────────────────────────────────────────────┐
│ Métricas de Ventas                                        │
├──────────────────┬──────────────────┬────────────────────┤
│ Total Ventas     │ Ticket Promedio  │ Ventas por Día     │
│ 147 transacciones│ $853             │ $4,048             │
└──────────────────┴──────────────────┴────────────────────┘
```

---

### **📦 INVENTARIO** (Control de Stock y Materias Primas)
**Objetivo:** Responder "¿Qué tengo? ¿Qué necesito? ¿Cuándo comprar?"  
**Audiencia:** Operación diaria

#### **KPIs Principales (4)**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 📊 Cobertura    │ 🚨 Stock Crítico│ ⏱️ Última Compra│ 💰 Valor Total  │
│ 45 días         │ 8 productos     │ Hace 3 días     │ $28,500         │
│ Muy saludable ✅│ Requieren repo. │ Frecuencia OK   │ Inversión       │
│ _/‾‾\_ sparkline│ [Ver Lista] 🔍  │ Próxima: ~5 días│ +5% vs mes ant. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**✅ Justificación:**
- **Cobertura en Días**: Cuánto tiempo durará el stock (4.4) - PREDICTIVO
- **Stock Crítico**: Urgencia de reposición (4.2) - ACCIONABLE
- **Última Compra**: Contexto de frecuencia (2.3) - OPERACIONAL
- **Valor Total**: Inversión inmovilizada (4.1) - FINANCIERO

#### **Nuevo: Panel de Rotación**
```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 Rotación de Inventario                                   │
├─────────────────────────────────────────────────────────────┤
│ Rotación Mensual:  4.2x                                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░░░           │
│                                                             │
│ ✅ Excelente - Tu inventario se vende 4.2 veces al mes      │
│                                                             │
│ 💡 Insights:                                                │
│    • Rotación ideal: 3-5x por mes                           │
│    • Tasa actual indica buena gestión de stock              │
│    • Productos de alta rotación: Granola, Pasta, Aceite     │
│                                                             │
│ [Ver Productos Lentos] 🐌  [Ver Productos Rápidos] 🚀      │
└─────────────────────────────────────────────────────────────┘
```

#### **Tabla de Productos con Stock Crítico**
```
┌──────────────┬────────┬──────────┬───────────┬──────────────┐
│ Producto     │ Stock  │ Mínimo   │ Cobertura │ Acción       │
├──────────────┼────────┼──────────┼───────────┼──────────────┤
│ Granola      │ 3 und  │ 10 und   │ 2 días ⚠️ │ [Comprar] 🛒 │
│ Aceite Coco  │ 5 und  │ 15 und   │ 4 días ⚠️ │ [Comprar] 🛒 │
│ Pasta Integral│ 8 und │ 12 und   │ 6 días    │ [Comprar] 🛒 │
└──────────────┴────────┴──────────┴───────────┴──────────────┘
```

---

## 🚀 FASE 5: Visuales Avanzados + Exportación

### **Nuevos Gráficos a Implementar**

#### **1. Gráfico de Donut (Distribución)**
```javascript
// Distribución de Rentabilidad en vista Rentabilidad
{
  type: 'doughnut',
  data: {
    labels: ['Rentables (78%)', 'Margen Bajo (10%)', 'En Pérdida (12%)'],
    datasets: [{
      data: [78, 10, 12],
      backgroundColor: ['#4a5c3a', '#f59e0b', '#dc2626']
    }]
  }
}
```

#### **2. Gráfico de Área (Tendencia Suavizada)**
```javascript
// Ventas últimos 30 días en Dashboard
{
  type: 'line',
  data: { ... },
  options: {
    fill: true,
    backgroundColor: 'rgba(74, 92, 58, 0.1)',
    tension: 0.4  // Curva suave
  }
}
```

#### **3. Gráfico de Barras Agrupadas (Comparación)**
```javascript
// Ingresos vs Gastos por mes (últimos 6 meses)
{
  type: 'bar',
  data: {
    labels: ['Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov'],
    datasets: [
      { label: 'Ingresos', data: [...], backgroundColor: '#4a5c3a' },
      { label: 'Gastos', data: [...], backgroundColor: '#dc2626' }
    ]
  }
}
```

#### **4. Gráfico Radar (Análisis Multidimensional)**
```javascript
// Evaluación de productos (precio, margen, rotación, stock)
{
  type: 'radar',
  data: {
    labels: ['Precio', 'Margen', 'Rotación', 'Disponibilidad', 'Demanda'],
    datasets: [{
      label: 'Granola Coco',
      data: [85, 75, 90, 45, 95],
      backgroundColor: 'rgba(74, 92, 58, 0.2)'
    }]
  }
}
```

### **Sistema de Exportación PDF**

#### **Botón Exportar en Cada Vista**
```html
<button class="lino-btn lino-btn-ghost" onclick="exportarPDF()">
    <i class="bi bi-file-pdf"></i> Exportar PDF
</button>
```

#### **Contenido del PDF por Vista**

**Dashboard PDF:**
- Logo LINO Saludable
- Título: "Reporte Dashboard - [Fecha]"
- 4 KPIs principales
- Gráfico de ventas (imagen embebida)
- Top 5 productos (tabla)
- Resumen ejecutivo
- Footer: Generado automáticamente

**Rentabilidad PDF:**
- Análisis de rentabilidad general
- KPIs de margen
- Gráfico de distribución
- Lista completa de productos con márgenes
- Productos críticos a ajustar
- Recomendaciones automáticas

**Reportes PDF:**
- Reporte financiero del período
- Comparación período anterior
- Gráficos de ingresos/gastos
- Métricas de rendimiento
- Análisis de tendencias

---

## 📊 IMPLEMENTACIÓN TÉCNICA

### **Prioridad 1: Dashboard Principal (HOY)**

```python
# dashboard_service.py - MEJORADO

def get_kpis_principales(self):
    return {
        'ventas_mes': {
            'total': self._calcular_ventas_mes(),
            'variacion': self._calcular_variacion_ventas(),
            'sparkline': self._get_sparkline_ventas()
        },
        'compras_mes': {  # ⬅️ NUEVO
            'total': self._calcular_compras_mes(),
            'variacion': self._calcular_variacion_compras(),
            'sparkline': self._get_sparkline_compras()
        },
        'ganancia_neta': {  # ⬅️ NUEVO
            'valor': self._calcular_ganancia_neta(),
            'margen_porcentaje': self._calcular_margen(),
            'variacion': self._calcular_variacion_ganancia()
        },
        'alertas': {
            'count': self._contar_alertas_criticas(),
            'criticas': self._obtener_alertas_urgentes()
        }
    }

def _calcular_compras_mes(self):
    """Compras REALES del mes actual"""
    return Compra.objects.filter(
        fecha_compra__gte=self.inicio_mes,
        fecha_compra__lte=self.hoy
    ).aggregate(total=Sum('precio_mayoreo'))['total'] or Decimal('0')

def _calcular_ganancia_neta(self):
    """Ganancia = Ventas - Compras (simplificado)"""
    ventas = self._calcular_ventas_mes()
    compras = self._calcular_compras_mes()
    return ventas - compras
```

### **Prioridad 2: Rentabilidad - Panel de Objetivo**

```python
# analytics.py - NUEVO

class RentabilidadService:
    
    def get_objetivo_margen_analisis(self):
        """Análisis detallado del objetivo de margen"""
        
        # Configuración (podría venir de DB)
        MARGEN_OBJETIVO = Decimal('35.0')
        
        # Cálculo actual
        margen_actual = self._calcular_margen_promedio_ponderado()
        gap = margen_actual - MARGEN_OBJETIVO
        progreso = (margen_actual / MARGEN_OBJETIVO) * 100
        
        # Productos a ajustar
        productos_bajos = self._obtener_productos_margen_bajo(threshold=25)
        
        # Recomendaciones automáticas
        recomendaciones = self._generar_recomendaciones(productos_bajos)
        
        return {
            'meta': float(MARGEN_OBJETIVO),
            'actual': float(margen_actual),
            'gap': float(gap),
            'progreso': float(progreso),
            'productos_a_ajustar': productos_bajos,
            'recomendaciones': recomendaciones
        }
    
    def _generar_recomendaciones(self, productos_bajos):
        """Genera sugerencias automáticas basadas en datos"""
        recomendaciones = []
        
        for producto in productos_bajos:
            margen_actual = producto['margen_porcentaje']
            precio_sugerido = self._calcular_precio_sugerido(
                producto, 
                margen_objetivo=30
            )
            
            recomendaciones.append({
                'tipo': 'ajuste_precio',
                'producto': producto['nombre'],
                'margen_actual': margen_actual,
                'precio_actual': producto['precio'],
                'precio_sugerido': precio_sugerido,
                'impacto_estimado': self._estimar_impacto(producto, precio_sugerido)
            })
        
        return recomendaciones
```

### **Prioridad 3: Inventario - Métricas Predictivas**

```python
# inventario_service.py - NUEVO

class InventarioService:
    
    def get_kpis_inventario(self):
        return {
            'cobertura_dias': self._calcular_cobertura_dias(),
            'stock_critico': self._contar_stock_critico(),
            'ultima_compra': self._dias_desde_ultima_compra(),
            'valor_total': self._calcular_valor_inventario(),
            'rotacion': self._calcular_rotacion_inventario()
        }
    
    def _calcular_cobertura_dias(self):
        """
        Cobertura = Stock_Actual / Ventas_Diarias_Promedio
        Indica cuántos días durará el stock al ritmo actual
        """
        productos = Producto.objects.filter(stock__gt=0)
        
        coberturas = []
        for producto in productos:
            ventas_diarias = self._calcular_ventas_diarias_promedio(producto)
            if ventas_diarias > 0:
                cobertura = producto.stock / ventas_diarias
                coberturas.append(cobertura)
        
        # Cobertura promedio ponderada por valor
        if coberturas:
            return statistics.median(coberturas)  # Mediana más robusta
        return 0
    
    def _calcular_rotacion_inventario(self):
        """
        Rotación = Ventas_Mes / Valor_Inventario_Promedio
        Indica cuántas veces se vende el inventario al mes
        """
        ventas_mes = self._obtener_ventas_mes()
        inventario_promedio = self._calcular_inventario_promedio()
        
        if inventario_promedio > 0:
            return ventas_mes / inventario_promedio
        return 0
    
    def _dias_desde_ultima_compra(self):
        """Días transcurridos desde la última compra"""
        ultima_compra = Compra.objects.order_by('-fecha_compra').first()
        if ultima_compra:
            return (timezone.now().date() - ultima_compra.fecha_compra).days
        return None
```

---

## 📅 ROADMAP DE IMPLEMENTACIÓN

### **Semana 1: Dashboard Principal (5 Nov - 11 Nov)**
- [x] Análisis completo de métricas ✅
- [ ] Implementar KPI "Compras del Mes"
- [ ] Implementar KPI "Ganancia Neta"
- [ ] Actualizar template dashboard_inteligente.html
- [ ] Testing y validación
- [ ] Commit: "✨ FEAT: Dashboard con métricas financieras reales"

### **Semana 2: Rentabilidad Mejorada (12 Nov - 18 Nov)**
- [ ] Implementar "Objetivo de Margen" KPI
- [ ] Crear Panel de Objetivo (componente nuevo)
- [ ] Sistema de recomendaciones automáticas
- [ ] Gráfico de Donut (distribución rentabilidad)
- [ ] Actualizar template dashboard_rentabilidad_v3.html
- [ ] Commit: "✨ FEAT: Sistema de objetivos y recomendaciones"

### **Semana 3: Inventario Predictivo (19 Nov - 25 Nov)**
- [ ] Implementar "Cobertura en Días"
- [ ] Implementar "Rotación de Inventario"
- [ ] Panel de Análisis de Rotación
- [ ] Tabla mejorada de stock crítico con cobertura
- [ ] Actualizar template lista_inventario.html
- [ ] Commit: "✨ FEAT: Inventario predictivo con cobertura"

### **Semana 4: Visuales Avanzados (26 Nov - 2 Dic)**
- [ ] Implementar Chart.js Donut
- [ ] Implementar Chart.js Área
- [ ] Implementar Chart.js Radar
- [ ] Gráficos comparativos (barras agrupadas)
- [ ] Animaciones y transiciones
- [ ] Commit: "✨ FEAT: Gráficos avanzados Chart.js"

### **Semana 5: Exportación PDF (3 Dic - 9 Dic)**
- [ ] Instalar jsPDF o html2pdf.js
- [ ] Template PDF Dashboard
- [ ] Template PDF Rentabilidad
- [ ] Template PDF Reportes
- [ ] Botones de exportación en todas las vistas
- [ ] Commit: "✨ FEAT: Sistema de exportación PDF"

### **Semana 6: Testing y Pulido (10 Dic - 16 Dic)**
- [ ] Testing E2E de todas las métricas
- [ ] Validación de cálculos
- [ ] Optimización de queries
- [ ] Responsive en todas las vistas
- [ ] Documentación de usuario
- [ ] Commit: "🎨 POLISH: Sistema de métricas completo"

---

## 🎯 RESUMEN EJECUTIVO

### **Decisiones Tomadas:**

1. **Dashboard Principal:**
   - ✅ Compras del Mes (dato real, no estimación)
   - ✅ Ganancia Neta (bottom line)
   - ❌ Rotación Inventario (va a Inventario, más apropiado)
   - ❌ Valor Inventario estimado 70% (impreciso, eliminado)

2. **Rentabilidad:**
   - ✅ Objetivo de Margen (nuevo panel)
   - ✅ Recomendaciones automáticas
   - ❌ Total Productos (redundante, eliminado)

3. **Inventario:**
   - ✅ Cobertura en Días (predictivo)
   - ✅ Rotación Inventario (eficiencia)
   - ✅ Última Compra (operacional)

4. **Reportes:**
   - ✅ Sin cambios (ya perfecto)

### **Filosofía de Diseño:**

```
CADA MÉTRICA DEBE RESPONDER UNA DE ESTAS 3 PREGUNTAS:

1. ¿Qué debo hacer AHORA? (Accionable)
2. ¿Cómo voy vs mi META? (Estratégico)
3. ¿Qué pasará si no hago nada? (Predictivo)

Si no responde ninguna → NO VA.
```

### **Próximo Paso Inmediato:**

**¿Empezamos con la implementación del Dashboard mejorado (Compras + Ganancia)?**

Dime y arrancamos código 🚀

