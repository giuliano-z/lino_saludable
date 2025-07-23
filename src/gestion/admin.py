from django.contrib import admin
from .models import Producto, Venta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'estado_stock', 'fecha_creacion')
    list_filter = ('categoria', 'fecha_creacion')
    search_fields = ('nombre', 'categoria')
    ordering = ('nombre',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'total', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('producto__nombre',)
    ordering = ('-fecha',)