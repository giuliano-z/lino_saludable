from django.contrib import admin
from .models import (
    Producto, Venta, Compra, MateriaPrima, ProductoMateriaPrima, 
    MovimientoMateriaPrima, PerfilUsuario, LoteMateriaPrima,
    HistorialCosto, ConfiguracionCostos, Receta, RecetaMateriaPrima,
    HistorialPreciosMateriaPrima
)

# Registros existentes (mantener)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'tipo_producto', 'precio', 'stock', 'categoria', 
        'costo_base', 'margen_ganancia', 'precio_venta_calculado', 'estado_stock'
    ]
    list_filter = ['categoria', 'tipo_producto', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria', 'tipo_producto')
        }),
        ('Inventario', {
            'fields': ('stock', 'stock_minimo', 'precio')
        }),
        ('Sistema de Costos', {
            'fields': (
                'costo_base', 'margen_ganancia', 'precio_venta_calculado',
                'actualizar_precio_automatico'
            )
        }),
        ('Fraccionamiento', {
            'fields': (
                'producto_origen', 'unidad_compra', 'unidad_venta',
                'factor_conversion', 'cantidad_origen', 'cantidad_fraccion'
            ),
            'classes': ('collapse',)
        }),
        ('Características', {
            'fields': (
                'marca', 'tamaño_porcion', 'atributos_dieteticos', 
                'codigo_barras', 'imagen'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = ['precio_venta_calculado']
        if obj and obj.tipo_producto == 'receta':
            readonly.append('costo_base')
        return readonly

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'productos_vendidos', 'total', 'cliente', 'fecha']
    list_filter = ['fecha']
    search_fields = ['cliente']

    def productos_vendidos(self, obj):
        return ", ".join([
            f"{detalle.producto.nombre} (x{detalle.cantidad})"
            for detalle in obj.detalles.all()
        ])
    productos_vendidos.short_description = 'Productos Vendidos'

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['materia_prima', 'proveedor', 'cantidad_mayoreo', 'precio_mayoreo', 'fecha_compra']
    list_filter = ['fecha_compra', 'proveedor']
    search_fields = ['materia_prima', 'proveedor']

# NUEVOS REGISTROS
class LoteMateriaPrimaInline(admin.TabularInline):
    model = LoteMateriaPrima
    extra = 0
    readonly_fields = ("cantidad", "cantidad_disponible", "precio_unitario", "fecha_entrada", "fecha_consumo", "observaciones")
    can_delete = False

@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'unidad_medida', 'stock_actual', 'stock_minimo', 'costo_unitario', 'necesita_restock', 'proveedor']
    list_filter = ['unidad_medida', 'activo', 'proveedor']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['stock_actual', 'stock_minimo', 'costo_unitario']
    inlines = [LoteMateriaPrimaInline]
    actions = ['actualizar_productos_relacionados']
    
    def actualizar_productos_relacionados(self, request, queryset):
        productos_actualizados = 0
        for materia_prima in queryset:
            productos_afectados = materia_prima.actualizar_productos_relacionados(usuario=request.user)
            productos_actualizados += len(productos_afectados)
        
        self.message_user(
            request,
            f"Se actualizaron {productos_actualizados} productos relacionados."
        )
    actualizar_productos_relacionados.short_description = "Actualizar productos que usan estas materias primas"

@admin.register(ProductoMateriaPrima)
class ProductoMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'materia_prima', 'cantidad_necesaria']
    list_filter = ['producto', 'materia_prima']

@admin.register(MovimientoMateriaPrima)
class MovimientoMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ['materia_prima', 'tipo_movimiento', 'cantidad', 'usuario', 'fecha']
    list_filter = ['tipo_movimiento', 'fecha', 'materia_prima']
    readonly_fields = ['fecha', 'cantidad_anterior', 'cantidad_nueva']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'departamento', 'activo']
    list_filter = ['rol', 'activo', 'departamento']

@admin.register(LoteMateriaPrima)
class LoteMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ("materia_prima", "cantidad", "cantidad_disponible", "precio_unitario", "fecha_entrada", "fecha_consumo")
    search_fields = ("materia_prima__nombre",)
    list_filter = ("materia_prima", "fecha_entrada", "fecha_consumo")
    readonly_fields = ("materia_prima", "cantidad", "precio_unitario", "fecha_entrada", "fecha_consumo", "observaciones")


# ==================== NUEVOS MODELOS DE COSTOS ====================

class RecetaMateriaPrimaInline(admin.TabularInline):
    model = RecetaMateriaPrima
    extra = 1
    autocomplete_fields = ['materia_prima']

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'productos_count', 'materias_count', 'fecha_creacion', 'costo_total_display', 'activa']
    list_filter = ['fecha_creacion', 'activa', 'creador']
    search_fields = ['nombre', 'descripcion']
    inlines = [RecetaMateriaPrimaInline]
    filter_horizontal = ['productos']
    
    def costo_total_display(self, obj):
        return f"${obj.costo_total():.2f}"
    costo_total_display.short_description = 'Costo Total'

@admin.register(RecetaMateriaPrima)
class RecetaMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ['receta', 'materia_prima', 'cantidad', 'unidad', 'costo_ingrediente_display']
    list_filter = ['receta', 'materia_prima', 'unidad']
    search_fields = ['receta__nombre', 'materia_prima__nombre']
    autocomplete_fields = ['receta', 'materia_prima']
    
    def costo_ingrediente_display(self, obj):
        return f"${obj.costo_ingrediente():.2f}"
    costo_ingrediente_display.short_description = 'Costo'

@admin.register(HistorialCosto)
class HistorialCostoAdmin(admin.ModelAdmin):
    list_display = [
        'producto', 'fecha', 'costo_anterior', 'costo_nuevo',
        'precio_anterior', 'precio_nuevo', 'porcentaje_cambio_costo_display', 'usuario'
    ]
    list_filter = ['fecha', 'producto', 'usuario']
    search_fields = ['producto__nombre', 'motivo']
    readonly_fields = [
        'producto', 'fecha', 'costo_anterior', 'costo_nuevo',
        'precio_anterior', 'precio_nuevo', 'usuario'
    ]
    
    def porcentaje_cambio_costo_display(self, obj):
        cambio = obj.porcentaje_cambio_costo()
        if cambio > 0:
            return f"+{cambio}%"
        elif cambio < 0:
            return f"{cambio}%"
        return "0%"
    porcentaje_cambio_costo_display.short_description = '% Cambio Costo'

@admin.register(ConfiguracionCostos)
class ConfiguracionCostosAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_modificacion', 'incluir_costos_indirectos', 
        'actualizar_automaticamente', 'redondear_precios'
    ]
    fieldsets = (
        ('Costos Indirectos', {
            'fields': (
                'incluir_costos_indirectos',
                'costo_envases_por_kg',
                'costo_etiquetas_por_unidad',
                'costo_envio_promedio'
            )
        }),
        ('Mano de Obra', {
            'fields': (
                'tiempo_fraccionamiento_por_kg',
                'valor_hora_trabajo'
            )
        }),
        ('Configuraciones Globales', {
            'fields': (
                'actualizar_automaticamente',
                'redondear_precios'
            )
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionCostos.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False


# ==================== 🚀 ADMINISTRADOR HISTORIAL DE PRECIOS ====================
@admin.register(HistorialPreciosMateriaPrima)
class HistorialPreciosMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = [
        'materia_prima', 'fecha_cambio', 'precio_anterior_display', 
        'precio_nuevo_display', 'porcentaje_cambio_display', 
        'productos_afectados_count', 'usuario'
    ]
    list_filter = ['fecha_cambio', 'materia_prima', 'usuario']
    search_fields = ['materia_prima__nombre', 'motivo']
    readonly_fields = [
        'fecha_cambio', 'porcentaje_cambio_display', 
        'diferencia_absoluta_display', 'impacto_economico_display'
    ]
    ordering = ['-fecha_cambio']
    
    def precio_anterior_display(self, obj):
        return f"${obj.precio_anterior:.2f}"
    precio_anterior_display.short_description = 'Precio Anterior'
    
    def precio_nuevo_display(self, obj):
        return f"${obj.precio_nuevo:.2f}"
    precio_nuevo_display.short_description = 'Precio Nuevo'
    
    def porcentaje_cambio_display(self, obj):
        cambio = obj.porcentaje_cambio()
        color = "green" if cambio >= 0 else "red"
        return f'<span style="color: {color};">{cambio:+.2f}%</span>'
    porcentaje_cambio_display.short_description = 'Cambio %'
    porcentaje_cambio_display.allow_tags = True
    
    def diferencia_absoluta_display(self, obj):
        diff = obj.diferencia_absoluta()
        return f"${diff:+.2f}"
    diferencia_absoluta_display.short_description = 'Diferencia'
    
    def impacto_economico_display(self, obj):
        impacto = obj.impacto_economico_estimado()
        return f"${impacto:.2f}"
    impacto_economico_display.short_description = 'Impacto Stock'
    
    def has_add_permission(self, request):
        # Solo lectura - se crean automáticamente
        return False
    
    def has_change_permission(self, request, obj=None):
        # Solo lectura - no modificar historial
        return False