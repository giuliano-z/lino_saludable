from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()

# ===== FILTROS EXISTENTES =====
@register.filter
def get_color_atributo(producto, atributo):
    """Template filter para obtener el color de un atributo dietético."""
    return producto.get_color_atributo(atributo)

@register.filter  
def split(value, delimiter=','):
    """Template filter para dividir strings."""
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []

@register.filter
def attr_display_name(attr):
    """Template filter para mostrar nombres amigables de atributos."""
    names = {
        'organico': 'Orgánico',
        'vegano': 'Vegano', 
        'sin_tacc': 'Sin TACC',
        'sin_azucar': 'Sin Azúcar',
        'integral': 'Integral',
        'natural': 'Natural',
    }
    return names.get(attr, attr.title())

@register.filter
def add_class(field, css_class):
    """Template filter para agregar clases CSS a campos de formulario."""
    try:
        # Si ya tiene la clase widget, agregar la nueva clase
        existing_classes = field.field.widget.attrs.get('class', '')
        if existing_classes:
            new_classes = f"{existing_classes} {css_class}"
        else:
            new_classes = css_class
            
        field.field.widget.attrs['class'] = new_classes
        return field
    except AttributeError:
        return field

@register.filter
def total_cantidad(detalles):
    """Template filter para calcular la cantidad total de productos vendidos."""
    try:
        return sum(detalle.cantidad for detalle in detalles)
    except:
        return 0

# ===== NUEVO SISTEMA LINO COMPONENTS =====

@register.inclusion_tag('components/lino_kpi_card.html')
def lino_kpi_card(title, value, label, icon="bi-circle", color="olive", extra_class=""):
    """
    Renderiza una tarjeta KPI usando el sistema Lino
    
    Uso: {% lino_kpi_card "Stock Actual" "125" "Kilogramos" "bi-boxes" "green" %}
    """
    return {
        'title': title,
        'value': value,
        'label': label,
        'icon': icon,
        'color': color,
        'extra_class': extra_class,
    }

@register.inclusion_tag('components/lino_card_header.html')
def lino_card_header(title, icon="bi-info-circle", color="olive", actions=None):
    """
    Renderiza un header de card consistente
    
    Uso: {% lino_card_header "Información General" "bi-info-circle" "olive" %}
    """
    return {
        'title': title,
        'icon': icon,
        'color': color,
        'actions': actions or [],
    }

@register.inclusion_tag('components/lino_button.html')
def lino_btn(text, url="#", style="primary", size="md", icon="", extra_class="", target=""):
    """
    Renderiza un botón usando el sistema Lino
    
    Uso: {% lino_btn "Editar" "/editar/" "primary" "md" "bi-pencil" %}
    """
    return {
        'text': text,
        'url': url,
        'style': style,
        'size': size,
        'icon': icon,
        'extra_class': extra_class,
        'target': target,
    }

@register.inclusion_tag('components/lino_info_section.html')
def lino_info_section(title, icon="bi-info-circle", color="olive"):
    """
    Renderiza una sección de información con el estilo Lino
    
    Uso: {% lino_info_section "Identificación" "bi-tag" "primary" %}
    """
    return {
        'title': title,
        'icon': icon,
        'color': color,
    }

@register.inclusion_tag('components/lino_value_box.html')
def lino_value_box(value, label, color="primary", size="md"):
    """
    Renderiza una caja de valor destacado
    
    Uso: {% lino_value_box "$3500.00" "Costo Unitario" "success" "lg" %}
    """
    return {
        'value': value,
        'label': label,
        'color': color,
        'size': size,
    }

@register.inclusion_tag('components/lino_badge.html')
def lino_badge(text, type="olive", size="md", icon=""):
    """
    Renderiza un badge con el sistema Lino
    
    Uso: {% lino_badge "Stock Normal" "success" "lg" "bi-check-circle" %}
    """
    return {
        'text': text,
        'type': type,
        'size': size,
        'icon': icon,
    }

@register.simple_tag
def lino_icon(name, color="", size="", extra_class=""):
    """
    Renderiza un icono con clases consistentes
    
    Uso: {% lino_icon "bi-boxes" "text-primary" "fs-4" %}
    """
    classes = ['bi', name]
    if color:
        classes.append(color)
    if size:
        classes.append(size)
    if extra_class:
        classes.append(extra_class)
    
    return format_html('<i class="{}"></i>', ' '.join(classes))

@register.filter
def lino_color_class(color_name):
    """
    Convierte nombres de colores Lino a clases CSS
    
    Uso: {{ "olive"|lino_color_class }}
    """
    color_map = {
        'olive': 'lino-card-header--olive',
        'green': 'lino-card-header--green', 
        'brown': 'lino-card-header--brown',
        'earth': 'lino-card-header--earth',
        'success': 'lino-card-header--success',
        'primary': 'lino-card-header--olive',  # Default
    }
    return color_map.get(color_name, 'lino-card-header--olive')

@register.filter
def lino_btn_class(style):
    """
    Convierte estilos de botón a clases Lino
    
    Uso: {{ "primary"|lino_btn_class }}
    """
    style_map = {
        'primary': 'lino-btn--primary',
        'success': 'lino-btn--success',
        'warning': 'lino-btn--warning',
        'danger': 'lino-btn--danger',
        'outline': 'lino-btn--outline',
    }
    return style_map.get(style, 'lino-btn--primary')

@register.filter
def lino_size_class(size, component='btn'):
    """
    Convierte tamaños a clases Lino
    
    Uso: {{ "lg"|lino_size_class:"btn" }}
    """
    if component == 'btn':
        size_map = {
            'sm': 'lino-btn--sm',
            'md': '',
            'lg': 'lino-btn--lg',
        }
    elif component == 'badge':
        size_map = {
            'sm': '',
            'md': '',
            'lg': 'lino-badge--lg',
        }
    else:
        return ''
    
    return size_map.get(size, '')

@register.filter
def money_format(value):
    """Template filter para formatear moneda."""
    try:
        if value is None:
            return "$0"
        return f"${float(value):,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return "$0"

@register.inclusion_tag('components/lino_actions_panel.html')
def lino_actions_panel(actions=None, title="Acciones Rápidas", size="compact"):
    """
    Renderiza un panel de acciones rápidas reutilizable
    
    Uso: 
    {% lino_actions_panel actions title="Acciones Rápidas" size="compact" %}
    
    Donde actions es una lista de diccionarios con:
    - text: Texto del botón
    - url: URL de destino  
    - icon: Icono Bootstrap
    - color: Color del botón (success, orange, olive)
    """
    default_actions = [
        {
            'text': 'Nueva Venta',
            'url': 'gestion:crear_venta',
            'icon': 'bi-plus-circle',
            'color': 'success'
        },
        {
            'text': 'Agregar Producto', 
            'url': 'gestion:crear_producto',
            'icon': 'bi-box',
            'color': 'orange'
        },
        {
            'text': 'Generar Reporte',
            'url': 'gestion:reportes', 
            'icon': 'bi-graph-up',
            'color': 'olive'
        }
    ]
    
    return {
        'actions': actions or default_actions,
        'title': title,
        'size': size,
    }

@register.inclusion_tag('components/lino_search_panel.html')
def lino_search_panel(title="Panel de Control", search_placeholder="Buscar...", 
                     show_select_filter=False, select_options=None, 
                     select_name="categoria", select_placeholder="Todas las categorías",
                     quick_filters=None):
    """
    Componente de búsqueda reutilizable estilo dashboard
    
    Uso: {% lino_search_panel "Panel de Control" "Buscar productos..." True proveedores "proveedor" "Todos los proveedores" filtros_rapidos %}
    """
    return {
        'title': title,
        'search_placeholder': search_placeholder,
        'show_select_filter': show_select_filter,
        'select_options': select_options or [],
        'select_name': select_name,
        'select_placeholder': select_placeholder,
        'quick_filters': quick_filters or [],
    }
