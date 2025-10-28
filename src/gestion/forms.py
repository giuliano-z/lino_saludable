
from django import forms
from .models import (
    Producto, Venta, Compra, MateriaPrima, ProductoMateriaPrima, MovimientoMateriaPrima, PerfilUsuario, VentaDetalle, Receta
)
from django.forms import inlineformset_factory


# Formulario placeholder para registrar ventas con verificación de materias primas
class VentaConMateriasForm(forms.Form):
    """Formulario placeholder para registrar ventas con verificación de materias primas."""
    # Puedes agregar campos y lógica según tus necesidades reales
    pass


class ProductoForm(forms.ModelForm):

    cantidad_a_producir = forms.IntegerField(
        min_value=1,
        required=False,
        label='Cantidad a producir',
        help_text='Cantidad de unidades a producir (solo para edición)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    
    # Campo adicional para nueva categoría
    nueva_categoria = forms.CharField(
        required=False,
        label='Nueva Categoría',
        help_text='Escriba una nueva categoría si no encuentra la que busca',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la nueva categoría...',
            'style': 'display: none;'  # Inicialmente oculto
        })
    )

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'categoria', 'stock', 'stock_minimo',
            # Sistema de costos avanzado
            'tipo_producto', 'costo_base', 'margen_ganancia', 'precio_venta_calculado', 'actualizar_precio_automatico',
            # Campos por tipo de producto
            'materia_prima_asociada', 'receta',
            # Fraccionamiento
            'producto_origen', 'unidad_compra', 'unidad_venta', 'factor_conversion', 'cantidad_origen', 'cantidad_fraccion',
            # Otros campos
            'atributos_dieteticos', 'marca', 'origen'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'id_categoria'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            
            # Sistema de costos avanzado
            'tipo_producto': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_producto'}),
            'costo_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'margen_ganancia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'precio_venta_calculado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_precio_venta_calculado'}),
            'actualizar_precio_automatico': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_actualizar_precio_automatico'}),
            
            # Campos por tipo de producto
            'materia_prima_asociada': forms.Select(attrs={'class': 'form-control', 'id': 'id_materia_prima_asociada'}),
            'receta': forms.Select(attrs={'class': 'form-control', 'id': 'id_receta'}),
            
            # Fraccionamiento
            'producto_origen': forms.Select(attrs={'class': 'form-control'}),
            'unidad_compra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kg, l, unidad...'}),
            'unidad_venta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'g, ml, unidad...'}),
            'factor_conversion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0.001'}),
            'cantidad_origen': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0.001'}),
            'cantidad_fraccion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0.001'}),
            
            # Otros campos
            'atributos_dieteticos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: organico,vegano,sin_tacc (separados por comas)'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del producto'
            }),
            'origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País o región de origen'
            }),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio de Venta ($)',
            'stock': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo (Alerta)',
            
            # Sistema de costos avanzado
            'tipo_producto': 'Tipo de Producto',
            'costo_base': 'Costo Base Unitario ($)',
            'margen_ganancia': 'Margen de Ganancia (%)',
            'precio_venta_calculado': 'Precio de Venta ($)',
            'actualizar_precio_automatico': 'Actualizar precio automáticamente',
            
            # Campos por tipo de producto
            'materia_prima_asociada': 'Materia Prima (Fraccionamiento)',
            'receta': 'Receta (Con Receta)',
            
            # Fraccionamiento
            'producto_origen': 'Producto de Origen',
            'unidad_compra': 'Unidad de Compra',
            'unidad_venta': 'Unidad de Venta',
            'factor_conversion': 'Factor de Conversión',
            'cantidad_origen': 'Cantidad Origen',
            'cantidad_fraccion': 'Cantidad por Fracción',
            
            # Otros campos
            'atributos_dieteticos': 'Atributos Dietéticos',
            'marca': 'Marca',
            'origen': 'Origen',
        }
        help_texts = {
            'stock_minimo': 'Cantidad mínima antes de mostrar alerta de stock bajo',
            'tipo_producto': 'Selecciona el tipo: Reventa, Fraccionamiento o Con Receta',
            'costo_base': 'Se calcula automáticamente según el tipo de producto',
            'margen_ganancia': 'Porcentaje de ganancia deseado (ej: 35 para 35%)',
            'precio_venta_calculado': 'Precio calculado automáticamente con el margen',
            'materia_prima_asociada': 'Solo para productos de fraccionamiento',
            'receta': 'Solo para productos con receta',
            'cantidad_origen': 'Cantidad del producto origen utilizada',
            'cantidad_fraccion': 'Cantidad que contiene cada unidad fraccionada',
            'tiene_receta': 'Marca si el producto se produce a partir de una receta',
            'receta': 'Selecciona la receta principal si corresponde',
            'atributos_dieteticos': 'Características especiales: orgánico, vegano, sin TACC, etc.',
            'marca': 'Marca comercial del producto',
            'origen': 'País o región de procedencia',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener todas las categorías disponibles
        from .models import Producto
        
        # Categorías predefinidas
        categorias_predefinidas = list(Producto.CATEGORIAS_DIETETICA)
        
        # Categorías dinámicas de la base de datos
        categorias_bd = Producto.objects.exclude(categoria__in=[cat[0] for cat in Producto.CATEGORIAS_DIETETICA]).values_list('categoria', flat=True).distinct()
        categorias_dinamicas = [(cat, cat) for cat in categorias_bd if cat and cat.strip()]
        
        # Crear lista completa de opciones
        todas_categorias = categorias_predefinidas + categorias_dinamicas
        
        # Configurar el widget del campo categoria
        self.fields['categoria'].widget.choices = todas_categorias
        
        # Configurar el campo receta (sistema de costos)
        if 'receta' in self.fields:
            self.fields['receta'].queryset = Receta.objects.all()
            self.fields['receta'].required = False
            self.fields['receta'].empty_label = "Selecciona una receta"
            
        # Configurar el campo materia_prima_asociada
        if 'materia_prima_asociada' in self.fields:
            self.fields['materia_prima_asociada'].queryset = MateriaPrima.objects.all()
            self.fields['materia_prima_asociada'].required = False
            self.fields['materia_prima_asociada'].empty_label = "Selecciona materia prima"
            
        # Configurar el campo producto_origen (para fraccionamiento)
        if 'producto_origen' in self.fields:
            self.fields['producto_origen'].queryset = Producto.objects.exclude(tipo_producto='fraccionamiento')
            self.fields['producto_origen'].required = False
            self.fields['producto_origen'].empty_label = "Seleccionar producto origen"
        
        # Configurar campos del sistema de costos
        if 'tipo_producto' in self.fields:
            self.fields['tipo_producto'].required = True
            
        if 'costo_base' in self.fields:
            self.fields['costo_base'].required = False
            
        if 'margen_ganancia' in self.fields:
            self.fields['margen_ganancia'].required = False
            
        if 'precio_venta_calculado' in self.fields:
            self.fields['precio_venta_calculado'].required = False
            
        # Hacer campos de fraccionamiento opcionales por defecto
        campos_fraccionamiento = ['unidad_compra', 'unidad_venta', 'factor_conversion', 'cantidad_origen', 'cantidad_fraccion']
        for campo in campos_fraccionamiento:
            if campo in self.fields:
                self.fields[campo].required = False

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        nueva_categoria = cleaned_data.get('nueva_categoria')
        tipo_producto = cleaned_data.get('tipo_producto')
        
        # Si seleccionó "nueva" pero no escribió una nueva categoría
        if categoria == 'nueva':
            if not nueva_categoria:
                raise forms.ValidationError('Debe escribir el nombre de la nueva categoría')
            
            # Convertir a formato slug para coherencia
            nueva_cat_slug = nueva_categoria.lower().replace(' ', '_').replace('ñ', 'n')
            cleaned_data['categoria'] = nueva_cat_slug
            
            # Verificar que no exista ya
            from .models import Producto
            if nueva_cat_slug in [choice[0] for choice in Producto.CATEGORIAS_DIETETICA]:
                raise forms.ValidationError(f'La categoría "{nueva_categoria}" ya existe')
        
        # Validaciones condicionales según el tipo de producto
        if tipo_producto:
            if tipo_producto == 'fraccionamiento':
                # Para fraccionamiento, validar campos específicos
                if not cleaned_data.get('producto_origen'):
                    raise forms.ValidationError('Para productos fraccionados debe seleccionar un producto origen')
                if not cleaned_data.get('factor_conversion'):
                    raise forms.ValidationError('Para productos fraccionados debe especificar el factor de conversión')
                if not cleaned_data.get('unidad_compra'):
                    raise forms.ValidationError('Para productos fraccionados debe especificar la unidad de compra')
                if not cleaned_data.get('unidad_venta'):
                    raise forms.ValidationError('Para productos fraccionados debe especificar la unidad de venta')
            
            elif tipo_producto == 'receta':
                # Para recetas, validar que tenga receta asociada
                if cleaned_data.get('tiene_receta') and not cleaned_data.get('receta'):
                    raise forms.ValidationError('Para productos con receta debe seleccionar una receta')
            
            # Para todos los tipos, margen de ganancia es opcional pero si se especifica debe ser válido
            margen = cleaned_data.get('margen_ganancia')
            if margen is not None and margen < 0:
                raise forms.ValidationError('El margen de ganancia no puede ser negativo')
        
        # En edición, cantidad_a_producir puede ser vacía o 0
        if self.instance and self.instance.pk:
            cantidad = cleaned_data.get('cantidad_a_producir')
            if cantidad is not None and cantidad < 1:
                cleaned_data['cantidad_a_producir'] = None
                
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # El campo categoria ya viene procesado del clean()
        if commit:
            instance.save()
        return instance

## Formulario para la cabecera de la venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente (opcional)'}),
        }

## Formulario para cada producto en la venta
class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f'No hay suficiente stock para {producto.nombre}. Disponible: {producto.stock}'
                )
        return cleaned_data

## Formset para múltiples productos en una venta
VentaDetalleFormSet = inlineformset_factory(
    Venta,
    VentaDetalle,
    form=VentaDetalleForm,
    extra=1,
    can_delete=True
)

class CompraForm(forms.ModelForm):
    """Formulario para registrar compras de materias primas."""
    materia_prima = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Materia Prima',
        help_text='Selecciona la materia prima a comprar'
    )

    def __init__(self, *args, **kwargs):
        from .models import MateriaPrima
        super().__init__(*args, **kwargs)
        self.fields['materia_prima'].queryset = MateriaPrima.objects.filter(activo=True)
        # Si hay una materia prima seleccionada, sugerir proveedor automáticamente
        if 'materia_prima' in self.data:
            try:
                mp_id = int(self.data.get('materia_prima'))
                mp = MateriaPrima.objects.get(pk=mp_id)
                self.fields['proveedor'].initial = mp.proveedor
            except Exception:
                pass
        elif self.instance.pk and self.instance.materia_prima:
            self.fields['proveedor'].initial = self.instance.materia_prima.proveedor

    class Meta:
        model = Compra
        fields = ['materia_prima', 'proveedor', 'cantidad_mayoreo', 'precio_mayoreo']
        widgets = {
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'cantidad_mayoreo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Cantidad'
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
            'cantidad_mayoreo': 'Cantidad',
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

## Formularios principales para materias primas, productos y movimientos

class MateriaPrimaForm(forms.ModelForm):
    """Formulario para crear o editar materias primas."""
    class Meta:
        model = MateriaPrima
        fields = ['nombre', 'descripcion', 'unidad_medida', 'stock_actual', 
                 'stock_minimo', 'costo_unitario', 'proveedor', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unidad_medida': forms.Select(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre de la Materia Prima',
            'descripcion': 'Descripción',
            'unidad_medida': 'Unidad de Medida',
            'stock_actual': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo',
            'costo_unitario': 'Costo Unitario ($)',
            'proveedor': 'Proveedor Principal',
            'activo': 'Materia Prima Activa',
        }

class ProductoMateriaPrimaForm(forms.ModelForm):
    """Formulario para asociar materias primas a productos."""
    class Meta:
        model = ProductoMateriaPrima
        fields = ['producto', 'materia_prima', 'cantidad_necesaria']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'materia_prima': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_necesaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'producto': 'Producto',
            'materia_prima': 'Materia Prima',
            'cantidad_necesaria': 'Cantidad Necesaria',
        }

class MovimientoMateriaPrimaForm(forms.ModelForm):
    """Formulario para registrar movimientos de materias primas."""
    class Meta:
        model = MovimientoMateriaPrima
        fields = ['materia_prima', 'tipo_movimiento', 'cantidad', 'motivo']
        widgets = {
            'materia_prima': forms.Select(attrs={'class': 'form-control'}),
            'tipo_movimiento': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'materia_prima': 'Materia Prima',
            'tipo_movimiento': 'Tipo de Movimiento',
            'cantidad': 'Cantidad',
            'motivo': 'Motivo/Observaciones',
        }

class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para editar perfil de usuario."""
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'telefono', 'departamento']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'rol': 'Rol del Usuario',
            'telefono': 'Teléfono',
            'departamento': 'Departamento',
        }


## Formulario para búsqueda y filtros de materias primas
class BusquedaMateriaPrimaForm(forms.Form):
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    unidad_medida = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas las unidades')] + MateriaPrima.UNIDADES_MEDIDA,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    stock_bajo = forms.BooleanField(
        required=False,
        label="Solo mostrar stock bajo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# ==================== FORMULARIO RECETA ====================
class RecetaForm(forms.ModelForm):
    """Formulario para crear y editar recetas."""
    
    class Meta:
        model = Receta
        fields = ['nombre', 'descripcion', 'productos', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la receta...'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la receta...'
            }),
            'productos': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Receta',
            'descripcion': 'Descripción',
            'productos': 'Productos que usan esta receta',
            'activa': 'Receta activa',
        }
        help_texts = {
            'nombre': 'Ingrese un nombre descriptivo para la receta',
            'descripcion': 'Agregue detalles sobre la preparación o características',
            'productos': 'Seleccione los productos que utilizarán esta receta',
            'activa': 'Marque si la receta está activa y puede utilizarse',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar queryset de productos
        self.fields['productos'].queryset = Producto.objects.filter(
            tiene_receta=True
        ).order_by('nombre')
        
        # Hacer que el campo nombre sea requerido y único
        self.fields['nombre'].required = True
        
        # Configurar valor por defecto para activa
        if not self.instance.pk:
            self.fields['activa'].initial = True

    def save(self, commit=True):
        """Guarda la receta y maneja las materias primas dinámicas."""
        receta = super().save(commit=commit)
        
        if commit:
            # Aquí procesaremos los ingredientes dinámicos
            # Esta lógica se implementará en la vista
            pass
            
        return receta