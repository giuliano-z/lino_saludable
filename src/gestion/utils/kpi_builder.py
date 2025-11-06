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
    en_stock = productos_queryset.filter(stock__gt=0).count()
    
    # Stock Bajo = productos con stock <= stock_minimo (incluye stock=0)
    # Esto cubre tanto productos agotados como productos con stock bajo
    bajo_stock = productos_queryset.filter(
        stock__lte=F('stock_minimo')
    ).count()
    
    sin_stock = productos_queryset.filter(stock=0).count()
    
    # Valor total del inventario
    valor_total = productos_queryset.aggregate(
        total=Sum(F('stock') * F('precio'))
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
    
    # Producto más vendido (requiere VentaDetalle)
    from gestion.models import VentaDetalle
    producto_top = VentaDetalle.objects.filter(
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
    Compatible con sistema legacy (1 producto) y nuevo (multi-producto)
    
    Args:
        compras_queryset: QuerySet de Compra
        
    Returns:
        list: Lista de 4 KPIs formateados
    """
    from django.db.models import Case, When, F
    from gestion.models import CompraDetalle
    
    total_compras = compras_queryset.count()
    
    # Inversión total (compatible legacy + nuevo)
    # Legacy: precio_mayoreo, Nuevo: total
    inversion = compras_queryset.annotate(
        importe=Case(
            When(total__isnull=False, then=F('total')),
            default=F('precio_mayoreo')
        )
    ).aggregate(total=Sum('importe'))['total'] or Decimal('0')
    
    # Proveedores únicos
    proveedores = compras_queryset.values('proveedor').distinct().count()
    
    # Materias compradas distintas (compatible con legacy y nuevo sistema)
    # Legacy: materia_prima directamente en Compra
    # Nuevo: materias primas en CompraDetalle
    from gestion.models import CompraDetalle
    
    # Contar materias de compras legacy (tienen materia_prima no null)
    materias_legacy = compras_queryset.filter(
        materia_prima__isnull=False
    ).values('materia_prima').distinct().count()
    
    # Contar materias de compras nuevas (CompraDetalle)
    compras_ids = compras_queryset.values_list('id', flat=True)
    materias_nuevas = CompraDetalle.objects.filter(
        compra_id__in=compras_ids
    ).values('materia_prima').distinct().count()
    
    # Total: sumar ambas (sin duplicados si una materia está en ambos sistemas)
    # Usar set para evitar duplicados
    materias_legacy_ids = set(compras_queryset.filter(
        materia_prima__isnull=False
    ).values_list('materia_prima_id', flat=True))
    
    materias_nuevas_ids = set(CompraDetalle.objects.filter(
        compra_id__in=compras_ids
    ).values_list('materia_prima_id', flat=True))
    
    materias_distintas = len(materias_legacy_ids | materias_nuevas_ids)  # Unión de conjuntos
    
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
    """Prepara KPIs para la vista de recetas."""
    from gestion.models import Receta
    from decimal import Decimal
    
    total_recetas = recetas_queryset.count()
    recetas_activas = recetas_queryset.filter(activa=True).count()
    
    # Costo promedio de recetas (calculado en Python porque costo_total es un método)
    costo_promedio = Decimal('0')
    if total_recetas > 0:
        costos = [receta.costo_total() for receta in recetas_queryset]
        total_costos = sum(costos) if costos else Decimal('0')
        costo_promedio = total_costos / total_recetas if total_recetas > 0 else Decimal('0')
    
    # Receta más usada (por productos que la usan)
    receta_destacada = recetas_queryset.annotate(
        productos_count=Count('productos')
    ).order_by('-productos_count').first()
    
    receta_destacada_nombre = receta_destacada.nombre if receta_destacada else "N/A"


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
