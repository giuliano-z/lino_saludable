/**
 * LINO DESIGN SYSTEM V3 - ADVANCED TOOLTIPS & POPOVERS
 * 
 * Sistema de tooltips y popovers avanzado con:
 * 1. Posicionamiento inteligente
 * 2. Detección de colisiones con viewport
 * 3. Animaciones fluidas
 * 4. Accesibilidad completa
 * 5. Múltiples triggers (hover, click, focus)
 * 6. Contenido dinámico y HTML
 */

class LinoTooltipSystem {
    constructor() {
        this.tooltips = new Map();
        this.activeTooltip = null;
        this.config = {
            defaultPosition: 'top',
            offset: 8,
            showDelay: 500,
            hideDelay: 100,
            animationDuration: 200,
            maxWidth: 250,
            className: 'lino-tooltip'
        };
        
        this.init();
    }
    
    init() {
        this.createTooltipStyles();
        this.bindEvents();
        this.scanForTooltips();
        
        console.log('💬 LINO Tooltip System inicializado');
    }
    
    createTooltipStyles() {
        if (document.getElementById('lino-tooltip-styles')) return;
        
        const styles = `
        /* LINO TOOLTIP SYSTEM STYLES */
        .lino-tooltip {
            position: absolute;
            z-index: 9999;
            padding: 0.5rem 0.75rem;
            background: var(--lino-surface-dark, #2d3748);
            color: var(--lino-text-inverse, white);
            border-radius: var(--lino-radius-sm, 4px);
            font-size: 0.875rem;
            font-weight: 500;
            line-height: 1.4;
            max-width: 250px;
            word-wrap: break-word;
            box-shadow: var(--lino-shadow-lg, 0 10px 15px -3px rgba(0, 0, 0, 0.1));
            opacity: 0;
            transform: translateY(4px);
            transition: opacity 0.2s ease, transform 0.2s ease;
            pointer-events: none;
        }
        
        .lino-tooltip.lino-tooltip--visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .lino-tooltip::before {
            content: '';
            position: absolute;
            width: 0;
            height: 0;
            border: 6px solid transparent;
        }
        
        /* Arrow positions */
        .lino-tooltip--top::before {
            bottom: -12px;
            left: 50%;
            transform: translateX(-50%);
            border-top-color: var(--lino-surface-dark, #2d3748);
        }
        
        .lino-tooltip--bottom::before {
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            border-bottom-color: var(--lino-surface-dark, #2d3748);
        }
        
        .lino-tooltip--left::before {
            right: -12px;
            top: 50%;
            transform: translateY(-50%);
            border-left-color: var(--lino-surface-dark, #2d3748);
        }
        
        .lino-tooltip--right::before {
            left: -12px;
            top: 50%;
            transform: translateY(-50%);
            border-right-color: var(--lino-surface-dark, #2d3748);
        }
        
        /* Variants */
        .lino-tooltip--success {
            background: var(--lino-success-color, #28a745);
        }
        
        .lino-tooltip--success::before {
            border-top-color: var(--lino-success-color, #28a745);
        }
        
        .lino-tooltip--warning {
            background: var(--lino-warning-color, #ffc107);
            color: var(--lino-text-primary, #333);
        }
        
        .lino-tooltip--warning::before {
            border-top-color: var(--lino-warning-color, #ffc107);
        }
        
        .lino-tooltip--danger {
            background: var(--lino-danger-color, #dc3545);
        }
        
        .lino-tooltip--danger::before {
            border-top-color: var(--lino-danger-color, #dc3545);
        }
        
        .lino-tooltip--large {
            max-width: 350px;
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
        }
        
        /* Popover styles */
        .lino-popover {
            position: absolute;
            z-index: 9999;
            background: var(--lino-surface-primary, white);
            border: 1px solid var(--lino-border-color, #e2e8f0);
            border-radius: var(--lino-radius-md, 6px);
            box-shadow: var(--lino-shadow-xl, 0 20px 25px -5px rgba(0, 0, 0, 0.1));
            opacity: 0;
            transform: scale(0.95);
            transition: opacity 0.2s ease, transform 0.2s ease;
            pointer-events: none;
            min-width: 200px;
            max-width: 400px;
        }
        
        .lino-popover.lino-popover--visible {
            opacity: 1;
            transform: scale(1);
            pointer-events: auto;
        }
        
        .lino-popover__header {
            padding: 0.75rem 1rem 0;
            font-weight: 600;
            color: var(--lino-text-primary, #1a202c);
            border-bottom: 1px solid var(--lino-border-color, #e2e8f0);
            margin-bottom: 0.5rem;
        }
        
        .lino-popover__body {
            padding: 0.75rem 1rem;
            color: var(--lino-text-secondary, #4a5568);
            line-height: 1.5;
        }
        
        .lino-popover__footer {
            padding: 0.5rem 1rem 0.75rem;
            border-top: 1px solid var(--lino-border-color, #e2e8f0);
            margin-top: 0.5rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .lino-tooltip {
                max-width: 200px;
                font-size: 0.8rem;
            }
            
            .lino-popover {
                max-width: calc(100vw - 2rem);
                margin: 1rem;
            }
        }
        
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .lino-tooltip,
            .lino-popover {
                transition: none !important;
            }
        }
        `;
        
        const styleElement = document.createElement('style');
        styleElement.id = 'lino-tooltip-styles';
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
    }
    
    scanForTooltips() {
        // Escanear elementos con data-tooltip
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            this.createTooltip(element);
        });
        
        // Escanear elementos con title
        document.querySelectorAll('[title]:not([data-tooltip])').forEach(element => {
            const title = element.getAttribute('title');
            if (title) {
                element.setAttribute('data-tooltip', title);
                element.removeAttribute('title');
                this.createTooltip(element);
            }
        });
        
        // Escanear popovers
        document.querySelectorAll('[data-popover]').forEach(element => {
            this.createPopover(element);
        });
    }
    
    createTooltip(element, options = {}) {
        const config = {
            ...this.config,
            ...options,
            content: element.getAttribute('data-tooltip'),
            position: element.getAttribute('data-tooltip-position') || this.config.defaultPosition,
            trigger: element.getAttribute('data-tooltip-trigger') || 'hover',
            variant: element.getAttribute('data-tooltip-variant') || 'default',
            delay: parseInt(element.getAttribute('data-tooltip-delay')) || this.config.showDelay,
            size: element.getAttribute('data-tooltip-size') || 'default'
        };
        
        if (!config.content) return;
        
        const tooltip = {
            element,
            config,
            tooltipElement: null,
            showTimeout: null,
            hideTimeout: null
        };
        
        this.tooltips.set(element, tooltip);
        this.bindTooltipEvents(tooltip);
        
        return tooltip;
    }
    
    createPopover(element, options = {}) {
        const config = {
            ...this.config,
            ...options,
            content: element.getAttribute('data-popover'),
            title: element.getAttribute('data-popover-title'),
            html: element.getAttribute('data-popover-html') === 'true',
            position: element.getAttribute('data-popover-position') || 'bottom',
            trigger: element.getAttribute('data-popover-trigger') || 'click'
        };
        
        const popover = {
            element,
            config,
            popoverElement: null,
            isVisible: false
        };
        
        this.tooltips.set(element, popover);
        this.bindPopoverEvents(popover);
        
        return popover;
    }
    
    bindTooltipEvents(tooltip) {
        const { element, config } = tooltip;
        
        if (config.trigger === 'hover') {
            element.addEventListener('mouseenter', () => this.showTooltip(tooltip));
            element.addEventListener('mouseleave', () => this.hideTooltip(tooltip));
            element.addEventListener('focus', () => this.showTooltip(tooltip));
            element.addEventListener('blur', () => this.hideTooltip(tooltip));
        } else if (config.trigger === 'click') {
            element.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTooltip(tooltip);
            });
        } else if (config.trigger === 'focus') {
            element.addEventListener('focus', () => this.showTooltip(tooltip));
            element.addEventListener('blur', () => this.hideTooltip(tooltip));
        }
    }
    
    bindPopoverEvents(popover) {
        const { element, config } = popover;
        
        if (config.trigger === 'click') {
            element.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.togglePopover(popover);
            });
        } else if (config.trigger === 'hover') {
            element.addEventListener('mouseenter', () => this.showPopover(popover));
            element.addEventListener('mouseleave', () => this.hidePopover(popover));
        }
    }
    
    showTooltip(tooltip) {
        clearTimeout(tooltip.hideTimeout);
        
        tooltip.showTimeout = setTimeout(() => {
            this.hideActiveTooltip();
            this.renderTooltip(tooltip);
            this.positionTooltip(tooltip);
            this.activeTooltip = tooltip;
        }, tooltip.config.delay);
    }
    
    hideTooltip(tooltip) {
        clearTimeout(tooltip.showTimeout);
        
        tooltip.hideTimeout = setTimeout(() => {
            if (tooltip.tooltipElement) {
                tooltip.tooltipElement.classList.remove('lino-tooltip--visible');
                setTimeout(() => {
                    if (tooltip.tooltipElement && tooltip.tooltipElement.parentNode) {
                        tooltip.tooltipElement.parentNode.removeChild(tooltip.tooltipElement);
                    }
                    tooltip.tooltipElement = null;
                    if (this.activeTooltip === tooltip) {
                        this.activeTooltip = null;
                    }
                }, this.config.animationDuration);
            }
        }, this.config.hideDelay);
    }
    
    toggleTooltip(tooltip) {
        if (tooltip.tooltipElement && tooltip.tooltipElement.classList.contains('lino-tooltip--visible')) {
            this.hideTooltip(tooltip);
        } else {
            this.showTooltip(tooltip);
        }
    }
    
    renderTooltip(tooltip) {
        const { config } = tooltip;
        
        const tooltipElement = document.createElement('div');
        tooltipElement.className = `lino-tooltip lino-tooltip--${config.position}`;
        
        if (config.variant !== 'default') {
            tooltipElement.classList.add(`lino-tooltip--${config.variant}`);
        }
        
        if (config.size !== 'default') {
            tooltipElement.classList.add(`lino-tooltip--${config.size}`);
        }
        
        tooltipElement.textContent = config.content;
        tooltipElement.setAttribute('role', 'tooltip');
        tooltipElement.setAttribute('id', `tooltip-${Date.now()}`);
        
        // Accesibilidad
        tooltip.element.setAttribute('aria-describedby', tooltipElement.id);
        
        document.body.appendChild(tooltipElement);
        tooltip.tooltipElement = tooltipElement;
        
        // Forzar reflow antes de mostrar
        tooltipElement.offsetHeight;
        
        requestAnimationFrame(() => {
            tooltipElement.classList.add('lino-tooltip--visible');
        });
    }
    
    positionTooltip(tooltip) {
        const { tooltipElement, config, element } = tooltip;
        if (!tooltipElement) return;
        
        const elementRect = element.getBoundingClientRect();
        const tooltipRect = tooltipElement.getBoundingClientRect();
        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        
        let position = config.position;
        let left, top;
        
        // Calcular posición inicial
        switch (position) {
            case 'top':
                left = elementRect.left + (elementRect.width / 2) - (tooltipRect.width / 2);
                top = elementRect.top - tooltipRect.height - config.offset;
                break;
            case 'bottom':
                left = elementRect.left + (elementRect.width / 2) - (tooltipRect.width / 2);
                top = elementRect.bottom + config.offset;
                break;
            case 'left':
                left = elementRect.left - tooltipRect.width - config.offset;
                top = elementRect.top + (elementRect.height / 2) - (tooltipRect.height / 2);
                break;
            case 'right':
                left = elementRect.right + config.offset;
                top = elementRect.top + (elementRect.height / 2) - (tooltipRect.height / 2);
                break;
        }
        
        // Detectar colisiones y ajustar
        const collision = this.detectCollision({ left, top, width: tooltipRect.width, height: tooltipRect.height }, viewport);
        
        if (collision.top || collision.bottom) {
            if (position === 'top' && collision.top) {
                position = 'bottom';
                top = elementRect.bottom + config.offset;
                tooltipElement.className = tooltipElement.className.replace('lino-tooltip--top', 'lino-tooltip--bottom');
            } else if (position === 'bottom' && collision.bottom) {
                position = 'top';
                top = elementRect.top - tooltipRect.height - config.offset;
                tooltipElement.className = tooltipElement.className.replace('lino-tooltip--bottom', 'lino-tooltip--top');
            }
        }
        
        if (collision.left || collision.right) {
            if (position === 'left' && collision.left) {
                position = 'right';
                left = elementRect.right + config.offset;
                tooltipElement.className = tooltipElement.className.replace('lino-tooltip--left', 'lino-tooltip--right');
            } else if (position === 'right' && collision.right) {
                position = 'left';
                left = elementRect.left - tooltipRect.width - config.offset;
                tooltipElement.className = tooltipElement.className.replace('lino-tooltip--right', 'lino-tooltip--left');
            }
        }
        
        // Ajustar para mantener dentro del viewport
        left = Math.max(8, Math.min(left, viewport.width - tooltipRect.width - 8));
        top = Math.max(8, Math.min(top, viewport.height - tooltipRect.height - 8));
        
        tooltipElement.style.left = `${left + window.scrollX}px`;
        tooltipElement.style.top = `${top + window.scrollY}px`;
    }
    
    detectCollision(rect, viewport) {
        return {
            top: rect.top < 0,
            bottom: rect.top + rect.height > viewport.height,
            left: rect.left < 0,
            right: rect.left + rect.width > viewport.width
        };
    }
    
    showPopover(popover) {
        this.hideActivePopover();
        this.renderPopover(popover);
        this.positionPopover(popover);
        popover.isVisible = true;
    }
    
    hidePopover(popover) {
        if (popover.popoverElement) {
            popover.popoverElement.classList.remove('lino-popover--visible');
            setTimeout(() => {
                if (popover.popoverElement && popover.popoverElement.parentNode) {
                    popover.popoverElement.parentNode.removeChild(popover.popoverElement);
                }
                popover.popoverElement = null;
                popover.isVisible = false;
            }, this.config.animationDuration);
        }
    }
    
    togglePopover(popover) {
        if (popover.isVisible) {
            this.hidePopover(popover);
        } else {
            this.showPopover(popover);
        }
    }
    
    renderPopover(popover) {
        const { config } = popover;
        
        const popoverElement = document.createElement('div');
        popoverElement.className = `lino-popover lino-popover--${config.position}`;
        popoverElement.setAttribute('role', 'dialog');
        popoverElement.setAttribute('aria-modal', 'false');
        
        let content = '';
        
        if (config.title) {
            content += `<div class="lino-popover__header">${config.title}</div>`;
        }
        
        content += `<div class="lino-popover__body">`;
        
        if (config.html) {
            content += config.content;
        } else {
            content += this.escapeHtml(config.content);
        }
        
        content += '</div>';
        
        popoverElement.innerHTML = content;
        document.body.appendChild(popoverElement);
        popover.popoverElement = popoverElement;
        
        // Cerrar al hacer click fuera
        setTimeout(() => {
            document.addEventListener('click', (e) => {
                if (!popoverElement.contains(e.target) && !popover.element.contains(e.target)) {
                    this.hidePopover(popover);
                }
            }, { once: true });
        }, 0);
        
        requestAnimationFrame(() => {
            popoverElement.classList.add('lino-popover--visible');
        });
    }
    
    positionPopover(popover) {
        // Similar a positionTooltip pero para popovers
        const { popoverElement, config, element } = popover;
        if (!popoverElement) return;
        
        const elementRect = element.getBoundingClientRect();
        const popoverRect = popoverElement.getBoundingClientRect();
        
        let left = elementRect.left + (elementRect.width / 2) - (popoverRect.width / 2);
        let top = elementRect.bottom + config.offset;
        
        // Ajustar para viewport
        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        
        left = Math.max(16, Math.min(left, viewport.width - popoverRect.width - 16));
        top = Math.max(16, Math.min(top, viewport.height - popoverRect.height - 16));
        
        popoverElement.style.left = `${left + window.scrollX}px`;
        popoverElement.style.top = `${top + window.scrollY}px`;
    }
    
    hideActiveTooltip() {
        if (this.activeTooltip) {
            this.hideTooltip(this.activeTooltip);
        }
    }
    
    hideActivePopover() {
        this.tooltips.forEach(tooltip => {
            if (tooltip.popoverElement && tooltip.isVisible) {
                this.hidePopover(tooltip);
            }
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    bindEvents() {
        // Cerrar tooltips al presionar Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideActiveTooltip();
                this.hideActivePopover();
            }
        });
        
        // Reposicionar en resize
        window.addEventListener('resize', this.debounce(() => {
            if (this.activeTooltip && this.activeTooltip.tooltipElement) {
                this.positionTooltip(this.activeTooltip);
            }
            
            this.tooltips.forEach(tooltip => {
                if (tooltip.popoverElement && tooltip.isVisible) {
                    this.positionPopover(tooltip);
                }
            });
        }, 100));
        
        // Observer para elementos dinámicos
        const observer = new MutationObserver(() => {
            this.scanForTooltips();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // API pública
    show(element) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            if (tooltip.config.content) {
                this.showTooltip(tooltip);
            } else {
                this.showPopover(tooltip);
            }
        }
    }
    
    hide(element) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            if (tooltip.config.content) {
                this.hideTooltip(tooltip);
            } else {
                this.hidePopover(tooltip);
            }
        }
    }
    
    update(element, content, options = {}) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            tooltip.config = { ...tooltip.config, ...options, content };
            if (tooltip.tooltipElement && tooltip.tooltipElement.classList.contains('lino-tooltip--visible')) {
                tooltip.tooltipElement.textContent = content;
                this.positionTooltip(tooltip);
            }
        }
    }
    
    destroy(element) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            this.hide(element);
            this.tooltips.delete(element);
            element.removeAttribute('aria-describedby');
        }
    }
}

// Instancia global
window.LinoTooltips = new LinoTooltipSystem();

// API global para desarrollo
window.linoTooltip = {
    show: (element) => window.LinoTooltips.show(element),
    hide: (element) => window.LinoTooltips.hide(element),
    update: (element, content, options) => window.LinoTooltips.update(element, content, options),
    create: (element, options) => window.LinoTooltips.createTooltip(element, options),
    destroy: (element) => window.LinoTooltips.destroy(element)
};

// Auto-inicialización
document.addEventListener('DOMContentLoaded', () => {
    console.log('💬 LINO Tooltip System cargado');
});
