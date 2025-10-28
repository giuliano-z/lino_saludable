from import_export import resources
from .models import Producto, Venta, VentaDetalle

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')
        export_order = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')


# Exporta solo la cabecera de la venta (sin productos)
class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta
        fields = ('id', 'cliente', 'total', 'fecha')
        export_order = ('id', 'cliente', 'total', 'fecha')

# Exporta los productos vendidos en cada venta
class VentaDetalleResource(resources.ModelResource):
    class Meta:
        model = VentaDetalle
        fields = ('id', 'venta__id', 'venta__cliente', 'producto__nombre', 'cantidad', 'precio_unitario', 'subtotal')
        export_order = ('id', 'venta__id', 'venta__cliente', 'producto__nombre', 'cantidad', 'precio_unitario', 'subtotal')