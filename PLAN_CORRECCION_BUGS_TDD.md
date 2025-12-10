# 🔴 PLAN DE CORRECCIÓN DE BUGS - TDD APLICADO

**Fecha:** 2 de Diciembre 2025 20:10  
**Metodología:** Test-Driven Development (Rojo-Verde-Refactor)  
**Prioridad:** 🔴 CRÍTICA (errores afectan funcionalidad principal)

---

## 👤 CREDENCIALES DE ACCESO LOCAL

### Para Login en http://127.0.0.1:8000

```
Usuario 1 (Recomendado):
  Username: sister_emprendedora
  Password: SisterLino2025!
  Rol: Superadmin

Usuario 2:
  Username: el_super_creador
  Password: CreadorLino2025!
  Rol: Superadmin
```

**⚠️ IMPORTANTE:** Estas son contraseñas de desarrollo. En producción usar variables de entorno.

---

## 🐛 BUGS IDENTIFICADOS

### 🔴 **BUG #1: Stock Negativo en Validación**

**Descripción del Error:**
```
Producto tiene stock = 6
Usuario intenta vender cantidad = 3
Sistema dice: "El stock no puede ser negativo (stock actual: -1)"
```

**Diagnóstico Inicial:**
- Hay una contradicción en la lógica de validación
- El mensaje dice "stock actual: -1" pero el producto tiene 6 unidades
- Posible problema: validación se ejecuta ANTES o DESPUÉS del descuento incorrecto

**Impacto:** 🔴 CRÍTICO - Bloquea las ventas completamente

---

### 🔴 **BUG #2: Productos Faltantes en Formulario de Ventas**

**Descripción del Error:**
```
Producto: "Pasas de Uva" (categoría GRANEL o PREPARADO)
Visible en: Lista de productos ✅
Visible en: Formulario de ventas ❌
```

**Diagnóstico Inicial:**
- Posible filtro incorrecto en la vista de crear venta
- ¿Solo muestra productos con stock > 0?
- ¿Filtro por categoría excluye algunos productos?
- ¿Productos activos = False?

**Impacto:** 🔴 CRÍTICO - No se pueden vender ciertos productos

---

## 🔬 ANÁLISIS TÉCNICO (Pre-TDD)

### Investigación Necesaria:

1. **Revisar modelo Producto:**
   - Campo `stock`
   - Validaciones en `clean()`
   - Método `stock_disponible()`

2. **Revisar modelo VentaDetalle:**
   - Signal `post_save`
   - Lógica de descuento de stock

3. **Revisar vista crear_venta:**
   - QuerySet de productos disponibles
   - Filtros aplicados
   - JavaScript del formulario

4. **Revisar signals:**
   - ¿Hay signal que modifica stock antes de validar?
   - Orden de ejecución de signals

---

## 🧪 PLAN TDD - BUG #1: Stock Negativo

### FASE 1: REPRODUCIR EL BUG (Rojo)

#### Test 1.1: Verificar stock antes de venta
```python
# tests/test_ventas_stock.py
def test_producto_tiene_stock_suficiente(self):
    """Un producto con stock 6 debe permitir vender 3 unidades"""
    # Arrange
    producto = Producto.objects.create(
        nombre="Test Producto",
        stock=6,
        precio=100,
        activo=True
    )
    
    # Assert BEFORE
    self.assertEqual(producto.stock, 6)
    
    # Act
    venta = Venta.objects.create(total=300)
    detalle = VentaDetalle.objects.create(
        venta=venta,
        producto=producto,
        cantidad=3,
        precio_unitario=100
    )
    
    # Assert AFTER
    producto.refresh_from_db()
    self.assertEqual(producto.stock, 3)  # Debe quedar 3
```

#### Test 1.2: Reproducir el bug exacto
```python
def test_bug_stock_negativo_mensaje_incorrecto(self):
    """Reproducir: stock=6, venta=3, error dice stock=-1"""
    producto = Producto.objects.create(
        nombre="Test",
        stock=6,
        precio=100
    )
    
    venta = Venta.objects.create(total=300)
    
    # Esto NO debería fallar, pero actualmente falla
    with self.assertRaises(ValidationError) as cm:
        detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=producto,
            cantidad=3
        )
    
    # El error dice que stock es -1, pero debería ser 3
    self.assertIn("stock actual: -1", str(cm.exception))
    # Este test DEBERÍA FALLAR si encontramos el bug
```

---

### FASE 2: INVESTIGAR CÓDIGO ACTUAL

**Archivos a revisar:**
1. `src/gestion/models.py` - Líneas 310-950 (Producto, VentaDetalle)
2. `src/gestion/signals.py` - Signals de descuento de stock
3. `src/gestion/views.py` - Vista crear_venta
4. `src/gestion/forms.py` - VentaDetalleForm validaciones

---

### FASE 3: HIPÓTESIS DEL BUG #1

**Hipótesis 1:** Signal se ejecuta dos veces
```python
# Signal descuenta stock al crear VentaDetalle
@receiver(post_save, sender=VentaDetalle)
def descontar_stock(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock -= instance.cantidad  # Se ejecuta
        producto.save()  # Esto dispara otro signal?
```

**Hipótesis 2:** Validación ocurre DESPUÉS del descuento
```python
# Orden de ejecución:
1. VentaDetalle.save() llamado
2. Signal post_save descuenta stock (6 - 3 = 3)
3. Validación clean() se ejecuta
4. clean() ve stock=3, pero valida contra cantidad original?
```

**Hipótesis 3:** Hay un pre_save signal que descuenta antes
```python
@receiver(pre_save, sender=VentaDetalle)
def validar_stock(sender, instance, **kwargs):
    producto = instance.producto
    producto.stock -= instance.cantidad  # Descuenta aquí
    # Luego post_save descuenta de nuevo -> stock negativo
```

---

### FASE 4: SOLUCIÓN PROPUESTA (Verde)

**Solución Correcta:**
```python
# 1. ELIMINAR descuento en pre_save (si existe)
# 2. VALIDAR en clean() ANTES de guardar
# 3. DESCONTAR en post_save UNA SOLA VEZ

# models.py - VentaDetalle
class VentaDetalle(models.Model):
    # ... campos ...
    
    def clean(self):
        """Validar ANTES de guardar"""
        super().clean()
        
        # Validar stock disponible
        if self.producto.stock < self.cantidad:
            raise ValidationError(
                f'Stock insuficiente para {self.producto.nombre}. '
                f'Stock disponible: {self.producto.stock}, '
                f'Cantidad solicitada: {self.cantidad}'
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecutar validaciones
        super().save(*args, **kwargs)

# signals.py
@receiver(post_save, sender=VentaDetalle)
def descontar_stock_venta(sender, instance, created, **kwargs):
    """Descontar stock SOLO al crear (no al editar)"""
    if created:  # Solo si es nuevo
        producto = instance.producto
        producto.stock = F('stock') - instance.cantidad
        producto.save(update_fields=['stock'])
```

---

## 🧪 PLAN TDD - BUG #2: Productos Faltantes

### FASE 1: REPRODUCIR EL BUG (Rojo)

#### Test 2.1: Verificar que producto existe
```python
def test_producto_pasas_existe_y_activo(self):
    """El producto Pasas de Uva debe existir y estar activo"""
    pasas = Producto.objects.get(nombre__icontains="pasas")
    self.assertTrue(pasas.activo)
    self.assertGreater(pasas.stock, 0)
```

#### Test 2.2: Verificar que aparece en formulario
```python
def test_producto_aparece_en_formulario_venta(self):
    """Pasas debe aparecer en opciones de venta"""
    pasas = Producto.objects.get(nombre__icontains="pasas")
    
    # Simular request GET a crear_venta
    response = self.client.get('/gestion/ventas/crear/')
    
    # El producto debe estar en el contexto
    productos_disponibles = response.context['productos']
    self.assertIn(pasas, productos_disponibles)
```

---

### FASE 2: INVESTIGAR CÓDIGO ACTUAL

**Archivos a revisar:**
1. `src/gestion/views.py` - Vista `crear_venta`
2. `src/gestion/templates/*/crear_venta.html` - Formulario
3. JavaScript que carga productos dinámicamente

---

### FASE 3: HIPÓTESIS DEL BUG #2

**Hipótesis 1:** Filtro excluye productos GRANEL
```python
# views.py - crear_venta
def crear_venta(request):
    productos = Producto.objects.filter(
        activo=True,
        categoria='PREPARADO'  # ❌ Excluye GRANEL
    )
```

**Hipótesis 2:** Stock = 0 excluye producto
```python
productos = Producto.objects.filter(
    activo=True,
    stock__gt=0  # ❌ Excluye si stock es 0
)
```

**Hipótesis 3:** JavaScript filtra incorrectamente
```javascript
// crear_venta.html
productos.filter(p => p.categoria === 'PREPARADO')
// ❌ Solo muestra preparados
```

---

### FASE 4: SOLUCIÓN PROPUESTA (Verde)

**Solución Correcta:**
```python
# views.py
def crear_venta(request):
    # Incluir TODOS los productos activos con stock
    productos = Producto.objects.filter(
        activo=True,
        stock__gt=0
    ).order_by('nombre')
    
    # O si queremos permitir venta con stock 0 (bajo pedido):
    productos = Producto.objects.filter(
        activo=True
    ).exclude(
        categoria='MATERIA_PRIMA'  # Solo excluir MP
    ).order_by('nombre')
```

---

## 🔍 AUDITORÍA COMPLETA DEL SISTEMA

### Herramienta: Sistema de Auditoría Automática

Voy a crear un script que detecte automáticamente:

```
✅ Verificaciones a Realizar:

1. MODELOS:
   - Validaciones faltantes
   - Fields sin constraints
   - Métodos sin try/except
   - Signals duplicados

2. VISTAS:
   - QuerySets sin filtros de seguridad
   - Ausencia de permisos
   - Transacciones sin atomic
   - N+1 queries

3. TEMPLATES:
   - CSRF tokens faltantes
   - Inputs sin validación
   - XSS vulnerabilities

4. JAVASCRIPT:
   - Validaciones solo en cliente
   - AJAX sin manejo de errores
   - Race conditions

5. TESTS:
   - Coverage < 60%
   - Tests faltantes para bugs conocidos
   - Assertions débiles
```

---

## 🚀 PLAN DE EJECUCIÓN

### Orden de Trabajo:

```
FASE 1: SETUP (15 min)
  ✓ Login con credenciales
  ✓ Verificar sistema funciona básicamente
  ✓ Crear rama dev/fix-bugs-criticos

FASE 2: BUG #1 - Stock Negativo (1-2 horas)
  1. Escribir tests que reproducen el bug (Rojo)
  2. Investigar código actual
  3. Identificar causa raíz
  4. Implementar fix (Verde)
  5. Refactorizar
  6. Verificar manualmente
  7. Commit

FASE 3: BUG #2 - Productos Faltantes (1 hora)
  1. Escribir tests (Rojo)
  2. Investigar filtros en vista
  3. Implementar fix (Verde)
  4. Verificar manualmente
  5. Commit

FASE 4: AUDITORÍA AUTOMÁTICA (30 min)
  1. Ejecutar script de auditoría
  2. Generar reporte de problemas
  3. Priorizar fixes

FASE 5: PROFESIONALIZACIÓN (continuo)
  1. Agregar tests faltantes
  2. Mejorar arquitectura (Service Layer)
  3. Documentar código crítico
  4. Setup CI/CD
```

---

## 💡 PROPUESTAS DE PROFESIONALIZACIÓN

### 1. **Implementar Service Layer**

**Problema Actual:**
```python
# views.py - Lógica mezclada
def crear_venta(request):
    if request.method == 'POST':
        venta = Venta.objects.create(...)
        for producto_data in productos:
            detalle = VentaDetalle.objects.create(...)
            producto.stock -= cantidad  # ❌ Lógica en vista
            producto.save()
            if producto.stock < producto.stock_minimo:
                Alerta.objects.create(...)  # ❌ Más lógica
```

**Solución Profesional:**
```python
# services/venta_service.py
class VentaService:
    @staticmethod
    @transaction.atomic
    def crear_venta_completa(cliente, productos_data):
        """
        Crea una venta con todos los detalles y side effects.
        
        Args:
            cliente: str
            productos_data: List[Dict] con producto_id y cantidad
            
        Returns:
            Venta creada
            
        Raises:
            ValidationError si stock insuficiente
        """
        # 1. Validar stock de TODOS los productos primero
        VentaService._validar_stock_suficiente(productos_data)
        
        # 2. Crear venta
        venta = Venta.objects.create(cliente=cliente)
        
        # 3. Crear detalles
        for data in productos_data:
            VentaService._crear_detalle(venta, data)
        
        # 4. Calcular total
        venta.calcular_total()
        
        return venta
    
    @staticmethod
    def _validar_stock_suficiente(productos_data):
        """Validar ANTES de crear cualquier cosa"""
        for data in productos_data:
            producto = Producto.objects.get(id=data['producto_id'])
            if producto.stock < data['cantidad']:
                raise ValidationError(
                    f'Stock insuficiente para {producto.nombre}'
                )

# views.py - Vista limpia
def crear_venta(request):
    if request.method == 'POST':
        try:
            venta = VentaService.crear_venta_completa(
                cliente=request.POST['cliente'],
                productos_data=request.POST.getlist('productos')
            )
            messages.success(request, 'Venta creada')
            return redirect('detalle_venta', venta.id)
        except ValidationError as e:
            messages.error(request, str(e))
```

**Beneficios:**
- ✅ Vista simple (solo maneja HTTP)
- ✅ Servicio testeable independientemente
- ✅ Transacción atómica (todo o nada)
- ✅ Reutilizable (API, comandos, etc)

---

### 2. **Implementar Logging Estructurado**

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/lino.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'gestion': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
}

# services/venta_service.py
import logging
logger = logging.getLogger('gestion')

class VentaService:
    @staticmethod
    def crear_venta_completa(cliente, productos_data):
        logger.info(f'Creando venta para {cliente}')
        try:
            venta = ...
            logger.info(f'Venta {venta.id} creada exitosamente')
            return venta
        except Exception as e:
            logger.error(f'Error al crear venta: {e}', exc_info=True)
            raise
```

---

### 3. **Implementar Cache para Performance**

```python
# services/dashboard_service.py
from django.core.cache import cache

class DashboardService:
    @staticmethod
    def get_metricas_principales():
        # Cachear métricas por 5 minutos
        cache_key = 'dashboard_metricas'
        metricas = cache.get(cache_key)
        
        if metricas is None:
            metricas = {
                'ventas_totales': Venta.objects.aggregate(
                    Sum('total')
                )['total__sum'],
                'productos_bajo_stock': Producto.objects.filter(
                    stock__lt=F('stock_minimo')
                ).count(),
                # ... más métricas ...
            }
            cache.set(cache_key, metricas, 300)  # 5 min
        
        return metricas
```

---

### 4. **Implementar Validaciones en Capas**

```python
# Capa 1: Validación de Django Forms
class VentaForm(forms.Form):
    cliente = forms.CharField(max_length=200)
    
    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']
        if not cliente:
            raise ValidationError('Cliente requerido')
        return cliente

# Capa 2: Validación de Modelo
class Venta(models.Model):
    def clean(self):
        if self.total < 0:
            raise ValidationError('Total no puede ser negativo')

# Capa 3: Validación de Servicio
class VentaService:
    @staticmethod
    def _validar_reglas_negocio(venta):
        """Reglas complejas de negocio"""
        if venta.total > 100000:
            # Ventas grandes requieren aprobación
            raise ValidationError('Venta requiere aprobación gerencial')
```

---

## 📊 MÉTRICAS DE ÉXITO

### Antes vs Después:

| Métrica | Antes | Meta | Herramienta |
|---------|-------|------|-------------|
| **Bugs Críticos** | 2 | 0 | Tests |
| **Test Coverage** | ~20% | >60% | pytest-cov |
| **Response Time** | ? | <500ms | Django Debug Toolbar |
| **Code Complexity** | ? | <10 | pylint |
| **Error Rate** | ? | <0.1% | Sentry |
| **Deployment Time** | Manual | <5 min | GitHub Actions |

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

1. **Login y verificación manual** (5 min)
2. **Reproducir Bug #1 manualmente** (5 min)
3. **Reproducir Bug #2 manualmente** (5 min)
4. **Empezar TDD para Bug #1** (empezar por los tests)

---

**¿Listo para empezar?** 🚀

Vamos a aplicar ingeniería de software profesional paso a paso!
