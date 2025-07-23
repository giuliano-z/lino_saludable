from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto

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