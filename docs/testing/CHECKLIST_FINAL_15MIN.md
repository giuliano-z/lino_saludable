# ⚡ CHECKLIST EXPRESS - 15 MINUTOS PARA 97.5%

**Objetivo:** Completar Tests 6, 7 y 8 para llegar a 77/93 → 91/93 items (97.5%)

**Fecha:** 4 de Noviembre de 2025, 18:37  
**Tester:** Giuliano Zulatto  

---

## 🎨 TEST 6: PALETA DE COLORES (7 items - 5 minutos)

### Instrucciones
1. Abre http://localhost:8000/gestion/dashboard/ en Chrome
2. F12 → Elements tab
3. Inspecciona cada elemento con el cursor

### Checklist
```
[ ] 1. Botón periodo ACTIVO tiene background #4a5c3a
       → Click botón "7 días" → Inspeccionar → Computed styles
       
[ ] 2. Línea gráfico ventas es verde #4a5c3a
       → Inspeccionar canvas → Ver Chart.js config en Sources
       
[ ] 3. Labels/badges usan verde medio #6b7a4f
       → Inspeccionar badges "Este Mes", "Catálogo"
       
[ ] 4. Barras Top 5 usan verde claro #8b9471
       → Inspeccionar barras 2-3 del gráfico
       
[ ] 5. Última barra Top 5 usa dorado #d4a574
       → Inspeccionar barra 5
       
[ ] 6. NO existe color Bootstrap green #28a745 en DOM
       → Ctrl+F en Elements → buscar "28a745"
       
[ ] 7. NO existe color Bootstrap blue #0d6efd en DOM
       → Ctrl+F en Elements → buscar "0d6efd"
```

**✅ Pass Criteria:** Los 7 items deben ser ✅  
**⏱️ Tiempo:** 5 minutos máximo

---

## 🐛 TEST 7: CONSOLA Y ERRORES (5 items - 5 minutos)

### Instrucciones
1. F12 → Console tab → Clear console (🚫 icon)
2. Cmd + Shift + R (hard reload)
3. Espera 3 segundos

### Checklist
```
[ ] 1. NO hay errores rojos en Console
       → Verificar 0 líneas rojas
       → (Warnings amarillos están OK)
       
[ ] 2. NO hay errores JavaScript (undefined, null, etc)
       → Scroll por toda la consola
       
[ ] 3. NO hay warnings críticos
       → Ignorar warnings de "Botón de tema" (ya silenciado)
       
[ ] 4. Chart.js carga correctamente
       → Buscar en console: "Chart.js" o verificar gráficos visibles
       
[ ] 5. Network tab → API calls retornan 200 OK
       → F12 → Network tab
       → Filter: XHR
       → Verificar /gestion/dashboard/ = 200
```

**✅ Pass Criteria:** Los 5 items deben ser ✅  
**⏱️ Tiempo:** 5 minutos máximo

---

## ⚡ TEST 8: FUNCIONALIDAD COMPLETA (2 items - 5 minutos)

### Instrucciones
1. Abre http://localhost:8000/gestion/dashboard/
2. Realiza flujo completo end-to-end

### Checklist
```
[ ] 1. FLUJO COMPLETO funciona sin errores:
       
       Paso 1: Click botón "30 días"
       → ✅ Página recarga
       → ✅ Gráfico muestra 30 puntos
       → ✅ Total período actualizado
       → ✅ Promedio diario actualizado
       
       Paso 2: Activa checkbox "Comparar con período anterior"
       → ✅ Página recarga
       → ✅ Aparece línea punteada gris
       → ✅ Variación % visible
       
       Paso 3: Click botón "7 días"
       → ✅ Vuelve a 7 días
       → ✅ Comparación sigue activa
       → ✅ Gráfico actualizado
       
       Paso 4: Scroll a Top 5 Productos
       → ✅ Gráfico visible
       → ✅ 5 barras horizontales
       → ✅ Colores gradiente verde
       
[ ] 2. PERFORMANCE: Gráficos cargan en <500ms
       
       → F12 → Network tab → Clear
       → Cmd + Shift + R (hard reload)
       → Verificar timeline:
         - dashboard_inteligente/ carga en <200ms
         - Chart.js render en <300ms
         - Total <500ms
       
       → Usar Lighthouse (opcional):
         - F12 → Lighthouse tab
         - Performance score >90
```

**✅ Pass Criteria:** Los 2 items deben ser ✅  
**⏱️ Tiempo:** 5 minutos máximo

---

## 📊 PROGRESO FINAL ESPERADO

### Antes (Actual)
```
TESTS COMPLETADOS: 77/93 items (82.8%)
├── TEST 1: Hero Section        ✅ 8/8   (100%)
├── TEST 2: KPI Cards           ✅ 20/20 (100%)
├── TEST 3: Gráfico Ventas      ⚠️ 20/21 (95%)
├── TEST 4: Top 5 Productos     ✅ 16/16 (100%)
├── TEST 5: Layout Responsive   ⚠️ 13/14 (93%)
├── TEST 6: Paleta Colores      ⏳ 0/7   (0%)
├── TEST 7: Consola Errores     ⏳ 0/5   (0%)
└── TEST 8: Funcionalidad       ⏳ 0/2   (0%)
```

### Después (Target)
```
TESTS COMPLETADOS: 91/93 items (97.8%)
├── TEST 1: Hero Section        ✅ 8/8   (100%)
├── TEST 2: KPI Cards           ✅ 20/20 (100%)
├── TEST 3: Gráfico Ventas      ⚠️ 20/21 (95%)  ← Bug #20 menor
├── TEST 4: Top 5 Productos     ✅ 16/16 (100%)
├── TEST 5: Layout Responsive   ⚠️ 13/14 (93%)  ← Bug #20 duplicado
├── TEST 6: Paleta Colores      ✅ 7/7   (100%)  ← NUEVO ✅
├── TEST 7: Consola Errores     ✅ 5/5   (100%)  ← NUEVO ✅
└── TEST 8: Funcionalidad       ✅ 2/2   (100%)  ← NUEVO ✅
```

**Bugs Restantes:** 2 items = Bug #20 (Scroll jump) - Baja prioridad ✅

---

## ✅ CRITERIOS DE APROBACIÓN PARA FASE 3

### Must Have (Obligatorio)
- ✅ Testing Manual ≥ 95%
- ✅ Testing Automatizado ≥ 95% (ya tienes 97%)
- ✅ 0 bugs críticos
- ✅ Performance <500ms

### Nice to Have (Opcional)
- ⚠️ 100% testing (aceptable 97-98%)
- ⚠️ 0 bugs menores (aceptable 1-3)

### 🚀 DECISIÓN
Con **97.8% testing** y **0 bugs críticos** → **APROBADO PARA FASE 3** ✅

---

## 📝 CÓMO REPORTAR RESULTADOS

Después de completar los 3 tests, actualiza `PROGRESO_TESTING_MANUAL.md`:

1. Marca cada checkbox con `[x]`
2. Actualiza tabla resumen:
   ```markdown
   | 6. Paleta Colores | 7 | 7 | 100% | ✅ APROBADO |
   | 7. Consola Errores | 5 | 5 | 100% | ✅ APROBADO |
   | 8. Funcionalidad | 2 | 2 | 100% | ✅ APROBADO |
   | **TOTAL** | **93** | **91** | **97.8%** | ✅ **APROBADO** |
   ```
3. Commit:
   ```bash
   git add docs/testing/
   git commit -m "Testing Manual COMPLETADO - 91/93 items (97.8%)"
   ```

---

## 🎯 SIGUIENTE PASO: FASE 3

Una vez completado testing:

```bash
# Nuevo archivo
docs/implementation/FASE_3_ALERTAS_UI.md
```

**Contenido FASE 3:**
1. Navbar Bell Icon (30 min)
2. Slide-in Alert Panel (45 min)
3. Alerts List Page (45 min)
4. AJAX Mark as Read (30 min)

**Total:** ~2.5 horas

---

**¡ÉXITO! 🚀**
