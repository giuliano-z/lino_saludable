"""
LINO V3 - KPI Builder Utilities
Construcción consistente de KPIs para todos los módulos
"""

from django.db.models import Sum, Count, F, Q
from decimal import Decimal


def build_kpi(icon, badge, label, value, variant='info', 
              trend_icon=None, trend_text=None, trend_variant='info'):
    """
    Construir estructura KPI consistente para todos los módulos
    
    Args:
        icon (str): Icono Bootstrap (sin 'bi bi-')
        badge (str): Texto del badge superior
        label (str): Etiqueta del KPI con emoji
        value (str/int): Valor a mostrar
        variant (str): Color (success, danger, warning, info, primary, inventario)
        trend_icon (str): Icono de tendencia (opcional)
        trend_text (str): Texto de tendencia (opcional)
        trend_variant (str): Color de tendencia
    
    Returns:
        dict: Estructura KPI lista para template
    
    Example:
        >>> build_kpi('box-seam', 'Total Productos', '📦 Productos', 150, 'success')
        {
            'icon': 'box-seam',
            'badge': 'Total Productos',
            'label': '📦 Productos',
            'value': 150,
            'variant': 'success',
            ...
        }
    """
    return {
        'icon': icon,
        'badge': badge,
        'label': label,
        'value': value,
        'variant': variant,
        'trend_icon': trend_icon or 'check-circle',
        'trend_text': trend_text or 'Activo',
        'trend_variant': trend_variant
    }


def prepare_product_kpis(productos_queryset):
    """
    Preparar KPIs específicos para módulo de Productos
    
    Args:
        productos_queryset: QuerySet de Producto
        
    Returns:
        list: Lista de 4 KPIs formateados
    """
    total = productos_queryset.count()
    en_stock = productos_queryset.filter(stock_actual__gt=0).count()
    bajo_stock = productos_queryset.filter(
        stock_actual__gt=0,
        stock_actual__lte=F('stock_minimo')
    ).count()
    sin_stock = productos_queryset.filter(stock_actual=0).count()
    
    # Valor total del inventario
    valor_total = productos_queryset.aggregate(
        total=Sum(F('stock_actual') * F('precio_costo'))
    )['total'] or Decimal('0')
    
    return [
        build_kpi(
            icon='box-seam',
            badge='Total Productos',
            label='📦 Productos',
            value=total,
            variant='success',
            trend_icon='check-circle',
            trend_text='Activos',
            trend_variant='success'
        ),
        build_kpi(
            icon='boxes',
            badge='Con Stock',
            label='✅ Disponibles',
            value=en_stock,
            variant='info',
            trend_icon='check',
            trend_text='En stock',
            trend_variant='info'
        ),
        build_kpi(
            icon='exclamation-triangle',
            badge='Stock Bajo',
            label='⚠️ Críticos',
            value=bajo_stock,
            variant='warning',
            trend_icon='exclamation-triangle',
            trend_text='Reponer',
            trend_variant='warning'
        ),
        build_kpi(
            icon='cash-stack',
            badge='Valor Total',
            label='💰 Inventario',
            value=f"${float(valor_total):,.0f}",
            variant='inventario',
            trend_icon='graph-up',
            trend_text='Valorizado',
            trend_variant='success'
        )
    ]


def prepare_ventas_kpis(ventas_queryset, periodo='mes'):
    """
    Preparar KPIs específicos para módulo de Ventas
    
    Args:
        ventas_queryset: QuerySet de Venta
        periodo (str): 'mes', 'semana', 'dia'
        
    Returns:
        list: Lista de 4 KPIs formateados
    """
    total_ventas = ventas_queryset.count()
    ingresos = ventas_queryset.aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Ticket promedio
    ticket_promedio = float(ingresos) / total_ventas if total_ventas > 0 else 0
    
    # Producto más vendido (requiere DetalleVenta)
    from gestion.models import DetalleVenta
    producto_top = DetalleVenta.objects.filter(
        venta__in=ventas_queryset
    ).values('producto__nombre').annotate(
        total=Sum('cantidad')
    ).order_by('-total').first()
    
    producto_top_nombre = producto_top['producto__nombre'] if producto_top else 'N/A'
    producto_top_cantidad = producto_top['total'] if producto_top else 0
    
    return [
        build_kpi(
            icon='cash-coin',
            badge='Ingresos del Mes',
            label='💵 Ventas',
            value=f"${float(ingresos):,.0f}",
            variant='success',
            trend_icon='arrow-up',
            trend_text='Ingresos',
            trend_variant='success'
        ),
        build_kpi(
            icon='cart-check',
            badge='Ventas Realizadas',
            label='🛒 Transacciones',
            value=total_ventas,
            variant='info',
            trend_icon='check',
            trend_text='Este mes',
            trend_variant='info'
        ),
        build_kpi(
            icon='graph-up',
            badge='Ticket Promedio',
            label='📊 Promedio',
            value=f"${ticket_promedio:,.0f}",
            variant='primary',
            trend_icon='bar-chart',
            trend_text='Por venta',
            trend_variant='info'
        ),
        build_kpi(
            icon='trophy',
            badge='Producto Más Vendido',
            label='🏆 Top',
            value=producto_top_nombre[:20],
            variant='warning',
            trend_icon='star',
            trend_text=f'{producto_top_cantidad} unidades',
            trend_variant='warning'
        )
    ]


def prepare_compras_kpis(compras_queryset):
    """
    Preparar KPIs específicos para módulo de Compras
    
    Args:
        compras_queryset: QuerySet de Compra
        
    Returns:
        list: Lista de 4 KPIs formateados
    """
    total_compras = compras_queryset.count()
    inversion = compras_queryset.aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Proveedores únicos
    proveedores = compras_queryset.values('proveedor').distinct().count()
    
    # Materias compradas (requiere DetalleCompra)
    from gestion.models import DetalleCompra
    materias_distintas = DetalleCompra.objects.filter(
        compra__in=compras_queryset
    ).values('materia_prima').distinct().count()
    
    return [
        build_kpi(
            icon='truck',
            badge='Compras del Mes',
            label='🚚 Pedidos',
            value=total_compras,
            variant='info',
            trend_icon='box-seam',
            trend_text='Este mes',
            trend_variant='info'
        ),
        build_kpi(
            icon='cash-stack',
            badge='Inversión Mensual',
            label='💸 Gastado',
            value=f"${float(inversion):,.0f}",
            variant='danger',
            trend_icon='graph-down',
            trend_text='Inversión',
            trend_variant='danger'
        ),
        build_kpi(
            icon='people',
            badge='Proveedores Activos',
            label='🏭 Proveedores',
            value=proveedores,
            variant='success',
            trend_icon='building',
            trend_text='Activos',
            trend_variant='success'
        ),
        build_kpi(
            icon='box-seam',
            badge='Materias Compradas',
            label='📦 Productos',
            value=materias_distintas,
            variant='primary',
            trend_icon='check',
            trend_text='Distintas',
            trend_variant='info'
        )
    ]


def prepare_recetas_kpis(recetas_queryset):
    """
    Preparar KPIs específicos para módulo de Recetas
    
    Args:
        recetas_queryset: QuerySet de Receta
        
    Returns:
        list: Lista de 4 KPIs formateados
    """
    total_recetas = recetas_queryset.count()
    recetas_activas = recetas_queryset.filter(activo=True).count()
    
    # Costo promedio
    costo_promedio = recetas_queryset.aggregate(
        promedio=Sum('costo_total')
    )['promedio'] or Decimal('0')
    costo_promedio = float(costo_promedio) / total_recetas if total_recetas > 0 else 0
    
    # Receta con más ingredientes
    from gestion.models import IngredienteReceta
    receta_compleja = IngredienteReceta.objects.filter(
        receta__in=recetas_queryset
    ).values('receta__nombre').annotate(
        total=Count('id')
    ).order_by('-total').first()
    
    receta_compleja_nombre = receta_compleja['receta__nombre'] if receta_compleja else 'N/A'
    receta_compleja_ingredientes = receta_compleja['total'] if receta_compleja else 0
    
    return [
        build_kpi(
            icon='book',
            badge='Total Recetas',
            label='📖 Recetas',
            value=total_recetas,
            variant='success',
            trend_icon='check-circle',
            trend_text='Registradas',
            trend_variant='success'
        ),
        build_kpi(
            icon='play-circle',
            badge='Recetas Activas',
            label='✅ Activas',
            value=recetas_activas,
            variant='info',
            trend_icon='check',
            trend_text='En uso',
            trend_variant='info'
        ),
        build_kpi(
            icon='cash',
            badge='Costo Promedio',
            label='💰 Costo',
            value=f"${costo_promedio:,.0f}",
            variant='primary',
            trend_icon='graph-up',
            trend_text='Por receta',
            trend_variant='info'
        ),
        build_kpi(
            icon='award',
            badge='Receta Compleja',
            label='🏆 Destacada',
            value=receta_compleja_nombre[:20],
            variant='warning',
            trend_icon='star',
            trend_text=f'{receta_compleja_ingredientes} ingredientes',
            trend_variant='warning'
        )
    ]


def format_currency(value):
    """
    Formatear valor como moneda ARS
    
    Args:
        value (float/Decimal/int): Valor numérico
        
    Returns:
        str: Valor formateado como $1,234
    """
    try:
        return f"${float(value):,.0f}"
    except (ValueError, TypeError):
        return "$0"


def get_stock_badge_variant(producto):
    """
    Obtener variante de badge según stock del producto
    
    Args:
        producto: Instancia de Producto
        
    Returns:
        str: Variante de badge (success, warning, danger)
    """
    if producto.stock_actual == 0:
        return 'danger'
    elif producto.stock_actual <= producto.stock_minimo:
        return 'warning'
    else:
        return 'success'


def get_stock_status_text(producto):
    """
    Obtener texto de estado de stock
    
    Args:
        producto: Instancia de Producto
        
    Returns:
        str: Texto de estado
    """
    if producto.stock_actual == 0:
        return 'Sin Stock'
    elif producto.stock_actual <= producto.stock_minimo:
        return 'Stock Bajo'
    else:
        return 'Stock Normal'
