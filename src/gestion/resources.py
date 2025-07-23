from import_export import resources
from .models import Producto, Venta

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')
        export_order = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')

class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta
        fields = ('id', 'producto__nombre', 'cantidad', 'total', 'fecha')
        export_order = ('id', 'producto__nombre', 'cantidad', 'total', 'fecha')