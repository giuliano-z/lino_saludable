/**
 * LINO DESIGN SYSTEM V3 - MODAL MANAGER
 * Sistema completo de modales con enfoque de ingeniería senior
 * Features: Accesibilidad, Performance, API moderna
 */

class LinoModalManager {
    constructor() {
        this.activeModals = new Map();
        this.focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        this.init();
    }

    init() {
        // Event listeners globales
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        document.addEventListener('click', this.handleClickOutside.bind(this));
        
        // Auto-inicializar modales existentes
        this.initExistingModals();
        
        console.log('🚀 LINO Modal Manager iniciado');
    }

    /**
     * Crear y mostrar modal
     */
    create(options = {}) {
        const defaultOptions = {
            id: `lino-modal-${Date.now()}`,
            size: 'md',
            title: 'Modal',
            subtitle: '',
            body: '',
            footer: '',
            closable: true,
            backdrop: true,
            keyboard: true,
            animation: true,
            onShow: null,
            onHide: null,
            onConfirm: null,
            onCancel: null
        };

        const config = { ...defaultOptions, ...options };
        
        // Crear estructura HTML
        const modalHTML = this.generateModalHTML(config);
        
        // Insertar en DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Obtener referencia
        const modalElement = document.getElementById(config.id);
        
        // Configurar eventos
        this.setupModalEvents(modalElement, config);
        
        // Registrar modal activo
        this.activeModals.set(config.id, {
            element: modalElement,
            config: config
        });
        
        // Mostrar modal
        this.show(config.id);
        
        return config.id;
    }

    /**
     * Generar HTML del modal
     */
    generateModalHTML(config) {
        const sizeClass = config.size ? `lino-modal--${config.size}` : '';
        const animationClass = config.animation ? 'lino-modal--animate-in' : '';
        
        return `
            <div id="${config.id}" 
                 class="lino-modal-overlay" 
                 aria-hidden="true" 
                 role="dialog" 
                 aria-modal="true"
                 aria-labelledby="${config.id}-title">
                <div class="lino-modal ${sizeClass} ${animationClass}">
                    ${this.generateHeader(config)}
                    ${this.generateBody(config)}
                    ${this.generateFooter(config)}
                </div>
            </div>
        `;
    }

    generateHeader(config) {
        if (!config.title && !config.closable) return '';
        
        return `
            <div class="lino-modal-header">
                <div>
                    ${config.title ? `<h3 id="${config.id}-title" class="lino-modal-title">${config.title}</h3>` : ''}
                    ${config.subtitle ? `<p class="lino-modal-subtitle">${config.subtitle}</p>` : ''}
                </div>
                ${config.closable ? `
                    <button type="button" class="lino-modal-close" data-modal-close="${config.id}" aria-label="Cerrar modal">
                        <i class="fas fa-times"></i>
                    </button>
                ` : ''}
            </div>
        `;
    }

    generateBody(config) {
        return `
            <div class="lino-modal-body">
                ${config.body}
            </div>
        `;
    }

    generateFooter(config) {
        if (!config.footer) return '';
        
        return `
            <div class="lino-modal-footer lino-modal-footer--end">
                ${config.footer}
            </div>
        `;
    }

    /**
     * Configurar eventos del modal
     */
    setupModalEvents(modalElement, config) {
        // Botón cerrar
        const closeBtn = modalElement.querySelector('[data-modal-close]');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hide(config.id));
        }

        // Botones de acción personalizados
        const confirmBtn = modalElement.querySelector('[data-modal-confirm]');
        if (confirmBtn && config.onConfirm) {
            confirmBtn.addEventListener('click', () => {
                const result = config.onConfirm();
                if (result !== false) {
                    this.hide(config.id);
                }
            });
        }

        const cancelBtn = modalElement.querySelector('[data-modal-cancel]');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                if (config.onCancel) config.onCancel();
                this.hide(config.id);
            });
        }
    }

    /**
     * Mostrar modal
     */
    show(modalId) {
        const modal = this.activeModals.get(modalId);
        if (!modal) return;

        const { element, config } = modal;

        // Bloquear scroll del body
        document.body.classList.add('lino-modal-open');

        // Mostrar overlay
        element.setAttribute('aria-hidden', 'false');
        element.classList.add('lino-modal-overlay--show');

        // Focus management
        this.manageFocus(element, true);

        // Callback
        if (config.onShow) config.onShow(modalId);

        console.log(`📖 Modal ${modalId} mostrado`);
    }

    /**
     * Ocultar modal
     */
    hide(modalId) {
        const modal = this.activeModals.get(modalId);
        if (!modal) return;

        const { element, config } = modal;

        // Animación de salida
        if (config.animation) {
            element.querySelector('.lino-modal').classList.add('lino-modal--animate-out');
            setTimeout(() => this.destroy(modalId), 200);
        } else {
            this.destroy(modalId);
        }

        // Callback
        if (config.onHide) config.onHide(modalId);

        console.log(`📕 Modal ${modalId} ocultado`);
    }

    /**
     * Destruir modal
     */
    destroy(modalId) {
        const modal = this.activeModals.get(modalId);
        if (!modal) return;

        const { element } = modal;

        // Restaurar focus
        this.manageFocus(element, false);

        // Remover del DOM
        element.remove();

        // Limpiar registro
        this.activeModals.delete(modalId);

        // Restaurar scroll si no hay más modales
        if (this.activeModals.size === 0) {
            document.body.classList.remove('lino-modal-open');
        }

        console.log(`🗑️  Modal ${modalId} destruido`);
    }

    /**
     * Gestión de focus para accesibilidad
     */
    manageFocus(modalElement, isShowing) {
        if (isShowing) {
            // Guardar elemento con focus actual
            this.previousFocus = document.activeElement;

            // Focus al primer elemento focuseable del modal
            const firstFocusable = modalElement.querySelector(this.focusableElements);
            if (firstFocusable) {
                firstFocusable.focus();
            }
        } else {
            // Restaurar focus anterior
            if (this.previousFocus && typeof this.previousFocus.focus === 'function') {
                this.previousFocus.focus();
            }
        }
    }

    /**
     * Manejo de teclado
     */
    handleKeyDown(event) {
        if (this.activeModals.size === 0) return;

        // Obtener modal activo (el último)
        const modalIds = Array.from(this.activeModals.keys());
        const activeModalId = modalIds[modalIds.length - 1];
        const activeModal = this.activeModals.get(activeModalId);

        if (!activeModal) return;

        const { element, config } = activeModal;

        // ESC para cerrar
        if (event.key === 'Escape' && config.keyboard) {
            event.preventDefault();
            this.hide(activeModalId);
            return;
        }

        // TAB para navegación
        if (event.key === 'Tab') {
            this.handleTabNavigation(event, element);
        }
    }

    /**
     * Navegación con TAB (trap focus)
     */
    handleTabNavigation(event, modalElement) {
        const focusableElements = modalElement.querySelectorAll(this.focusableElements);
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (event.shiftKey) {
            // SHIFT + TAB
            if (document.activeElement === firstElement) {
                event.preventDefault();
                lastElement.focus();
            }
        } else {
            // TAB
            if (document.activeElement === lastElement) {
                event.preventDefault();
                firstElement.focus();
            }
        }
    }

    /**
     * Click fuera del modal
     */
    handleClickOutside(event) {
        if (this.activeModals.size === 0) return;

        // Verificar si el click fue en el overlay
        if (event.target.classList.contains('lino-modal-overlay')) {
            const modalId = event.target.id;
            const modal = this.activeModals.get(modalId);
            
            if (modal && modal.config.backdrop) {
                this.hide(modalId);
            }
        }
    }

    /**
     * Inicializar modales existentes en el DOM
     */
    initExistingModals() {
        const existingModals = document.querySelectorAll('[data-modal-trigger]');
        
        existingModals.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.dataset.modalTrigger;
                
                if (modalId) {
                    this.show(modalId);
                }
            });
        });
    }

    /**
     * MÉTODOS DE CONVENIENCIA
     */

    /**
     * Modal de confirmación
     */
    confirm(options = {}) {
        const defaultOptions = {
            title: '¿Confirmar acción?',
            body: '¿Estás seguro de que quieres continuar?',
            confirmText: 'Confirmar',
            cancelText: 'Cancelar',
            confirmClass: 'lino-btn--danger',
            cancelClass: 'lino-btn--secondary'
        };

        const config = { ...defaultOptions, ...options };

        config.footer = `
            <button type="button" class="lino-btn ${config.cancelClass}" data-modal-cancel>
                ${config.cancelText}
            </button>
            <button type="button" class="lino-btn ${config.confirmClass}" data-modal-confirm>
                ${config.confirmText}
            </button>
        `;

        return this.create(config);
    }

    /**
     * Modal de alerta
     */
    alert(options = {}) {
        const defaultOptions = {
            title: 'Información',
            body: 'Mensaje de alerta',
            confirmText: 'Aceptar',
            confirmClass: 'lino-btn--primary'
        };

        const config = { ...defaultOptions, ...options };

        config.footer = `
            <button type="button" class="lino-btn ${config.confirmClass}" data-modal-confirm>
                ${config.confirmText}
            </button>
        `;

        return this.create(config);
    }

    /**
     * Modal de loading
     */
    loading(message = 'Cargando...') {
        return this.create({
            body: `
                <div class="lino-text-center">
                    <div class="lino-spinner"></div>
                    <div class="lino-text-base">${message}</div>
                </div>
            `,
            closable: false,
            backdrop: false,
            keyboard: false
        });
    }
}

// API Global simplificada
window.LinoModal = {
    manager: new LinoModalManager(),
    
    // Métodos principales
    show: (modalId) => window.LinoModal.manager.show(modalId),
    hide: (modalId) => window.LinoModal.manager.hide(modalId),
    create: (options) => window.LinoModal.manager.create(options),
    
    // Métodos de conveniencia
    confirm: (options) => window.LinoModal.manager.confirm(options),
    alert: (options) => window.LinoModal.manager.alert(options),
    loading: (message) => window.LinoModal.manager.loading(message)
};

// Auto-inicialización cuando el DOM está listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🎯 LINO Modals System Ready!');
    });
} else {
    console.log('🎯 LINO Modals System Ready!');
}

/**
 * EJEMPLOS DE USO:
 * 
 * // Modal básico
 * LinoModal.create({
 *     title: 'Nuevo Producto',
 *     body: '<p>Contenido del modal</p>',
 *     size: 'lg'
 * });
 * 
 * // Modal de confirmación
 * LinoModal.confirm({
 *     title: '¿Eliminar producto?',
 *     body: 'Esta acción no se puede deshacer',
 *     onConfirm: () => {
 *         console.log('Confirmado!');
 *         return true; // Cerrar modal
 *     }
 * });
 * 
 * // Modal de loading
 * const loadingId = LinoModal.loading('Procesando venta...');
 * setTimeout(() => LinoModal.hide(loadingId), 3000);
 */
