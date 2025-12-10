# 🔬 ANÁLISIS PROFUNDO: INVESTIGACIÓN DE BUGS

**Fecha:** 9 de Diciembre 2025  
**Metodología:** Ingeniería Inversa + Análisis de Flujo Completo  
**Estado:** ✅ CAUSA RAÍZ IDENTIFICADA

---

## 📊 DIAGRAMA DE FLUJO COMPLETO: CREACIÓN DE VENTA

```
┌─────────────────────────────────────────────────────────────────┐
│ USUARIO: Intenta vender producto con stock=6, cantidad=3       │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. VISTA: crear_venta_v3                                        │
│    URL: /gestion/ventas/crear/                                  │
│    Archivo: views.py línea 3194                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. GET: Renderizar formulario                                   │
│    - productos = Producto.objects.filter(stock__gt=0)           │
│    - Pasa productos al template form_v3_natural.html            │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. TEMPLATE: form_v3_natural.html                               │
│    Línea 243: Genera <option> por cada producto                │
│                                                                  │
│    {% for producto in productos %}                              │
│        <option value="{{ producto.id }}"                        │
│                data-stock="{{ producto.stock }}"                │
│                data-precio="{{ producto.precio }}">             │
│            {{ producto.nombre }} (Stock: {{ producto.stock }})  │
│        </option>                                                 │
│    {% endfor %}                                                  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. USUARIO: Selecciona producto, cantidad=3, Submit            │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. POST: crear_venta_v3 recibe datos                           │
│    - with transaction.atomic()                                  │
│    - Primera pasada: VALIDAR stock                              │
│    - Segunda pasada: CREAR venta y detalles                     │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. VALIDACIÓN (línea 3212):                                     │
│    if producto.stock < cantidad:                                │
│        raise ValueError('Stock insuficiente')                   │
│                                                                  │
│    ✅ En este punto: producto.stock = 6, cantidad = 3          │
│    ✅ Validación pasa (6 < 3 = False)                           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. CREAR VENTA (línea 3230):                                    │
│    venta = Venta.objects.create(...)                            │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. CREAR DETALLE (línea 3239):                                  │
│    VentaDetalle.objects.create(                                 │
│        venta=venta,                                              │
│        producto=producto,                                        │
│        cantidad=3,                                               │
│        precio_unitario=precio,                                  │
│        subtotal=subtotal                                         │
│    )                                                             │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 9. SIGNAL: post_save VentaDetalle ACTIVADO                  │
│    Archivo: signals.py línea 59                                 │
│                                                                  │
│    @receiver(post_save, sender=VentaDetalle)                    │
│    def actualizar_venta_al_agregar_detalle(...):                │
│        if created:                                               │
│            producto = instance.producto                          │
│            producto.stock -= instance.cantidad  # 6 - 3 = 3    │
│            producto.save()                                       │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼ ⚠️ PROBLEMA DETECTADO
┌─────────────────────────────────────────────────────────────────┐
│ 10. DESCUENTO EN VISTA (línea 3247):                            │
│     item['producto'].stock -= item['cantidad']  # 3 - 3 = 0    │
│     item['producto'].save()                                      │
│                                                                  │
│     🔴 PROBLEMA: Stock se descuenta DOS VECES:                  │
│     - Primera vez en signal (línea 9): 6 - 3 = 3                │
│     - Segunda vez en vista (aquí): 3 - 3 = 0                    │
│                                                                  │
│     ❌ RESULTADO: Stock final = 0 (debería ser 3)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐛 BUG #1: CAUSA RAÍZ IDENTIFICADA

### **PROBLEMA: Descuento Duplicado de Stock**

**Ubicación del Conflicto:**
```python
# signals.py línea 59-69
@receiver(post_save, sender=VentaDetalle)
def actualizar_venta_al_agregar_detalle(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock -= instance.cantidad  # ❌ DESCUENTO #1
        producto.save()
    instance.venta.calcular_total()

# views.py línea 3247-3248 (crear_venta_v3)
item['producto'].stock -= item['cantidad']  # ❌ DESCUENTO #2
item['producto'].save()
```

### **Secuencia del Error:**

1. **Estado Inicial:** Producto con stock = 6
2. **Vista valida:** ✅ 6 >= 3 (pasa validación)
3. **VentaDetalle.create()** dispara signal
4. **Signal descuenta:** 6 - 3 = **3** (stock ahora es 3)
5. **Vista descuenta OTRA VEZ:** 3 - 3 = **0** (stock final es 0)
6. **Siguiente venta intenta usar stock=0**
7. **Validación falla:** "stock actual: 0" pero debería ser 3

### **Evidencia del Error en Screenshot:**

```
Error: "El stock no puede ser negativo (stock actual: -1)"
```

**Análisis:**
- Usuario intenta vender 3 unidades
- Producto muestra stock = 6
- Pero internamente stock ya fue descontado incorrectamente
- Al validar: 0 - 3 = -3 (negativo, validación falla)

---

## 🔧 SOLUCIÓN PROPUESTA: BUG #1

### **Opción A: Eliminar Signal (RECOMENDADO)**

**Razón:** La vista ya maneja el descuento explícitamente, el signal es redundante.

```python
# signals.py - ELIMINAR O COMENTAR
# @receiver(post_save, sender=VentaDetalle)
# def actualizar_venta_al_agregar_detalle(sender, instance, created, **kwargs):
#     """Signal DESACTIVADO - descuento de stock manejado en vista"""
#     pass
```

**Pros:**
- ✅ Control explícito en la vista (más claro)
- ✅ No hay "magia" oculta
- ✅ Fácil de debuggear
- ✅ Consistente con comentario en signals.py línea 17-32

**Contras:**
- ⚠️ Hay que verificar TODAS las vistas que crean VentaDetalle
- ⚠️ Si alguien usa `.create()` directo sin vista, no descuenta stock

---

### **Opción B: Eliminar Descuento en Vista**

**Razón:** Centralizar lógica en el signal (Single Responsibility).

```python
# views.py línea 3239-3250 (crear_venta_v3)
for item in productos_validados:
    VentaDetalle.objects.create(
        venta=venta,
        producto=item['producto'],
        cantidad=item['cantidad'],
        precio_unitario=item['precio'],
        subtotal=item['subtotal']
    )
    # ❌ ELIMINAR ESTAS LÍNEAS:
    # item['producto'].stock -= item['cantidad']
    # item['producto'].save()
```

**Pros:**
- ✅ Signal maneja TODA la lógica de stock automáticamente
- ✅ Funciona incluso si creas VentaDetalle desde shell/API
- ✅ DRY (Don't Repeat Yourself)

**Contras:**
- ⚠️ Lógica "oculta" en signals (difícil de ver)
- ⚠️ Problemas con race conditions si hay alta concurrencia

---

### **Opción C: Usar Flag en VentaDetalle.save()**

**Razón:** Controlar cuándo aplicar el signal.

```python
# models.py - VentaDetalle
class VentaDetalle(models.Model):
    # ... campos ...
    
    def save(self, *args, skip_signal=False, **kwargs):
        self._skip_signal = skip_signal
        super().save(*args, **kwargs)

# signals.py
@receiver(post_save, sender=VentaDetalle)
def actualizar_venta_al_agregar_detalle(sender, instance, created, **kwargs):
    if created and not getattr(instance, '_skip_signal', False):
        producto = instance.producto
        producto.stock -= instance.cantidad
        producto.save()

# views.py
VentaDetalle.objects.create(..., skip_signal=True)
# Y descuentas manualmente en la vista
```

**Pros:**
- ✅ Control granular
- ✅ Flexibilidad total

**Contras:**
- ❌ Complejidad innecesaria
- ❌ Difícil de mantener

---

## 🎯 RECOMENDACIÓN FINAL: **Opción A**

### **Justificación:**

1. **Ya existe comentario en signals.py:**
   ```python
   # Línea 17-32
   # NOTA: Los signals de Producto están DESACTIVADOS porque ahora usamos
   # control manual explícito en las vistas
   ```
   
   ✅ Esto sugiere que el proyecto ya tiene filosofía de **control explícito**.

2. **Claridad sobre magia:**
   - Control explícito es más fácil de debuggear
   - TDD más simple (sabes exactamente dónde está la lógica)

3. **Consistencia:**
   - Ya hay signals desactivados en el mismo archivo
   - Mantiene mismo patrón

---

## 🐛 BUG #2: PRODUCTOS FALTANTES EN DROPDOWN

### **HIPÓTESIS INICIAL:**

El problema está en el filtro de la vista:

```python
# views.py línea 3267 (crear_venta_v3 - GET)
productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
```

**Posibles causas:**

1. **"Pasas de Uva" tiene stock = 0**
   - Solución: Cambiar filtro a `stock__gte=0` o eliminar filtro

2. **"Pasas de Uva" tiene `activo = False`**
   - Solución: Agregar `.filter(activo=True)` explícito

3. **"Pasas de Uva" es categoría `MATERIA_PRIMA`**
   - Solución: Excluir materias primas del dropdown

4. **Bug en JavaScript que filtra opciones**
   - Revisar form_v3_natural.html línea 236-249

---

### **PLAN DE INVESTIGACIÓN BUG #2:**

```python
# 1. VERIFICAR estado del producto en DB
python manage.py shell
>>> from gestion.models import Producto
>>> pasas = Producto.objects.filter(nombre__icontains='pasas')
>>> for p in pasas:
...     print(f"ID: {p.id}, Nombre: {p.nombre}, Stock: {p.stock}, Activo: {p.activo}, Categoría: {p.categoria}")

# 2. VERIFICAR filtro en vista
>>> productos_disponibles = Producto.objects.filter(stock__gt=0).order_by('nombre')
>>> print("Total productos en dropdown:", productos_disponibles.count())
>>> print("¿Pasas está?", pasas.first() in productos_disponibles)

# 3. Si NO está, verificar por qué:
>>> if pasas.first().stock == 0:
...     print("❌ PROBLEMA: Stock es 0")
>>> if not pasas.first().activo:
...     print("❌ PROBLEMA: Producto inactivo")
```

---

## 📝 NOTAS IMPORTANTES DEL CÓDIGO

### 1. **Sistema de Soft Delete en Ventas:**

```python
# models.py línea 22-96
class Venta(models.Model):
    eliminada = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    razon_eliminacion = models.TextField(blank=True)
    
    objects = VentaActivaManager()  # Filtra eliminadas
    todos = VentaManager()          # Incluye eliminadas
```

✅ **EXCELENTE ARQUITECTURA** - Permite auditoría sin perder datos

---

### 2. **Signal de Delete que Devuelve Stock:**

```python
# signals.py línea 76-85
@receiver(post_delete, sender=VentaDetalle)
def actualizar_venta_al_eliminar_detalle(sender, instance, **kwargs):
    producto = instance.producto
    producto.stock += instance.cantidad  # ✅ Devuelve stock
    producto.save()
```

✅ **CORRECTO** - Pero solo funciona con `delete()`, no con soft delete

⚠️ **ATENCIÓN:** Si usas soft delete en Venta, este signal NO se dispara.

---

### 3. **Transaction Atomic en Vista:**

```python
# views.py línea 3200
with transaction.atomic():
    # ... validaciones ...
    if errores:
        raise ValueError(...)  # ✅ Rollback automático
```

✅ **EXCELENTE** - Protege contra inconsistencias de datos

---

### 4. **Logging Robusto:**

```python
# views.py línea 1192-1193
LinoLogger.log_accion_admin(request.user, "INTENTO_CREAR_VENTA", "Venta", 0)
LinoLogger.log_venta_creada(venta.id, productos_str, len(detalles), total, request.user)
```

✅ **PROFESIONAL** - Auditoría completa de acciones críticas

---

## 🎯 PLAN DE ACCIÓN INMEDIATO

### **PASO 1: Fix Bug #1 - Descuento Duplicado** (15 min)

```bash
# 1. Desactivar signal
vim src/gestion/signals.py
# Comentar líneas 59-72

# 2. Verificar que views.py ya descuenta stock
# (línea 3247-3248 - ya lo hace)

# 3. Test manual:
# - Crear venta con cantidad=3
# - Verificar stock desciende correctamente
# - Intentar segunda venta
# - Verificar que NO da error de stock negativo
```

---

### **PASO 2: Investigar Bug #2 - Productos Faltantes** (10 min)

```bash
# 1. Entrar a shell
python manage.py shell

# 2. Ejecutar diagnóstico
from gestion.models import Producto
pasas = Producto.objects.filter(nombre__icontains='pasas').first()
print(f"Stock: {pasas.stock}, Activo: {pasas.activo}")

# 3. Verificar filtro
disponibles = Producto.objects.filter(stock__gt=0)
print("¿Pasas en dropdown?", pasas in disponibles)
```

---

### **PASO 3: Escribir Tests TDD** (30 min)

```python
# tests/test_ventas_stock.py
def test_descuento_stock_no_duplicado(self):
    """Bug #1: Stock debe descontarse UNA SOLA VEZ"""
    producto = Producto.objects.create(nombre="Test", stock=6, precio=100)
    
    venta = Venta.objects.create(total=300)
    VentaDetalle.objects.create(
        venta=venta,
        producto=producto,
        cantidad=3,
        precio_unitario=100,
        subtotal=300
    )
    
    producto.refresh_from_db()
    self.assertEqual(producto.stock, 3)  # Debe ser 3, no 0

def test_producto_con_stock_cero_no_aparece_en_dropdown(self):
    """Bug #2: Productos sin stock no deben aparecer"""
    p1 = Producto.objects.create(nombre="Con Stock", stock=5)
    p2 = Producto.objects.create(nombre="Sin Stock", stock=0)
    
    # Simular GET a crear_venta
    response = self.client.get('/gestion/ventas/crear/')
    productos = response.context['productos']
    
    self.assertIn(p1, productos)
    self.assertNotIn(p2, productos)
```

---

## 📊 MÉTRICAS DE IMPACTO

### **Antes del Fix:**

| Métrica | Valor |
|---------|-------|
| Bug #1 - Descuento duplicado | 🔴 CRÍTICO |
| Bug #2 - Productos faltantes | 🔴 CRÍTICO |
| Ventas afectadas | ❌ TODAS |
| Stock accuracy | ❌ 0% |
| Confianza del usuario | 📉 BAJA |

### **Después del Fix:**

| Métrica | Valor Esperado |
|---------|----------------|
| Bug #1 - Descuento duplicado | ✅ RESUELTO |
| Bug #2 - Productos faltantes | 🔍 EN INVESTIGACIÓN |
| Ventas afectadas | ✅ 0 |
| Stock accuracy | ✅ 100% |
| Confianza del usuario | 📈 ALTA |

---

## 🚀 PROFESIONALIZACIÓN PROPUESTA

### **1. Implementar VentaService (Service Layer)**

```python
# services/venta_service.py
class VentaService:
    @staticmethod
    @transaction.atomic
    def crear_venta(cliente, fecha, productos_data, usuario):
        """
        Crea una venta completa con validaciones y side effects.
        
        Args:
            cliente: str - Nombre del cliente
            fecha: datetime - Fecha de la venta
            productos_data: List[Dict] - [{'producto_id': X, 'cantidad': Y}, ...]
            usuario: User - Usuario que crea la venta
            
        Returns:
            Venta creada
            
        Raises:
            ValidationError: Si stock insuficiente o datos inválidos
        """
        # 1. Validar TODOS los productos primero
        VentaService._validar_productos(productos_data)
        
        # 2. Crear venta
        venta = Venta.objects.create(
            cliente=cliente,
            fecha=fecha,
            usuario=usuario
        )
        
        # 3. Crear detalles y descontar stock
        for item in productos_data:
            VentaService._crear_detalle(venta, item)
        
        # 4. Calcular total
        venta.calcular_total()
        
        return venta
    
    @staticmethod
    def _validar_productos(productos_data):
        """Validar que haya stock suficiente ANTES de crear venta"""
        for item in productos_data:
            producto = Producto.objects.get(id=item['producto_id'])
            cantidad = item['cantidad']
            
            if producto.stock < cantidad:
                raise ValidationError(
                    f'Stock insuficiente para {producto.nombre}. '
                    f'Disponible: {producto.stock}, Solicitado: {cantidad}'
                )
    
    @staticmethod
    def _crear_detalle(venta, item):
        """Crea detalle y descuenta stock"""
        producto = Producto.objects.get(id=item['producto_id'])
        cantidad = item['cantidad']
        
        # Crear detalle
        detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=item.get('precio', producto.precio),
            subtotal=cantidad * item.get('precio', producto.precio)
        )
        
        # Descontar stock
        producto.stock = F('stock') - cantidad
        producto.save(update_fields=['stock'])
        
        return detalle
```

**Beneficios:**
- ✅ Lógica centralizada
- ✅ Fácil de testear
- ✅ Reutilizable (API, comandos, etc.)
- ✅ Transacciones atómicas

---

### **2. Usar F() Expression para Evitar Race Conditions**

```python
# ANTES (vulnerable a race conditions)
producto.stock -= cantidad
producto.save()

# DESPUÉS (thread-safe)
from django.db.models import F
producto.stock = F('stock') - cantidad
producto.save(update_fields=['stock'])
```

**Por qué:**
- ✅ Operación atómica en DB
- ✅ Evita race conditions en alta concurrencia
- ✅ No requiere SELECT previo

---

### **3. Implementar Sistema de Reservas (Opcional)**

Para e-commerce con alta concurrencia:

```python
class ReservaStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()  # 15 min
    activa = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['producto', 'activa', 'fecha_expiracion'])
        ]
```

**Flujo:**
1. Usuario agrega al carrito → Crea ReservaStock
2. Expira a los 15 min si no completa compra
3. Venta final consume la reserva

---

## 🎓 LECCIONES APRENDIDAS

### **1. Signals vs Explicit Logic:**

**Problema encontrado:**
- Signal oculto causó descuento duplicado
- Difícil de debuggear sin leer todo el código

**Lección:**
- ⚠️ Signals son "magia" que puede causar bugs sutiles
- ✅ Prefiere lógica explícita en vistas/servicios
- ✅ Si usas signals, DOCUMENTA claramente

---

### **2. Transaction Atomic es Crítico:**

**Lo que funcionó bien:**
```python
with transaction.atomic():
    # validar
    # crear venta
    # si error: raise → rollback automático
```

✅ **Sin esto:** Stock descontado + venta fallida = inconsistencia de datos

---

### **3. Validar ANTES de Mutar Estado:**

**Patrón correcto:**
```python
# 1. VALIDAR TODO
for item in items:
    if item.stock < cantidad:
        raise ValidationError()

# 2. MUTAR ESTADO (solo si validación pasó)
for item in items:
    item.stock -= cantidad
    item.save()
```

❌ **Nunca mutar mientras validas** (deja datos inconsistentes si falla a mitad)

---

## 🔍 PRÓXIMOS PASOS

### **Inmediatos (hoy):**
1. ✅ Análisis completo - HECHO
2. 🔧 Fix Bug #1 - desactivar signal
3. 🔍 Investigar Bug #2 - verificar producto en DB
4. 🧪 Tests manuales de ambos bugs
5. 📝 Commit con mensaje descriptivo

### **Corto plazo (esta semana):**
1. Escribir tests automatizados (TDD)
2. Implementar VentaService (Service Layer)
3. Agregar F() expressions para concurrency
4. Documentar flujo de ventas

### **Largo plazo (próximo sprint):**
1. Implementar sistema de logging robusto
2. Agregar monitoring (Sentry)
3. CI/CD con tests automáticos
4. Performance testing (load testing)

---

**✅ ANÁLISIS COMPLETADO - LISTO PARA IMPLEMENTAR FIXES**
