"""
🎨 SCRIPT MEJORAS FRONTEND INMEDIATAS - LINO SALUDABLE
Mejoras CSS y JS que se pueden aplicar en tiempo real
"""

# ==================== CSS PROFESIONAL PARA DIETÉTICA ====================

MEJORAS_CSS = """
/* 🎨 MEJORAS VISUALES PROFESIONALES PARA LINO SALUDABLE */

/* === VARIABLES DE COLOR TEMA DIETÉTICA === */
:root {
    --lino-primary: #2c5530;      /* Verde dietética */
    --lino-secondary: #4a7c59;    /* Verde claro */
    --lino-success: #28a745;      /* Verde éxito */
    --lino-warning: #ffc107;      /* Amarillo alertas */
    --lino-danger: #dc3545;       /* Rojo crítico */
    --lino-info: #17a2b8;         /* Azul información */
    --lino-light: #f8f9fa;        /* Gris claro */
    --lino-dark: #343a40;         /* Gris oscuro */
}

/* === MEJORAS DASHBOARD === */
.dashboard-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    padding: 2rem 0;
}

.dashboard-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(44, 85, 48, 0.1);
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
    border-left: 4px solid var(--lino-primary);
}

.dashboard-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(44, 85, 48, 0.15);
}

.stat-number {
    font-size: 3rem;
    font-weight: 700;
    color: var(--lino-primary);
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--lino-dark);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.875rem;
}

/* === NAVEGACIÓN PROFESIONAL === */
.navbar-lino {
    background: linear-gradient(135deg, var(--lino-primary) 0%, var(--lino-secondary) 100%);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: white !important;
}

.nav-link {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: white !important;
}

/* === TABLA PRODUCTOS PROFESIONAL === */
.table-productos {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.table-productos th {
    background: var(--lino-primary);
    color: white;
    font-weight: 600;
    border: none;
    padding: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.875rem;
}

.table-productos td {
    padding: 1rem;
    border-bottom: 1px solid #e9ecef;
    vertical-align: middle;
}

.table-productos tbody tr:hover {
    background-color: #f8f9fa;
    transform: scale(1.01);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
}

/* === STOCK STATUS VISUAL === */
.stock-alto {
    color: var(--lino-success);
    font-weight: bold;
}

.stock-medio {
    color: var(--lino-warning);
    font-weight: bold;
}

.stock-bajo {
    color: var(--lino-danger);
    font-weight: bold;
    animation: pulse 2s infinite;
}

.stock-critico {
    color: white;
    background: var(--lino-danger);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
    animation: blink 1s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}

/* === BOTONES PROFESIONALES === */
.btn-lino-primary {
    background: linear-gradient(135deg, var(--lino-primary) 0%, var(--lino-secondary) 100%);
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-lino-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(44, 85, 48, 0.3);
}

/* === FORMULARIOS ELEGANTES === */
.form-control-lino {
    border: 2px solid #e9ecef;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
}

.form-control-lino:focus {
    border-color: var(--lino-primary);
    box-shadow: 0 0 0 0.2rem rgba(44, 85, 48, 0.25);
}

/* === ALERTAS PERSONALIZADAS === */
.alert-lino {
    border: none;
    border-radius: 8px;
    border-left: 4px solid var(--lino-primary);
    background: rgba(44, 85, 48, 0.05);
}

/* === RESPONSIVE MEJORAS === */
@media (max-width: 768px) {
    .dashboard-card {
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
    }
    
    .table-responsive {
        border: none;
    }
}

/* === LOADING STATES === */
.loading {
    opacity: 0.7;
    pointer-events: none;
}

.spinner-lino {
    border: 3px solid #f3f3f3;
    border-top: 3px solid var(--lino-primary);
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
"""

# ==================== JAVASCRIPT INTERACTIVO ====================

MEJORAS_JS = """
// 🚀 MEJORAS JAVASCRIPT INTERACTIVAS - LINO SALUDABLE

document.addEventListener('DOMContentLoaded', function() {
    
    // === AUTO-CLASIFICAR STOCK POR COLOR === 
    function clasificarStock() {
        document.querySelectorAll('[data-stock]').forEach(function(element) {
            const stock = parseInt(element.dataset.stock || element.textContent);
            
            element.classList.remove('stock-alto', 'stock-medio', 'stock-bajo', 'stock-critico');
            
            if (stock === 0) {
                element.classList.add('stock-critico');
                element.innerHTML = '<i class="fas fa-exclamation-triangle"></i> AGOTADO';
            } else if (stock <= 5) {
                element.classList.add('stock-bajo');
                element.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${stock}`;
            } else if (stock <= 20) {
                element.classList.add('stock-medio');
                element.innerHTML = `<i class="fas fa-info-circle"></i> ${stock}`;
            } else {
                element.classList.add('stock-alto');
                element.innerHTML = `<i class="fas fa-check-circle"></i> ${stock}`;
            }
        });
    }
    
    // === BÚSQUEDA EN TIEMPO REAL ===
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const filter = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.table tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
    
    // === TOOLTIPS INFORMATIVOS ===
    function agregarTooltips() {
        document.querySelectorAll('.stock-critico').forEach(function(el) {
            el.title = '¡ATENCIÓN! Stock crítico - Reposición urgente';
        });
        
        document.querySelectorAll('.stock-bajo').forEach(function(el) {
            el.title = 'Stock bajo - Considerar reposición';
        });
    }
    
    // === ANIMACIONES SUAVES ===
    function animarEntrada() {
        const cards = document.querySelectorAll('.dashboard-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    // === CONFIRMACIONES ELEGANTES ===
    function confirmarAcciones() {
        document.querySelectorAll('[data-confirm]').forEach(function(button) {
            button.addEventListener('click', function(e) {
                const message = this.dataset.confirm || '¿Está seguro?';
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // === EJECUTAR MEJORAS ===
    clasificarStock();
    agregarTooltips();
    animarEntrada();
    confirmarAcciones();
    
    // === ACTUALIZAR CADA 30 SEGUNDOS ===
    setInterval(clasificarStock, 30000);
});

// === FUNCIÓN GLOBAL PARA FEEDBACK VISUAL ===
function mostrarNotificacion(mensaje, tipo = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
"""

def aplicar_mejoras_css():
    """Aplica las mejoras CSS al archivo principal"""
    css_path = "/Users/giulianozulatto/Proyectos/lino_saludable/src/static/css/mejoras_lino.css"
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(MEJORAS_CSS)
    
    print("✅ Mejoras CSS aplicadas en: mejoras_lino.css")
    return css_path

def aplicar_mejoras_js():
    """Aplica las mejoras JavaScript"""
    js_path = "/Users/giulianozulatto/Proyectos/lino_saludable/src/static/js/mejoras_lino.js"
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(MEJORAS_JS)
    
    print("✅ Mejoras JavaScript aplicadas en: mejoras_lino.js")
    return js_path

def mostrar_instrucciones_inclusion():
    """Muestra cómo incluir las mejoras en templates"""
    instrucciones = """
    <!-- 📝 INCLUIR EN BASE.HTML O TEMPLATES -->
    
    <!-- En la sección <head> -->
    <link rel="stylesheet" href="{% static 'css/mejoras_lino.css' %}">
    
    <!-- Antes del cierre </body> -->
    <script src="{% static 'js/mejoras_lino.js' %}"></script>
    
    <!-- Para usar clases de stock automático, agregar data-stock: -->
    <td data-stock="{{ producto.stock }}">{{ producto.stock }}</td>
    
    <!-- Para botones con confirmación: -->
    <button class="btn btn-danger" data-confirm="¿Eliminar producto?">Eliminar</button>
    """
    
    print("📋 INSTRUCCIONES DE INCLUSIÓN:")
    print(instrucciones)

if __name__ == "__main__":
    print("🎨 APLICANDO MEJORAS FRONTEND PROFESIONALES...")
    aplicar_mejoras_css()
    aplicar_mejoras_js()
    mostrar_instrucciones_inclusion()
    print("\n🚀 ¡MEJORAS APLICADAS! Recarga el navegador para ver cambios.")
