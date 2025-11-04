# 🎨 LINO CSS - Arquitectura y Guía de Uso

**Versión:** 3.0 Consolidada  
**Última actualización:** 29 de octubre de 2025  
**Autor:** Sistema LINO Saludable

---

## 📚 Tabla de Contenidos

1. [Estructura de Archivos](#estructura-de-archivos)
2. [Orden de Carga](#orden-de-carga)
3. [Sistema de Variables](#sistema-de-variables)
4. [Componentes Disponibles](#componentes-disponibles)
5. [Convenciones de Naming](#convenciones-de-naming)
6. [Guía de Uso](#guía-de-uso)
7. [Cómo Extender](#cómo-extender)

---

## 📁 Estructura de Archivos

```
src/static/css/
├── lino-main.css              ⭐ CSS PRINCIPAL (110KB, 5186 líneas)
│   ├── Variables globales     (colores, espaciado, tipografía)
│   ├── Layout general         (sidebar, header, content area)
│   ├── Componentes base       (botones, cards, forms, tablas)
│   ├── Componentes avanzados  (KPIs, gráficos, wizards básicos)
│   ├── Utilities              (spacing, display, text)
│   └── Responsive             (breakpoints móvil/tablet/desktop)
│
└── lino-wizard-ventas.css     🎯 CSS ESPECÍFICO (10KB, 526 líneas)
    └── Solo para formulario wizard de creación de ventas
```

### 🚫 **Archivos Eliminados (Duplicados)**

- ❌ `lino-design-tokens.css` → Consolidado en `lino-main.css`
- ❌ `lino-components.css` → Consolidado en `lino-main.css`
- ❌ `lino-dietetica-v3.css` → Renombrado a `lino-main.css`

---

## 🔗 Orden de Carga

### **Base HTML (base.html)**

```html
<!-- 1. Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- 2. Bootstrap CSS (base framework) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

<!-- 3. LINO MAIN CSS (sistema de diseño completo) -->
<link rel="stylesheet" href="{% static 'css/lino-main.css' %}?v=20241029">

<!-- 4. Chart.js (gráficos) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### **Templates Específicos (form_v3_natural.html, etc.)**

```html
{% block extra_head %}
<!-- CSS específico SOLO cuando sea necesario -->
<link rel="stylesheet" href="{% static 'css/lino-wizard-ventas.css' %}?v=20241029">
{% endblock %}
```

**⚠️ REGLA:** Solo agregar CSS específico si el componente NO puede reutilizar clases de `lino-main.css`

---

## 🎨 Sistema de Variables

### **Colores Principales (Verde Oliva Natural)**

Basados en el logo oficial de LINO Dietética:

```css
:root {
    /* PALETA PRINCIPAL */
    --lino-primary: #4a5c3a;      /* 🌿 Verde oliva del logo */
    --lino-secondary: #e8e4d4;    /* 🏜️ Beige crema del fondo */
    --lino-accent: #8b9471;       /* 🍃 Verde sage natural */
    --lino-dark: #3d4a2f;         /* 🌲 Verde oliva profundo */
    --lino-light: #f2efea;        /* ☁️ Crema muy claro */
    
    /* COLORES FUNCIONALES */
    --lino-success: #7fb069;      /* ✅ Verde éxito */
    --lino-warning: #d4a574;      /* ⚠️ Naranja cálido */
    --lino-danger: #c85a54;       /* ❌ Rojo suave */
    --lino-info: #6b9dc7;         /* ℹ️ Azul información */
    
    /* GRISES COMPLEMENTARIOS (10 tonos) */
    --lino-gray-50: #fafaf9;      /* Casi blanco */
    --lino-gray-100: #f5f4f0;
    --lino-gray-200: #e8e6df;
    --lino-gray-300: #d1d5db;
    --lino-gray-400: #9ca3af;
    --lino-gray-500: #6b7280;
    --lino-gray-600: #6b7280;
    --lino-gray-700: #4b5563;
    --lino-gray-800: #374151;
    --lino-gray-900: #1f2937;     /* Casi negro */
}
```

### **Espaciado (Sistema de 8px)**

```css
:root {
    --lino-space-1: 0.25rem;     /* 4px */
    --lino-space-2: 0.5rem;      /* 8px */
    --lino-space-3: 0.75rem;     /* 12px */
    --lino-space-4: 1rem;        /* 16px */
    --lino-space-5: 1.25rem;     /* 20px */
    --lino-space-6: 1.5rem;      /* 24px */
    --lino-space-8: 2rem;        /* 32px */
    --lino-space-10: 2.5rem;     /* 40px */
    --lino-space-12: 3rem;       /* 48px */
}
```

### **Tipografía**

```css
:root {
    --lino-font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    
    /* Pesos */
    --lino-font-light: 300;
    --lino-font-normal: 400;
    --lino-font-medium: 500;
    --lino-font-semibold: 600;
    --lino-font-bold: 700;
    
    /* Tamaños */
    --lino-text-xs: 0.75rem;     /* 12px */
    --lino-text-sm: 0.875rem;    /* 14px */
    --lino-text-base: 1rem;      /* 16px */
    --lino-text-lg: 1.125rem;    /* 18px */
    --lino-text-xl: 1.25rem;     /* 20px */
    --lino-text-2xl: 1.5rem;     /* 24px */
    --lino-text-3xl: 1.875rem;   /* 30px */
    --lino-text-4xl: 2.25rem;    /* 36px */
}
```

### **Sombras (Basadas en Verde Oliva)**

```css
:root {
    --lino-shadow-sm: 0 1px 2px rgba(74, 92, 58, 0.1);
    --lino-shadow: 0 4px 6px rgba(74, 92, 58, 0.15);
    --lino-shadow-lg: 0 10px 15px rgba(74, 92, 58, 0.2);
}
```

### **Border Radius**

```css
:root {
    --lino-radius-sm: 6px;
    --lino-radius-md: 8px;
    --lino-radius-lg: 12px;
    --lino-radius-xl: 16px;
    --lino-radius-full: 9999px;
}
```

### **Transiciones**

```css
:root {
    --lino-transition-base: all 0.2s ease;
    --lino-transition-slow: all 0.3s ease;
}
```

---

## 🧩 Componentes Disponibles

### **1. Sistema de Botones**

#### Variantes de Color

```html
<!-- Primario (verde oliva) -->
<button class="lino-btn lino-btn-primary">Guardar</button>

<!-- Success (verde éxito) -->
<button class="lino-btn lino-btn-success">Aprobar</button>

<!-- Warning (naranja) -->
<button class="lino-btn lino-btn-warning">Advertir</button>

<!-- Danger (rojo) -->
<button class="lino-btn lino-btn-danger">Eliminar</button>

<!-- Ghost (transparente con borde) -->
<button class="lino-btn lino-btn-ghost">Cancelar</button>

<!-- Outline -->
<button class="lino-btn lino-btn-outline-primary">Ver más</button>
```

#### Tamaños

```html
<button class="lino-btn lino-btn-sm">Pequeño</button>
<button class="lino-btn">Normal</button>
<button class="lino-btn lino-btn-lg">Grande</button>
```

#### Con Iconos

```html
<button class="lino-btn lino-btn-primary">
    <i class="bi bi-plus-circle"></i> Agregar
</button>
```

---

### **2. Cards y Contenedores**

```html
<!-- Card básica -->
<div class="lino-card">
    <div class="lino-card-header">
        <h3 class="lino-card-title">Título</h3>
        <span class="lino-card-badge">Nuevo</span>
    </div>
    <div class="lino-card-body">
        Contenido de la card
    </div>
    <div class="lino-card-footer">
        <button class="lino-btn lino-btn-primary">Acción</button>
    </div>
</div>

<!-- Card con estadísticas -->
<div class="lino-stat-card">
    <div class="lino-stat-value">$12,450</div>
    <div class="lino-stat-label">Ventas del Mes</div>
    <div class="lino-stat-change lino-stat-change--positive">+12%</div>
</div>
```

---

### **3. Formularios**

```html
<!-- Grupo de formulario (NO superposición) -->
<div class="lino-form-group">
    <label class="lino-label lino-label-required">Nombre del Cliente</label>
    <input type="text" class="lino-input" placeholder="Ej: Juan Pérez">
    <small class="lino-helper-text">
        <i class="bi bi-info-circle"></i>
        Puede ser nombre completo o empresa
    </small>
</div>

<!-- Select -->
<div class="lino-form-group">
    <label class="lino-label">Producto</label>
    <select class="lino-select">
        <option value="">Seleccione...</option>
        <option value="1">Producto 1</option>
    </select>
</div>

<!-- Textarea -->
<div class="lino-form-group">
    <label class="lino-label">Observaciones</label>
    <textarea class="lino-textarea" rows="4"></textarea>
</div>

<!-- Estados especiales -->
<input type="text" class="lino-input lino-input-readonly" readonly>
<input type="text" class="lino-input lino-input-error">
<input type="text" class="lino-input lino-input-success">
```

---

### **4. Tablas**

```html
<table class="lino-table lino-table--striped lino-table--hover">
    <thead>
        <tr>
            <th>Producto</th>
            <th>Stock</th>
            <th>Precio</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Granola Orgánica</td>
            <td><span class="lino-badge lino-badge-warning">Bajo</span></td>
            <td>$450.00</td>
            <td>
                <button class="lino-btn lino-btn-sm lino-btn-ghost">
                    <i class="bi bi-eye"></i>
                </button>
            </td>
        </tr>
    </tbody>
</table>
```

---

### **5. Badges y Pills**

```html
<!-- Badges de estado -->
<span class="lino-badge lino-badge-success">Activo</span>
<span class="lino-badge lino-badge-warning">Pendiente</span>
<span class="lino-badge lino-badge-danger">Vencido</span>
<span class="lino-badge lino-badge-info">Nuevo</span>

<!-- Pills con contador -->
<span class="lino-pill">Productos <span class="lino-pill-count">24</span></span>
```

---

### **6. Breadcrumbs**

```html
<nav class="lino-breadcrumb">
    <a href="#" class="lino-breadcrumb-item">
        <i class="bi bi-house"></i> Dashboard
    </a>
    <span class="lino-breadcrumb-separator">/</span>
    <a href="#" class="lino-breadcrumb-item">Productos</a>
    <span class="lino-breadcrumb-separator">/</span>
    <span class="lino-breadcrumb-item--active">Crear Producto</span>
</nav>
```

---

### **7. Alertas y Notificaciones**

```html
<!-- Alertas -->
<div class="lino-alert lino-alert-success">
    <i class="bi bi-check-circle"></i>
    <span>Producto guardado exitosamente</span>
</div>

<div class="lino-alert lino-alert-warning">
    <i class="bi bi-exclamation-triangle"></i>
    <span>Stock bajo detectado</span>
</div>

<div class="lino-alert lino-alert-danger">
    <i class="bi bi-x-circle"></i>
    <span>Error al procesar la operación</span>
</div>
```

---

### **8. Empty States**

```html
<div class="lino-empty-state">
    <i class="bi bi-inbox lino-empty-state__icon"></i>
    <h4 class="lino-empty-state__title">No hay productos</h4>
    <p class="lino-empty-state__text">
        Comience agregando productos con el botón de arriba
    </p>
    <button class="lino-btn lino-btn-primary">
        <i class="bi bi-plus-circle"></i> Agregar Producto
    </button>
</div>
```

---

## 🏷️ Convenciones de Naming

### **Prefijo `.lino-`**

Todas las clases del sistema LINO usan el prefijo `.lino-` para evitar conflictos con Bootstrap:

```css
/* ✅ CORRECTO */
.lino-btn { }
.lino-card { }
.lino-table { }

/* ❌ INCORRECTO (puede chocar con Bootstrap) */
.btn { }
.card { }
.table { }
```

### **BEM Simplificado**

Usamos una variante simplificada de BEM:

```html
<!-- Bloque -->
<div class="lino-card">
    
    <!-- Elemento (usa __) -->
    <div class="lino-card__header">
        <h3 class="lino-card__title">Título</h3>
    </div>
    
    <!-- Modificador (usa --) -->
    <div class="lino-card lino-card--highlighted">
        Contenido destacado
    </div>
</div>
```

### **Estados**

```css
/* Hover, focus, active */
.lino-btn:hover { }
.lino-input:focus { }
.lino-link--active { }

/* Estados condicionales */
.lino-badge--success { }
.lino-alert--warning { }
.lino-table--striped { }
```

---

## 📖 Guía de Uso

### **Caso 1: Crear Formulario Nuevo**

```html
<form method="post">
    {% csrf_token %}
    
    <div class="lino-card">
        <div class="lino-card-header">
            <h3 class="lino-card-title">Nuevo Producto</h3>
        </div>
        <div class="lino-card-body">
            
            <div class="lino-form-group">
                <label class="lino-label lino-label-required">Nombre</label>
                <input type="text" name="nombre" class="lino-input" required>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="lino-form-group">
                        <label class="lino-label">Precio</label>
                        <input type="number" name="precio" class="lino-input" step="0.01">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="lino-form-group">
                        <label class="lino-label">Stock</label>
                        <input type="number" name="stock" class="lino-input">
                    </div>
                </div>
            </div>
            
        </div>
        <div class="lino-card-footer">
            <a href="{% url 'lista' %}" class="lino-btn lino-btn-ghost">Cancelar</a>
            <button type="submit" class="lino-btn lino-btn-primary">Guardar</button>
        </div>
    </div>
</form>
```

### **Caso 2: Mostrar Lista con Tabla**

```html
<div class="lino-card">
    <div class="lino-card-header">
        <h3 class="lino-card-title">Productos</h3>
        <a href="{% url 'crear' %}" class="lino-btn lino-btn-primary lino-btn-sm">
            <i class="bi bi-plus-circle"></i> Nuevo
        </a>
    </div>
    <div class="lino-card-body">
        
        {% if productos %}
        <table class="lino-table lino-table--striped lino-table--hover">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Stock</th>
                    <th>Precio</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for producto in productos %}
                <tr>
                    <td><strong>{{ producto.nombre }}</strong></td>
                    <td>{{ producto.stock }}</td>
                    <td>${{ producto.precio }}</td>
                    <td>
                        {% if producto.activo %}
                        <span class="lino-badge lino-badge-success">Activo</span>
                        {% else %}
                        <span class="lino-badge lino-badge-danger">Inactivo</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="{% url 'detalle' producto.id %}" class="lino-btn lino-btn-sm lino-btn-ghost">
                            <i class="bi bi-eye"></i>
                        </a>
                        <a href="{% url 'editar' producto.id %}" class="lino-btn lino-btn-sm lino-btn-ghost">
                            <i class="bi bi-pencil"></i>
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="lino-empty-state">
            <i class="bi bi-inbox lino-empty-state__icon"></i>
            <h4 class="lino-empty-state__title">No hay productos</h4>
        </div>
        {% endif %}
        
    </div>
</div>
```

### **Caso 3: Dashboard con KPIs**

```html
<div class="row mb-4">
    <div class="col-md-3">
        <div class="lino-stat-card">
            <div class="lino-stat-value">${{ total_ventas }}</div>
            <div class="lino-stat-label">Ventas del Mes</div>
            <div class="lino-stat-change lino-stat-change--positive">+12%</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="lino-stat-card">
            <div class="lino-stat-value">{{ productos_vendidos }}</div>
            <div class="lino-stat-label">Productos Vendidos</div>
            <div class="lino-stat-change lino-stat-change--negative">-3%</div>
        </div>
    </div>
    <!-- Más KPIs... -->
</div>
```

---

## 🚀 Cómo Extender el Sistema

### **1. Agregar Nueva Variante de Botón**

Si necesitas un botón especial (ej: botón de WhatsApp):

```css
/* Agregar al final de lino-main.css */
.lino-btn-whatsapp {
    background: #25d366;
    color: white;
    border-color: #25d366;
}

.lino-btn-whatsapp:hover {
    background: #1da851;
    border-color: #1da851;
    color: white;
}
```

### **2. Crear Componente Específico**

Si el componente es MUY específico de una vista (como wizard-ventas):

```css
/* Crear archivo: lino-mi-componente.css */

.lino-mi-componente {
    /* Usar variables de lino-main.css */
    background: var(--lino-primary);
    border-radius: var(--lino-radius-md);
    padding: var(--lino-space-4);
}
```

Cargarlo solo en el template que lo necesita:

```html
{% block extra_head %}
<link rel="stylesheet" href="{% static 'css/lino-mi-componente.css' %}">
{% endblock %}
```

### **3. Overrides Específicos**

Para pequeños ajustes en una vista:

```html
{% block extra_head %}
<style>
    /* Ajustes específicos para esta vista */
    .lino-card {
        max-width: 800px;
        margin: 0 auto;
    }
</style>
{% endblock %}
```

---

## ⚠️ Reglas de Oro

### **1. SIEMPRE usar variables CSS**

```css
/* ✅ CORRECTO */
.mi-componente {
    color: var(--lino-primary);
    padding: var(--lino-space-4);
}

/* ❌ INCORRECTO */
.mi-componente {
    color: #4a5c3a;  /* Hardcoded */
    padding: 16px;   /* Hardcoded */
}
```

### **2. NO sobrescribir Bootstrap directamente**

```css
/* ❌ INCORRECTO - Afecta a todo Bootstrap */
.btn {
    background: var(--lino-primary);
}

/* ✅ CORRECTO - Crea tu propia clase */
.lino-btn {
    background: var(--lino-primary);
}
```

### **3. Mantener el prefijo `.lino-`**

Todas las clases personalizadas deben usar el prefijo para evitar conflictos.

### **4. Respetar el sistema de espaciado**

Usa múltiplos de 4px (var(--lino-space-*)) para consistencia visual.

### **5. Documentar componentes nuevos**

Si agregas un componente importante, documéntalo en este archivo.

---

## 🛠️ Debugging y Troubleshooting

### **Problema: Los estilos no se aplican**

```html
<!-- ✅ Solución: Verificar orden de carga -->
<!-- lino-main.css DEBE estar después de Bootstrap -->

<link rel="stylesheet" href="bootstrap.min.css">
<link rel="stylesheet" href="{% static 'css/lino-main.css' %}">
```

### **Problema: Colores inconsistentes**

```css
/* ❌ NO crear nuevas variables de color */
:root {
    --mi-verde: #5a7c4a; /* EVITAR */
}

/* ✅ Usar las existentes */
.mi-clase {
    background: var(--lino-primary);   /* O var(--lino-accent) */
}
```

### **Problema: Cache del navegador**

```html
<!-- Agregar versión query param -->
<link rel="stylesheet" href="{% static 'css/lino-main.css' %}?v=20241029">

<!-- O forzar recarga: Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows) -->
```

---

## 📚 Recursos Adicionales

- **Paleta de colores oficial:** Ver variables en `lino-main.css` líneas 1-35
- **Componentes visuales:** Ver `LINO_ANALISIS_COMPLETO_CONSISTENCIA_VISUAL.md`
- **Bootstrap Icons:** https://icons.getbootstrap.com/
- **Chart.js:** https://www.chartjs.org/docs/latest/

---

## 🎯 Próximos Pasos

1. **Crear biblioteca visual de componentes** (HTML estático mostrando todos)
2. **Testing cross-browser** (Chrome, Firefox, Safari)
3. **Optimización de performance** (minificar CSS en producción)
4. **Tema oscuro** (modo dark opcional)

---

**📝 Última actualización:** 29 de octubre de 2025  
**📧 Soporte:** Sistema LINO Saludable  
**🌿 Versión:** 3.0 - Consolidada y Normalizada
