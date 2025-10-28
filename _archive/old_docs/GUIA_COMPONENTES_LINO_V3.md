# 📚 LINO DESIGN SYSTEM V3 - GUÍA DE COMPONENTES

## 🎨 **SISTEMA DE DISEÑO PROFESIONAL**

Esta guía documenta todos los componentes del LINO Design System V3, creado con enfoque de ingeniería senior para escalabilidad, mantenibilidad y consistencia visual.

---

## 🏗️ **ARQUITECTURA DEL SISTEMA**

### **Estructura Modular**
```
static/css/
├── lino-design-system.css    # Variables, utilidades base, layouts
├── lino-kpi-cards.css        # Componentes KPI especializados  
├── lino-forms.css            # Sistema completo de formularios
└── lino-tables.css           # Tablas avanzadas con sorting/pagination
```

### **Nomenclatura BEM Extendida**
- **Bloque**: `.lino-component`
- **Elemento**: `.lino-component__element`
- **Modificador**: `.lino-component--modifier`
- **Estado**: `.lino-component.is-active`

---

## 🎯 **1. KPI CARDS - DASHBOARD COMPONENTS**

### **Estructura Base**
```html
<div class="lino-kpi-card lino-kpi-card--success">
    <div class="lino-kpi-card__header">
        <h3 class="lino-kpi-card__title">Ingresos del Mes</h3>
        <div class="lino-kpi-card__icon">
            <i class="bi bi-cash-stack"></i>
        </div>
    </div>
    <div class="lino-kpi-card__content">
        <div class="lino-kpi-card__value">25,480</div>
        <div class="lino-kpi-card__currency">ARS $</div>
        <div class="lino-kpi-card__trend lino-kpi-card__trend--up">
            <i class="bi bi-arrow-up"></i>
            <span>+12%</span>
        </div>
    </div>
</div>
```

### **Variantes Disponibles**
- `lino-kpi-card--success` (verde)
- `lino-kpi-card--danger` (rojo)
- `lino-kpi-card--warning` (amarillo)
- `lino-kpi-card--info` (azul)
- `lino-kpi-card--primary` (oliva)

### **Estados**
- `lino-kpi-card--loading` (animación pulse)
- `lino-kpi-card--updated` (efecto highlight)

### **Grid Layout**
```html
<div class="lino-kpi-grid">
    <!-- KPI cards aquí -->
</div>
```

---

## 📝 **2. FORMS - SISTEMA DE FORMULARIOS**

### **Formulario Completo**
```html
<div class="lino-form">
    <div class="lino-form__header lino-form__header--primary">
        <h2 class="lino-form__title">
            <i class="bi bi-plus-circle"></i>
            Nuevo Producto
        </h2>
        <p class="lino-form__subtitle">Ingresa los datos del producto</p>
    </div>
    
    <div class="lino-form__body">
        <div class="lino-form-group">
            <label class="lino-label lino-label--required">Nombre</label>
            <input type="text" class="lino-input" required>
            <span class="lino-form-help">Ingresa el nombre completo</span>
        </div>
        
        <div class="lino-form-group--grid">
            <div class="lino-form-group">
                <label class="lino-label">Precio</label>
                <div class="lino-input-group">
                    <span class="lino-input-group__addon">$</span>
                    <input type="number" class="lino-input">
                </div>
            </div>
            
            <div class="lino-form-group">
                <label class="lino-label">Categoría</label>
                <select class="lino-input lino-select">
                    <option>Seleccionar...</option>
                </select>
            </div>
        </div>
    </div>
    
    <div class="lino-form__footer">
        <button class="lino-btn lino-btn--secondary">Cancelar</button>
        <button class="lino-btn lino-btn--primary">Guardar</button>
    </div>
</div>
```

### **Tipos de Input**
- `lino-input` - Input básico
- `lino-textarea` - Área de texto
- `lino-select` - Select con estilo custom
- `lino-checkbox` - Checkbox con label
- `lino-radio` - Radio button con label

### **Estados de Validación**
- `lino-input--error` - Campo con error
- `lino-input--success` - Campo válido
- `lino-form-error` - Mensaje de error
- `lino-form-success` - Mensaje de éxito

### **Layouts Especiales**
- `lino-form--inline` - Formulario en línea
- `lino-search-form` - Buscador con botón
- `lino-floating-label` - Labels flotantes

---

## 📊 **3. TABLES - SISTEMA DE TABLAS**

### **Tabla Completa con Funcionalidades**
```html
<div class="lino-table-container">
    <div class="lino-table-header">
        <h3 class="lino-table-title">Lista de Productos</h3>
        <div class="lino-table-controls">
            <div class="lino-table-search">
                <i class="bi bi-search lino-table-search__icon"></i>
                <input type="text" class="lino-table-search__input" placeholder="Buscar...">
            </div>
            <button class="lino-btn lino-btn--primary">
                <i class="bi bi-plus"></i> Nuevo
            </button>
        </div>
    </div>
    
    <div class="lino-table-responsive">
        <table class="lino-table lino-table--striped">
            <thead class="lino-table__header lino-table__header--primary">
                <tr>
                    <th class="sortable" data-sort="name">Nombre</th>
                    <th class="sortable" data-sort="price">Precio</th>
                    <th class="center">Stock</th>
                    <th class="center">Estado</th>
                    <th class="center">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Quinoa Orgánica</td>
                    <td class="currency">$2,500.00</td>
                    <td class="number">15</td>
                    <td class="center">
                        <span class="lino-table-badge lino-table-badge--success">Activo</span>
                    </td>
                    <td>
                        <div class="lino-table-actions">
                            <a href="#" class="lino-table-action lino-table-action--view">
                                <i class="bi bi-eye"></i>
                            </a>
                            <a href="#" class="lino-table-action lino-table-action--edit">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <a href="#" class="lino-table-action lino-table-action--delete">
                                <i class="bi bi-trash"></i>
                            </a>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="lino-table-pagination">
        <div class="lino-table-pagination__info">
            Mostrando 1-10 de 45 registros
        </div>
        <nav class="lino-table-pagination__controls">
            <ul class="lino-pagination">
                <li class="lino-pagination__item lino-pagination__item--disabled">
                    <span class="lino-pagination__link">←</span>
                </li>
                <li class="lino-pagination__item lino-pagination__item--active">
                    <span class="lino-pagination__link">1</span>
                </li>
                <li class="lino-pagination__item">
                    <a href="#" class="lino-pagination__link">2</a>
                </li>
                <li class="lino-pagination__item">
                    <a href="#" class="lino-pagination__link">→</a>
                </li>
            </ul>
        </nav>
    </div>
</div>
```

### **Variantes de Tabla**
- `lino-table--striped` - Filas alternadas
- `lino-table--bordered` - Con bordes
- `lino-table--compact` - Espaciado reducido
- `lino-table--cards` - Vista de tarjetas en móvil

### **Tipos de Celda**
- `number` - Números alineados a la derecha
- `currency` - Moneda con formato
- `center` - Centrado
- `positive` - Valores positivos (verde)
- `negative` - Valores negativos (rojo)

---

## 🚨 **4. ALERTS - SISTEMA DE ALERTAS**

### **Alert Básica**
```html
<div class="lino-alert lino-alert--warning">
    <div class="lino-alert__content">
        <i class="bi bi-exclamation-triangle-fill lino-alert__icon"></i>
        <div class="lino-alert__text">
            <strong>¡Atención!</strong> 5 productos sin stock crítico
        </div>
    </div>
</div>
```

### **Variantes**
- `lino-alert--success` - Éxito (verde)
- `lino-alert--danger` - Error (rojo)  
- `lino-alert--warning` - Advertencia (amarillo)
- `lino-alert--info` - Información (azul)

---

## 🎨 **5. SISTEMA DE VARIABLES CSS**

### **Colores Principales**
```css
--lino-primary: #8c9c6c;         /* Verde oliva principal */
--lino-olive: #8c9c6c;           /* Alias verde oliva */
--lino-orange: #ff7b25;          /* Naranja energético */
--lino-success: #28a745;         /* Verde éxito */
--lino-danger: #dc3545;          /* Rojo peligro */
--lino-warning: #ffc107;         /* Amarillo advertencia */
--lino-info: #17a2b8;           /* Azul información */
```

### **Espaciado Modular**
```css
--lino-spacing-xs: 0.25rem;     /* 4px */
--lino-spacing-sm: 0.5rem;      /* 8px */
--lino-spacing-md: 0.75rem;     /* 12px */
--lino-spacing-lg: 1rem;        /* 16px */
--lino-spacing-xl: 1.25rem;     /* 20px */
--lino-spacing-2xl: 1.5rem;     /* 24px */
```

### **Tipografía**
```css
--lino-font-family-primary: 'Inter', sans-serif;
--lino-text-xs: 0.75rem;        /* 12px */
--lino-text-sm: 0.875rem;       /* 14px */
--lino-text-base: 1rem;         /* 16px */
--lino-text-lg: 1.125rem;       /* 18px */
--lino-text-xl: 1.25rem;        /* 20px */
```

---

## 📱 **6. RESPONSIVE DESIGN**

### **Breakpoints**
```css
--lino-bp-sm: 640px;    /* Móvil grande */
--lino-bp-md: 768px;    /* Tablet */
--lino-bp-lg: 1024px;   /* Desktop */
--lino-bp-xl: 1280px;   /* Desktop grande */
```

### **Grid KPI Automático**
```css
.lino-kpi-grid {
    display: grid;
    gap: var(--lino-spacing-lg);
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

---

## ♿ **7. ACCESIBILIDAD**

### **Focus States**
- Todos los componentes interactivos tienen estados de focus visibles
- Contraste optimizado para WCAG 2.1 AA
- Soporte para `prefers-reduced-motion`

### **Navegación por Teclado**
```css
.lino-btn:focus,
.lino-input:focus {
    outline: 2px solid var(--lino-primary);
    outline-offset: 2px;
}
```

---

## 🔧 **8. IMPLEMENTACIÓN**

### **Inclusión en Templates**
```html
<!-- En base.html -->
<link rel="stylesheet" href="{% static 'css/lino-design-system.css' %}">
<link rel="stylesheet" href="{% static 'css/lino-kpi-cards.css' %}">
<link rel="stylesheet" href="{% static 'css/lino-forms.css' %}">
<link rel="stylesheet" href="{% static 'css/lino-tables.css' %}">
```

### **Orden de Carga Recomendado**
1. **lino-design-system.css** - Base y variables
2. **lino-kpi-cards.css** - Componentes KPI
3. **lino-forms.css** - Sistema de formularios
4. **lino-tables.css** - Sistema de tablas
5. **CSS Legacy** - Para compatibilidad temporal

---

## 📊 **9. MÉTRICAS Y PERFORMANCE**

### **Tamaños de Archivos**
- `lino-design-system.css`: ~20KB (variables + base)
- `lino-kpi-cards.css`: ~9KB (componentes KPI)
- `lino-forms.css`: ~15KB (formularios completos)
- `lino-tables.css`: ~12KB (tablas avanzadas)
- **Total**: ~56KB (comprimido: ~8KB)

### **Compatibilidad**
- ✅ **Chrome/Edge 88+**
- ✅ **Firefox 85+** 
- ✅ **Safari 14+**
- ✅ **CSS Custom Properties requeridas**

---

## 🚀 **10. PRÓXIMAS ITERACIONES**

### **Componentes Pendientes**
1. **Modales** - Sistema de ventanas modales
2. **Tooltips** - Información contextual
3. **Calendarios** - Selección de fechas
4. **Gráficos** - Integración con Chart.js
5. **Navegación** - Breadcrumbs y menús

### **Optimizaciones**
1. **Tree-shaking** - Carga selectiva de componentes
2. **CSS-in-JS** - Para aplicaciones React futuras
3. **Dark Mode** - Tema oscuro completo
4. **Animaciones** - Micro-interacciones avanzadas

---

## 💡 **CONSEJOS DE IMPLEMENTACIÓN**

### **Para Desarrolladores**
1. **Usa variables CSS** para cambios globales rápidos
2. **Mantén la nomenclatura BEM** para consistencia
3. **Testa en móvil** desde el primer momento
4. **Aprovecha los modificadores** para variaciones

### **Para Diseñadores**
1. **Sistema de 8px** para espaciado consistente
2. **Palette limitada** para coherencia visual
3. **Estados claros** para cada componente
4. **Feedback visual** en todas las interacciones

---

## 🎉 **CONCLUSIÓN**

El **LINO Design System V3** proporciona una base sólida y escalable para el frontend de LINO Saludable, con componentes profesionales, accesibles y fáciles de mantener.

**¡El sistema está listo para escalar y evolucionar!** 🚀

---

*Documentación generada para LINO Design System V3*  
*Versión: 3.0 | Fecha: Octubre 2025*
