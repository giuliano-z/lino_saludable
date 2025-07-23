from django.db import models
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    stock_minimo = models.IntegerField(default=5, help_text="Stock mínimo antes de alerta")
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    @property
    def estado_stock(self):
        if self.stock == 0:
            return 'agotado'
        elif self.stock <= self.stock_minimo:
            return 'critico'
        elif self.stock <= self.stock_minimo * 2:
            return 'bajo'
        else:
            return 'normal'

    class Meta:
        verbose_name_plural = "Productos"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Venta de {self.cantidad} {self.producto.nombre}"

    class Meta:
        verbose_name_plural = "Ventas"

class Compra(models.Model):
    fecha_compra = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=100)
    materia_prima = models.CharField(max_length=200, help_text="Ej: Pistachos a granel")
    cantidad_mayoreo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Cantidad en kilos"
    )
    precio_mayoreo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio total de la compra"
    )
    precio_unitario_mayoreo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        editable=False,
        help_text="Precio por kilo (calculado automáticamente)"
    )
    stock_mayoreo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Stock disponible para racionar"
    )
    
    class Meta:
        verbose_name = "Compra al Mayoreo"
        verbose_name_plural = "Compras al Mayoreo"
        ordering = ['-fecha_compra']
    
    def save(self, *args, **kwargs):
        if self.cantidad_mayoreo and self.precio_mayoreo:
            self.precio_unitario_mayoreo = self.precio_mayoreo / self.cantidad_mayoreo
        
        if not self.pk:
            self.stock_mayoreo = self.cantidad_mayoreo
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.materia_prima} - {self.proveedor} ({self.fecha_compra})"