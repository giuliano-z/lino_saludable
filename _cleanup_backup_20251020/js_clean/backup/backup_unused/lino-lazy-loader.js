/**
 * 🚀 LINO LAZY LOADING SYSTEM V3
 * Sistema avanzado de carga perezosa para optimización de performance
 */

class LinoLazyLoader {
    constructor(options = {}) {
        this.options = {
            rootMargin: '50px',
            threshold: 0.1,
            enableImageLazyLoad: true,
            enableComponentLazyLoad: true,
            enableScriptLazyLoad: true,
            enableStyleLazyLoad: true,
            ...options
        };
        
        this.observer = null;
        this.loadedResources = new Set();
        this.init();
    }

    init() {
        console.log('🚀 LINO Lazy Loader iniciado');
        this.createIntersectionObserver();
        this.setupImageLazyLoading();
        this.setupComponentLazyLoading();
        this.setupScriptLazyLoading();
        this.setupStyleLazyLoading();
        this.setupDataLazyLoading();
    }

    // 👁️ Crear Intersection Observer
    createIntersectionObserver() {
        if (!('IntersectionObserver' in window)) {
            console.warn('IntersectionObserver no soportado, fallback a carga inmediata');
            this.loadAllImmediately();
            return;
        }

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadElement(entry.target);
                    this.observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: this.options.rootMargin,
            threshold: this.options.threshold
        });
    }

    // 🖼️ Lazy loading de imágenes
    setupImageLazyLoading() {
        if (!this.options.enableImageLazyLoad) return;

        // Imágenes con data-src
        const lazyImages = document.querySelectorAll('img[data-src], img[data-srcset]');
        lazyImages.forEach(img => {
            this.observer.observe(img);
        });

        // Imágenes de fondo con data-bg
        const lazyBackgrounds = document.querySelectorAll('[data-bg]');
        lazyBackgrounds.forEach(element => {
            this.observer.observe(element);
        });

        console.log(`🖼️ ${lazyImages.length + lazyBackgrounds.length} imágenes configuradas para lazy loading`);
    }

    // 🧩 Lazy loading de componentes V3
    setupComponentLazyLoading() {
        if (!this.options.enableComponentLazyLoad) return;

        // Componentes pesados que pueden cargarse después
        const lazyComponents = document.querySelectorAll('[data-lazy-component]');
        lazyComponents.forEach(component => {
            this.observer.observe(component);
        });

        // Tablas grandes
        const largeTables = document.querySelectorAll('table[data-lazy], .lino-table[data-lazy]');
        largeTables.forEach(table => {
            this.observer.observe(table);
        });

        // Charts y gráficos
        const charts = document.querySelectorAll('[data-chart], .chart-container[data-lazy]');
        charts.forEach(chart => {
            this.observer.observe(chart);
        });

        console.log(`🧩 ${lazyComponents.length + largeTables.length + charts.length} componentes configurados para lazy loading`);
    }

    // 📜 Lazy loading de scripts
    setupScriptLazyLoading() {
        if (!this.options.enableScriptLazyLoad) return;

        // Scripts no críticos
        const lazyScripts = document.querySelectorAll('script[data-lazy-src]');
        lazyScripts.forEach(script => {
            // Crear trigger invisible
            const trigger = document.createElement('div');
            trigger.className = 'lazy-script-trigger';
            trigger.style.height = '1px';
            trigger.dataset.lazyScript = script.dataset.lazySrc;
            
            script.parentNode.insertBefore(trigger, script);
            this.observer.observe(trigger);
        });

        console.log(`📜 ${lazyScripts.length} scripts configurados para lazy loading`);
    }

    // 🎨 Lazy loading de estilos
    setupStyleLazyLoading() {
        if (!this.options.enableStyleLazyLoad) return;

        // CSS no crítico
        const lazyStyles = document.querySelectorAll('link[data-lazy-href]');
        lazyStyles.forEach(link => {
            const trigger = document.createElement('div');
            trigger.className = 'lazy-style-trigger';
            trigger.style.height = '1px';
            trigger.dataset.lazyStyle = link.dataset.lazyHref;
            
            document.body.appendChild(trigger);
            this.observer.observe(trigger);
        });

        console.log(`🎨 ${lazyStyles.length} stylesheets configurados para lazy loading`);
    }

    // 📊 Lazy loading de datos
    setupDataLazyLoading() {
        // Contenedores que cargan datos via AJAX
        const lazyDataContainers = document.querySelectorAll('[data-lazy-url]');
        lazyDataContainers.forEach(container => {
            this.observer.observe(container);
        });

        console.log(`📊 ${lazyDataContainers.length} contenedores de datos configurados para lazy loading`);
    }

    // ⚡ Cargar elemento específico
    loadElement(element) {
        const startTime = performance.now();

        try {
            if (element.tagName === 'IMG') {
                this.loadImage(element);
            } else if (element.hasAttribute('data-bg')) {
                this.loadBackground(element);
            } else if (element.hasAttribute('data-lazy-component')) {
                this.loadComponent(element);
            } else if (element.hasAttribute('data-lazy-script')) {
                this.loadScript(element);
            } else if (element.hasAttribute('data-lazy-style')) {
                this.loadStyle(element);
            } else if (element.hasAttribute('data-lazy-url')) {
                this.loadData(element);
            }

            const loadTime = performance.now() - startTime;
            console.log(`⚡ Elemento cargado en ${loadTime.toFixed(2)}ms`);

        } catch (error) {
            console.error('❌ Error cargando elemento:', error);
        }
    }

    // 🖼️ Cargar imagen específica
    loadImage(img) {
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;

        if (src) {
            img.src = src;
            img.removeAttribute('data-src');
        }

        if (srcset) {
            img.srcset = srcset;
            img.removeAttribute('data-srcset');
        }

        // Añadir clase de cargado
        img.classList.add('lazy-loaded');
        
        // Efecto de fade in
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
        
        img.onload = () => {
            img.style.opacity = '1';
        };

        this.loadedResources.add(img.src || img.srcset);
    }

    // 🎨 Cargar fondo
    loadBackground(element) {
        const bgImage = element.dataset.bg;
        element.style.backgroundImage = `url(${bgImage})`;
        element.removeAttribute('data-bg');
        element.classList.add('lazy-loaded');
        
        this.loadedResources.add(bgImage);
    }

    // 🧩 Cargar componente
    async loadComponent(element) {
        const componentType = element.dataset.lazyComponent;
        
        try {
            switch (componentType) {
                case 'chart':
                    await this.loadChart(element);
                    break;
                case 'table':
                    await this.loadTable(element);
                    break;
                case 'map':
                    await this.loadMap(element);
                    break;
                default:
                    await this.loadGenericComponent(element);
            }
            
            element.classList.add('lazy-loaded');
            element.removeAttribute('data-lazy-component');
            
        } catch (error) {
            console.error(`❌ Error cargando componente ${componentType}:`, error);
        }
    }

    // 📊 Cargar gráfico
    async loadChart(element) {
        // Mostrar placeholder de carga
        element.innerHTML = `
            <div class="lino-loading-placeholder">
                <div class="lino-spinner"></div>
                <p>Cargando gráfico...</p>
            </div>
        `;

        // Simular carga de chart library
        const chartData = element.dataset.chartData;
        if (chartData) {
            // Aquí iría la lógica real del chart
            await new Promise(resolve => setTimeout(resolve, 500));
            element.innerHTML = '<div class="chart-placeholder">📊 Gráfico cargado</div>';
        }
    }

    // 📄 Cargar tabla
    async loadTable(element) {
        const tableUrl = element.dataset.tableUrl;
        if (!tableUrl) return;

        element.innerHTML = `
            <div class="lino-loading-placeholder">
                <div class="lino-spinner"></div>
                <p>Cargando datos...</p>
            </div>
        `;

        try {
            // Simular carga de datos
            await new Promise(resolve => setTimeout(resolve, 300));
            element.innerHTML = '<div class="table-placeholder">📄 Tabla cargada</div>';
        } catch (error) {
            element.innerHTML = '<div class="error-placeholder">❌ Error cargando tabla</div>';
        }
    }

    // 🗺️ Cargar mapa
    async loadMap(element) {
        element.innerHTML = `
            <div class="lino-loading-placeholder">
                <div class="lino-spinner"></div>
                <p>Cargando mapa...</p>
            </div>
        `;

        await new Promise(resolve => setTimeout(resolve, 800));
        element.innerHTML = '<div class="map-placeholder">🗺️ Mapa cargado</div>';
    }

    // 🔧 Cargar componente genérico
    async loadGenericComponent(element) {
        const componentUrl = element.dataset.componentUrl;
        if (componentUrl) {
            try {
                const response = await fetch(componentUrl);
                const html = await response.text();
                element.innerHTML = html;
            } catch (error) {
                element.innerHTML = '<div class="error-placeholder">❌ Error cargando componente</div>';
            }
        }
    }

    // 📜 Cargar script
    loadScript(element) {
        const scriptSrc = element.dataset.lazyScript;
        
        const script = document.createElement('script');
        script.src = scriptSrc;
        script.async = true;
        
        script.onload = () => {
            console.log(`📜 Script cargado: ${scriptSrc}`);
            element.classList.add('lazy-loaded');
        };
        
        script.onerror = () => {
            console.error(`❌ Error cargando script: ${scriptSrc}`);
        };
        
        document.head.appendChild(script);
        this.loadedResources.add(scriptSrc);
    }

    // 🎨 Cargar estilo
    loadStyle(element) {
        const styleSrc = element.dataset.lazyStyle;
        
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = styleSrc;
        
        link.onload = () => {
            console.log(`🎨 Estilo cargado: ${styleSrc}`);
            element.classList.add('lazy-loaded');
        };
        
        link.onerror = () => {
            console.error(`❌ Error cargando estilo: ${styleSrc}`);
        };
        
        document.head.appendChild(link);
        this.loadedResources.add(styleSrc);
    }

    // 📊 Cargar datos
    async loadData(element) {
        const dataUrl = element.dataset.lazyUrl;
        const loadingTemplate = element.dataset.loadingTemplate || 'Cargando...';
        
        element.innerHTML = `<div class="lino-loading-placeholder">${loadingTemplate}</div>`;
        
        try {
            const response = await fetch(dataUrl);
            const data = await response.json();
            
            // Procesar datos según tipo
            const dataType = element.dataset.dataType || 'html';
            
            switch (dataType) {
                case 'json':
                    element.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    break;
                case 'table':
                    element.innerHTML = this.renderDataAsTable(data);
                    break;
                default:
                    element.innerHTML = data.html || JSON.stringify(data);
            }
            
            element.classList.add('lazy-loaded');
            this.loadedResources.add(dataUrl);
            
        } catch (error) {
            element.innerHTML = '<div class="error-placeholder">❌ Error cargando datos</div>';
            console.error('Error loading data:', error);
        }
    }

    // 📋 Renderizar datos como tabla
    renderDataAsTable(data) {
        if (!Array.isArray(data) || data.length === 0) {
            return '<p>No hay datos disponibles</p>';
        }

        const headers = Object.keys(data[0]);
        
        return `
            <table class="lino-table">
                <thead>
                    <tr>
                        ${headers.map(header => `<th>${header}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${data.map(row => `
                        <tr>
                            ${headers.map(header => `<td>${row[header] || ''}</td>`).join('')}
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    // 🚫 Fallback para navegadores sin soporte
    loadAllImmediately() {
        // Cargar todas las imágenes inmediatamente
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });

        // Cargar todos los fondos
        document.querySelectorAll('[data-bg]').forEach(element => {
            this.loadBackground(element);
        });

        console.log('⚠️ Carga inmediata activada (fallback)');
    }

    // 📊 Obtener estadísticas de carga
    getStats() {
        return {
            loadedResources: this.loadedResources.size,
            observedElements: this.observer ? 0 : 0, // Se actualiza dinámicamente
            resourceList: Array.from(this.loadedResources)
        };
    }

    // 🔄 Actualizar configuración
    updateOptions(newOptions) {
        this.options = { ...this.options, ...newOptions };
        console.log('⚙️ Configuración de Lazy Loader actualizada');
    }

    // 🧹 Cleanup
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
        this.loadedResources.clear();
        console.log('🧹 Lazy Loader destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoLazyLoader = new LinoLazyLoader();
    
    // Comando global para estadísticas
    window.getLazyStats = () => window.LinoLazyLoader.getStats();
});
