/**
 * 🎯 LINO RESOURCE PRELOADER V3
 * Sistema avanzado de precarga de recursos para optimización predictiva
 */

class LinoResourcePreloader {
    constructor(options = {}) {
        this.options = {
            enablePredictivePreloading: true,
            enableUserBehaviorTracking: true,
            enableIntersectionPreloading: true,
            enableMouseHoverPreloading: true,
            enableTouchPreloading: true,
            preloadPriority: 'high',
            preloadTimeout: 5000,
            maxConcurrentPreloads: 6,
            userBehaviorSampleSize: 100,
            ...options
        };

        this.preloadQueue = [];
        this.preloadedResources = new Set();
        this.failedPreloads = new Set();
        this.userBehaviorData = new Map();
        this.preloadStats = {
            attempted: 0,
            successful: 0,
            failed: 0,
            cached: 0
        };
        
        this.currentPreloads = 0;
        this.init();
    }

    init() {
        console.log('🎯 LINO Resource Preloader iniciado');
        this.setupPredictivePreloading();
        this.setupIntersectionPreloading();
        this.setupMouseHoverPreloading();
        this.setupTouchPreloading();
        this.setupUserBehaviorTracking();
        this.preloadCriticalResources();
        this.setupNetworkAdaptivePreloading();
    }

    // 🔮 Configurar precarga predictiva
    setupPredictivePreloading() {
        if (!this.options.enablePredictivePreloading) return;

        // Analizar patrones de navegación
        this.analyzeNavigationPatterns();
        
        // Precargar rutas probables
        this.preloadProbableRoutes();
        
        // Configurar precarga basada en tiempo
        this.setupTimeBasedPreloading();
        
        console.log('🔮 Precarga predictiva configurada');
    }

    // 📊 Analizar patrones de navegación
    analyzeNavigationPatterns() {
        const currentPath = window.location.pathname;
        const sessionData = this.getSessionData();
        
        // Incrementar contador de visitas para esta ruta
        sessionData.visits = sessionData.visits || {};
        sessionData.visits[currentPath] = (sessionData.visits[currentPath] || 0) + 1;
        
        // Registrar ruta anterior para análisis de secuencias
        if (sessionData.lastPath && sessionData.lastPath !== currentPath) {
            sessionData.sequences = sessionData.sequences || {};
            const sequence = `${sessionData.lastPath}->${currentPath}`;
            sessionData.sequences[sequence] = (sessionData.sequences[sequence] || 0) + 1;
        }
        
        sessionData.lastPath = currentPath;
        this.saveSessionData(sessionData);
        
        console.log('📊 Patrones de navegación actualizados');
    }

    // 🎯 Precargar rutas probables
    preloadProbableRoutes() {
        const sessionData = this.getSessionData();
        const currentPath = window.location.pathname;
        
        if (!sessionData.sequences) return;
        
        // Encontrar rutas más probables después de la actual
        const probableRoutes = Object.entries(sessionData.sequences)
            .filter(([sequence]) => sequence.startsWith(currentPath + '->'))
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3) // Top 3 rutas más probables
            .map(([sequence]) => sequence.split('->')[1]);
        
        // Precargar recursos de rutas probables
        probableRoutes.forEach(route => {
            this.preloadRouteResources(route);
        });
        
        console.log(`🎯 Precargando ${probableRoutes.length} rutas probables`);
    }

    // ⏰ Configurar precarga basada en tiempo
    setupTimeBasedPreloading() {
        // Precargar recursos después de que la página se haya cargado completamente
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.preloadNonCriticalResources();
            }, 2000); // Esperar 2 segundos después del load
        });
        
        // Precargar en idle time
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                this.preloadDuringIdleTime();
            });
        }
    }

    // 👁️ Configurar precarga por intersección
    setupIntersectionPreloading() {
        if (!this.options.enableIntersectionPreloading || !('IntersectionObserver' in window)) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.handleIntersectionPreload(entry.target);
                }
            });
        }, {
            rootMargin: '200px 0px', // Precargar cuando esté 200px cerca
            threshold: 0
        });

        // Observar enlaces
        document.querySelectorAll('a[href]').forEach(link => {
            if (this.shouldPreloadLink(link)) {
                observer.observe(link);
            }
        });

        // Observar imágenes lazy
        document.querySelectorAll('img[data-src]').forEach(img => {
            observer.observe(img);
        });

        // Observar componentes que requieren recursos
        document.querySelectorAll('[data-preload]').forEach(element => {
            observer.observe(element);
        });

        console.log('👁️ Intersection preloading configurado');
    }

    // 🖱️ Configurar precarga por hover
    setupMouseHoverPreloading() {
        if (!this.options.enableMouseHoverPreloading) return;

        let hoverTimeout;

        document.addEventListener('mouseover', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.shouldPreloadLink(link)) {
                hoverTimeout = setTimeout(() => {
                    this.preloadLinkResources(link);
                }, 100); // Precargar después de 100ms de hover
            }
        });

        document.addEventListener('mouseout', () => {
            if (hoverTimeout) {
                clearTimeout(hoverTimeout);
            }
        });

        console.log('🖱️ Mouse hover preloading configurado');
    }

    // 👆 Configurar precarga por touch
    setupTouchPreloading() {
        if (!this.options.enableTouchPreloading) return;

        document.addEventListener('touchstart', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.shouldPreloadLink(link)) {
                // En touch devices, precargar inmediatamente en touchstart
                this.preloadLinkResources(link);
            }
        });

        console.log('👆 Touch preloading configurado');
    }

    // 📈 Configurar tracking de comportamiento
    setupUserBehaviorTracking() {
        if (!this.options.enableUserBehaviorTracking) return;

        // Tracking de clics
        document.addEventListener('click', (e) => {
            this.trackUserInteraction('click', e.target);
        });

        // Tracking de scroll
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.trackScrollBehavior();
            }, 100);
        });

        // Tracking de tiempo en página
        this.trackTimeOnPage();

        console.log('📈 User behavior tracking configurado');
    }

    // 🔗 Verificar si debe precargar enlace
    shouldPreloadLink(link) {
        const href = link.href;
        
        // No precargar enlaces externos
        if (!href || !href.startsWith(window.location.origin)) return false;
        
        // No precargar anchors
        if (href.includes('#')) return false;
        
        // No precargar descargas
        if (link.hasAttribute('download')) return false;
        
        // No precargar si ya está precargado
        if (this.preloadedResources.has(href)) return false;
        
        // No precargar si falló anteriormente
        if (this.failedPreloads.has(href)) return false;
        
        return true;
    }

    // 🎯 Manejar precarga por intersección
    handleIntersectionPreload(element) {
        if (element.tagName === 'A') {
            this.preloadLinkResources(element);
        } else if (element.tagName === 'IMG') {
            this.preloadImage(element);
        } else if (element.hasAttribute('data-preload')) {
            this.preloadElementResources(element);
        }
    }

    // 🔗 Precargar recursos de enlace
    async preloadLinkResources(link) {
        const href = link.href;
        
        if (!this.shouldPreloadLink(link)) return;
        
        try {
            // Precargar la página
            await this.preloadResource(href, 'document');
            
            // Precargar recursos críticos de la ruta
            const route = this.extractRouteFromUrl(href);
            await this.preloadRouteResources(route);
            
            console.log(`🔗 Recursos de enlace precargados: ${href}`);
            
        } catch (error) {
            console.warn('Error precargando enlace:', error);
            this.failedPreloads.add(href);
        }
    }

    // 🖼️ Precargar imagen
    async preloadImage(img) {
        const src = img.dataset.src || img.src;
        if (!src || this.preloadedResources.has(src)) return;
        
        try {
            await this.preloadResource(src, 'image');
            console.log(`🖼️ Imagen precargada: ${src}`);
        } catch (error) {
            console.warn('Error precargando imagen:', error);
        }
    }

    // 🧩 Precargar recursos de elemento
    async preloadElementResources(element) {
        const preloadData = element.dataset.preload;
        
        try {
            const resources = JSON.parse(preloadData);
            
            for (const resource of resources) {
                await this.preloadResource(resource.url, resource.type);
            }
            
            console.log(`🧩 Recursos de elemento precargados`);
            
        } catch (error) {
            console.warn('Error precargando recursos de elemento:', error);
        }
    }

    // 🛣️ Precargar recursos de ruta
    async preloadRouteResources(route) {
        const routeResources = this.getRouteResources(route);
        
        for (const resource of routeResources) {
            await this.preloadResource(resource.url, resource.type, resource.priority);
        }
    }

    // 📋 Obtener recursos de ruta
    getRouteResources(route) {
        const resourceMap = {
            'productos': [
                { url: '/static/js/modules/productos.js', type: 'script', priority: 'high' },
                { url: '/static/css/modules/productos.css', type: 'style', priority: 'high' },
                { url: '/api/productos/', type: 'fetch', priority: 'medium' }
            ],
            'inventario': [
                { url: '/static/js/modules/inventario.js', type: 'script', priority: 'high' },
                { url: '/static/css/modules/inventario.css', type: 'style', priority: 'high' },
                { url: '/api/inventario/', type: 'fetch', priority: 'medium' }
            ],
            'ventas': [
                { url: '/static/js/modules/ventas.js', type: 'script', priority: 'high' },
                { url: '/static/css/modules/ventas.css', type: 'style', priority: 'high' },
                { url: '/api/ventas/', type: 'fetch', priority: 'medium' }
            ],
            'reportes': [
                { url: '/static/js/modules/reportes.js', type: 'script', priority: 'medium' },
                { url: '/static/css/modules/reportes.css', type: 'style', priority: 'medium' },
                { url: 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js', type: 'script', priority: 'low' }
            ]
        };
        
        return resourceMap[route] || [];
    }

    // ⚡ Precargar recurso específico
    async preloadResource(url, type = 'fetch', priority = 'low') {
        if (this.preloadedResources.has(url) || this.currentPreloads >= this.options.maxConcurrentPreloads) {
            return;
        }

        this.currentPreloads++;
        this.preloadStats.attempted++;

        try {
            const link = document.createElement('link');
            
            switch (type) {
                case 'script':
                    link.rel = 'preload';
                    link.as = 'script';
                    link.href = url;
                    break;
                case 'style':
                    link.rel = 'preload';
                    link.as = 'style';
                    link.href = url;
                    break;
                case 'image':
                    link.rel = 'preload';
                    link.as = 'image';
                    link.href = url;
                    break;
                case 'document':
                    link.rel = 'prefetch';
                    link.href = url;
                    break;
                case 'fetch':
                    // Para APIs, usar fetch con cache
                    await fetch(url, { 
                        cache: 'force-cache',
                        priority: priority 
                    });
                    this.preloadedResources.add(url);
                    this.preloadStats.successful++;
                    return;
            }

            // Configurar prioridad
            if (link.rel === 'preload') {
                link.setAttribute('importance', priority);
            }

            // Configurar timeout
            const timeout = setTimeout(() => {
                this.handlePreloadTimeout(url);
            }, this.options.preloadTimeout);

            link.onload = () => {
                clearTimeout(timeout);
                this.preloadedResources.add(url);
                this.preloadStats.successful++;
                this.currentPreloads--;
            };

            link.onerror = () => {
                clearTimeout(timeout);
                this.failedPreloads.add(url);
                this.preloadStats.failed++;
                this.currentPreloads--;
            };

            document.head.appendChild(link);
            
        } catch (error) {
            this.preloadStats.failed++;
            this.currentPreloads--;
            this.failedPreloads.add(url);
            console.warn(`Error precargando ${url}:`, error);
        }
    }

    // ⏰ Manejar timeout de precarga
    handlePreloadTimeout(url) {
        console.warn(`⏰ Timeout precargando: ${url}`);
        this.failedPreloads.add(url);
        this.preloadStats.failed++;
        this.currentPreloads--;
    }

    // 🚀 Precargar recursos críticos
    preloadCriticalResources() {
        const criticalResources = [
            { url: '/static/css/lino-v3.css', type: 'style', priority: 'high' },
            { url: '/static/js/lino-core.js', type: 'script', priority: 'high' },
            { url: '/static/fonts/lino-icons.woff2', type: 'font', priority: 'high' }
        ];

        criticalResources.forEach(resource => {
            this.preloadResource(resource.url, resource.type, resource.priority);
        });

        console.log('🚀 Recursos críticos en precarga');
    }

    // ⏱️ Precargar recursos no críticos
    preloadNonCriticalResources() {
        const nonCriticalResources = [
            { url: '/static/js/features/charts.js', type: 'script', priority: 'low' },
            { url: '/static/js/features/tables.js', type: 'script', priority: 'low' },
            { url: '/static/css/features/animations.css', type: 'style', priority: 'low' }
        ];

        nonCriticalResources.forEach(resource => {
            this.preloadResource(resource.url, resource.type, resource.priority);
        });

        console.log('⏱️ Recursos no críticos en precarga');
    }

    // 🎯 Precargar durante idle time
    preloadDuringIdleTime() {
        const idleResources = [
            '/api/productos/',
            '/api/inventario/',
            '/api/ventas/summary/',
            '/static/images/backgrounds/dashboard.jpg'
        ];

        idleResources.forEach(url => {
            if ('requestIdleCallback' in window) {
                requestIdleCallback(() => {
                    this.preloadResource(url, 'fetch', 'low');
                });
            }
        });

        console.log('🎯 Precarga en idle time configurada');
    }

    // 🌐 Configurar precarga adaptiva a la red
    setupNetworkAdaptivePreloading() {
        if (!('connection' in navigator)) return;

        const connection = navigator.connection;
        
        // Ajustar estrategia según tipo de conexión
        connection.addEventListener('change', () => {
            this.adaptPreloadingToNetwork(connection);
        });

        // Configuración inicial
        this.adaptPreloadingToNetwork(connection);

        console.log('🌐 Precarga adaptiva a la red configurada');
    }

    // 📶 Adaptar precarga a la red
    adaptPreloadingToNetwork(connection) {
        const effectiveType = connection.effectiveType;
        
        switch (effectiveType) {
            case 'slow-2g':
            case '2g':
                this.options.maxConcurrentPreloads = 1;
                this.options.preloadTimeout = 10000;
                this.options.enablePredictivePreloading = false;
                break;
            case '3g':
                this.options.maxConcurrentPreloads = 3;
                this.options.preloadTimeout = 7000;
                this.options.enablePredictivePreloading = true;
                break;
            case '4g':
            default:
                this.options.maxConcurrentPreloads = 6;
                this.options.preloadTimeout = 5000;
                this.options.enablePredictivePreloading = true;
                break;
        }

        console.log(`📶 Precarga adaptada para conexión ${effectiveType}`);
    }

    // 📊 Tracking de interacción
    trackUserInteraction(type, target) {
        const data = this.userBehaviorData.get(type) || [];
        
        data.push({
            timestamp: Date.now(),
            target: target.tagName,
            className: target.className,
            href: target.href || null
        });

        // Mantener solo los últimos registros
        if (data.length > this.options.userBehaviorSampleSize) {
            data.shift();
        }

        this.userBehaviorData.set(type, data);
    }

    // 📜 Tracking de scroll
    trackScrollBehavior() {
        const scrollData = this.userBehaviorData.get('scroll') || [];
        
        scrollData.push({
            timestamp: Date.now(),
            scrollY: window.scrollY,
            viewportHeight: window.innerHeight,
            documentHeight: document.documentElement.scrollHeight
        });

        if (scrollData.length > 50) {
            scrollData.shift();
        }

        this.userBehaviorData.set('scroll', scrollData);
    }

    // ⏱️ Tracking de tiempo en página
    trackTimeOnPage() {
        this.pageStartTime = Date.now();
        
        window.addEventListener('beforeunload', () => {
            const timeOnPage = Date.now() - this.pageStartTime;
            const sessionData = this.getSessionData();
            
            sessionData.timeOnPage = sessionData.timeOnPage || {};
            sessionData.timeOnPage[window.location.pathname] = timeOnPage;
            
            this.saveSessionData(sessionData);
        });
    }

    // 🔗 Extraer ruta de URL
    extractRouteFromUrl(url) {
        try {
            const urlObj = new URL(url);
            return urlObj.pathname.split('/')[1] || 'home';
        } catch {
            return 'home';
        }
    }

    // 💾 Obtener datos de sesión
    getSessionData() {
        try {
            const data = sessionStorage.getItem('lino_session_data');
            return data ? JSON.parse(data) : {};
        } catch {
            return {};
        }
    }

    // 💾 Guardar datos de sesión
    saveSessionData(data) {
        try {
            sessionStorage.setItem('lino_session_data', JSON.stringify(data));
        } catch (error) {
            console.warn('Error guardando datos de sesión:', error);
        }
    }

    // 📊 Obtener estadísticas
    getStats() {
        return {
            ...this.preloadStats,
            successRate: (this.preloadStats.successful / this.preloadStats.attempted * 100).toFixed(2),
            currentPreloads: this.currentPreloads,
            preloadedResources: this.preloadedResources.size,
            failedPreloads: this.failedPreloads.size,
            userBehaviorDataPoints: Array.from(this.userBehaviorData.values()).reduce((sum, arr) => sum + arr.length, 0)
        };
    }

    // 🧹 Cleanup
    destroy() {
        this.preloadQueue = [];
        this.preloadedResources.clear();
        this.failedPreloads.clear();
        this.userBehaviorData.clear();
        
        console.log('🧹 Resource Preloader destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoResourcePreloader = new LinoResourcePreloader();
    
    // Comandos globales
    window.getPreloadStats = () => window.LinoResourcePreloader.getStats();
    window.preloadResource = (url, type, priority) => window.LinoResourcePreloader.preloadResource(url, type, priority);
});
