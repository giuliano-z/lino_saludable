from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core import serializers
from django.db.models import Q
from .models import Producto, Venta, MateriaPrima
import json
from datetime import datetime, timedelta

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

@require_GET
def api_productos(request):
    """API para sincronización de productos"""
    try:
        productos = Producto.objects.all()
        data = []
        for producto in productos:
            data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'stock': producto.stock,
                'descripcion': producto.descripcion or '',
                'updated_at': producto.id  # Simular timestamp
            })
        
        return JsonResponse({
            'status': 'success',
            'data': data,
            'count': len(data),
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def api_inventario(request):
    """API para sincronización de inventario/materias primas"""
    try:
        materias_primas = MateriaPrima.objects.all()
        data = []
        for materia in materias_primas:
            data.append({
                'id': materia.id,
                'nombre': materia.nombre,
                'stock_actual': float(materia.stock_actual),
                'stock_minimo': float(materia.stock_minimo),
                'unidad_medida': materia.unidad_medida,
                'costo_unitario': float(materia.costo_unitario),
                'proveedor': materia.proveedor or '',
                'updated_at': materia.id
            })
        
        return JsonResponse({
            'status': 'success', 
            'data': data,
            'count': len(data),
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def api_ventas(request):
    """API para sincronización de ventas"""
    try:
        # Últimas 100 ventas para no saturar
        ventas = Venta.objects.all().order_by('-fecha')[:100]
        data = []
        for venta in ventas:
            data.append({
                'id': venta.id,
                'fecha': venta.fecha.isoformat(),
                'total': float(venta.total),
                'cliente': venta.cliente or '',
                'items_count': venta.detalles.count(),
                'updated_at': venta.id
            })
        
        return JsonResponse({
            'status': 'success',
            'data': data, 
            'count': len(data),
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)