from django import forms
from .models import Producto, Venta, Compra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'stock_minimo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribir o seleccionar categoría...',
                'list': 'categorias-list',
                'autocomplete': 'off'
            }),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'stock': 'Stock Actual',
            'categoria': 'Categoría',
            'stock_minimo': 'Stock Mínimo (Alerta)',
        }
        help_texts = {
            'stock_minimo': 'Cantidad mínima antes de mostrar alerta de stock bajo',
        }

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if categoria:
            return categoria.strip().title()
        return categoria

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'total']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f'No hay suficiente stock. Stock disponible: {producto.stock}'
                )
            
            cleaned_data['total'] = producto.precio * cantidad

        return cleaned_data
    
class CompraForm(forms.ModelForm):
    """Formulario para registrar compras al mayoreo"""
    class Meta:
        model = Compra  # IMPORTANTE: Asegúrate de importar Compra en la línea de imports
        fields = ['proveedor', 'materia_prima', 'cantidad_mayoreo', 'precio_mayoreo']
        widgets = {
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'materia_prima': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pistachos a granel, Almendras, etc.'
            }),
            'cantidad_mayoreo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Cantidad en kilos'
            }),
            'precio_mayoreo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Precio total de la compra'
            }),
        }
        labels = {
            'proveedor': 'Proveedor',
            'materia_prima': 'Materia Prima',
            'cantidad_mayoreo': 'Cantidad (kg)',
            'precio_mayoreo': 'Precio Total ($)',
        }
    
    def clean_cantidad_mayoreo(self):
        cantidad = self.cleaned_data.get('cantidad_mayoreo')
        if cantidad and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        return cantidad
    
    def clean_precio_mayoreo(self):
        precio = self.cleaned_data.get('precio_mayoreo')
        if precio and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio