# 🧪 **GUÍA DE TESTING - FASE 1 COMPLETADA**

## 🎯 **Objetivo**
Verificar que los cambios de Fase 1 funcionan correctamente en el navegador.

---

## 🌐 **Pre-requisitos**

1. ✅ Servidor Django corriendo: `http://127.0.0.1:8000/`
2. ✅ Virtual environment activado
3. ✅ Base de datos con datos de ejemplo

---

## 📋 **CHECKLIST DE TESTING**

### **1. Login/Logout** ⏱️ 5 min

#### **1.1 Login** 🔐
**URL**: `http://127.0.0.1:8000/accounts/login/`

**Verificar**:
- [ ] Diseño moderno con fondo gradiente verde natural
- [ ] Logo circular con hoja 🌿 en el centro
- [ ] Header verde (#4a5c3a) con degradado
- [ ] Inputs con iconos (persona y llave)
- [ ] Placeholder text presente
- [ ] Footer con enlace de contacto
- [ ] Indicador de versión "LINO V3.0"

**Probar Funcionalidad**:
1. Ingresar credenciales incorrectas
   - [ ] Aparece alerta roja con mensaje de error
2. Ingresar credenciales correctas
   - [ ] Botón cambia a "Validando..."
   - [ ] Redirección exitosa

**Usuario de prueba**:
```
Usuario: admin
Contraseña: [tu contraseña]
```

---

#### **1.2 Logout** 👋
**URL**: `http://127.0.0.1:8000/accounts/logout/`

**Verificar**:
- [ ] Icono verde con check ✓
- [ ] Mensaje "¡Hasta pronto! 👋"
- [ ] Texto explicativo
- [ ] Botón "Iniciar Sesión Nuevamente" (verde)
- [ ] Botón "Volver al Inicio" (gris)
- [ ] Sección de seguridad con shield icon
- [ ] Footer con corazón rojo

**Probar**:
1. Click en "Iniciar Sesión Nuevamente"
   - [ ] Redirección a login
2. Click en "Volver al Inicio"
   - [ ] Redirección a home

---

### **2. Vista Productos** ⏱️ 10 min

**URL**: `http://127.0.0.1:8000/productos/lino/`

#### **2.1 Page Header**
- [ ] Título: "Gestión de Productos"
- [ ] Subtítulo: "Administra el inventario completo..."
- [ ] Icono de caja 📦
- [ ] Botón "Nuevo Producto" (verde, esquina superior derecha)

#### **2.2 KPIs (Tarjetas Métricas)**
Verificar que hay **4 tarjetas** en fila:

**Tarjeta 1: Total Productos**
- [ ] Fondo blanco
- [ ] Label: "TOTAL PRODUCTOS" (uppercase, gris)
- [ ] Valor numérico grande (verde #4a5c3a)
- [ ] Icono circular verde con caja
- [ ] Subtítulo: "Activos en inventario"
- [ ] Hover: Barra verde superior aparece

**Tarjeta 2: Stock Crítico**
- [ ] Valor numérico (amarillo #f59e0b)
- [ ] Icono amarillo con triángulo de advertencia
- [ ] Subtítulo: "Requieren atención"

**Tarjeta 3: Agotados**
- [ ] Valor numérico (rojo #dc2626)
- [ ] Icono rojo con X
- [ ] Subtítulo: "Sin stock disponible"

**Tarjeta 4: Valor Inventario**
- [ ] Valor en formato "$X,XXX" (verde #059669)
- [ ] Icono verde con signo de dólar
- [ ] Subtítulo: "Valor total en stock"

**JavaScript**: Abrir consola del navegador (F12)
- [ ] No hay errores en consola
- [ ] Valores de KPIs se actualizan correctamente

#### **2.3 Filtros y Búsqueda**
- [ ] Card "Filtros de Búsqueda"
- [ ] Input de búsqueda con icono de lupa
- [ ] Select de categoría
- [ ] Select de estado de stock
- [ ] Botones "Aplicar Filtros" y "Limpiar"

#### **2.4 Productos (Lista de Tarjetas)**
- [ ] Productos en grid de 3 columnas
- [ ] Cada tarjeta tiene:
  - [ ] Header con nombre del producto
  - [ ] Precio y stock
  - [ ] Badge de estado (verde/amarillo/rojo)
  - [ ] Categoría con icono
  - [ ] Atributos (orgánico, vegano, sin TACC)
  - [ ] Botones "Editar" y "Eliminar"

**Hover**:
- [ ] Tarjetas tienen efecto de elevación al pasar mouse

---

### **3. Vista Compras** ⏱️ 10 min

**URL**: `http://127.0.0.1:8000/compras/lino/`

#### **3.1 Page Header**
- [ ] Título: "Gestión de Compras"
- [ ] Subtítulo: "Control de compras de materias primas..."
- [ ] Icono de camión 🚚
- [ ] Botón "Nueva Compra" (verde)

#### **3.2 KPIs (4 Tarjetas)**

**Tarjeta 1: Total Compras**
- [ ] Verde (#4a5c3a)
- [ ] Icono de camión
- [ ] Valor numérico

**Tarjeta 2: Total Invertido**
- [ ] Verde éxito (#059669)
- [ ] Icono de dólar
- [ ] Valor en formato "$X,XXX"

**Tarjeta 3: Este Mes**
- [ ] Amarillo (#f59e0b)
- [ ] Icono de calendario
- [ ] Valor numérico

**Tarjeta 4: Proveedores**
- [ ] Azul (#3b82f6)
- [ ] Icono de personas
- [ ] Valor numérico

#### **3.3 Búsqueda y Filtros**
- [ ] Container con fondo blanco
- [ ] Header: "Buscar y Filtrar" con icono de lupa
- [ ] Input de búsqueda grande
- [ ] Dropdown de filtros (materia prima, fechas)
- [ ] Botones "Buscar" y "Limpiar"

#### **3.4 Acciones Rápidas**
- [ ] Card "Acciones Rápidas" con icono de rayo
- [ ] Botón "Nueva Compra" (verde, grande)
- [ ] Botones secundarios (Reporte, Exportar)

#### **3.5 Tabla de Compras**
- [ ] Header: "Lista de Compras" con icono de lista
- [ ] Badge con cantidad total
- [ ] Tabla enterprise con:
  - [ ] Header verde (#4a5c3a)
  - [ ] Iconos en columnas
  - [ ] Hover en filas (fondo gris claro)
  - [ ] Badges de estado (HOY/RECIENTE/COMPLETADO)
  - [ ] Botones de acción (Ver/Editar/Eliminar)

#### **3.6 Panel de Estadísticas**
Dos cards en fila:

**Card 1: Resumen de Compras**
- [ ] "Hoy" y "Esta Semana" en grid 2 columnas
- [ ] Valores numéricos grandes

**Card 2: Inversión Mensual**
- [ ] "Este Mes" y "Promedio" en grid 2 columnas
- [ ] Valores con "$"

---

## 🎨 **4. Verificación de Estilos**

### **Paleta de Colores** (usar inspector del navegador)

**Verificar que los elementos usan estos colores**:

| Color | Hex | Uso |
|-------|-----|-----|
| Verde LINO | `#4a5c3a` | Primary, KPIs principales, headers |
| Verde Éxito | `#059669` | Valores positivos, iconos success |
| Rojo | `#dc2626` | Alertas, valores críticos |
| Amarillo | `#f59e0b` | Advertencias, stock crítico |
| Azul | `#3b82f6` | Info, proveedores |
| Fondo | `#fafaf9` | Background páginas |

### **Tipografía**
- [ ] Labels uppercase en KPIs
- [ ] Letter-spacing en labels
- [ ] Font-weight 700 en valores numéricos
- [ ] Subtítulos más pequeños y grises

### **Efectos Hover**
- [ ] KPIs: Barra superior verde aparece
- [ ] KPIs: Elevación sutil (transform: translateY(-2px))
- [ ] Tablas: Fila con fondo gris al pasar mouse
- [ ] Botones: Elevación y color más oscuro

---

## 📱 **5. Responsive Design**

**Probar en diferentes tamaños** (usar DevTools > Device Toolbar):

### **Desktop (>1200px)**
- [ ] KPIs en 4 columnas
- [ ] Tabla con todas las columnas visibles

### **Tablet (768px - 1200px)**
- [ ] KPIs en 2 columnas (2x2)
- [ ] Tabla con scroll horizontal si es necesario

### **Mobile (<768px)**
- [ ] KPIs en 1 columna
- [ ] Header responsive (botones apilados)
- [ ] Tabla con scroll horizontal

---

## 🐛 **6. Bugs Comunes a Verificar**

### **Login**
- [ ] Sin errores 404 en CSS
- [ ] Gradiente visible en header
- [ ] Inputs focusables con borde verde

### **Productos**
- [ ] KPIs muestran valores dinámicos (no "0" estáticos)
- [ ] JavaScript actualiza valores correctamente
- [ ] Modal de eliminación funciona

### **Compras**
- [ ] Total invertido muestra "$" y separador de miles
- [ ] Badges de estado con texto correcto
- [ ] Botones de acción funcionales

---

## ✅ **7. Checklist Final**

**Antes de reportar completado**:

- [ ] Login rediseñado funciona
- [ ] Logout con mensaje funciona
- [ ] Productos: 4 KPIs enterprise visibles
- [ ] Productos: Header homogéneo
- [ ] Compras: 4 KPIs enterprise visibles
- [ ] Compras: Tabla enterprise con hover
- [ ] Compras: Panel de estadísticas inferior
- [ ] Sin errores en consola del navegador
- [ ] Sin errores 404 en archivos CSS/JS
- [ ] Responsive funciona en mobile

---

## 📊 **8. Reporte de Bugs**

**Si encuentras problemas, documenta**:

```markdown
## Bug #X: [Descripción corta]

**Vista**: Productos / Compras / Login / Logout
**Navegador**: Chrome / Firefox / Safari
**Dispositivo**: Desktop / Mobile

**Pasos para reproducir**:
1. Ir a [URL]
2. Hacer [acción]
3. Observar [problema]

**Resultado esperado**: [...]
**Resultado actual**: [...]

**Screenshot**: [adjuntar si es posible]
```

---

## 🎯 **9. Criterios de Aceptación**

**Para considerar Fase 1 como APROBADA**:

- ✅ 100% de checks completados en Login/Logout
- ✅ 90%+ de checks completados en Productos
- ✅ 90%+ de checks completados en Compras
- ✅ Sin errores críticos en consola
- ✅ Responsive funciona en al menos 2 resoluciones

---

## 📞 **10. Contacto**

**Si necesitas ayuda**:
- Revisar: `/docs/implementation/REPORTE_FASE1_COMPLETADO.md`
- CSS: `/src/gestion/static/css/lino-enterprise-components.css`
- Views: `/src/gestion/views.py` (buscar `lista_productos_lino` y `lista_compras_lino`)

---

**Última actualización**: 30 Octubre 2025  
**Versión**: LINO V3.0 Testing Guide
