# 📘 MANUAL LINO SALUDABLE - VERSIÓN RESUMIDA

**Sistema de Gestión para Dietética**  
**Usuario:** sister_emprendedora  
**Fecha:** 6 de Noviembre de 2025

---

## 🚀 INICIO RÁPIDO

### **Acceso al Sistema**
```
URL: https://web-production-b0ad1.up.railway.app/admin/
Usuario: sister_emprendedora
Contraseña: [tu contraseña personal]
```

### **Navegación Básica**
```
GESTION (menú principal):
├── 📦 Materias Primas → Ingredientes y stock
├── 🍪 Productos → Brownies, galletas, etc.
├── 📝 Recetas → Cómo hacer cada producto
├── 🛒 Compras → Registrar compras a proveedores
├── 💰 Ventas → Registrar ventas a clientes
├── 🚨 Alertas → Stock bajo o vencimientos
└── 📊 Dashboard → Métricas del negocio
```

---

## 📦 1. GESTIÓN DE INVENTARIO

### **Materias Primas**

**Agregar ingrediente:**
```
GESTION → Materia primas → ADD

Nombre: Harina Integral Orgánica
Unidad medida: kg
Precio por unidad: 450
Stock actual: 5.0
Stock mínimo: 2.0
Activo: ✓

→ SAVE
```

**Ajustar stock:**
```
GESTION → Movimiento materia primas → ADD

Materia prima: [seleccionar]
Tipo: AJUSTE (o COMPRA, PRODUCCION)
Cantidad: 2.5
Observaciones: "Corrección stock físico"

→ SAVE
```

### **Productos**

**Agregar producto:**
```
GESTION → Productos → ADD

Nombre: Brownie Chocolate Premium
Precio venta: 800
Precio costo: [se calcula automático]
Stock actual: 0
Stock mínimo: 10
Tiene receta: ✓ SÍ
Activo: ✓

→ SAVE
```

### **Recetas**

**Crear receta:**
```
1. GESTION → Recetas → ADD
   Producto: Brownie Chocolate
   Nombre: Receta Brownie Clásico
   Rendimiento: 12 (unidades que salen)
   → SAVE

2. GESTION → Receta materia primas → ADD (repetir para cada ingrediente)
   Receta: Receta Brownie Clásico
   Materia prima: Harina
   Cantidad: 0.200
   → SAVE
   
   [Repetir para: cacao, azúcar, aceite, nueces, etc.]
```

---

## 🛒 2. OPERACIONES DIARIAS

### **Registrar Compra**

```
PASO 1: Crear compra
GESTION → Compras → ADD
Proveedor: Almacén Orgánico
Fecha: [hoy]
Factura: A-123456
Total: 8500
→ SAVE

PASO 2: Agregar detalles
GESTION → Compra detalles → ADD
Compra: [la que creaste]
Materia prima: Harina Integral
Cantidad: 5.0
Precio: 450
→ SAVE

[Repetir para cada ingrediente comprado]

✅ Stock se actualiza automáticamente
```

### **Registrar Venta**

```
PASO 1: Crear venta
GESTION → Ventas → ADD
Cliente: María González (o dejar vacío)
Fecha: [hoy]
Hora: 14:30
Total: 4800
Método pago: Efectivo
→ SAVE

PASO 2: Agregar productos
GESTION → Venta detalles → ADD
Venta: [la que creaste]
Producto: Brownie Chocolate
Cantidad: 6
Precio unitario: 800
→ SAVE

[Repetir para cada producto vendido]

✅ Stock se descuenta automáticamente
✅ Ganancia se calcula sola
```

### **Alertas**

```
REVISAR DIARIAMENTE (5 minutos):

GESTION → Alertas → Ver todas

Tipos de alertas:
🚨 CRÍTICO - Stock agotado (actuar HOY)
⚠️ ADVERTENCIA - Stock bajo (comprar pronto)
⏰ VENCIMIENTO - Producto vence pronto (vender/usar urgente)

ACCIÓN:
1. Ver alerta
2. Actuar (comprar, producir, vender)
3. Marcar como resuelta
```

---

## 📊 3. MÉTRICAS Y ANÁLISIS

### **Dashboard Principal**

```
GESTION → Dashboard

VER RÁPIDAMENTE:
• 💰 Ventas del día/semana/mes
• 📈 Ganancia neta
• 🔝 Top 5 productos más vendidos
• 📉 Productos de baja rotación
• 🚨 Alertas activas
• 📊 Gráficas de tendencias
```

### **KPIs Importantes**

```
REVISAR SEMANALMENTE:
─────────────────────────────────────────
📊 Total Ventas Semana: $85,000
💰 Ganancia Neta: $68,000 (80% margen)
🛒 Ticket Promedio: $2,125
🔝 Producto Estrella: Brownies (45 vendidos)
📈 Crecimiento: +12% vs semana anterior
```

### **Reportes Útiles**

```
1. VENTAS POR PERÍODO
   GESTION → Ventas
   Filtrar por fecha: Del [fecha] al [fecha]
   Ver total en la parte inferior

2. PRODUCTOS MÁS VENDIDOS
   Dashboard → Top Productos
   Ver tabla con ranking

3. ROTACIÓN DE STOCK
   Dashboard → Rotación Inventario
   Identificar productos lentos

4. ANÁLISIS DE COSTOS
   Dashboard → Márgenes por Producto
   Ver cuáles dan más ganancia
```

---

## ⚙️ 4. CONFIGURACIÓN

### **Parámetros del Sistema**

```
GESTION → Configuracion costoss (configurar UNA VEZ)

Margen objetivo: 80%
Cobertura stock: 15 días
Alerta stock: 20%
Alerta vencimiento: 15 días
Costo hora producción: 500
Overhead mensual: 16000

→ SAVE
```

### **Usuarios**

```
AUTHENTICATION → Users

Cambiar contraseña:
1. Click en tu usuario
2. Cambiar contraseña (abajo)
3. Ingresar contraseña nueva
4. SAVE
```

### **Backup de Datos**

```
MENSUAL (15 minutos):

1. GESTION → Productos → Seleccionar todos
   Action: Export → Descargar Excel

2. Repetir para:
   • Materia primas
   • Ventas del mes
   • Compras del mes

3. Guardar en Google Drive o Dropbox
```

---

## 🎯 5. CASOS PRÁCTICOS

### **Día Típico (30 minutos totales)**

```
MAÑANA (8:00 - 10 min):
□ Login al sistema
□ Revisar ALERTAS
□ Verificar stock productos del día
□ Planificar compras/producción

DURANTE EL DÍA:
□ Registrar ventas inmediatamente
□ Atender pedidos
□ Producir según necesidad

NOCHE (20:00 - 20 min):
□ Registrar ventas del día (si faltó alguna)
□ Revisar stock actualizado
□ Corregir errores si hay
□ Planificar mañana
```

### **Pedido Grande (Ejemplo: 100 brownies)**

```
DÍA 1 - COTIZAR:
1. Ver receta brownie (rendimiento: 12 unid)
2. Calcular tandas: 100÷12 = 8.3 → hacer 9 tandas
3. Verificar stock ingredientes (multiplicar receta × 9)
4. Calcular precio: Costo $53 × 100 = $5,300
   Precio venta: $800 × 100 = $80,000 (descuento 10% = $72,000)
5. Cotizar al cliente: $72,000

DÍA 2 - COMPRAR:
1. Comprar ingredientes faltantes
2. Registrar compra en sistema

DÍA 3-4 - PRODUCIR:
1. Hacer tandas (9 tandas = 108 brownies)
2. Actualizar stock en sistema

DÍA 5 - ENTREGAR:
1. Entregar 100 brownies
2. Cobrar $72,000
3. Registrar venta en sistema
✅ Ganancia: ~$66,700
```

### **Stock Negativo - Corrección**

```
PROBLEMA: Stock dice -3 unidades

CAUSA: Vendiste sin stock suficiente

SOLUCIÓN:
1. GESTION → Productos → [producto]
2. Ver stock actual: -3
3. GESTION → Movimiento materia primas → ADD
4. Tipo: AJUSTE
5. Cantidad: +3 (o más si produciste)
6. Observaciones: "Corrección stock - producción no registrada"
7. SAVE

✅ Stock corregido
```

---

## ✅ 6. CHECKLISTS

### **Checklist Diario (5 min)**
```
□ Revisar alertas
□ Registrar ventas del día
□ Verificar stock productos principales
```

### **Checklist Semanal (15 min)**
```
□ Revisar total ventas semana
□ Ver productos más vendidos
□ Planificar producciones semana siguiente
□ Actualizar precios si cambiaron costos
□ Verificar productos próximos a vencer
```

### **Checklist Mensual (30 min)**
```
□ Backup de datos (exportar a Excel)
□ Analizar ventas del mes
□ Comparar con mes anterior
□ Revisar productos de baja rotación
□ Actualizar costos materias primas
□ Limpiar alertas viejas
□ Planificar mes siguiente
```

---

## 🆘 7. PROBLEMAS COMUNES

| Problema | Solución Rápida |
|----------|----------------|
| **No puedo entrar** | Verificar URL `/admin/`, usuario y contraseña |
| **Stock incorrecto** | Crear AJUSTE en Movimiento materia primas |
| **Costos mal calculados** | Actualizar precios en Materia primas |
| **Producto no aparece** | Verificar que esté marcado como "Activo" |
| **Stock negativo** | Crear AJUSTE con cantidad positiva |
| **Venta con precio mal** | Editar Venta detalle y corregir precio |
| **Alertas no aparecen** | Verificar Stock mínimo configurado |
| **Sistema lento** | Limpiar caché navegador o revisar internet |

---

## 💡 8. TIPS PRO

```
✅ Registra INMEDIATAMENTE (no confíes en tu memoria)
✅ Revisa alertas TODOS LOS DÍAS (5 minutos)
✅ Stock físico = Stock sistema (ajusta diferencias)
✅ Backup mensual (por si acaso)
✅ Usa Observaciones (anota detalles importantes)
✅ Nombres descriptivos (no "Producto 1", sino "Brownie Chocolate Premium")
✅ Una vez al mes, cuenta stock físicamente y compara

❌ No acumules registros para después
❌ No ignores alertas
❌ No compartas tu contraseña
❌ No dejes ventas sin registrar
```

---

## 📊 9. NÚMEROS CLAVE

### **Revisar Semanalmente:**
```
• Total ventas semana
• Producto más vendido
• Alertas pendientes
• Comparación con semana anterior
```

### **Revisar Mensualmente:**
```
• Total ventas mes vs anterior
• Margen promedio (debe ser > 80%)
• Productos de baja rotación
• Tendencia de costos
```

### **Metas Anuales:**
```
• Crecimiento 10-15% mensual
• Mantener margen > 85%
• Menos 5% desperdicio
• 70%+ clientes recurrentes
```

---

## 🎯 10. FLUJO COMPLETO TÍPICO

```
1. COMPRA → Ir al proveedor → Traer ingredientes → Registrar en sistema
2. PRODUCCIÓN → Hacer productos → Actualizar stock en sistema
3. VENTA → Vender producto → Registrar venta → Stock se descuenta solo
4. ANÁLISIS → Ver dashboard → Tomar decisiones
5. REPETIR → Ajustar basado en datos reales
```

---

## 📱 11. ACCESO MÓVIL

```
✅ FUNCIONA EN CELULAR:
• Registrar ventas rápidas
• Ver stock actual
• Consultar alertas
• Ver precios productos

⚠️ MEJOR EN COMPUTADORA:
• Registrar compras grandes
• Ver reportes completos
• Configurar recetas
• Análisis profundo

TIP: Guarda en favoritos del celular para acceso rápido
```

---

## 🎓 12. RESUMEN EJECUTIVO

### **Lo Esencial**

```
EL SISTEMA TE AYUDA A:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Controlar stock (qué tenés y cuánto)
✓ Calcular costos (cuánto gastás)
✓ Registrar ventas (cuánto ganás)
✓ Alertarte (qué falta o vence)
✓ Analizar negocio (qué funciona mejor)
✓ Tomar decisiones (basadas en datos reales)

TIEMPO DIARIO NECESARIO:
• 5 min mañana (revisar alertas)
• 2-3 min por venta (registrar)
• 10 min noche (cierre día)
TOTAL: ~30 minutos/día

BENEFICIO:
• Sabés EXACTAMENTE cuánto ganás en cada producto
• Nunca te quedás sin ingredientes
• No perdés plata por mal cálculo de costos
• Tomás decisiones con datos, no a ojo
```

---

## 🚀 PRIMEROS PASOS

### **Tu Primera Semana**

```
DÍA 1 (1 hora):
□ Cambiar contraseña
□ Configurar parámetros sistema
□ Agregar 5 materias primas principales
□ Agregar 2-3 productos principales

DÍA 2 (30 min):
□ Crear 1 receta completa
□ Hacer venta de prueba
□ Registrar compra de prueba

DÍA 3-7 (30 min/día):
□ Usar sistema diariamente
□ Registrar todas las operaciones reales
□ Familiarizarte con navegación
□ Revisar dashboard

DESPUÉS DE 1 SEMANA:
✅ Ya te sentirás cómoda
✅ Será automático
✅ Verás el valor del sistema
```

---

## 📞 SOPORTE

```
Si tenés dudas o problemas:
1. Revisar este manual
2. Revisar sección "Problemas Comunes"
3. Contactar a tu hermano (el_super_creador)
4. Revisar manual completo (6 partes detalladas)
```

---

## 🎉 ¡ÉXITO!

**Recordá:**
- El sistema es tu herramienta, vos sos la experta
- Los primeros días serán lentos, después será natural
- Un mes usando el sistema = decisiones 10x mejores
- Registrar todo = poder del negocio

**¡Mucho éxito con LINO Saludable!** 🚀🍪🎂

---

📚 **MANUAL RESUMIDO - v1.0**  
📅 **6 de Noviembre de 2025**  
🌐 **https://web-production-b0ad1.up.railway.app/admin/**

---

## 📖 MANUALES DISPONIBLES

Este es el **MANUAL RESUMIDO** (versión compacta).

También disponible: **MANUAL COMPLETO** (6 partes con ejemplos detallados):
1. `MANUAL_USUARIO_COMPLETO.md` - Primeros pasos
2. `MANUAL_PARTE_2_INVENTARIO.md` - Gestión inventario
3. `MANUAL_PARTE_3_OPERACIONES.md` - Operaciones diarias
4. `MANUAL_PARTE_4_METRICAS.md` - Análisis y métricas
5. `MANUAL_PARTE_5_CONFIGURACION.md` - Configuración
6. `MANUAL_PARTE_6_CASOS_PRACTICOS.md` - Casos prácticos

**Recomendación:** Empezá con este resumido. Si necesitás más detalles de algo específico, consultá la parte correspondiente del manual completo.
