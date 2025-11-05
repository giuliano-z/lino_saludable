# 🧪 GUÍA DE TESTING MANUAL - Dashboard LINO

**Objetivo:** Verificar visualmente todas las funcionalidades de FASE 1 + FASE 2

---

## 📋 PREPARACIÓN

### 1. Abrir el Dashboard
1. Navega a: `http://127.0.0.1:8000/gestion/`
2. Asegúrate de estar logueado
3. Abre Developer Tools (F12)
4. Ve a la pestaña Console

### 2. Limpiar Caché
1. Presiona **Cmd + Shift + R** (Mac) o **Ctrl + Shift + R** (Windows)
2. Verifica que no hay errores en consola
3. Verifica que CSS se cargó (Network tab → lino-main.css)

---

## ✅ TEST 1: HERO SECTION (5 minutos)

### Saludo Dinámico
- [ ] **Antes de las 12pm:** Debería decir "☀️ ¡Buenos días, [nombre]!"
- [ ] **Entre 12pm y 6pm:** Debería decir "🌤️ ¡Buenas tardes, [nombre]!"
- [ ] **Después de 6pm:** Debería decir "🌙 ¡Buenas noches, [nombre]!"

**Cómo probar:** Cambia la hora del sistema y recarga

### Fecha
- [ ] Muestra: "Tuesday, 4 de November de 2025" (en español)
- [ ] Formato correcto

### Stats del Día (3 cards)
- [ ] **💰 Ventas Hoy:** Muestra valor real (no $0 si hay ventas)
- [ ] **📋 Transacciones:** Cuenta operaciones de hoy
- [ ] **📦 Productos Vendidos:** Suma unidades vendidas hoy
- [ ] Variación % muestra flecha ↑ verde si positivo, ↓ rojo si negativo

### Búsqueda Rápida
- [ ] Campo de búsqueda visible
- [ ] 3 filtros rápidos presentes: 🌱 Orgánicos, 🚫 Sin TACC, 🌾 Cereales
- [ ] Al hacer clic en filtro, navega a lista de productos

**Screenshot recomendado:** 📸 Hero completo

---

## ✅ TEST 2: KPI CARDS (10 minutos)

### 💰 Ventas del Mes
- [ ] **Valor:** Muestra total real del mes (no $0)
- [ ] **Badge "Este Mes":** Verde visible
- [ ] **Icono:** 💰 Cash stack
- [ ] **Variación %:** Calculada vs mes anterior
- [ ] **Trend arrow:** ↑ verde si positivo, ↓ rojo si negativo
- [ ] **Sparkline:** Gráfico mini visible con 7 puntos
- [ ] **Color de card:** Verde (#4a5c3a background en header)

**Acción:** Anota el total: $___________

### 🌱 Productos Activos
- [ ] **Valor:** Cuenta total de productos# Activar entorno
source venv/bin/activate

# Navegar a src
cd /Users/giulianozulatto/Proyectos/lino_saludable/src

# Correr servidor
python manage.py runserver

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# Tests automatizados
python test_dashboard.py

# Collectstatic
python manage.py collectstatic --noinput

# Hard reload browser
Cmd + Shift + R
- [ ] **Badge "Catálogo":** Visible
- [ ] **Icono:** 🌱 Basket
- [ ] **Stock saludable:** Si no hay productos bajo stock
- [ ] **⚠️ X bajo stock:** Si hay productos críticos
- [ ] **Botón "Ver productos":** Navega a lista
- [ ] **Color de card:** Verde primario

**Acción:** Anota el total: _____ productos

### 💎 Valor Inventario
- [ ] **Valor:** Muestra total del inventario (no $0)
- [ ] **Badge "Patrimonio":** Visible
- [ ] **Icono:** 💎 Gem
- [ ] **ROI %:** Calculado y visible
- [ ] **Sparkline:** Tendencia visible
- [ ] **Color de card:** Azul/Info

**Acción:** Anota el valor: $___________

### 🔔 Alertas Críticas
- [ ] **Valor:** Cuenta alertas danger no leídas
- [ ] **Badge "Notificaciones":** Visible
- [ ] **Icono:** 🔔 Bell
- [ ] **"Todo bajo control":** Si count = 0
- [ ] **"Requieren atención":** Si count > 0
- [ ] **Botón "Ver alertas":** Funcional
- [ ] **Color de card:** Rojo/Danger

**Acción:** Anota alertas: _____ críticas

**Screenshot recomendado:** 📸 Los 4 KPIs juntos

---

## ✅ TEST 3: GRÁFICO EVOLUCIÓN DE VENTAS (15 minutos)

### Renderizado Básico
- [ ] Gráfico se muestra (no blanco en blanco)
- [ ] Título: "📊 Evolución de Ventas"
- [ ] Canvas visible con línea verde
- [ ] Eje X muestra fechas (formato DD/MM)
- [ ] Eje Y muestra valores monetarios ($)
- [ ] Grid semi-transparente visible

### Datos Reales
- [ ] **NO muestra $0 en todos los días** si hay ventas
- [ ] Puntos en días con ventas reales
- [ ] Línea conecta puntos correctamente
- [ ] Valor de hoy (04/11) muestra $3000 (tu venta de prueba)

**Acción:** Haz hover sobre un punto
- [ ] Tooltip muestra: "Ventas ($): $3,000" (o el valor real)
- [ ] Formato moneda argentina (. como separador de miles)

### Filtro 7 Días
- [ ] Botón "7 días" tiene fondo verde (#4a5c3a) - está activo por defecto
- [ ] Gráfico muestra últimos 7 días
- [ ] Labels van desde 29/10 hasta 04/11

### Filtro 30 Días
- [ ] Haz clic en "30 días"
- [ ] Página recarga
- [ ] Botón "30 días" ahora está activo (verde)
- [ ] Gráfico muestra 30 puntos en eje X
- [ ] URL cambia a: `?periodo=30`

### Filtro 90 Días
- [ ] Haz clic en "90 días"
- [ ] Página recarga
- [ ] Botón "90 días" activo
- [ ] Gráfico muestra 90 puntos
- [ ] URL: `?periodo=90`

### Comparación de Períodos
- [ ] Vuelve a 7 días
- [ ] Activa toggle "Comparar períodos"
- [ ] Página recarga
- [ ] Aparece segunda línea punteada gris
- [ ] Línea gris muestra período anterior (7 días antes)
- [ ] Aparece métrica "vs Período Anterior"
- [ ] Variación % calculada correctamente
- [ ] Color verde si +%, dorado si -%

### Métricas Inferiores
- [ ] **"$X Total Período":** Suma correcta de todos los días
- [ ] **"$Y Promedio Diario":** Total / número de días
- [ ] **"Z% vs Período Anterior":** Solo si comparación activa
- [ ] Colores: Verde oscuro (#4a5c3a) para Total
- [ ] Font size grande (1.75rem)

**Acción:** Anota valores con periodo 7 días:
- Total: $___________
- Promedio: $___________

**Screenshot recomendado:** 📸 Gráfico con comparación activa

---

## ✅ TEST 4: GRÁFICO TOP 5 PRODUCTOS (10 minutos)

### Renderizado Básico
- [ ] Gráfico se muestra correctamente
- [ ] Título: "⭐ Top 5 Productos (Último Mes)"
- [ ] Barras horizontales (no verticales)
- [ ] Máximo 5 barras visibles
- [ ] Gradiente de verdes LINO

### Datos
- [ ] Nombres de productos en eje Y (izquierda)
- [ ] Valores monetarios en eje X (abajo)
- [ ] Barras ordenadas de mayor a menor (arriba = más ingresos)
- [ ] Colores van de verde oscuro a dorado

**Acción:** Anota el top 3:
1. ___________________ - $___________
2. ___________________ - $___________
3. ___________________ - $___________

### Interacción
- [ ] Haz hover sobre una barra
- [ ] Tooltip muestra: "Ingresos: $X,XXX"
- [ ] Formato moneda argentina

### Layout
- [ ] Altura 280px (no corta valores)
- [ ] No hay margen blanco excesivo arriba/abajo
- [ ] Padding reducido (compacto)
- [ ] Font size legible (12px nombres, 11px valores)
- [ ] Eje X muestra valores completos (no cortados)

**Screenshot recomendado:** 📸 Top 5 completo con hover

---

## ✅ TEST 5: LAYOUT Y RESPONSIVIDAD (10 minutos)

### Desktop (Pantalla completa)
- [ ] Hero ocupa ancho completo
- [ ] 4 KPIs en fila horizontal
- [ ] Gráficos ocupan 8 columnas (izquierda)
- [ ] Sidebar ocupa 4 columnas (derecha)
- [ ] "Actividad Reciente" visible en sidebar
- [ ] "Productos Destacados" visible en sidebar

### Tablet (Reducir ventana a ~768px)
- [ ] KPIs se reorganizan en 2 filas
- [ ] Gráficos mantienen altura
- [ ] Sidebar se mueve debajo de gráficos
- [ ] Todo legible y funcional

### Mobile (Reducir a ~375px)
- [ ] KPIs apilados verticalmente
- [ ] Gráficos ocupan ancho completo
- [ ] Botones de período se adaptan (btn-group-sm)
- [ ] Sidebar al final
- [ ] No hay scroll horizontal

**Screenshot recomendado:** 📸 Vista mobile

---

## ✅ TEST 6: PALETA DE COLORES (5 minutos)

Verifica que NO haya colores Bootstrap estándar:

### Colores Incorrectos (NO deben aparecer)
- [ ] ❌ Verde Bootstrap (#28a745)
- [ ] ❌ Azul Bootstrap (#0d6efd)
- [ ] ❌ Rojo Bootstrap (#dc3545)

### Colores Correctos LINO (Deben aparecer)
- [ ] ✅ Verde principal: #4a5c3a (botones activos, línea gráfico)
- [ ] ✅ Verde medio: #6b7a4f (labels, texto secundario)
- [ ] ✅ Verde claro: #8b9471 (barras Top 5)
- [ ] ✅ Dorado: #d4a574 (barra más clara Top 5)

**Acción:** Inspecciona un botón activo (F12 → Inspector)
- [ ] Verifica: `background-color: rgb(74, 92, 58)` (que es #4a5c3a)

---

## ✅ TEST 7: CONSOLA Y ERRORES (5 minutos)

### Consola JavaScript (F12 → Console)
- [ ] Sin errores rojos
- [ ] Sin warnings importantes
- [ ] Chart.js se carga correctamente
- [ ] JSON parsing sin errores

### Network (F12 → Network)
- [ ] lino-main.css se carga (status 200)
- [ ] Chart.js CDN se carga (status 200)
- [ ] No hay 404s
- [ ] Tiempo de carga < 2 segundos

### Django Server (Terminal)
- [ ] Sin errores 500
- [ ] Sin warnings de queries lentas
- [ ] Requests completan en < 100ms

---

## ✅ TEST 8: FUNCIONALIDAD COMPLETA (10 minutos)

### Crear una Venta Nueva
1. Ve a "Ventas" → "Nueva Venta"
2. Crea una venta con:
   - 1 producto
   - Cantidad: 2
   - Total: $500
3. Guarda la venta

### Verificar Actualización
1. Vuelve al Dashboard
2. Recarga con Cmd+Shift+R
3. Verifica:
   - [ ] "Ventas Hoy" aumentó $500
   - [ ] "Transacciones" aumentó +1
   - [ ] Gráfico de Evolución muestra el nuevo valor en 04/11
   - [ ] Top 5 se actualizó si corresponde

---

## 📊 RESUMEN DE TESTING MANUAL

**Completados:** ___/75 ✅

**Porcentaje:** ___%

### Estado
- [ ] ✅ APROBADO (> 95%)
- [ ] ⚠️ NECESITA AJUSTES (80-95%)
- [ ] ❌ REQUIERE CORRECCIONES (< 80%)

---

## 🐛 BUGS ENCONTRADOS

```
[Anota aquí cualquier problema que encuentres]

1. 

2. 

3. 

```

---

## 📝 OBSERVACIONES

```
[Comentarios generales sobre UX, performance, diseño]




```

---

## ✅ APROBACIÓN FINAL

**Tester:** Giuliano Zulatto  
**Fecha:** 4 de Noviembre de 2025  
**Hora:** ___:___  

**Firma:** ___________________

---

## 🎯 PRÓXIMOS PASOS

Si todo está ✅:
- [ ] Commit final de testing
- [ ] Documentar resultados
- [ ] Planificar FASE 3

Si hay bugs ❌:
- [ ] Crear tickets de issues
- [ ] Priorizar correcciones
- [ ] Re-test después de fixes
