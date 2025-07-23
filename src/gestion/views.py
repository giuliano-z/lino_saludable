from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from .resources import ProductoResource, VentaResource
from .models import Producto, Venta, Compra
from .forms import ProductoForm, VentaForm, CompraForm

@login_required
def dashboard(request):
    # Estadísticas de productos
    total_productos = Producto.objects.count()
    productos_stock_bajo = Producto.objects.filter(stock__lte=F('stock_minimo'))
    productos_stock_bajo_count = productos_stock_bajo.count()
    
    # Estadísticas de ventas
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    ventas_mes = Venta.objects.filter(fecha__date__gte=inicio_mes).count()
    ingresos_mes = Venta.objects.filter(fecha__date__gte=inicio_mes).aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # NUEVAS ESTADÍSTICAS DE COMPRAS
    from .models import Compra
    total_compras = Compra.objects.count()
    compras_mes = Compra.objects.filter(fecha_compra__gte=inicio_mes).count()
    inversion_mes = Compra.objects.filter(fecha_compra__gte=inicio_mes).aggregate(
        total=Sum('precio_mayoreo')
    )['total'] or 0
    inversion_total = Compra.objects.aggregate(
        total=Sum('precio_mayoreo')
    )['total'] or 0
    
    # Stock crítico de materias primas
    materias_stock_bajo = Compra.objects.filter(stock_mayoreo__lte=5).count()
    
    # Últimas actividades
    ultimas_ventas = Venta.objects.select_related('producto').order_by('-fecha')[:5]
    ultimas_compras = Compra.objects.order_by('-fecha_compra')[:5]
    
    context = {
        # Productos
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo[:10],  # Solo mostrar 10
        'productos_stock_bajo_count': productos_stock_bajo_count,
        
        # Ventas
        'ventas_mes': ventas_mes,
        'ingresos_mes': ingresos_mes,
        'ultimas_ventas': ultimas_ventas,
        
        # NUEVAS VARIABLES DE COMPRAS
        'total_compras': total_compras,
        'compras_mes': compras_mes,
        'inversion_mes': inversion_mes,
        'inversion_total': inversion_total,
        'materias_stock_bajo': materias_stock_bajo,
        'ultimas_compras': ultimas_compras,
    }
    
    return render(request, 'gestion/dashboard.html', context)

@login_required
def verificar_alertas_stock(request):
    """Función para verificar y mostrar alertas de stock usando stock_minimo personalizado"""
    productos_agotados = Producto.objects.filter(stock=0)
    productos_criticos = Producto.objects.filter(stock__gt=0).extra(
        where=["stock <= stock_minimo"]
    )
    productos_bajos = Producto.objects.filter(stock__gt=0).extra(
        where=["stock > stock_minimo AND stock <= stock_minimo * 2"]
    )
    
    alertas = []
    
    if productos_agotados.exists():
        alertas.append({
            'tipo': 'danger',
            'titulo': 'Productos Agotados',
            'mensaje': f'{productos_agotados.count()} producto(s) sin stock',
            'productos': productos_agotados
        })
    
    if productos_criticos.exists():
        alertas.append({
            'tipo': 'warning',
            'titulo': 'Stock Crítico',
            'mensaje': f'{productos_criticos.count()} producto(s) con stock crítico',
            'productos': productos_criticos
        })
    
    if productos_bajos.exists():
        alertas.append({
            'tipo': 'info',
            'titulo': 'Stock Bajo',
            'mensaje': f'{productos_bajos.count()} producto(s) con stock bajo',
            'productos': productos_bajos
        })
    
    return alertas

@login_required
def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('gestion:lista_productos')
        else:
            messages.error(request, 'Error al crear el producto. Verifica los datos.')
    else:
        form = ProductoForm()
    
    # Obtener categorías existentes para autocompletado
    categorias_existentes = Producto.objects.exclude(
        categoria__isnull=True
    ).exclude(categoria='').values_list('categoria', flat=True).distinct()
    
    return render(request, 'gestion/producto_form.html', {
        'form': form,
        'titulo': 'Crear Producto',
        'categorias_existentes': categorias_existentes
    })

@require_GET
def producto_precio(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
        return JsonResponse({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'stock': producto.stock
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('gestion:lista_productos')
        else:
            messages.error(request, 'Error al actualizar el producto. Verifica los datos.')
    else:
        form = ProductoForm(instance=producto)
    
    # Obtener categorías existentes para autocompletado
    categorias_existentes = Producto.objects.exclude(
        categoria__isnull=True
    ).exclude(categoria='').values_list('categoria', flat=True).distinct()
    
    return render(request, 'gestion/producto_form.html', {
        'form': form,
        'titulo': 'Editar Producto',
        'categorias_existentes': categorias_existentes
    })

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('gestion:lista_productos')
    
    context = {
        'objeto': producto,
        'tipo': 'producto',
        'cancel_url': reverse('gestion:lista_productos')
    }
    return render(request, 'gestion/confirmar_eliminacion.html', context)

@login_required
def lista_ventas(request):
    ventas = Venta.objects.all()
    
    # Filtros
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if query:
        ventas = ventas.filter(producto__nombre__icontains=query)
    
    if fecha_inicio:
        ventas = ventas.filter(fecha__date__gte=fecha_inicio)
    
    if fecha_fin:
        ventas = ventas.filter(fecha__date__lte=fecha_fin)
    
    ventas = ventas.order_by('-fecha')
    
    # Calcular totales
    total_productos_vendidos = ventas.aggregate(total=Sum('cantidad'))['total'] or 0
    total_ingresos = ventas.aggregate(total=Sum('total'))['total'] or 0
    
    context = {
        'ventas': ventas,
        'query': query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_productos_vendidos': total_productos_vendidos,
        'total_ingresos': total_ingresos,
    }
    
    return render(request, 'gestion/lista_ventas.html', context)

@login_required
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto
            
            # Verificar stock disponible
            if venta.cantidad > producto.stock:
                messages.error(request, f'No hay suficiente stock. Stock disponible: {producto.stock}')
                return render(request, 'gestion/venta_form.html', {
                    'form': form,
                    'titulo': 'Registrar Venta'
                })
            
            # Calcular total y reducir stock
            venta.total = producto.precio * venta.cantidad
            producto.stock -= venta.cantidad
            
            # Guardar ambos objetos
            venta.save()
            producto.save()
            
            messages.success(request, f'Venta registrada exitosamente. Stock actualizado.')
            return redirect('gestion:lista_ventas')
        else:
            messages.error(request, 'Error al registrar la venta. Verifica los datos.')
    else:
        form = VentaForm()
    
    return render(request, 'gestion/venta_form.html', {
        'form': form,
        'titulo': 'Registrar Venta'
    })

@login_required
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        # Restaurar stock antes de eliminar
        producto = venta.producto
        producto.stock += venta.cantidad
        producto.save()
        
        venta.delete()
        messages.success(request, f'Venta eliminada. Se restauraron {venta.cantidad} unidades al stock de {producto.nombre}.')
        return redirect('gestion:lista_ventas')
    
    context = {
        'objeto': venta,
        'tipo': 'venta',
        'cancel_url': reverse('gestion:lista_ventas')
    }
    return render(request, 'gestion/confirmar_eliminacion.html', context)

@login_required
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'gestion/detalle_venta.html', {'venta': venta})

@login_required
def index(request):
    if request.user.is_authenticated:
        return redirect('gestion:dashboard')
    else:
        return redirect('login')

@login_required
def exportar_productos(request):
    producto_resource = ProductoResource()
    dataset = producto_resource.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="productos_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    return response

@login_required
def exportar_ventas(request):
    venta_resource = VentaResource()
    dataset = venta_resource.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="ventas_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    return response

@login_required
def reportes(request):
    # Por ahora solo redirigir al dashboard
    messages.info(request, 'Los reportes detallados estarán disponibles próximamente.')
    return redirect('gestion:dashboard')

@login_required
def lista_compras(request):
    """Vista para listar todas las compras al mayoreo"""
    compras = Compra.objects.all().order_by('-fecha_compra')
    
    # CALCULAR total invertido
    total_invertido = compras.aggregate(
        total=Sum('precio_mayoreo')
    )['total'] or 0
    
    context = {
        'compras': compras,
        'total_invertido': total_invertido,
    }
    return render(request, 'gestion/lista_compras.html', context)

@login_required
def crear_compra(request):
    """Vista para crear una nueva compra al mayoreo"""
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save()
            messages.success(request, f'Compra de {compra.materia_prima} registrada exitosamente.')
            return redirect('gestion:lista_compras')
    else:
        form = CompraForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nueva Compra al Mayoreo'
    }
    return render(request, 'gestion/crear_compra.html', context)

@login_required
def reportes(request):
    from django.db.models import Sum, Count, Avg
    from datetime import datetime, timedelta
    
    # Fechas para filtros
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    inicio_mes = hoy.replace(day=1)
    
    # Estadísticas generales
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    total_compras = Compra.objects.count()
    
    # Ingresos y gastos
    ingresos_totales = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
    gastos_totales = Compra.objects.aggregate(Sum('precio_mayoreo'))['precio_mayoreo__sum'] or 0
    ganancia_bruta = ingresos_totales - gastos_totales
    
    # Calcular margen de ganancia
    margen_ganancia = 0
    if ingresos_totales > 0:
        margen_ganancia = (ganancia_bruta / ingresos_totales) * 100
    
    # Estadísticas del mes actual
    ventas_mes = Venta.objects.filter(fecha__date__gte=inicio_mes).count()
    ingresos_mes = Venta.objects.filter(fecha__date__gte=inicio_mes).aggregate(Sum('total'))['total__sum'] or 0
    compras_mes = Compra.objects.filter(fecha_compra__gte=inicio_mes).count()
    gastos_mes = Compra.objects.filter(fecha_compra__gte=inicio_mes).aggregate(Sum('precio_mayoreo'))['precio_mayoreo__sum'] or 0
    
    # Productos más vendidos
    productos_mas_vendidos = Venta.objects.values('producto__nombre').annotate(
        total_vendido=Sum('cantidad'),
        ingresos=Sum('total')
    ).order_by('-total_vendido')[:10]
    
    # Ventas por día (últimos 30 días)
    ventas_por_dia = []
    for i in range(30):
        fecha = hoy - timedelta(days=i)
        ventas_dia = Venta.objects.filter(fecha__date=fecha).aggregate(
            total=Sum('total')
        )['total'] or 0
        ventas_por_dia.append({
            'fecha': fecha.strftime('%d/%m'),
            'total': float(ventas_dia)
        })
    ventas_por_dia.reverse()
    
    # Stock crítico
    productos_stock_critico = Producto.objects.filter(
        stock__lte=F('stock_minimo')
    ).count()
    
    materias_stock_critico = Compra.objects.filter(stock_mayoreo__lte=5).count()
    
    context = {
        # Generales
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        
        # Financiero
        'ingresos_totales': ingresos_totales,
        'gastos_totales': gastos_totales,
        'ganancia_bruta': ganancia_bruta,
        'margen_ganancia': margen_ganancia,  # NUEVO
        
        # Mes actual
        'ventas_mes': ventas_mes,
        'ingresos_mes': ingresos_mes,
        'compras_mes': compras_mes,
        'gastos_mes': gastos_mes,
        
        # Análisis
        'productos_mas_vendidos': productos_mas_vendidos,
        'ventas_por_dia': ventas_por_dia,
        'productos_stock_critico': productos_stock_critico,
        'materias_stock_critico': materias_stock_critico,
    }
    
    return render(request, 'gestion/reportes.html', context)