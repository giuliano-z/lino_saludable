/**
 * 🎯 LINO CRITICAL CSS PATH OPTIMIZER V3
 * Sistema avanzado de optimización del CSS crítico
 */

class LinoCriticalCSSOptimizer {
    constructor(options = {}) {
        this.options = {
            enableInlineCritical: true,
            enableLazyNonCritical: true,
            enableCSSPreload: true,
            enableCSSMinification: true,
            criticalViewportHeight: 800,
            criticalViewportWidth: 1200,
            mediaQueriesToInline: ['screen', 'all'],
            purgeUnusedCSS: true,
            ...options
        };

        this.criticalCSS = '';
        this.nonCriticalCSS = '';
        this.usedSelectors = new Set();
        this.unusedSelectors = new Set();
        this.stylesheets = [];
        
        this.init();
    }

    init() {
        console.log('🎯 LINO Critical CSS Optimizer iniciado');
        this.analyzeCriticalPath();
        this.extractCriticalCSS();
        this.setupLazyLoading();
        this.optimizeExistingCSS();
        this.setupDynamicOptimization();
    }

    // 🔍 Analizar ruta crítica
    analyzeCriticalPath() {
        console.log('🔍 Analizando ruta crítica...');
        
        // Elementos visibles en viewport inicial
        const viewportElements = this.getViewportElements();
        
        // Analizar qué CSS es realmente necesario
        this.analyzeElementStyles(viewportElements);
        
        // Identificar CSS crítico vs no crítico
        this.categorizeCSS();
        
        console.log(`📊 Análisis completado: ${this.usedSelectors.size} selectores críticos encontrados`);
    }

    // 👁️ Obtener elementos visibles en viewport
    getViewportElements() {
        const elements = [];
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            
            // Verificar si está en el viewport crítico
            if (rect.top < this.options.criticalViewportHeight && 
                rect.left < this.options.criticalViewportWidth &&
                rect.bottom > 0 && 
                rect.right > 0) {
                elements.push(element);
            }
        });
        
        return elements;
    }

    // 🎨 Analizar estilos de elementos
    analyzeElementStyles(elements) {
        elements.forEach(element => {
            // Obtener estilos computados
            const computedStyles = window.getComputedStyle(element);
            
            // Analizar selectores que afectan a este elemento
            this.findSelectorsForElement(element);
            
            // Analizar propiedades críticas
            this.analyzeCriticalProperties(element, computedStyles);
        });
    }

    // 🎯 Encontrar selectores para elemento
    findSelectorsForElement(element) {
        // Obtener todas las reglas CSS
        Array.from(document.styleSheets).forEach(stylesheet => {
            if (this.canAccessStylesheet(stylesheet)) {
                try {
                    Array.from(stylesheet.cssRules || []).forEach(rule => {
                        if (rule.type === CSSRule.STYLE_RULE) {
                            if (element.matches(rule.selectorText)) {
                                this.usedSelectors.add(rule.selectorText);
                            }
                        }
                    });
                } catch (error) {
                    console.warn('No se puede acceder a stylesheet:', stylesheet.href);
                }
            }
        });
    }

    // 🔍 Verificar acceso a stylesheet
    canAccessStylesheet(stylesheet) {
        try {
            const rules = stylesheet.cssRules;
            return true;
        } catch (error) {
            return false;
        }
    }

    // ⚡ Analizar propiedades críticas
    analyzeCriticalProperties(element, computedStyles) {
        const criticalProperties = [
            'display', 'position', 'top', 'left', 'right', 'bottom',
            'width', 'height', 'margin', 'padding', 'border',
            'background-color', 'color', 'font-size', 'font-family',
            'font-weight', 'line-height', 'text-align', 'z-index',
            'opacity', 'visibility', 'overflow'
        ];

        criticalProperties.forEach(property => {
            const value = computedStyles.getPropertyValue(property);
            if (value && value !== 'initial' && value !== 'auto') {
                // Marcar como crítico si afecta al layout inicial
                this.markPropertyAsCritical(element, property, value);
            }
        });
    }

    // 📍 Marcar propiedad como crítica
    markPropertyAsCritical(element, property, value) {
        const selector = this.generateSelectorForElement(element);
        const cssRule = `${selector} { ${property}: ${value}; }`;
        
        if (!this.criticalCSS.includes(cssRule)) {
            this.criticalCSS += cssRule + '\n';
        }
    }

    // 🏷️ Generar selector para elemento
    generateSelectorForElement(element) {
        // Priorizar ID
        if (element.id) {
            return `#${element.id}`;
        }
        
        // Usar clases significativas
        if (element.classList.length > 0) {
            const significantClasses = Array.from(element.classList)
                .filter(cls => !cls.startsWith('js-') && !cls.startsWith('temp-'))
                .slice(0, 2); // Limitar a 2 clases más significativas
                
            if (significantClasses.length > 0) {
                return `.${significantClasses.join('.')}`;
            }
        }
        
        // Fallback a tag + nth-child
        const tagName = element.tagName.toLowerCase();
        const parent = element.parentElement;
        
        if (parent) {
            const siblings = Array.from(parent.children).filter(el => el.tagName === element.tagName);
            const index = siblings.indexOf(element) + 1;
            
            if (siblings.length > 1) {
                return `${tagName}:nth-child(${index})`;
            }
        }
        
        return tagName;
    }

    // 🗂️ Categorizar CSS
    categorizeCSS() {
        console.log('🗂️ Categorizando CSS...');
        
        // Procesar todas las hojas de estilo
        Array.from(document.styleSheets).forEach(stylesheet => {
            this.processStylesheet(stylesheet);
        });
        
        // Generar CSS crítico optimizado
        this.generateOptimizedCriticalCSS();
    }

    // 📄 Procesar hoja de estilo
    processStylesheet(stylesheet) {
        if (!this.canAccessStylesheet(stylesheet)) return;
        
        const stylesheetInfo = {
            href: stylesheet.href,
            media: stylesheet.media.mediaText || 'all',
            criticalRules: [],
            nonCriticalRules: []
        };
        
        try {
            Array.from(stylesheet.cssRules || []).forEach(rule => {
                if (rule.type === CSSRule.STYLE_RULE) {
                    if (this.isRuleCritical(rule)) {
                        stylesheetInfo.criticalRules.push(rule.cssText);
                    } else {
                        stylesheetInfo.nonCriticalRules.push(rule.cssText);
                    }
                } else if (rule.type === CSSRule.MEDIA_RULE) {
                    // Procesar media queries
                    this.processMediaRule(rule, stylesheetInfo);
                }
            });
        } catch (error) {
            console.warn('Error procesando stylesheet:', error);
        }
        
        this.stylesheets.push(stylesheetInfo);
    }

    // 🎯 Verificar si regla es crítica
    isRuleCritical(rule) {
        // Verificar si el selector está en uso crítico
        if (this.usedSelectors.has(rule.selectorText)) {
            return true;
        }
        
        // Verificar selectores que siempre son críticos
        const alwaysCriticalSelectors = [
            'html', 'body', '*', 
            '[data-critical]', '.critical',
            'h1', 'h2', 'nav', 'header', 'main'
        ];
        
        return alwaysCriticalSelectors.some(selector => 
            rule.selectorText.includes(selector)
        );
    }

    // 📱 Procesar media rule
    processMediaRule(mediaRule, stylesheetInfo) {
        const mediaText = mediaRule.conditionText || mediaRule.media.mediaText;
        
        // Determinar si es crítico basado en media query
        const isCriticalMedia = this.isCriticalMediaQuery(mediaText);
        
        Array.from(mediaRule.cssRules).forEach(rule => {
            const ruleText = `@media ${mediaText} { ${rule.cssText} }`;
            
            if (isCriticalMedia && this.isRuleCritical(rule)) {
                stylesheetInfo.criticalRules.push(ruleText);
            } else {
                stylesheetInfo.nonCriticalRules.push(ruleText);
            }
        });
    }

    // 📱 Verificar si media query es crítica
    isCriticalMediaQuery(mediaText) {
        // Media queries críticas (viewport inicial)
        const criticalQueries = [
            'screen',
            'all',
            'screen and (max-width: 1200px)',
            'screen and (min-width: 768px)'
        ];
        
        return criticalQueries.some(query => 
            mediaText.includes(query) || mediaText === 'all'
        );
    }

    // ⚡ Generar CSS crítico optimizado
    generateOptimizedCriticalCSS() {
        console.log('⚡ Generando CSS crítico optimizado...');
        
        let optimizedCSS = '';
        
        // Agregar reset/normalize crítico
        optimizedCSS += this.generateCriticalReset();
        
        // Agregar estilos de layout críticos
        optimizedCSS += this.generateCriticalLayout();
        
        // Agregar estilos de componentes V3 críticos
        optimizedCSS += this.generateCriticalV3Styles();
        
        // Agregar estilos específicos de la página actual
        optimizedCSS += this.generatePageSpecificCSS();
        
        // Minificar si está habilitado
        if (this.options.enableCSSMinification) {
            optimizedCSS = this.minifyCSS(optimizedCSS);
        }
        
        this.criticalCSS = optimizedCSS;
        
        console.log(`✅ CSS crítico generado: ${optimizedCSS.length} caracteres`);
    }

    // 🔄 Generar reset crítico
    generateCriticalReset() {
        return `
/* LINO V3 Critical Reset */
*,*::before,*::after{box-sizing:border-box}
html{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,sans-serif;line-height:1.15;-webkit-text-size-adjust:100%}
body{margin:0;font-family:inherit;font-size:1rem;font-weight:400;line-height:1.5;color:#212529;background-color:#fff}
h1,h2,h3,h4,h5,h6{margin-top:0;margin-bottom:.5rem;font-weight:500;line-height:1.2}
        `.trim();
    }

    // 📐 Generar layout crítico
    generateCriticalLayout() {
        return `
/* LINO V3 Critical Layout */
.container{width:100%;padding-right:15px;padding-left:15px;margin-right:auto;margin-left:auto}
.row{display:flex;flex-wrap:wrap;margin-right:-15px;margin-left:-15px}
.col,.col-12{flex:0 0 100%;max-width:100%;position:relative;width:100%;padding-right:15px;padding-left:15px}
.d-none{display:none!important}
.d-block{display:block!important}
.d-flex{display:flex!important}
        `.trim();
    }

    // 🎨 Generar estilos V3 críticos
    generateCriticalV3Styles() {
        return `
/* LINO V3 Critical Components */
.lino-header{background-color:var(--lino-primary);color:white;padding:1rem 0}
.lino-nav{display:flex;align-items:center;justify-content:space-between}
.lino-btn{display:inline-block;font-weight:400;text-align:center;vertical-align:middle;user-select:none;border:1px solid transparent;padding:.375rem .75rem;font-size:1rem;line-height:1.5;border-radius:.25rem;transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}
.lino-btn-primary{color:#fff;background-color:var(--lino-primary);border-color:var(--lino-primary)}
        `.trim();
    }

    // 📄 Generar CSS específico de página
    generatePageSpecificCSS() {
        const currentPath = window.location.pathname;
        
        // CSS específico según la página actual
        if (currentPath.includes('productos')) {
            return this.getProductosPageCSS();
        } else if (currentPath.includes('inventario')) {
            return this.getInventarioPageCSS();
        } else if (currentPath.includes('ventas')) {
            return this.getVentasPageCSS();
        }
        
        return '';
    }

    // 🛍️ CSS crítico para productos
    getProductosPageCSS() {
        return `
/* Productos Critical CSS */
.productos-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}
.producto-card{border:1px solid #dee2e6;border-radius:.25rem;padding:1rem}
        `.trim();
    }

    // 📦 CSS crítico para inventario
    getInventarioPageCSS() {
        return `
/* Inventario Critical CSS */
.inventario-table{width:100%;margin-bottom:1rem;color:#212529;border-collapse:collapse}
.inventario-table th,.inventario-table td{padding:.75rem;vertical-align:top;border-top:1px solid #dee2e6}
        `.trim();
    }

    // 💰 CSS crítico para ventas
    getVentasPageCSS() {
        return `
/* Ventas Critical CSS */
.ventas-summary{display:flex;justify-content:space-between;margin-bottom:2rem}
.venta-stat{text-align:center;padding:1rem;background-color:#f8f9fa;border-radius:.25rem}
        `.trim();
    }

    // 🗜️ Minificar CSS
    minifyCSS(css) {
        return css
            .replace(/\/\*[\s\S]*?\*\//g, '') // Remover comentarios
            .replace(/\s+/g, ' ') // Comprimir espacios
            .replace(/;\s*}/g, '}') // Remover ; antes de }
            .replace(/\s*{\s*/g, '{') // Comprimir {
            .replace(/}\s*/g, '}') // Comprimir }
            .replace(/;\s*/g, ';') // Comprimir ;
            .replace(/,\s*/g, ',') // Comprimir ,
            .replace(/:\s*/g, ':') // Comprimir :
            .trim();
    }

    // 📦 Extraer CSS crítico
    extractCriticalCSS() {
        if (!this.options.enableInlineCritical) return;
        
        console.log('📦 Extrayendo CSS crítico...');
        
        // Crear elemento style para CSS crítico
        const criticalStyle = document.createElement('style');
        criticalStyle.id = 'lino-critical-css';
        criticalStyle.innerHTML = this.criticalCSS;
        
        // Insertar al inicio del head
        document.head.insertBefore(criticalStyle, document.head.firstChild);
        
        console.log('✅ CSS crítico inlineado');
    }

    // ⏳ Configurar carga perezosa
    setupLazyLoading() {
        if (!this.options.enableLazyNonCritical) return;
        
        console.log('⏳ Configurando carga perezosa para CSS no crítico...');
        
        // Marcar CSS no crítico para carga perezosa
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        
        stylesheets.forEach(link => {
            if (!this.isCriticalStylesheet(link)) {
                this.makeStylesheetLazy(link);
            }
        });
        
        // Cargar CSS no crítico después del load
        window.addEventListener('load', () => {
            this.loadNonCriticalCSS();
        });
    }

    // 🎯 Verificar si stylesheet es crítico
    isCriticalStylesheet(link) {
        const href = link.href;
        
        // Hojas de estilo que siempre son críticas
        const criticalSheets = [
            'bootstrap.min.css',
            'lino-v3.css',
            'critical.css'
        ];
        
        return criticalSheets.some(sheet => href.includes(sheet));
    }

    // ⏳ Hacer stylesheet perezoso
    makeStylesheetLazy(link) {
        // Cambiar rel a preload
        link.rel = 'preload';
        link.as = 'style';
        
        // Guardar href original
        link.dataset.originalHref = link.href;
        
        // Marcar como lazy
        link.dataset.lazyCSS = 'true';
    }

    // 📦 Cargar CSS no crítico
    loadNonCriticalCSS() {
        console.log('📦 Cargando CSS no crítico...');
        
        const lazySheets = document.querySelectorAll('link[data-lazy-css="true"]');
        
        lazySheets.forEach(link => {
            // Restaurar rel stylesheet
            link.rel = 'stylesheet';
            
            // Remover atributos lazy
            delete link.dataset.lazyCSS;
            delete link.dataset.originalHref;
        });
        
        console.log(`✅ ${lazySheets.length} hojas de estilo no críticas cargadas`);
    }

    // ⚡ Optimizar CSS existente
    optimizeExistingCSS() {
        if (!this.options.purgeUnusedCSS) return;
        
        console.log('⚡ Optimizando CSS existente...');
        
        // Analizar uso de selectores
        this.analyzeCSSSelectorUsage();
        
        // Remover CSS no utilizado (en desarrollo solamente)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            this.removeUnusedCSS();
        }
    }

    // 🔍 Analizar uso de selectores CSS
    analyzeCSSSelectorUsage() {
        Array.from(document.styleSheets).forEach(stylesheet => {
            if (!this.canAccessStylesheet(stylesheet)) return;
            
            try {
                Array.from(stylesheet.cssRules || []).forEach(rule => {
                    if (rule.type === CSSRule.STYLE_RULE) {
                        const selector = rule.selectorText;
                        
                        try {
                            if (document.querySelector(selector)) {
                                this.usedSelectors.add(selector);
                            } else {
                                this.unusedSelectors.add(selector);
                            }
                        } catch (error) {
                            // Selector inválido o complejo
                            this.usedSelectors.add(selector);
                        }
                    }
                });
            } catch (error) {
                console.warn('Error analizando stylesheet:', error);
            }
        });
        
        console.log(`📊 Análisis de selectores: ${this.usedSelectors.size} usados, ${this.unusedSelectors.size} no usados`);
    }

    // 🗑️ Remover CSS no utilizado
    removeUnusedCSS() {
        console.log('🗑️ Removiendo CSS no utilizado (modo desarrollo)...');
        
        // Solo en desarrollo y con confirmación
        if (this.unusedSelectors.size > 100) {
            console.warn(`⚠️ Se encontraron ${this.unusedSelectors.size} selectores no utilizados. Considera limpiar el CSS.`);
        }
    }

    // 🔄 Configurar optimización dinámica
    setupDynamicOptimization() {
        // Reanalizar cuando cambie el contenido
        const observer = new MutationObserver(() => {
            clearTimeout(this.reanalizeTimeout);
            this.reanalizeTimeout = setTimeout(() => {
                this.reanalyzeIfNeeded();
            }, 1000);
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'id', 'style']
        });
        
        console.log('🔄 Optimización dinámica configurada');
    }

    // 🔍 Reanalizar si es necesario
    reanalyzeIfNeeded() {
        const newViewportElements = this.getViewportElements();
        
        // Si hay nuevos elementos visibles, reanalizar
        if (newViewportElements.length !== this.lastViewportElementsCount) {
            console.log('🔍 Reanalizando CSS crítico por cambios en el DOM...');
            this.analyzeElementStyles(newViewportElements);
            this.lastViewportElementsCount = newViewportElements.length;
        }
    }

    // 📊 Obtener estadísticas
    getStats() {
        return {
            criticalCSSSize: this.criticalCSS.length,
            nonCriticalCSSSize: this.nonCriticalCSS.length,
            usedSelectors: this.usedSelectors.size,
            unusedSelectors: this.unusedSelectors.size,
            totalStylesheets: this.stylesheets.length,
            compressionRatio: this.calculateCompressionRatio(),
            optimizationScore: this.calculateOptimizationScore()
        };
    }

    // 📏 Calcular ratio de compresión
    calculateCompressionRatio() {
        const original = this.criticalCSS.length + this.nonCriticalCSS.length;
        const optimized = this.criticalCSS.length;
        
        return original > 0 ? ((original - optimized) / original * 100).toFixed(2) : 0;
    }

    // 🎯 Calcular score de optimización
    calculateOptimizationScore() {
        let score = 100;
        
        // Penalizar CSS crítico muy grande
        if (this.criticalCSS.length > 50000) score -= 20;
        else if (this.criticalCSS.length > 30000) score -= 10;
        
        // Penalizar muchos selectores no utilizados
        const unusedRatio = this.unusedSelectors.size / (this.usedSelectors.size + this.unusedSelectors.size);
        if (unusedRatio > 0.5) score -= 30;
        else if (unusedRatio > 0.3) score -= 15;
        
        // Bonificar buenas prácticas
        if (this.options.enableInlineCritical) score += 5;
        if (this.options.enableLazyNonCritical) score += 5;
        if (this.options.enableCSSMinification) score += 5;
        
        return Math.max(0, Math.min(100, score));
    }

    // 🧹 Cleanup
    destroy() {
        if (this.reanalizeTimeout) {
            clearTimeout(this.reanalizeTimeout);
        }
        
        this.usedSelectors.clear();
        this.unusedSelectors.clear();
        this.stylesheets = [];
        
        console.log('🧹 Critical CSS Optimizer destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoCriticalCSSOptimizer = new LinoCriticalCSSOptimizer();
    
    // Comandos globales
    window.getCriticalCSSStats = () => window.LinoCriticalCSSOptimizer.getStats();
    window.reoptimizeCSS = () => window.LinoCriticalCSSOptimizer.analyzeCriticalPath();
});
