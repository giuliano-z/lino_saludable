/**
 * LINO DESIGN SYSTEM V3 - THEME MANAGER
 * Sistema completo de gestión de temas con detección automática
 * Features: Auto-detection, LocalStorage, Smooth transitions
 */

class LinoThemeManager {
    constructor() {
        this.themes = {
            light: {
                name: 'Claro',
                icon: 'fas fa-sun',
                value: 'light'
            },
            dark: {
                name: 'Oscuro', 
                icon: 'fas fa-moon',
                value: 'dark'
            },
            auto: {
                name: 'Automático',
                icon: 'fas fa-magic',
                value: 'auto'
            }
        };
        
        this.currentTheme = 'auto';
        this.systemPreference = 'light';
        this.storageKey = 'lino-theme-preference';
        
        this.init();
    }

    init() {
        // Detectar preferencia del sistema
        this.detectSystemPreference();
        
        // Cargar preferencia guardada
        this.loadSavedTheme();
        
        // Aplicar tema inicial
        this.applyTheme();
        
        // Listeners para cambios del sistema
        this.setupSystemChangeListener();
        
        // Crear toggle si no existe
        this.createThemeToggle();
        
        console.log('🌙 LINO Theme Manager iniciado - Tema:', this.getEffectiveTheme());
    }

    /**
     * Detectar preferencia del sistema
     */
    detectSystemPreference() {
        if (window.matchMedia) {
            this.systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
    }

    /**
     * Cargar tema guardado del localStorage
     */
    loadSavedTheme() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved && this.themes[saved]) {
            this.currentTheme = saved;
        }
    }

    /**
     * Obtener tema efectivo (resolviendo 'auto')
     */
    getEffectiveTheme() {
        return this.currentTheme === 'auto' ? this.systemPreference : this.currentTheme;
    }

    /**
     * Aplicar tema al DOM
     */
    applyTheme(withAnimation = false) {
        const effectiveTheme = this.getEffectiveTheme();
        
        // Agregar clase de animación si se requiere
        if (withAnimation) {
            document.body.classList.add('lino-theme-switching');
            setTimeout(() => {
                document.body.classList.remove('lino-theme-switching');
            }, 300);
        }

        // Aplicar atributo data-theme
        document.documentElement.setAttribute('data-theme', effectiveTheme);
        
        // También aplicar al body para compatibilidad
        document.body.setAttribute('data-theme', effectiveTheme);

        // Actualizar meta theme-color para PWA
        this.updateMetaThemeColor(effectiveTheme);

        // Actualizar toggle visual
        this.updateToggleState();

        // Dispatch evento personalizado
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: {
                theme: this.currentTheme,
                effective: effectiveTheme
            }
        }));

        console.log(`🎨 Tema aplicado: ${this.currentTheme} (efectivo: ${effectiveTheme})`);
    }

    /**
     * Cambiar tema
     */
    setTheme(theme, save = true) {
        if (!this.themes[theme]) {
            console.warn(`❌ Tema no válido: ${theme}`);
            return;
        }

        this.currentTheme = theme;

        if (save) {
            localStorage.setItem(this.storageKey, theme);
        }

        this.applyTheme(true);
    }

    /**
     * Alternar entre light/dark (ignorando auto)
     */
    toggleTheme() {
        const effectiveTheme = this.getEffectiveTheme();
        const newTheme = effectiveTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    /**
     * Configurar listener para cambios del sistema
     */
    setupSystemChangeListener() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                this.systemPreference = e.matches ? 'dark' : 'light';
                
                // Solo aplicar si el tema actual es 'auto'
                if (this.currentTheme === 'auto') {
                    this.applyTheme(true);
                }
                
                console.log(`🔄 Preferencia del sistema cambió a: ${this.systemPreference}`);
            });
        }
    }

    /**
     * Actualizar meta theme-color para PWA
     */
    updateMetaThemeColor(theme) {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }

        const colors = {
            light: '#2E8B57', // lino-primary light
            dark: '#0d1117'   // dark background
        };

        metaThemeColor.content = colors[theme] || colors.light;
    }

    /**
     * Crear toggle de tema
     */
    createThemeToggle() {
        // Buscar contenedor existente
        let container = document.querySelector('.lino-theme-toggle-container');
        
        if (!container) {
            // Crear y agregar al header si existe
            const header = document.querySelector('.lino-page-header-content .lino-page-actions');
            if (header) {
                container = document.createElement('div');
                container.className = 'lino-theme-toggle-container';
                container.style.marginLeft = 'var(--lino-spacing-sm)';
                header.appendChild(container);
            } else {
                return; // No hay donde poner el toggle
            }
        }

        // Generar HTML del toggle
        container.innerHTML = this.generateToggleHTML();

        // Configurar eventos
        this.setupToggleEvents(container);
    }

    /**
     * Generar HTML del toggle
     */
    generateToggleHTML() {
        return `
            <div class="lino-theme-toggle" title="Cambiar tema">
                ${Object.entries(this.themes).map(([key, theme]) => `
                    <div class="lino-theme-toggle__option" data-theme="${key}">
                        <i class="${theme.icon} lino-theme-toggle__icon"></i>
                        <span>${theme.name}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Configurar eventos del toggle
     */
    setupToggleEvents(container) {
        const options = container.querySelectorAll('.lino-theme-toggle__option');
        
        options.forEach(option => {
            option.addEventListener('click', () => {
                const theme = option.dataset.theme;
                this.setTheme(theme);
            });
        });
    }

    /**
     * Actualizar estado visual del toggle
     */
    updateToggleState() {
        const options = document.querySelectorAll('.lino-theme-toggle__option');
        
        options.forEach(option => {
            const isActive = option.dataset.theme === this.currentTheme;
            option.classList.toggle('lino-theme-toggle__option--active', isActive);
        });
    }

    /**
     * API pública simplificada
     */
    getTheme() {
        return this.getEffectiveTheme();
    }

    getEffectiveTheme() {
        return this.currentTheme === 'auto' ? this.systemPreference : this.currentTheme;
    }

    isDark() {
        return this.getEffectiveTheme() === 'dark';
    }

    isLight() {
        return this.getEffectiveTheme() === 'light';
    }

    /**
     * Utilidades para desarrolladores
     */
    getSystemPreference() {
        return this.systemPreference;
    }

    getThemeInfo() {
        return {
            current: this.currentTheme,
            effective: this.getEffectiveTheme(),
            system: this.systemPreference,
            themes: this.themes
        };
    }
}

// Inicialización automática
let linoThemeManager;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        linoThemeManager = new LinoThemeManager();
        window.LinoTheme = linoThemeManager;
        initializeThemeToggle();
        
        // Aplicar tema inicial inmediatamente
        linoThemeManager.applyTheme(false);
        console.log('🎨 LINO Theme inicializado:', linoThemeManager.getTheme());
    });
} else {
    linoThemeManager = new LinoThemeManager();
    window.LinoTheme = linoThemeManager;
    initializeThemeToggle();
    
    // Aplicar tema inicial inmediatamente
    linoThemeManager.applyTheme(false);
    console.log('🎨 LINO Theme inicializado:', linoThemeManager.getTheme());
}

// Función para inicializar el botón de toggle
function initializeThemeToggle() {
    const toggleButton = document.getElementById('lino-theme-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', (e) => {
            e.preventDefault();
            if (linoThemeManager) {
                linoThemeManager.toggleTheme();
                console.log('🎨 Tema alternado:', linoThemeManager.getTheme());
            }
        });
        console.log('🎯 Botón de tema conectado exitosamente');
    } else {
        console.warn('⚠️ Botón de tema no encontrado en el DOM');
        // Intentar nuevamente después de un momento
        setTimeout(initializeThemeToggle, 500);
    }
}

// API Global simplificada
window.LinoTheme = window.LinoTheme || {
    set: (theme) => linoThemeManager?.setTheme(theme),
    toggle: () => linoThemeManager?.toggleTheme(),
    get: () => linoThemeManager?.getTheme(),
    isDark: () => linoThemeManager?.isDark(),
    isLight: () => linoThemeManager?.isLight()
};

// Compatibilidad con testing legacy
window.toggleTheme = () => window.LinoTheme.toggle();

/**
 * EVENTOS PERSONALIZADOS
 * 
 * // Escuchar cambios de tema
 * window.addEventListener('themeChanged', (e) => {
 *     console.log('Tema cambió:', e.detail);
 * });
 */

/**
 * UTILIDADES CSS-IN-JS
 */
class LinoThemeUtils {
    static getCSSVariable(name) {
        return getComputedStyle(document.documentElement)
            .getPropertyValue(name).trim();
    }

    static setCSSVariable(name, value) {
        document.documentElement.style.setProperty(name, value);
    }

    static getCurrentColors() {
        return {
            primary: this.getCSSVariable('--lino-primary'),
            success: this.getCSSVariable('--lino-success'),
            warning: this.getCSSVariable('--lino-warning'),
            danger: this.getCSSVariable('--lino-danger'),
            info: this.getCSSVariable('--lino-info'),
            background: this.getCSSVariable('--lino-theme-bg'),
            surface: this.getCSSVariable('--lino-theme-surface'),
            textPrimary: this.getCSSVariable('--lino-theme-text-primary')
        };
    }

    static isColorSchemeSupported() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme)').matches !== undefined;
    }

    static getContrastRatio(color1, color2) {
        // Simplified contrast calculation
        // In a real implementation, you'd want a more robust function
        const getLuminance = (color) => {
            // Basic luminance calculation
            const rgb = parseInt(color.replace('#', ''), 16);
            const r = (rgb >> 16) & 0xff;
            const g = (rgb >> 8) & 0xff;
            const b = (rgb >> 0) & 0xff;
            return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        };
        
        const lum1 = getLuminance(color1);
        const lum2 = getLuminance(color2);
        
        return (Math.max(lum1, lum2) + 0.05) / (Math.min(lum1, lum2) + 0.05);
    }
}

// Exponer utilidades
window.LinoThemeUtils = LinoThemeUtils;

console.log('🎨 LINO Theme System loaded successfully!');

/**
 * EJEMPLOS DE USO:
 * 
 * // Cambiar tema programáticamente
 * LinoTheme.set('dark');
 * LinoTheme.set('light'); 
 * LinoTheme.set('auto');
 * 
 * // Alternar tema
 * LinoTheme.toggle();
 * 
 * // Verificar tema actual
 * console.log(LinoTheme.get()); // 'dark', 'light', or 'auto'
 * console.log(LinoTheme.isDark()); // true/false
 * 
 * // Escuchar cambios
 * window.addEventListener('themeChanged', (e) => {
 *     console.log('New theme:', e.detail.effective);
 * });
 * 
 * // Obtener colores actuales
 * const colors = LinoThemeUtils.getCurrentColors();
 * console.log(colors.primary); // Color primario actual
 */
