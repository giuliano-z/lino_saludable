# Create your models here.
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta de {self.cantidad} unidades de {self.producto.nombre}"
    
from django.contrib import admin
from .models import Producto, Venta

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    list_filter = ('categoria', 'stock')
    search_fields = ('nombre', 'descripcion')

class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'total')
    list_filter = ('fecha', 'producto')
    date_hierarchy = 'fecha'

# Registrar los modelos en el admin
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)