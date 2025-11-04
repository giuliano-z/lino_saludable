# 🔔 FASE 3: SISTEMA DE ALERTAS UI - Plan de Implementación

**Proyecto:** LINO Dashboard Inteligente  
**Fase:** 3 de 6  
**Estado:** 🟡 Pendiente  
**Prioridad:** Alta  
**Tiempo Estimado:** 2.5 horas  
**Fecha Inicio Planeada:** 4 de Noviembre de 2025, ~19:00  

---

## 📋 PREREQUISITOS

### ✅ Completados (FASE 1 + FASE 2)
- [x] Backend services (DashboardService, AlertasService)
- [x] Hero Section con saludo dinámico
- [x] 4 KPI Cards funcionales
- [x] Gráficos Chart.js (Evolución Ventas + Top 5 Productos)
- [x] Filtros período y comparación
- [x] Testing Manual 97.8% (91/93 items)
- [x] Testing Automatizado 97% (32/33 tests)
- [x] 21 bugs resueltos
- [x] Colores LINO aplicados consistentemente

### ⚠️ Pendiente (No Bloqueante)
- [ ] Bug #20: Scroll jump al cambiar período (baja prioridad)
- [ ] Issue #3: Productos destacados hardcodeados (media prioridad)
- [ ] Issue #4: Actividad reciente vacía (media prioridad)

**DECISIÓN:** Proceder con FASE 3 ✅

---

## 🎯 OBJETIVOS DE FASE 3

### Funcionalidades Core
1. **Navbar Bell Icon** con badge contador de alertas no leídas
2. **Slide-in Alert Panel** (sidebar derecho) con últimas 5 alertas
3. **Alerts List Page** completa con filtros y paginación
4. **AJAX Mark as Read** sin recargar página
5. **Real-time Updates** del contador cada 60 segundos

### UX Goals
- ✅ Notificaciones visibles desde cualquier página
- ✅ Panel no intrusivo (slide-in, no modal)
- ✅ Marcar leídas sin interrumpir flujo
- ✅ Colores según nivel (danger/warning/info)
- ✅ Responsive mobile/tablet/desktop

### Performance Goals
- ✅ API `/api/alertas/count/` < 50ms
- ✅ Panel render < 100ms
- ✅ AJAX update < 100ms
- ✅ No reloads innecesarios

---

## 📐 ARQUITECTURA

### Backend (Django)

#### Nuevos Endpoints
```python
# gestion/urls.py
urlpatterns += [
    # API endpoints
    path('api/alertas/count/', views.alertas_count_api, name='alertas_count'),
    path('api/alertas/no-leidas/', views.alertas_no_leidas_api, name='alertas_no_leidas'),
    path('api/alertas/<int:alerta_id>/marcar-leida/', views.marcar_alerta_leida, name='marcar_alerta_leida'),
    
    # UI endpoints
    path('alertas/', views.alertas_lista, name='alertas_lista'),
]
```

#### Nuevas Views (gestion/views.py)
```python
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def alertas_count_api(request):
    """Retorna count de alertas no leídas para el usuario"""
    service = AlertasService()
    count = service.get_alertas_count(usuario=request.user, solo_no_leidas=True)
    return JsonResponse({'count': count})

@login_required
def alertas_no_leidas_api(request):
    """Retorna últimas 5 alertas no leídas para slide-in panel"""
    service = AlertasService()
    alertas = service.get_alertas_usuario(
        usuario=request.user,
        solo_no_leidas=True,
        limit=5
    )
    
    data = [{
        'id': a.id,
        'tipo': a.tipo,
        'nivel': a.nivel,
        'titulo': a.titulo,
        'mensaje': a.mensaje,
        'fecha': a.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
        'icono': a.get_icono(),
    } for a in alertas]
    
    return JsonResponse({'alertas': data})

@require_POST
@login_required
def marcar_alerta_leida(request, alerta_id):
    """Marca una alerta como leída vía AJAX"""
    try:
        alerta = Alerta.objects.get(id=alerta_id, usuario=request.user)
        alerta.leida = True
        alerta.fecha_lectura = timezone.now()
        alerta.save()
        
        return JsonResponse({'success': True})
    except Alerta.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alerta no encontrada'}, status=404)

@login_required
def alertas_lista(request):
    """Página completa de lista de alertas con filtros"""
    service = AlertasService()
    
    # Filtros GET
    tipo = request.GET.get('tipo', None)
    nivel = request.GET.get('nivel', None)
    solo_no_leidas = request.GET.get('no_leidas', False) == 'true'
    
    # Obtener alertas
    alertas = service.get_alertas_usuario(
        usuario=request.user,
        tipo=tipo,
        nivel=nivel,
        solo_no_leidas=solo_no_leidas
    )
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(alertas, 20)
    page = request.GET.get('page', 1)
    alertas_page = paginator.get_page(page)
    
    context = {
        'alertas': alertas_page,
        'tipo_actual': tipo,
        'nivel_actual': nivel,
        'solo_no_leidas': solo_no_leidas,
        'tipos_disponibles': Alerta.TIPOS,
        'niveles_disponibles': Alerta.NIVELES,
    }
    
    return render(request, 'gestion/alertas_lista.html', context)
```

#### Extensión AlertasService (gestion/services/alertas_service.py)
```python
# Agregar método nuevo
def get_alertas_count(self, usuario=None, tipo=None, nivel=None, solo_no_leidas=True):
    """Retorna count de alertas con filtros"""
    queryset = Alerta.objects.all()
    
    if usuario:
        queryset = queryset.filter(usuario=usuario)
    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if nivel:
        queryset = queryset.filter(nivel=nivel)
    if solo_no_leidas:
        queryset = queryset.filter(leida=False)
    
    return queryset.count()
```

---

### Frontend (Templates + JS + CSS)

#### 1. Navbar Bell Icon (base.html)

**Ubicación:** `gestion/templates/gestion/base.html` (línea ~45, dentro del navbar)

```html
<!-- Alertas Bell Icon -->
<li class="nav-item dropdown" id="alertas-dropdown">
    <a class="nav-link position-relative" href="#" 
       id="alertas-bell" 
       data-bs-toggle="dropdown" 
       aria-expanded="false"
       onclick="toggleAlertasPanel(event)">
        <i class="bi bi-bell fs-5"></i>
        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" 
              id="alertas-badge" 
              style="display: none;">
            0
        </span>
    </a>
</li>
```

**CSS (static/css/lino-alertas.css - NUEVO archivo):**
```css
/* Navbar Bell Icon */
#alertas-bell {
    color: #4a5c3a;
    transition: all 0.2s ease;
    cursor: pointer;
}

#alertas-bell:hover {
    color: #6b7a4f;
    transform: scale(1.1);
}

#alertas-badge {
    font-size: 0.65rem;
    padding: 0.25rem 0.4rem;
    background: #dc3545 !important;
    min-width: 18px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1); }
    50% { transform: translate(-50%, -50%) scale(1.1); }
}

#alertas-bell.has-new {
    animation: shake 0.5s ease;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}
```

---

#### 2. Slide-in Alert Panel (alertas_panel.html)

**Archivo:** `gestion/templates/components/alertas_panel.html` (NUEVO)

```html
<!-- Slide-in Alert Panel -->
<div id="alertas-panel" class="alertas-panel">
    <!-- Header -->
    <div class="alertas-panel-header">
        <h5 class="mb-0">
            <i class="bi bi-bell-fill text-lino"></i>
            Notificaciones
        </h5>
        <button type="button" class="btn-close" onclick="closeAlertasPanel()"></button>
    </div>
    
    <!-- Body -->
    <div class="alertas-panel-body" id="alertas-panel-content">
        <!-- Se carga vía AJAX -->
        <div class="text-center py-4">
            <div class="spinner-border text-lino" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="alertas-panel-footer">
        <a href="{% url 'alertas_lista' %}" class="btn btn-sm btn-lino w-100">
            Ver todas las alertas
        </a>
    </div>
</div>

<!-- Overlay -->
<div id="alertas-overlay" class="alertas-overlay" onclick="closeAlertasPanel()"></div>
```

**CSS (static/css/lino-alertas.css):**
```css
/* Slide-in Panel */
.alertas-panel {
    position: fixed;
    top: 0;
    right: -400px; /* Hidden inicialmente */
    width: 400px;
    height: 100vh;
    background: #ffffff;
    box-shadow: -2px 0 10px rgba(0,0,0,0.1);
    z-index: 1050;
    transition: right 0.3s ease;
    display: flex;
    flex-direction: column;
}

.alertas-panel.open {
    right: 0;
}

.alertas-panel-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.alertas-panel-body {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.alertas-panel-footer {
    padding: 1rem;
    border-top: 1px solid #e0e0e0;
}

/* Alerta Item */
.alerta-item {
    padding: 1rem;
    border-left: 4px solid;
    background: #f8f9fa;
    margin-bottom: 0.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.alerta-item:hover {
    background: #e9ecef;
    transform: translateX(-5px);
}

.alerta-item.danger {
    border-left-color: #dc3545;
}

.alerta-item.warning {
    border-left-color: #ffc107;
}

.alerta-item.info {
    border-left-color: #0dcaf0;
}

.alerta-item.success {
    border-left-color: #4a5c3a;
}

.alerta-titulo {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.25rem;
}

.alerta-mensaje {
    font-size: 0.875rem;
    color: #6c757d;
    margin-bottom: 0.5rem;
}

.alerta-fecha {
    font-size: 0.75rem;
    color: #adb5bd;
}

/* Overlay */
.alertas-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1040;
    display: none;
}

.alertas-overlay.show {
    display: block;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .alertas-panel {
        width: 100%;
        right: -100%;
    }
}
```

---

#### 3. JavaScript (static/js/lino-alertas.js - NUEVO archivo)

```javascript
/**
 * LINO Alertas System - FASE 3
 * 
 * Funciones:
 * - updateAlertasBadge(): Actualiza contador navbar
 * - toggleAlertasPanel(): Abre/cierra panel
 * - loadAlertasPanel(): Carga alertas vía AJAX
 * - marcarAlertaLeida(): Marca alerta leída
 * - startAlertasPolling(): Auto-update cada 60s
 */

// Variables globales
let alertasPanelOpen = false;
let alertasPollingInterval = null;

/**
 * Actualiza el badge del navbar con count de alertas no leídas
 */
async function updateAlertasBadge() {
    try {
        const response = await fetch('/gestion/api/alertas/count/');
        const data = await response.json();
        
        const badge = document.getElementById('alertas-badge');
        const bell = document.getElementById('alertas-bell');
        
        if (data.count > 0) {
            badge.textContent = data.count > 99 ? '99+' : data.count;
            badge.style.display = 'block';
            bell.classList.add('has-new');
        } else {
            badge.style.display = 'none';
            bell.classList.remove('has-new');
        }
    } catch (error) {
        console.error('Error updating alertas badge:', error);
    }
}

/**
 * Toggle slide-in panel
 */
function toggleAlertasPanel(event) {
    event.preventDefault();
    
    const panel = document.getElementById('alertas-panel');
    const overlay = document.getElementById('alertas-overlay');
    
    if (alertasPanelOpen) {
        closeAlertasPanel();
    } else {
        panel.classList.add('open');
        overlay.classList.add('show');
        alertasPanelOpen = true;
        
        // Cargar alertas
        loadAlertasPanel();
    }
}

/**
 * Cierra el panel
 */
function closeAlertasPanel() {
    const panel = document.getElementById('alertas-panel');
    const overlay = document.getElementById('alertas-overlay');
    
    panel.classList.remove('open');
    overlay.classList.remove('show');
    alertasPanelOpen = false;
}

/**
 * Carga las últimas 5 alertas no leídas
 */
async function loadAlertasPanel() {
    const content = document.getElementById('alertas-panel-content');
    
    try {
        const response = await fetch('/gestion/api/alertas/no-leidas/');
        const data = await response.json();
        
        if (data.alertas.length === 0) {
            content.innerHTML = `
                <div class="text-center py-5 text-muted">
                    <i class="bi bi-check-circle fs-1"></i>
                    <p class="mt-2">¡Todo al día!</p>
                    <small>No tienes alertas pendientes</small>
                </div>
            `;
            return;
        }
        
        // Render alertas
        let html = '';
        data.alertas.forEach(alerta => {
            html += `
                <div class="alerta-item ${alerta.nivel}" 
                     onclick="marcarAlertaLeida(${alerta.id})">
                    <div class="d-flex align-items-start">
                        <i class="bi ${alerta.icono} fs-4 me-2"></i>
                        <div class="flex-grow-1">
                            <div class="alerta-titulo">${alerta.titulo}</div>
                            <div class="alerta-mensaje">${alerta.mensaje}</div>
                            <div class="alerta-fecha">
                                <i class="bi bi-clock"></i> ${alerta.fecha}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        content.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading alertas panel:', error);
        content.innerHTML = `
            <div class="alert alert-danger">
                Error al cargar alertas
            </div>
        `;
    }
}

/**
 * Marca una alerta como leída
 */
async function marcarAlertaLeida(alertaId) {
    try {
        const response = await fetch(`/gestion/api/alertas/${alertaId}/marcar-leida/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Actualizar badge
            updateAlertasBadge();
            
            // Recargar panel
            loadAlertasPanel();
            
            // Toast notification (opcional)
            showToast('Alerta marcada como leída', 'success');
        }
    } catch (error) {
        console.error('Error marking alerta as read:', error);
    }
}

/**
 * Inicia polling cada 60 segundos
 */
function startAlertasPolling() {
    // Update inmediato
    updateAlertasBadge();
    
    // Polling cada 60s
    alertasPollingInterval = setInterval(() => {
        updateAlertasBadge();
    }, 60000); // 60 segundos
}

/**
 * Helper: Get CSRF token
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Helper: Toast notification
 */
function showToast(message, type = 'info') {
    // Simple toast (puedes usar Bootstrap Toast o librería)
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Auto-start al cargar página
document.addEventListener('DOMContentLoaded', function() {
    startAlertasPolling();
});
```

---

#### 4. Alerts List Page (alertas_lista.html)

**Archivo:** `gestion/templates/gestion/alertas_lista.html` (NUEVO)

```html
{% extends 'gestion/base.html' %}
{% load static %}

{% block title %}Alertas - LINO Dashboard{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/lino-alertas.css' %}">
{% endblock %}

{% block content %}
<div class="container-fluid px-4 py-3">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'dashboard_inteligente' %}">Dashboard</a></li>
            <li class="breadcrumb-item active">Alertas</li>
        </ol>
    </nav>
    
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">
            <i class="bi bi-bell-fill text-lino"></i>
            Gestión de Alertas
        </h2>
        <span class="badge bg-lino">{{ alertas.paginator.count }} total</span>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" id="filtros-form">
                <div class="row g-3">
                    <div class="col-md-3">
                        <label class="form-label">Tipo</label>
                        <select name="tipo" class="form-select">
                            <option value="">Todos</option>
                            {% for tipo_val, tipo_label in tipos_disponibles %}
                            <option value="{{ tipo_val }}" {% if tipo_actual == tipo_val %}selected{% endif %}>
                                {{ tipo_label }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label class="form-label">Nivel</label>
                        <select name="nivel" class="form-select">
                            <option value="">Todos</option>
                            {% for nivel_val, nivel_label in niveles_disponibles %}
                            <option value="{{ nivel_val }}" {% if nivel_actual == nivel_val %}selected{% endif %}>
                                {{ nivel_label }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label class="form-label">Estado</label>
                        <select name="no_leidas" class="form-select">
                            <option value="">Todas</option>
                            <option value="true" {% if solo_no_leidas %}selected{% endif %}>No leídas</option>
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label class="form-label">&nbsp;</label>
                        <button type="submit" class="btn btn-lino w-100">
                            <i class="bi bi-funnel"></i> Filtrar
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Lista de Alertas -->
    <div class="row">
        {% for alerta in alertas %}
        <div class="col-12 mb-3">
            <div class="card alerta-card {% if not alerta.leida %}alerta-no-leida{% endif %}">
                <div class="card-body">
                    <div class="d-flex align-items-start">
                        <!-- Icono -->
                        <div class="alerta-icono alerta-{{ alerta.nivel }} me-3">
                            <i class="bi {{ alerta.get_icono }} fs-3"></i>
                        </div>
                        
                        <!-- Contenido -->
                        <div class="flex-grow-1">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="mb-0">{{ alerta.titulo }}</h5>
                                <small class="text-muted">{{ alerta.fecha_creacion|date:"d/m/Y H:i" }}</small>
                            </div>
                            
                            <p class="text-muted mb-2">{{ alerta.mensaje }}</p>
                            
                            <div class="d-flex gap-2">
                                <span class="badge bg-{{ alerta.get_nivel_color }}">{{ alerta.get_nivel_display }}</span>
                                <span class="badge bg-secondary">{{ alerta.get_tipo_display }}</span>
                                {% if alerta.leida %}
                                <span class="badge bg-success">
                                    <i class="bi bi-check"></i> Leída
                                </span>
                                {% endif %}
                            </div>
                        </div>
                        
                        <!-- Acciones -->
                        <div class="ms-3">
                            {% if not alerta.leida %}
                            <button class="btn btn-sm btn-outline-success" 
                                    onclick="marcarAlertaLeida({{ alerta.id }})">
                                <i class="bi bi-check2"></i> Marcar leída
                            </button>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="text-center py-5 text-muted">
                <i class="bi bi-inbox fs-1"></i>
                <p class="mt-3">No hay alertas con los filtros seleccionados</p>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Paginación -->
    {% if alertas.has_other_pages %}
    <nav class="mt-4">
        <ul class="pagination justify-content-center">
            {% if alertas.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ alertas.previous_page_number }}&tipo={{ tipo_actual }}&nivel={{ nivel_actual }}&no_leidas={{ solo_no_leidas }}">
                    Anterior
                </a>
            </li>
            {% endif %}
            
            {% for num in alertas.paginator.page_range %}
            <li class="page-item {% if alertas.number == num %}active{% endif %}">
                <a class="page-link" href="?page={{ num }}&tipo={{ tipo_actual }}&nivel={{ nivel_actual }}&no_leidas={{ solo_no_leidas }}">
                    {{ num }}
                </a>
            </li>
            {% endfor %}
            
            {% if alertas.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ alertas.next_page_number }}&tipo={{ tipo_actual }}&nivel={{ nivel_actual }}&no_leidas={{ solo_no_leidas }}">
                    Siguiente
                </a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/lino-alertas.js' %}"></script>
{% endblock %}
```

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Backend (60 min)

- [ ] **URLs** (10 min)
  - [ ] Agregar rutas API en `gestion/urls.py`
  - [ ] Agregar ruta UI lista en `gestion/urls.py`

- [ ] **Views** (30 min)
  - [ ] `alertas_count_api()` - Retornar JSON count
  - [ ] `alertas_no_leidas_api()` - Retornar JSON últimas 5
  - [ ] `marcar_alerta_leida()` - POST AJAX update
  - [ ] `alertas_lista()` - Render template con filtros

- [ ] **Services** (10 min)
  - [ ] Agregar `get_alertas_count()` a `AlertasService`

- [ ] **Models** (10 min)
  - [ ] Verificar método `get_icono()` en modelo `Alerta`
  - [ ] Agregar si no existe:
    ```python
    def get_icono(self):
        iconos = {
            'stock_bajo': 'bi-box-seam',
            'vencimiento': 'bi-calendar-x',
            'precio_cambio': 'bi-currency-dollar',
            'stock_critico': 'bi-exclamation-triangle-fill',
        }
        return iconos.get(self.tipo, 'bi-info-circle')
    ```

### Frontend (90 min)

- [ ] **CSS** (20 min)
  - [ ] Crear `static/css/lino-alertas.css`
  - [ ] Estilos navbar bell
  - [ ] Estilos slide-in panel
  - [ ] Estilos lista page
  - [ ] Responsive mobile

- [ ] **JavaScript** (40 min)
  - [ ] Crear `static/js/lino-alertas.js`
  - [ ] `updateAlertasBadge()`
  - [ ] `toggleAlertasPanel()`
  - [ ] `loadAlertasPanel()`
  - [ ] `marcarAlertaLeida()`
  - [ ] `startAlertasPolling()`

- [ ] **Templates** (30 min)
  - [ ] Modificar `base.html` - agregar bell icon navbar
  - [ ] Crear `components/alertas_panel.html`
  - [ ] Crear `gestion/alertas_lista.html`
  - [ ] Incluir panel en `base.html` (antes de `</body>`)

### Testing (30 min)

- [ ] **Funcional**
  - [ ] Badge actualiza al cargar página
  - [ ] Click bell abre panel
  - [ ] Panel carga alertas vía AJAX
  - [ ] Click alerta la marca leída
  - [ ] Badge decrementa automáticamente
  - [ ] "Ver todas" navega a lista completa
  - [ ] Filtros funcionan correctamente
  - [ ] Paginación funciona

- [ ] **UX**
  - [ ] Animaciones smooth
  - [ ] Overlay cierra panel al click
  - [ ] Responsive mobile
  - [ ] No hay scroll jump

- [ ] **Performance**
  - [ ] API count < 50ms
  - [ ] Panel render < 100ms
  - [ ] AJAX update < 100ms

---

## 🎨 DISEÑO UI/UX

### Paleta de Colores LINO (mantener consistencia)
```css
--lino-primary: #4a5c3a;    /* Verde principal */
--lino-medium: #6b7a4f;     /* Verde medio */
--lino-light: #8b9471;      /* Verde claro */
--lino-gold: #d4a574;       /* Dorado */

/* Niveles de alerta */
--alert-danger: #dc3545;    /* Rojo crítico */
--alert-warning: #ffc107;   /* Amarillo warning */
--alert-info: #0dcaf0;      /* Azul info */
--alert-success: #4a5c3a;   /* Verde LINO */
```

### Iconos Bootstrap Icons
- Bell: `bi-bell`, `bi-bell-fill`
- Check: `bi-check`, `bi-check2`, `bi-check-circle`
- Stock: `bi-box-seam`
- Vencimiento: `bi-calendar-x`
- Precio: `bi-currency-dollar`
- Crítico: `bi-exclamation-triangle-fill`

---

## 🧪 PLAN DE TESTING

### Test Manual Checklist (20 items)

**TEST 9: Sistema de Alertas UI**

```markdown
### Navbar Bell Icon (5 items)
- [ ] Badge visible con count correcto
- [ ] Badge oculto cuando count = 0
- [ ] Animación pulse cuando hay nuevas
- [ ] Click abre panel slide-in
- [ ] Icono campana verde LINO

### Slide-in Panel (7 items)
- [ ] Panel desliza desde derecha smooth
- [ ] Overlay oscuro visible
- [ ] Muestra últimas 5 alertas no leídas
- [ ] Colores según nivel (danger/warning/info)
- [ ] Click alerta la marca leída
- [ ] Badge decrementa inmediatamente
- [ ] "Ver todas" navega a lista

### Alerts List Page (6 items)
- [ ] Filtro por tipo funciona
- [ ] Filtro por nivel funciona
- [ ] Filtro "No leídas" funciona
- [ ] Paginación 20 items por página
- [ ] Breadcrumb correcto
- [ ] Marcar leída desde lista funciona

### Real-time Updates (2 items)
- [ ] Badge actualiza cada 60s automáticamente
- [ ] Polling inicia al cargar página
```

### Test Automatizado (agregar a test_dashboard.py)

```python
class TestAlertasAPI(TestRunner):
    """Tests para API de alertas"""
    
    def test_alertas_count_api(self):
        """Verifica que endpoint count retorna JSON correcto"""
        # Crear 3 alertas no leídas
        for i in range(3):
            Alerta.objects.create(
                usuario=self.usuario,
                tipo='stock_bajo',
                nivel='danger',
                titulo=f'Test {i}',
                mensaje='Test',
                leida=False
            )
        
        response = self.client.get('/gestion/api/alertas/count/')
        data = response.json()
        
        self.assert_equals(response.status_code, 200, "Status code 200")
        self.assert_equals(data['count'], 3, "Count correcto")
    
    def test_marcar_alerta_leida_api(self):
        """Verifica que AJAX mark as read funciona"""
        alerta = Alerta.objects.create(
            usuario=self.usuario,
            tipo='stock_bajo',
            nivel='danger',
            titulo='Test',
            mensaje='Test',
            leida=False
        )
        
        response = self.client.post(f'/gestion/api/alertas/{alerta.id}/marcar-leida/')
        data = response.json()
        
        self.assert_equals(response.status_code, 200, "Status 200")
        self.assert_true(data['success'], "Success true")
        
        alerta.refresh_from_db()
        self.assert_true(alerta.leida, "Alerta marcada leída")
```

---

## 📊 MÉTRICAS DE ÉXITO

### Funcional
- ✅ Badge actualiza correctamente (0 errores)
- ✅ Panel carga 5 alertas en <100ms
- ✅ AJAX mark as read funciona sin reload
- ✅ Polling cada 60s sin memory leaks

### UX
- ✅ Animaciones smooth (no lag)
- ✅ Responsive mobile/tablet/desktop
- ✅ Colores LINO consistentes
- ✅ No scroll jump ni glitches

### Performance
- ✅ `/api/alertas/count/` < 50ms
- ✅ `/api/alertas/no-leidas/` < 100ms
- ✅ Render panel < 100ms
- ✅ Memory usage estable con polling

---

## 🚀 DESPLIEGUE

### Pasos Post-Implementación

1. **Collectstatic**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Restart Server**
   ```bash
   # Kill puerto 8000
   lsof -ti:8000 | xargs kill -9
   
   # Restart
   python manage.py runserver
   ```

3. **Hard Reload Browser**
   ```
   Cmd + Shift + R
   ```

4. **Verificar en Consola**
   - F12 → Console
   - Verificar polling inicia: `[ALERTAS] Polling started`
   - Verificar 0 errores JavaScript

---

## 📌 ARCHIVOS CREADOS/MODIFICADOS

### Nuevos Archivos (3)
```
static/css/lino-alertas.css                     (~150 líneas)
static/js/lino-alertas.js                       (~200 líneas)
gestion/templates/components/alertas_panel.html (~80 líneas)
gestion/templates/gestion/alertas_lista.html    (~200 líneas)
```

### Archivos Modificados (3)
```
gestion/urls.py                    (+4 rutas)
gestion/views.py                   (+4 funciones, ~80 líneas)
gestion/services/alertas_service.py (+1 método, ~15 líneas)
gestion/templates/gestion/base.html (+20 líneas navbar + include panel)
gestion/models.py                  (+1 método get_icono si no existe)
```

---

## 🎯 DECISIÓN FINAL

**¿Empezar FASE 3?**

### Criterios Aprobación
- ✅ FASE 1 + FASE 2 100% completadas
- ✅ Testing Manual 97.8% (91/93 items)
- ✅ Testing Automatizado 97% (32/33)
- ✅ 0 bugs críticos
- ✅ Performance óptima

### Bloqueadores
- ❌ Ninguno

**ESTADO:** ✅ **APROBADO PARA INICIAR FASE 3**

---

## ⏭️ PRÓXIMOS PASOS

1. **Completar Tests 6-7-8** (~15 min)
   - Usar `CHECKLIST_FINAL_15MIN.md`

2. **Commit Testing Completo**
   ```bash
   git add docs/testing/
   git commit -m "Testing Manual COMPLETADO - 91/93 items (97.8%)"
   ```

3. **Iniciar FASE 3** (nuevo chat)
   - Usar este documento como guía
   - Implementar paso a paso según checklist

4. **Testing FASE 3** (~30 min)
   - Test manual con TEST 9 (20 items)
   - Tests automatizados API alertas

5. **FASE 4: Dark Mode** (siguiente)
   - Toggle tema oscuro/claro
   - LocalStorage persistencia
   - Colores LINO adaptados

---

**Fecha Creación:** 4 de Noviembre de 2025, 18:40  
**Autor:** Giuliano Zulatto  
**Versión:** 1.0  

🚀 **¡LISTO PARA FASE 3!**
