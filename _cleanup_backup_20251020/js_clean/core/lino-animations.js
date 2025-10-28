/**
 * LINO DESIGN SYSTEM V3 - ADVANCED ANIMATIONS & MICRO-INTERACTIONS
 * 
 * Sistema avanzado de animaciones que incluye:
 * 1. Micro-interacciones fluidas
 * 2. Animaciones de entrada/salida
 * 3. Efectos de hover avanzados
 * 4. Transiciones contextuales
 * 5. Performance optimization
 */

class LinoAnimationSystem {
    constructor() {
        this.animationQueue = [];
        this.isReducedMotion = this.checkReducedMotion();
        this.observers = new Map();
        this.timeline = new Map();
        
        this.init();
    }
    
    init() {
        this.setupIntersectionObserver();
        this.setupHoverEffects();
        this.setupFocusEffects();
        this.bindEvents();
        
        console.log('🎬 LINO Animation System inicializado');
    }
    
    checkReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }
    
    /**
     * Configurar animaciones de entrada con Intersection Observer
     */
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateIn(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px 0px -50px 0px'
        });
        
        // Observar elementos con animación de entrada
        document.querySelectorAll('[data-lino-animate]').forEach(el => {
            observer.observe(el);
        });
        
        this.observers.set('intersection', observer);
    }
    
    /**
     * Animaciones de entrada
     */
    animateIn(element) {
        if (this.isReducedMotion) return;
        
        const animationType = element.dataset.linoAnimate || 'fadeInUp';
        const delay = parseInt(element.dataset.linoDelay) || 0;
        const duration = parseInt(element.dataset.linoDuration) || 300;
        
        setTimeout(() => {
            element.classList.add('lino-animate-in');
            
            switch (animationType) {
                case 'fadeInUp':
                    this.fadeInUp(element, duration);
                    break;
                case 'slideInLeft':
                    this.slideInLeft(element, duration);
                    break;
                case 'slideInRight':
                    this.slideInRight(element, duration);
                    break;
                case 'scaleIn':
                    this.scaleIn(element, duration);
                    break;
                case 'rotateIn':
                    this.rotateIn(element, duration);
                    break;
                default:
                    this.fadeInUp(element, duration);
            }
        }, delay);
    }
    
    fadeInUp(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = `opacity ${duration}ms ease, transform ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        });
    }
    
    slideInLeft(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = 'translateX(-30px)';
        element.style.transition = `opacity ${duration}ms ease, transform ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateX(0)';
        });
    }
    
    slideInRight(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = 'translateX(30px)';
        element.style.transition = `opacity ${duration}ms ease, transform ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateX(0)';
        });
    }
    
    scaleIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = 'scale(0.9)';
        element.style.transition = `opacity ${duration}ms ease, transform ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
            element.style.transform = 'scale(1)';
        });
    }
    
    rotateIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = 'rotate(-10deg) scale(0.9)';
        element.style.transition = `opacity ${duration}ms ease, transform ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
            element.style.transform = 'rotate(0deg) scale(1)';
        });
    }
    
    /**
     * Efectos de hover avanzados
     */
    setupHoverEffects() {
        // Efecto de elevación para cards
        document.querySelectorAll('.lino-card, .lino-btn').forEach(element => {
            this.addHoverElevation(element);
        });
        
        // Efecto magnético para botones
        document.querySelectorAll('.lino-btn--primary').forEach(button => {
            this.addMagneticEffect(button);
        });
        
        // Efecto de ondas para clics
        document.querySelectorAll('.lino-btn, .lino-card').forEach(element => {
            this.addRippleEffect(element);
        });
    }
    
    addHoverElevation(element) {
        if (this.isReducedMotion) return;
        
        element.addEventListener('mouseenter', () => {
            element.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            element.style.transform = 'translateY(-2px)';
            element.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0)';
            element.style.boxShadow = '';
        });
    }
    
    addMagneticEffect(element) {
        if (this.isReducedMotion) return;
        
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            const moveX = x * 0.1;
            const moveY = y * 0.1;
            
            element.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = '';
        });
    }
    
    addRippleEffect(element) {
        element.addEventListener('click', (e) => {
            if (this.isReducedMotion) return;
            
            const ripple = document.createElement('span');
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.classList.add('lino-ripple');
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: linoRipple 0.6s ease-out;
                pointer-events: none;
                z-index: 1000;
            `;
            
            // Asegurar posición relativa
            const position = getComputedStyle(element).position;
            if (position === 'static') {
                element.style.position = 'relative';
            }
            element.style.overflow = 'hidden';
            
            element.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }
    
    /**
     * Efectos de foco para accesibilidad
     */
    setupFocusEffects() {
        document.querySelectorAll('button, input, select, textarea, a, [tabindex]').forEach(element => {
            element.addEventListener('focus', () => {
                if (this.isReducedMotion) return;
                
                element.style.transition = 'outline 0.2s ease, box-shadow 0.2s ease';
                element.style.outline = '2px solid var(--lino-focus-color, #007bff)';
                element.style.outlineOffset = '2px';
                element.style.boxShadow = '0 0 0 4px rgba(0, 123, 255, 0.1)';
            });
            
            element.addEventListener('blur', () => {
                element.style.outline = '';
                element.style.boxShadow = '';
            });
        });
    }
    
    /**
     * Animación de carga de elementos
     */
    showLoading(element, text = 'Cargando...') {
        if (this.isReducedMotion) {
            element.textContent = text;
            return;
        }
        
        const originalContent = element.innerHTML;
        element.innerHTML = `
            <span class="lino-loading">
                <span class="lino-loading__spinner"></span>
                <span class="lino-loading__text">${text}</span>
            </span>
        `;
        
        return () => {
            element.innerHTML = originalContent;
        };
    }
    
    /**
     * Transición suave entre estados
     */
    morphElement(element, newContent, duration = 300) {
        if (this.isReducedMotion) {
            element.innerHTML = newContent;
            return Promise.resolve();
        }
        
        return new Promise(resolve => {
            // Fade out
            element.style.transition = `opacity ${duration / 2}ms ease`;
            element.style.opacity = '0';
            
            setTimeout(() => {
                // Cambiar contenido
                element.innerHTML = newContent;
                
                // Fade in
                element.style.opacity = '1';
                
                setTimeout(resolve, duration / 2);
            }, duration / 2);
        });
    }
    
    /**
     * Animación de contadores
     */
    animateCounter(element, start = 0, end = null, duration = 1000) {
        if (this.isReducedMotion) {
            element.textContent = end || element.textContent;
            return;
        }
        
        const finalValue = end || parseInt(element.textContent) || 0;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (finalValue - start) * this.easeOutCubic(progress));
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    /**
     * Animación de progreso
     */
    animateProgress(progressBar, targetPercent, duration = 1000) {
        if (this.isReducedMotion) {
            progressBar.style.width = `${targetPercent}%`;
            return;
        }
        
        const startWidth = parseFloat(progressBar.style.width) || 0;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentWidth = startWidth + (targetPercent - startWidth) * this.easeOutCubic(progress);
            progressBar.style.width = `${currentWidth}%`;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    /**
     * Eventos del sistema
     */
    bindEvents() {
        // Detectar cambios en preferencias de movimiento
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addListener(() => {
            this.isReducedMotion = mediaQuery.matches;
            console.log(`🎭 Movimiento reducido: ${this.isReducedMotion ? 'activado' : 'desactivado'}`);
        });
        
        // Pausar animaciones cuando la página no es visible
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                document.body.classList.add('lino-animations-paused');
            } else {
                document.body.classList.remove('lino-animations-paused');
            }
        });
    }
    
    /**
     * API pública
     */
    animate(element, animation, options = {}) {
        const {
            duration = 300,
            delay = 0,
            easing = 'ease'
        } = options;
        
        if (this.isReducedMotion && !options.force) {
            return Promise.resolve();
        }
        
        return new Promise(resolve => {
            setTimeout(() => {
                if (typeof this[animation] === 'function') {
                    this[animation](element, duration);
                    setTimeout(resolve, duration);
                } else {
                    console.warn(`Animación '${animation}' no encontrada`);
                    resolve();
                }
            }, delay);
        });
    }
    
    /**
     * Limpiar recursos
     */
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
        this.animationQueue.length = 0;
        this.timeline.clear();
    }
}

// Instancia global
window.LinoAnimations = new LinoAnimationSystem();

// CSS para animaciones (se inyecta automáticamente)
const animationCSS = `
/* LINO ANIMATIONS CSS */
@keyframes linoRipple {
    from {
        transform: scale(0);
        opacity: 1;
    }
    to {
        transform: scale(2);
        opacity: 0;
    }
}

.lino-loading {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.lino-loading__spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: linoSpin 1s linear infinite;
}

@keyframes linoSpin {
    to { transform: rotate(360deg); }
}

.lino-animations-paused * {
    animation-play-state: paused !important;
    transition: none !important;
}

/* Reducir animaciones si está configurado */
@media (prefers-reduced-motion: reduce) {
    .lino-animate-in,
    .lino-loading__spinner {
        animation: none !important;
        transition: none !important;
    }
}
`;

// Inyectar CSS automáticamente
if (!document.getElementById('lino-animations-css')) {
    const style = document.createElement('style');
    style.id = 'lino-animations-css';
    style.textContent = animationCSS;
    document.head.appendChild(style);
}

// Auto-inicialización
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎬 LINO Animation System cargado');
    
    // API global para desarrollo
    window.linoAnimate = {
        fadeInUp: (el, duration) => window.LinoAnimations.fadeInUp(el, duration),
        slideInLeft: (el, duration) => window.LinoAnimations.slideInLeft(el, duration),
        slideInRight: (el, duration) => window.LinoAnimations.slideInRight(el, duration),
        scaleIn: (el, duration) => window.LinoAnimations.scaleIn(el, duration),
        rotateIn: (el, duration) => window.LinoAnimations.rotateIn(el, duration),
        showLoading: (el, text) => window.LinoAnimations.showLoading(el, text),
        morphElement: (el, content, duration) => window.LinoAnimations.morphElement(el, content, duration),
        animateCounter: (el, start, end, duration) => window.LinoAnimations.animateCounter(el, start, end, duration),
        animateProgress: (bar, percent, duration) => window.LinoAnimations.animateProgress(bar, percent, duration)
    };
});
