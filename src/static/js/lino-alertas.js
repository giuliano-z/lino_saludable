/**
 * LINO Alertas System - FASE 3
 * Sistema de notificaciones real-time con AJAX
 * 
 * Funciones principales:
 * - updateAlertasBadge(): Actualiza contador navbar cada 60s
 * - toggleAlertasPanel(): Abre/cierra panel slide-in
 * - loadAlertasPanel(): Carga alertas vía AJAX
 * - marcarAlertaLeida(): Marca alerta leída sin reload
 * - startAlertasPolling(): Auto-update cada 60 segundos
 * 
 * @version 1.0
 * @date 2025-11-04
 */

console.log('[LINO Alertas] Script cargado');

// ==========================================
// VARIABLES GLOBALES
// ==========================================

let alertasPanelOpen = false;
let alertasPollingInterval = null;
const POLLING_INTERVAL = 60000; // 60 segundos

// ==========================================
// ACTUALIZAR BADGE CONTADOR
// ==========================================

/**
 * Actualiza el badge del navbar con el count de alertas no leídas
 * Se ejecuta cada 60 segundos automáticamente
 */
async function updateAlertasBadge() {
    try {
        const response = await fetch('/gestion/api/alertas/count/');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const badge = document.getElementById('alertas-badge');
        const bell = document.getElementById('alertas-bell');
        
        if (!badge || !bell) {
            console.warn('[LINO Alertas] Elementos badge/bell no encontrados en DOM');
            return;
        }
        
        if (data.count > 0) {
            badge.textContent = data.count > 99 ? '99+' : data.count;
            badge.style.display = 'inline-block';
            
            // Animación shake solo si hay nuevas alertas
            const oldCount = parseInt(badge.dataset.lastCount || '0');
            if (data.count > oldCount) {
                bell.classList.add('has-new');
                setTimeout(() => bell.classList.remove('has-new'), 500);
            }
            
            badge.dataset.lastCount = data.count;
        } else {
            badge.style.display = 'none';
            bell.classList.remove('has-new');
        }
        
        console.log(`[LINO Alertas] Badge actualizado: ${data.count} alertas`);
        
    } catch (error) {
        console.error('[LINO Alertas] Error updating badge:', error);
    }
}

// ==========================================
// TOGGLE PANEL SLIDE-IN
// ==========================================

/**
 * Abre/cierra el panel slide-in de alertas
 * @param {Event} event - Evento del click
 */
function toggleAlertasPanel(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const panel = document.getElementById('alertas-panel');
    const overlay = document.getElementById('alertas-overlay');
    
    if (!panel || !overlay) {
        console.error('[LINO Alertas] Panel/overlay no encontrados');
        return;
    }
    
    if (alertasPanelOpen) {
        closeAlertasPanel();
    } else {
        // Abrir panel
        panel.classList.add('open');
        overlay.classList.add('show');
        alertasPanelOpen = true;
        
        // Cargar alertas
        loadAlertasPanel();
        
        console.log('[LINO Alertas] Panel abierto');
    }
}

/**
 * Cierra el panel slide-in
 */
function closeAlertasPanel() {
    const panel = document.getElementById('alertas-panel');
    const overlay = document.getElementById('alertas-overlay');
    
    if (panel) panel.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
    
    alertasPanelOpen = false;
    
    console.log('[LINO Alertas] Panel cerrado');
}

// ==========================================
// CARGAR ALERTAS EN PANEL
// ==========================================

/**
 * Carga las últimas 5 alertas no leídas vía AJAX
 * Renderiza el HTML en el panel
 */
async function loadAlertasPanel() {
    const content = document.getElementById('alertas-panel-content');
    
    if (!content) {
        console.error('[LINO Alertas] Panel content no encontrado');
        return;
    }
    
    // Mostrar loading
    content.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-lino" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>
    `;
    
    try {
        const response = await fetch('/gestion/api/alertas/no-leidas/');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.alertas.length === 0) {
            // Empty state
            content.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-check-circle fs-1"></i>
                    <p class="mt-2 mb-0 fw-semibold">¡Todo al día!</p>
                    <small class="text-muted">No tienes alertas pendientes</small>
                </div>
            `;
            return;
        }
        
        // Renderizar alertas
        let html = '';
        data.alertas.forEach(alerta => {
            html += `
                <div class="alerta-item ${alerta.nivel}" 
                     onclick="marcarAlertaLeida(${alerta.id})"
                     data-alerta-id="${alerta.id}">
                    <div class="d-flex align-items-start">
                        <i class="bi ${alerta.icono} fs-4 me-2 flex-shrink-0"></i>
                        <div class="flex-grow-1">
                            <div class="alerta-titulo">${escapeHtml(alerta.titulo)}</div>
                            <div class="alerta-mensaje">${escapeHtml(alerta.mensaje)}</div>
                            <div class="alerta-fecha">
                                <i class="bi bi-clock"></i> ${alerta.fecha}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        content.innerHTML = html;
        
        console.log(`[LINO Alertas] ${data.alertas.length} alertas cargadas`);
        
    } catch (error) {
        console.error('[LINO Alertas] Error loading panel:', error);
        content.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="bi bi-exclamation-triangle"></i>
                Error al cargar alertas
            </div>
        `;
    }
}

// ==========================================
// MARCAR ALERTA COMO LEÍDA
// ==========================================

/**
 * Marca una alerta como leída vía AJAX
 * @param {number} alertaId - ID de la alerta
 */
async function marcarAlertaLeida(alertaId) {
    console.log(`[LINO Alertas] Marcando alerta ${alertaId} como leída`);
    
    try {
        const response = await fetch(`/gestion/api/alertas/${alertaId}/marcar-leida/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Actualizar badge inmediatamente
            updateAlertasBadge();
            
            // Recargar panel para mostrar nuevas alertas
            if (alertasPanelOpen) {
                setTimeout(() => loadAlertasPanel(), 300);
            }
            
            // Toast notification (opcional - Bootstrap Toast)
            showToast('Alerta marcada como leída', 'success');
            
            console.log(`[LINO Alertas] Alerta ${alertaId} marcada correctamente`);
        }
        
    } catch (error) {
        console.error(`[LINO Alertas] Error marking alerta ${alertaId}:`, error);
        showToast('Error al marcar alerta', 'error');
    }
}

// ==========================================
// POLLING AUTO-UPDATE
// ==========================================

/**
 * Inicia el polling cada 60 segundos para actualizar el badge
 * Se ejecuta automáticamente al cargar la página
 */
function startAlertasPolling() {
    // Update inmediato
    updateAlertasBadge();
    
    // Evitar múltiples intervals
    if (alertasPollingInterval) {
        clearInterval(alertasPollingInterval);
    }
    
    // Polling cada 60s
    alertasPollingInterval = setInterval(() => {
        updateAlertasBadge();
    }, POLLING_INTERVAL);
    
    console.log('[LINO Alertas] Polling iniciado (60s interval)');
}

/**
 * Detiene el polling (útil para cleanup)
 */
function stopAlertasPolling() {
    if (alertasPollingInterval) {
        clearInterval(alertasPollingInterval);
        alertasPollingInterval = null;
        console.log('[LINO Alertas] Polling detenido');
    }
}

// ==========================================
// HELPERS & UTILITIES
// ==========================================

/**
 * Obtiene el valor de una cookie por nombre
 * @param {string} name - Nombre de la cookie
 * @returns {string|null} - Valor de la cookie o null
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
 * Escape HTML para prevenir XSS
 * @param {string} text - Texto a escapar
 * @returns {string} - Texto escapado
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Muestra un toast notification simple
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo: 'success', 'error', 'info'
 */
function showToast(message, type = 'info') {
    // Simple console log (puedes reemplazar con Bootstrap Toast)
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    console.log(`${icon} ${message}`);
    
    // Si tienes Bootstrap Toast en tu proyecto:
    // const toastEl = document.getElementById('liveToast');
    // if (toastEl) {
    //     const toast = new bootstrap.Toast(toastEl);
    //     toastEl.querySelector('.toast-body').textContent = message;
    //     toast.show();
    // }
}

// ==========================================
// AUTO-START AL CARGAR PÁGINA
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('[LINO Alertas] DOM ready, iniciando sistema');
    
    // Iniciar polling automático
    startAlertasPolling();
    
    // Event listener para cerrar panel con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && alertasPanelOpen) {
            closeAlertasPanel();
        }
    });
    
    console.log('[LINO Alertas] Sistema inicializado correctamente ✅');
});

// Cleanup al salir de la página
window.addEventListener('beforeunload', function() {
    stopAlertasPolling();
});

// ==========================================
// EXPONER FUNCIONES GLOBALES
// ==========================================

// Hacer funciones accesibles desde HTML onclick
window.toggleAlertasPanel = toggleAlertasPanel;
window.closeAlertasPanel = closeAlertasPanel;
window.marcarAlertaLeida = marcarAlertaLeida;
window.updateAlertasBadge = updateAlertasBadge;

console.log('[LINO Alertas] Funciones globales expuestas');
