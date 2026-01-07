"""
Vista temporal para resetear la base de datos desde el navegador.
⚠️  ELIMINAR DESPUÉS DE USAR
"""

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.models import User
from gestion.models import (
    Venta, VentaDetalle, Compra, CompraDetalle,
    LoteMateriaPrima, Alerta, Producto, MateriaPrima,
    MovimientoMateriaPrima, HistorialCosto,
    HistorialPreciosMateriaPrima, AjusteInventario,
    ProductoMateriaPrima, Receta, RecetaMateriaPrima
)


@csrf_exempt  # ⚠️  Deshabilitamos CSRF solo para esta vista temporal
@require_http_methods(["POST"])
def reset_database_view(request):
    """
    Resetea la base de datos de producción.
    ⚠️  Solo usar una vez y luego eliminar esta vista
    """
    # Verificación de seguridad
    secret_key = request.POST.get('secret_key', '')
    if secret_key != 'RESET_LINO_2026':
        return HttpResponse(
            '❌ Clave incorrecta',
            status=403,
            content_type='text/plain'
        )

    try:
        USUARIOS_A_MANTENER = ['sister_emprendedora', 'el_super_creador']
        
        with transaction.atomic():
            # Contar antes
            counts = {
                'ventas': Venta.objects.count(),
                'compras': Compra.objects.count(),
                'productos': Producto.objects.count(),
                'materias': MateriaPrima.objects.count(),
            }
            
            # Eliminar todo
            VentaDetalle.objects.all().delete()
            Venta.objects.all().delete()
            CompraDetalle.objects.all().delete()
            Compra.objects.all().delete()
            LoteMateriaPrima.objects.all().delete()
            Alerta.objects.all().delete()
            MovimientoMateriaPrima.objects.all().delete()
            HistorialCosto.objects.all().delete()
            HistorialPreciosMateriaPrima.objects.all().delete()
            AjusteInventario.objects.all().delete()
            RecetaMateriaPrima.objects.all().delete()
            ProductoMateriaPrima.objects.all().delete()
            Receta.objects.all().delete()
            Producto.objects.all().delete()
            MateriaPrima.objects.all().delete()
            User.objects.exclude(username__in=USUARIOS_A_MANTENER).delete()
        
        usuarios_finales = User.objects.all()
        usuarios_list = [f"{u.username} ({u.email})" for u in usuarios_finales]
        
        return HttpResponse(
            f"""
✅ RESET COMPLETADO

Registros eliminados:
- Ventas: {counts['ventas']}
- Compras: {counts['compras']}
- Productos: {counts['productos']}
- Materias primas: {counts['materias']}

Usuarios mantenidos:
{chr(10).join(usuarios_list)}

🎯 Sistema listo para empezar de cero
⚠️  IMPORTANTE: Elimina esta vista ahora
            """,
            content_type='text/plain'
        )
        
    except Exception as e:
        return HttpResponse(
            f'❌ ERROR: {str(e)}',
            status=500,
            content_type='text/plain'
        )
