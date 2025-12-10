# 🏗️ INGENIERÍA DE SOFTWARE APLICADA A LINO SALUDABLE

**Fecha:** 2 de Diciembre 2025  
**Proyecto:** Sistema Lino - Gestión Integral  
**Objetivo:** Profesionalizar el desarrollo mediante principios de Ingeniería de Software

---

## 📚 ÍNDICE

1. [Principios Fundamentales](#1-principios-fundamentales)
2. [Ciclo de Vida del Software](#2-ciclo-de-vida-del-software)
3. [Test-Driven Development (TDD)](#3-test-driven-development-tdd)
4. [Patrones de Diseño](#4-patrones-de-diseño)
5. [Arquitectura del Sistema](#5-arquitectura-del-sistema)
6. [Metodología Ágil](#6-metodología-ágil)
7. [Control de Versiones](#7-control-de-versiones)
8. [Plan de Mejora](#8-plan-de-mejora)

---

## 1️⃣ PRINCIPIOS FUNDAMENTALES

### 🎯 **El Desafío del Software**

> **"El software es diferente a cualquier otra ingeniería: los planos deben ser super flexibles porque las necesidades del negocio cambian constantemente"**

#### ¿Por qué el software es único?

```
Edificio Tradicional          |  Software
-----------------------------  |  -----------------------------
✓ Planos son sagrados          |  ✗ Planos deben ser flexibles
✓ Cambios son costosos         |  ✓ Cambios son inevitables
✓ Estructura física estática   |  ✓ Estructura lógica dinámica
✓ Deterioro por uso            |  ✓ "Deterioro" por cambios
```

#### Leyes de Lehman (Evolución del Software)

Estas leyes describen cómo el software evoluciona con el tiempo:

1. **Cambio Continuo**
   - *"Un programa debe cambiar o se vuelve inútil"*
   - **Aplicado a Lino:** Constantemente agregamos features (dashboard rentabilidad, alertas, recetas)

2. **Complejidad Creciente**
   - *"La estructura tiende a volverse más compleja con cada cambio"*
   - **Riesgo en Lino:** Sin refactoring, el sistema se vuelve caótico
   - **Solución:** Limpieza regular (como la que acabamos de hacer)

3. **Declive de Calidad**
   - *"La calidad disminuirá si no se adapta activamente"*
   - **Aplicado a Lino:** Necesitamos tests y verificación constante

---

## 2️⃣ CICLO DE VIDA DEL SOFTWARE

### 📊 **Fases del Proyecto**

```
┌─────────────────────────────────────────────────────────┐
│  FASE 1: Desarrollo Inicial (✅ COMPLETADO)            │
│  - Modelos de datos (17 modelos)                       │
│  - CRUD básico de productos, ventas, compras           │
│  - Dashboard inicial                                    │
│  - Deployment en Railway                               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  FASE 2: Evolución (🔄 EN PROGRESO)                   │
│  - Dashboard rentabilidad                              │
│  - Sistema de alertas                                  │
│  - Recetas y costos                                    │
│  - Mejoras de UI/UX                                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  FASE 3: Servicio (📅 PRÓXIMA)                        │
│  - Mantenimiento y pequeñas mejoras                    │
│  - Optimizaciones de performance                       │
│  - Corrección de bugs menores                          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  FASE 4: Retiro (🔮 FUTURO)                           │
│  - Migración a nueva tecnología                        │
│  - API REST para app móvil                             │
│  - Rediseño completo (si es necesario)                 │
└─────────────────────────────────────────────────────────┘
```

### 💰 **Distribución Real de Costos**

Según estudios de ingeniería de software:

```
Mantenimiento y Evolución: 69% ████████████████████████████
Desarrollo Inicial:        17% ████████
Corrección de Errores:     14% ██████
```

**Lección para Lino:**
- El 69% del esfuerzo será agregar nuevas funcionalidades
- Debemos diseñar pensando en el cambio
- El código debe ser fácil de modificar

---

## 3️⃣ TEST-DRIVEN DEVELOPMENT (TDD)

### 🔴🟢🔧 **Ciclo Rojo-Verde-Refactorizar**

```
┌──────────────┐
│ 1. ROJO      │  Escribir test que falla
│   (Write)    │  Ejemplo: test_crear_venta_descuenta_stock()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 2. VERDE     │  Escribir código mínimo para pasar
│   (Pass)     │  Ejemplo: venta.save() → producto.stock -= cantidad
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 3. REFACTOR  │  Mejorar el código manteniendo tests verdes
│   (Improve)  │  Ejemplo: Mover lógica a signal post_save
└──────────────┘
```

### 📝 **Ejemplo Práctico en Lino**

#### ❌ **Forma Tradicional (Sin TDD)**
```python
# 1. Escribimos código primero
def crear_venta(request):
    venta = Venta.objects.create(...)
    producto.stock -= cantidad
    producto.save()
    # ¿Funciona? ¿Qué pasa si stock es negativo?
```

#### ✅ **Forma TDD (Correcta)**
```python
# 1. ROJO: Escribir test primero
def test_crear_venta_descuenta_stock(self):
    """Al crear una venta, el stock del producto debe decrementar"""
    producto = Producto.objects.create(nombre="Test", stock=10)
    venta = Venta.objects.create(total=100)
    detalle = VentaDetalle.objects.create(
        venta=venta,
        producto=producto,
        cantidad=3
    )
    
    producto.refresh_from_db()
    self.assertEqual(producto.stock, 7)  # ❌ FALLA (aún no implementado)

# 2. VERDE: Implementar funcionalidad
@receiver(post_save, sender=VentaDetalle)
def descontar_stock(sender, instance, **kwargs):
    producto = instance.producto
    producto.stock -= instance.cantidad
    producto.save()
    # ✅ PASA

# 3. REFACTORIZAR: Agregar validaciones
@receiver(post_save, sender=VentaDetalle)
def descontar_stock(sender, instance, **kwargs):
    producto = instance.producto
    if producto.stock < instance.cantidad:
        raise ValueError("Stock insuficiente")
    producto.stock -= instance.cantidad
    producto.save()
    # ✅ PASA (con validación)
```

### 🎯 **Beneficios de TDD en Lino**

| Problema Sin Tests | Solución con TDD |
|-------------------|------------------|
| ❌ Bug en producción: venta con stock negativo | ✅ Test detecta el problema antes de deploy |
| ❌ Miedo a refactorizar (¿rompo algo?) | ✅ Tests dan confianza para cambiar código |
| ❌ No sabemos si una feature funciona | ✅ Tests documentan comportamiento esperado |
| ❌ Debugging manual tedioso | ✅ Tests automáticos encuentran bugs |

---

## 4️⃣ PATRONES DE DISEÑO

### 🏗️ **"Los patrones describen mejores prácticas y capturan experiencia para que otros la reutilicen"**

#### Patrones Aplicados en Lino

### 1. **MVC/MVT (Model-View-Template)**

```
┌─────────────────────────────────────────────────┐
│  MODEL (models.py)                              │
│  - Producto, Venta, Compra                      │
│  - Lógica de negocio (calcular_costo)          │
│  - Validaciones (clean)                         │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  VIEW (views.py)                                │
│  - lista_productos, crear_venta                 │
│  - Procesa requests                             │
│  - Llama a servicios                            │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  TEMPLATE (templates/)                          │
│  - lista_productos.html                         │
│  - Presenta datos al usuario                    │
│  - Bootstrap + Chart.js                         │
└─────────────────────────────────────────────────┘
```

**Ventaja:** Separación de responsabilidades (cambiar UI no afecta lógica)

---

### 2. **Service Layer Pattern**

```python
# ❌ MALO: Lógica en la vista
def dashboard(request):
    ventas = Venta.objects.all()
    total = sum(v.total for v in ventas)
    productos_bajo_stock = Producto.objects.filter(stock__lt=F('stock_minimo'))
    # ... más lógica compleja ...
    return render(request, 'dashboard.html', {...})

# ✅ BUENO: Lógica en servicio
# dashboard_service.py
class DashboardService:
    @staticmethod
    def get_metricas_principales():
        return {
            'ventas_totales': Venta.objects.aggregate(Sum('total'))['total__sum'],
            'productos_bajo_stock': Producto.objects.filter(
                stock__lt=F('stock_minimo')
            ).count(),
            ...
        }

# views.py
def dashboard(request):
    metricas = DashboardService.get_metricas_principales()
    return render(request, 'dashboard.html', metricas)
```

**Ventaja:** 
- Vista simple (fácil de entender)
- Servicio reutilizable (dashboard + API + reportes)
- Testeable (mock del servicio)

---

### 3. **Signal Pattern (Observer)**

```python
# Sin signals: código acoplado
def crear_venta_detalle(request):
    detalle = VentaDetalle.objects.create(...)
    detalle.producto.stock -= detalle.cantidad  # ❌ Acoplado
    detalle.producto.save()
    
    # ¿Y si necesitamos crear alerta también?
    if detalle.producto.stock < detalle.producto.stock_minimo:
        Alerta.objects.create(...)  # ❌ Más acoplamiento

# Con signals: desacoplado
@receiver(post_save, sender=VentaDetalle)
def actualizar_stock(sender, instance, **kwargs):
    producto = instance.producto
    producto.stock -= instance.cantidad
    producto.save()

@receiver(post_save, sender=Producto)
def verificar_alerta_stock(sender, instance, **kwargs):
    if instance.stock < instance.stock_minimo:
        Alerta.objects.create(producto=instance, ...)
```

**Ventaja:** 
- Cada componente hace una cosa
- Fácil agregar nuevas acciones (ej: enviar email)
- No modificamos código existente

---

### 4. **Repository Pattern (implícito en Django ORM)**

```python
# Django ORM es un Repository Pattern
productos = Producto.objects.filter(activo=True)  # ✅ Abstrae la BD

# Sin ORM tendríamos que:
cursor.execute("SELECT * FROM producto WHERE activo = 1")  # ❌ SQL crudo
```

**Ventaja:** Cambiamos de SQLite a PostgreSQL sin cambiar código

---

### 5. **Factory Pattern (Forms)**

```python
# Django Forms es un Factory Pattern
form = ProductoForm(request.POST, request.FILES)  # ✅ Crea objeto validado

if form.is_valid():
    producto = form.save()  # Factory crea el Producto
```

---

## 5️⃣ ARQUITECTURA DEL SISTEMA

### 🏛️ **Arquitectura en Capas**

```
┌─────────────────────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN                                   │
│  - Templates HTML (Bootstrap)                           │
│  - JavaScript (Chart.js, AJAX)                          │
│  - CSS (diseño responsive)                              │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Request/Response
                 ▼
┌─────────────────────────────────────────────────────────┐
│  CAPA DE APLICACIÓN (Django Views)                      │
│  - lista_productos, crear_venta                         │
│  - Autenticación y permisos                             │
│  - Orquestación de servicios                            │
└────────────────┬────────────────────────────────────────┘
                 │ Llamadas a servicios
                 ▼
┌─────────────────────────────────────────────────────────┐
│  CAPA DE NEGOCIO (Services)                             │
│  - DashboardService                                     │
│  - RentabilidadService                                  │
│  - AlertasService                                       │
│  - Lógica de dominio compleja                           │
└────────────────┬────────────────────────────────────────┘
                 │ Acceso a datos
                 ▼
┌─────────────────────────────────────────────────────────┐
│  CAPA DE PERSISTENCIA (Models + ORM)                    │
│  - Producto, Venta, Compra                              │
│  - Validaciones de modelo                               │
│  - Signals                                              │
└────────────────┬────────────────────────────────────────┘
                 │ SQL Queries
                 ▼
┌─────────────────────────────────────────────────────────┐
│  BASE DE DATOS                                          │
│  - PostgreSQL (producción)                              │
│  - SQLite (desarrollo)                                  │
└─────────────────────────────────────────────────────────┘
```

### 🎯 **Ventajas de esta Arquitectura**

| Característica | Beneficio |
|----------------|-----------|
| **Separación de capas** | Cambiar UI no afecta lógica de negocio |
| **Testeable** | Podemos testear cada capa independientemente |
| **Mantenible** | Fácil encontrar y corregir bugs |
| **Escalable** | Podemos agregar API REST sin cambiar otras capas |

---

## 6️⃣ METODOLOGÍA ÁGIL

### 🚀 **Programación Extrema (XP) Adaptada**

#### Prácticas que PODEMOS adoptar:

```
✅ 1. Integración Continua
   - Commit frecuente a main
   - Cada commit debe pasar tests
   - Railway deploya automáticamente

✅ 2. Pair Programming (versión adaptada)
   - Giuliano + Claude trabajando juntos
   - Revisión inmediata de código
   - Aprendizaje mutuo

✅ 3. Test-First (TDD)
   - Escribir test antes del código
   - Ciclo rojo-verde-refactor
   - Confianza para cambiar código

✅ 4. Refactoring Constante
   - Limpieza de código obsoleto (como hoy)
   - Mejora continua
   - Nunca dejar "código técnico" acumular

✅ 5. Diseño Simple
   - "Lo más simple que funcione"
   - No sobre-ingenierizar
   - YAGNI (You Aren't Gonna Need It)

⚠️ 6. Propiedad Colectiva del Código
   - Cualquiera puede modificar cualquier parte
   - (En nuestro caso: Giuliano tiene todo el control)

⚠️ 7. Ritmo Sostenible
   - No quemarse
   - Trabajar a un ritmo constante
```

---

### 📊 **Ciclo de Desarrollo Ideal**

```
1️⃣ PLANIFICACIÓN (1 día)
   - Definir feature (ej: "Exportar ventas a Excel")
   - Dividir en tareas pequeñas
   - Estimar esfuerzo

2️⃣ DISEÑO (30 min)
   - Pensar en arquitectura
   - ¿Qué modelos afecta?
   - ¿Qué servicios necesitamos?

3️⃣ TEST PRIMERO (15 min por test)
   - Escribir test que falla
   - Definir comportamiento esperado

4️⃣ IMPLEMENTACIÓN (variable)
   - Escribir código para pasar test
   - Lo más simple posible

5️⃣ REFACTOR (15 min)
   - Mejorar código
   - Tests siguen pasando
   - Eliminar duplicación

6️⃣ VERIFICACIÓN (30 min)
   - Prueba manual completa
   - Tests automáticos
   - Verificar en servidor local

7️⃣ DEPLOY (5 min)
   - Commit + push
   - Railway deploya automático
   - Monitorear logs

8️⃣ MONITOREO (1 hora)
   - Ver logs de producción
   - Verificar que funciona
   - Usuario reporta feedback
```

---

## 7️⃣ CONTROL DE VERSIONES

### 🌿 **Estrategia de Branching**

```
main (producción - Railway)
  ├── dev/feature-exportar-excel
  ├── dev/fix-stock-negativo
  ├── dev/mejora-dashboard
  └── hotfix/bug-critico-venta
```

### 📝 **Mensajes de Commit Convencionales**

```
feat:     Nueva funcionalidad
fix:      Corrección de bug
refactor: Mejora de código sin cambiar funcionalidad
test:     Agregar o modificar tests
docs:     Cambios en documentación
style:    Formato, espacios, etc
perf:     Mejoras de performance
chore:    Tareas de mantenimiento
```

**Ejemplo:**
```bash
git commit -m "feat: Agregar exportación de ventas a Excel

- Nuevo botón en lista de ventas
- Usa openpyxl para generar archivo
- Incluye fecha, cliente, total, productos
- Tests añadidos en test_ventas.py
- Probado al 100% en local
"
```

---

## 8️⃣ PLAN DE MEJORA PROFESIONAL

### 🎯 **Roadmap de Profesionalización**

#### **FASE 1: Fundamentos (AHORA - 2 semanas)**

```
✅ Limpieza de proyecto (HECHO HOY)
□ Implementar TDD en nuevas features
□ Crear suite de tests básica
   - test_ventas.py (crear, editar, eliminar)
   - test_productos.py (CRUD completo)
   - test_compras.py (con reversión de stock)
□ Documentar arquitectura actual
□ Definir estándares de código
```

#### **FASE 2: Testing (2-4 semanas)**

```
□ Coverage mínimo 60%
□ Tests de integración
   - Flujo completo: Producto → Venta → Stock
   - Flujo completo: Compra → MP → Lote
□ Tests E2E básicos
   - Login → Dashboard → Crear Venta
□ CI/CD con GitHub Actions
   - Tests automáticos en PR
   - Deploy automático solo si tests pasan
```

#### **FASE 3: Arquitectura (1 mes)**

```
□ Migrar toda la lógica de negocio a Services
□ Implementar API REST (Django REST Framework)
   - Endpoints para app móvil
   - Documentación Swagger
□ Separar frontend (opcional: React/Vue)
□ Cache con Redis
   - Dashboard metrics
   - Productos más vendidos
```

#### **FASE 4: Calidad (continuo)**

```
□ Code Review sistemático
□ Linting automático (pylint, black)
□ Type hints (Python typing)
□ Documentación de código (docstrings)
□ Performance monitoring (Django Debug Toolbar)
□ Error tracking (Sentry)
```

---

### 📚 **Métricas de Calidad**

#### Métricas a Medir:

```python
1. Test Coverage
   Target: >60% (actual: ~20%)
   
2. Code Complexity (Cyclomatic)
   Target: <10 por función
   
3. Code Duplication
   Target: <5%
   
4. Response Time
   Target: <500ms para el 95% de requests
   
5. Error Rate
   Target: <0.1%
   
6. Deployment Frequency
   Target: 1-2 deploys por semana
   
7. Mean Time to Recovery
   Target: <1 hora
```

---

### 🛠️ **Herramientas Profesionales**

#### Para Implementar:

```
✅ Git + GitHub (ya tenemos)
✅ Railway (ya tenemos)
✅ Django + PostgreSQL (ya tenemos)

□ Testing:
   - pytest (mejor que unittest)
   - pytest-django
   - pytest-cov (coverage)
   - factory_boy (test fixtures)
   - faker (datos de prueba)

□ Code Quality:
   - pylint o flake8 (linting)
   - black (formatting automático)
   - mypy (type checking)
   - pre-commit hooks

□ Monitoring:
   - Sentry (error tracking)
   - Prometheus + Grafana (métricas)
   - Django Debug Toolbar (dev)

□ Documentation:
   - Sphinx (docs automáticas)
   - MkDocs (wiki del proyecto)
   - Swagger/OpenAPI (API docs)

□ CI/CD:
   - GitHub Actions
   - Tests automáticos
   - Deploy automático staging
```

---

## 🎓 CONCEPTOS CLAVE A RECORDAR

### 1. **SOLID Principles**

```
S - Single Responsibility: Una clase = una responsabilidad
O - Open/Closed: Abierto a extensión, cerrado a modificación
L - Liskov Substitution: Subclases intercambiables
I - Interface Segregation: Interfaces pequeñas y específicas
D - Dependency Inversion: Depender de abstracciones
```

### 2. **DRY (Don't Repeat Yourself)**

```python
# ❌ MALO: Código duplicado
def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    return render(...)

def api_productos(request):
    productos = Producto.objects.filter(activo=True)  # Duplicado
    return JsonResponse(...)

# ✅ BUENO: Extraer a función
def get_productos_activos():
    return Producto.objects.filter(activo=True)

def lista_productos(request):
    productos = get_productos_activos()
    return render(...)

def api_productos(request):
    productos = get_productos_activos()
    return JsonResponse(...)
```

### 3. **YAGNI (You Aren't Gonna Need It)**

```
❌ No implementar features "por si acaso"
✅ Implementar solo lo que necesitamos AHORA
✅ Pero diseñar para que sea fácil agregar después
```

### 4. **KISS (Keep It Simple, Stupid)**

```
✅ Simplicidad > Complejidad
✅ Código legible > Código "inteligente"
✅ Solución directa > Sobre-ingeniería
```

---

## 🚦 VERIFICACIÓN PRE-COMMIT

### Checklist Obligatorio:

```bash
# 1. Tests pasan
□ python manage.py test

# 2. Sin errores de Django
□ python manage.py check --deploy

# 3. Servidor funciona
□ python manage.py runserver
□ Probar manualmente features modificadas

# 4. Git limpio
□ git status (sin archivos indeseados)
□ git diff (revisar cambios)

# 5. Commit descriptivo
□ Mensaje siguiendo convención
□ Descripción de qué cambió y por qué

# 6. Push solo si TODO está OK
□ Tests ✓
□ Manual testing ✓
□ Backup existe ✓
```

---

## 📊 ESTADO ACTUAL vs IDEAL

| Aspecto | Estado Actual | Estado Ideal | Gap |
|---------|---------------|--------------|-----|
| **Tests** | ~20% coverage | >60% coverage | 40% |
| **Documentación** | Básica | Completa | Media |
| **CI/CD** | Manual | Automático | Alto |
| **Code Review** | Ninguno | Sistemático | Alto |
| **Monitoring** | Logs básicos | Sentry + Metrics | Alto |
| **Architecture** | Monolito | Service-oriented | Medio |
| **Type Safety** | Ninguno | Type hints | Medio |

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### Esta Semana:

```
1. ✅ Limpieza de proyecto (HECHO)
2. □ Crear documento de arquitectura
3. □ Implementar primer test TDD
4. □ Documentar módulo de ventas
5. □ Configurar GitHub Actions básico
```

### Este Mes:

```
1. □ Suite de tests básica (>30% coverage)
2. □ Refactorizar vista más compleja a Service
3. □ Implementar logging estructurado
4. □ Crear API REST básica (1-2 endpoints)
```

---

## 📚 RECURSOS RECOMENDADOS

### Libros:
- Clean Code (Robert C. Martin)
- Test-Driven Development (Kent Beck)
- Refactoring (Martin Fowler)
- Domain-Driven Design (Eric Evans)

### Cursos:
- Test-Driven Development with Django
- Django REST Framework
- Software Architecture Patterns

### Herramientas:
- Django Debug Toolbar
- pytest + pytest-django
- black (code formatter)
- GitHub Actions

---

## 💡 CONCLUSIÓN

### El Software es una Disciplina de Ingeniería

```
NO es solo "hacer que funcione"
ES:
  ✓ Diseñar para el cambio
  ✓ Probar sistemáticamente  
  ✓ Documentar decisiones
  ✓ Refactorizar constantemente
  ✓ Pensar en el equipo (futuro yo = equipo)
```

### Lema para Lino Saludable:

> **"Código limpio, tests verdes, deploy seguro"**

---

**Última actualización:** 2 de Diciembre 2025  
**Autor:** Claude AI + Giuliano Zulatto  
**Versión:** 1.0

---

🏗️ **Sistema profesional en construcción - Un paso a la vez**
