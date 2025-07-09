from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Venta
from .forms import ProductoForm, VentaForm
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@login_required
def dashboard(request):
    # Obtener estadísticas básicas
    total_productos = Producto.objects.count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    
    # Ventas del día
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha__date=hoy)
    total_ventas_hoy = ventas_hoy.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Ventas de la semana
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    
    # Datos para el gráfico de ventas por día
    ventas_por_dia = {}
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        ventas_dia = Venta.objects.filter(fecha__date=dia)
        total_dia = ventas_dia.aggregate(total=Sum('total'))['total'] or 0
        ventas_por_dia[dias_semana[i]] = float(total_dia)
    
    # Productos más vendidos
    productos_mas_vendidos = Producto.objects.annotate(
        total_vendido=Sum('venta__cantidad')
    ).order_by('-total_vendido')[:5]
    
    # Productos con stock bajo (menos de 5 unidades)
    productos_stock_bajo = Producto.objects.filter(stock__lt=5)
    
    context = {
        'total_productos': total_productos,
        'productos_sin_stock': productos_sin_stock,
        'total_ventas_hoy': total_ventas_hoy,
        'ventas_por_dia': ventas_por_dia,
        'productos_mas_vendidos': productos_mas_vendidos,
        'productos_stock_bajo': productos_stock_bajo,
    }
    
    return render(request, 'gestion/dashboard.html', context)

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'gestion/lista_productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('gestion:lista_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'gestion/producto_form.html', {'form': form, 'titulo': 'Crear Producto'})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('gestion:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'gestion/producto_form.html', {'form': form, 'titulo': 'Editar Producto'})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('gestion:lista_productos')
    
    return render(request, 'gestion/confirmar_eliminacion.html', {'producto': producto})

@login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'gestion/lista_ventas.html', {'ventas': ventas})

@login_required
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            
            # Actualizar el stock del producto
            producto = venta.producto
            producto.stock -= venta.cantidad
            producto.save()
            
            venta.save()
            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('gestion:lista_ventas')
    else:
        form = VentaForm()
    
    return render(request, 'gestion/venta_form.html', {'form': form, 'titulo': 'Registrar Venta'})

@login_required
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'gestion/detalle_venta.html', {'venta': venta})

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

def index(request):
    if request.user.is_authenticated:
        return redirect('gestion:dashboard')
    else:
        return redirect('login')
