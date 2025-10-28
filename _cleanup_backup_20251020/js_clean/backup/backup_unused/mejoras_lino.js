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
