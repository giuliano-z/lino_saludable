# ✅ CHECKLIST DE TESTING - FASE 1 + FASE 2

**Fecha:** 4 de Noviembre de 2025  
**Responsable:** Giuliano Zulatto  
**Versión:** 1.0

---

## 📋 FASE 1 - DASHBOARD BÁSICO

### 1. Hero Section
- [ ] El saludo cambia según hora del día (☀️ Buenos días / 🌤️ Buenas tardes / 🌙 Buenas noches)
- [ ] Muestra el nombre del usuario correctamente
- [ ] Fecha se muestra en español
- [ ] 3 stats del día (Ventas Hoy, Transacciones, Productos Vendidos)
- [ ] Stats muestran valores reales (no mock data)
- [ ] Variación % vs día anterior funciona
- [ ] Búsqueda rápida visible y funcional
- [ ] 3 filtros rápidos (Orgánicos, Sin TACC, Cereales) funcionan

**Resultado:** ___/8 ✅

---

### 2. KPI Cards (4 Métricas Espectaculares)

#### 💰 Ventas del Mes
- [ ] Muestra total real del mes actual
- [ ] Variación % vs mes anterior calculada correctamente
- [ ] Flecha arriba ↑ verde si positivo, abajo ↓ rojo si negativo
- [ ] Sparkline muestra tendencia últimos 7 días
- [ ] No muestra "Sin cambios" cuando hay ventas

#### 🌱 Productos Activos
- [ ] Cuenta total de productos correctamente
- [ ] Detecta productos bajo stock
- [ ] Badge "Catálogo" visible
- [ ] Botón "Ver productos" navega correctamente
- [ ] Estado "Stock saludable" cuando no hay problemas

#### 💎 Valor Inventario
- [ ] Calcula valor total del inventario
- [ ] ROI% calculado correctamente
- [ ] Badge "Patrimonio" visible
- [ ] Valores en formato moneda argentina

#### 🔔 Alertas Críticas
- [ ] Cuenta alertas danger no leídas
- [ ] Muestra "Todo bajo control" cuando count = 0
- [ ] Muestra "Requieren atención" cuando count > 0
- [ ] Botón "Ver alertas" funcional
- [ ] Badge "Notificaciones" visible

**Resultado:** ___/20 ✅

---

### 3. Services Layer

#### DashboardService
- [ ] `get_kpis_principales()` retorna dict con 4 KPIs
- [ ] `get_resumen_hoy()` retorna datos del día actual
- [ ] `get_actividad_reciente()` retorna últimas operaciones
- [ ] `_get_sparkline_ventas()` genera array de 7 valores
- [ ] No hay queries N+1
- [ ] Maneja caso cuando no hay datos (retorna 0)

#### AlertasService
- [ ] `generar_alertas_stock()` crea alertas correctamente
- [ ] Detecta productos agotados (stock = 0)
- [ ] Detecta productos críticos (stock <= stock_minimo)
- [ ] No duplica alertas existentes
- [ ] Usa `producto.precio` (no precio_venta)

**Resultado:** ___/11 ✅

---

## 📊 FASE 2 - GRÁFICOS AVANZADOS

### 4. Gráfico Evolución de Ventas

#### Funcionalidad Básica
- [ ] Gráfico se renderiza sin errores
- [ ] Muestra datos reales (no $0 en todos los días)
- [ ] Eje X muestra fechas en formato DD/MM
- [ ] Eje Y muestra valores en formato moneda ($)
- [ ] Tooltips muestran valor al hacer hover
- [ ] Línea usa color verde LINO (#4a5c3a)

#### Filtros de Período
- [ ] Botón "7 días" filtra correctamente
- [ ] Botón "30 días" filtra correctamente
- [ ] Botón "90 días" filtra correctamente
- [ ] Botón activo tiene background verde (#4a5c3a)
- [ ] Botones inactivos tienen borde verde
- [ ] Cambiar período recarga página con nuevos datos

#### Comparación de Períodos
- [ ] Toggle "Comparar períodos" visible
- [ ] Al activar, muestra línea punteada gris
- [ ] Línea comparativa muestra período anterior
- [ ] Métrica "vs Período Anterior" aparece
- [ ] Variación % calculada correctamente
- [ ] Color verde si positivo, dorado si negativo

#### Métricas Inferiores
- [ ] "Total Período" muestra suma correcta
- [ ] "Promedio Diario" calculado correctamente
- [ ] Colores usan paleta LINO (verde #4a5c3a, #6b7a4f)
- [ ] Valores en formato moneda argentina
- [ ] Font size legible (1.75rem)

**Resultado:** ___/21 ✅

---

### 5. Gráfico Top 5 Productos

#### Funcionalidad Básica
- [ ] Gráfico se renderiza sin errores
- [ ] Muestra top 5 productos por ingresos
- [ ] Barras horizontales (indexAxis: 'y')
- [ ] Usa gradiente de verdes LINO
- [ ] Tooltips muestran valor al hacer hover
- [ ] Labels de productos completos y legibles

#### Layout y Diseño
- [ ] Altura 280px (no corta valores abajo)
- [ ] Padding reducido (compacto)
- [ ] Eje X muestra valores en formato moneda
- [ ] Eje Y muestra nombres de productos
- [ ] No hay margen blanco excesivo
- [ ] Font size apropiado (11-12px)

#### Datos
- [ ] Calcula ingresos = cantidad × precio_unitario
- [ ] Ordena por ingresos DESC
- [ ] Limita a 5 productos máximo
- [ ] Filtra últimos 30 días
- [ ] Maneja caso cuando no hay ventas

**Resultado:** ___/16 ✅

---

### 6. Layout y Responsividad

#### Desktop (> 992px)
- [ ] Grid 8/4 (gráficos izquierda, sidebar derecha)
- [ ] Hero section ocupa ancho completo
- [ ] KPIs en fila de 4 columnas
- [ ] Gráficos apilados verticalmente
- [ ] Sidebar con actividad reciente visible

#### Tablet (768px - 991px)
- [ ] Grid colapsa a col-lg-8 / col-lg-4
- [ ] KPIs en 2 filas de 2 columnas
- [ ] Gráficos mantienen altura
- [ ] Sidebar debajo de gráficos

#### Mobile (< 768px)
- [ ] Todo en columna única
- [ ] KPIs apilados verticalmente
- [ ] Gráficos mantienen aspect ratio
- [ ] Botones de período responsivos
- [ ] Sidebar al final

**Resultado:** ___/14 ✅

---

## 🎨 DISEÑO Y PALETA LINO

### Colores Verificados
- [ ] Verde principal: #4a5c3a
- [ ] Verde medio: #6b7a4f
- [ ] Verde claro: #8b9471
- [ ] Verde muy claro: #abae93
- [ ] Dorado: #d4a574
- [ ] Sin colores Bootstrap (success, info, danger)
- [ ] Botones usan .lino-btn-periodo

**Resultado:** ___/7 ✅

---

## 🐛 BUGS CONOCIDOS RESUELTOS

- [x] #13: Charts renderizando en blanco
- [x] #14: Botones en verde Bootstrap
- [x] #15: producto.precio_venta AttributeError
- [x] #16: KPIs mostrando ceros
- [x] #17: Top 5 cortado abajo
- [x] #18: Ventas no actualizándose
- [x] #19: Gráfico mostrando $0
- [x] #20: Colores no LINO
- [x] #21: Top 5 margen excesivo

**Resultado:** 21/21 ✅

---

## 🔍 TESTING DE REGRESIÓN

### Después de cada cambio verificar:
- [ ] No errores en consola JavaScript
- [ ] No errores 500 en Django
- [ ] No queries lentas (< 100ms)
- [ ] Carga de página < 2 segundos
- [ ] Sin warnings en consola
- [ ] CSS se carga correctamente
- [ ] Chart.js se inicializa
- [ ] Navegación funciona

**Resultado:** ___/8 ✅

---

## 📊 RESUMEN FINAL

**Total Items:** 97  
**Completados:** ___  
**Porcentaje:** ___%  

**Estado General:**
- [ ] APROBADO (> 95%)
- [ ] NECESITA AJUSTES (80-95%)
- [ ] REQUIERE CORRECCIONES (< 80%)

---

## 📝 NOTAS Y OBSERVACIONES

```
[Anota aquí cualquier bug encontrado o comportamiento inesperado]





```

---

## ✅ APROBACIÓN

**Tester:** ___________________  
**Fecha:** ___________________  
**Firma:** ___________________
