/**
 * ⚡ LINO CODE SPLITTING SYSTEM V3
 * Sistema inteligente de división de código para optimización de carga
 */

class LinoCodeSplitter {
    constructor(options = {}) {
        this.options = {
            enableRouteBasedSplitting: true,
            enableFeatureBasedSplitting: true,
            enableVendorSplitting: true,
            preloadCriticalRoutes: true,
            chunkLoadTimeout: 10000,
            retryAttempts: 3,
            ...options
        };

        this.chunks = new Map();
        this.loadedChunks = new Set();
        this.loadingChunks = new Set();
        this.failedChunks = new Set();
        this.preloadedChunks = new Set();
        
        this.init();
    }

    init() {
        console.log('⚡ LINO Code Splitter iniciado');
        this.defineChunks();
        this.setupRouteBasedSplitting();
        this.setupFeatureBasedSplitting();
        this.setupVendorSplitting();
        this.preloadCriticalChunks();
        this.setupErrorHandling();
    }

    // 📦 Definir chunks del sistema
    defineChunks() {
        // Chunks por ruta/página
        this.chunks.set('productos', {
            type: 'route',
            priority: 'high',
            files: [
                '/static/js/modules/productos.js',
                '/static/css/modules/productos.css'
            ],
            dependencies: ['vendor-charts', 'common-forms']
        });

        this.chunks.set('inventario', {
            type: 'route',
            priority: 'high',
            files: [
                '/static/js/modules/inventario.js',
                '/static/css/modules/inventario.css'
            ],
            dependencies: ['vendor-tables', 'common-filters']
        });

        this.chunks.set('ventas', {
            type: 'route',
            priority: 'medium',
            files: [
                '/static/js/modules/ventas.js',
                '/static/css/modules/ventas.css'
            ],
            dependencies: ['vendor-charts', 'common-forms']
        });

        this.chunks.set('reportes', {
            type: 'route',
            priority: 'low',
            files: [
                '/static/js/modules/reportes.js',
                '/static/css/modules/reportes.css'
            ],
            dependencies: ['vendor-charts', 'vendor-pdf']
        });

        // Chunks de funcionalidades
        this.chunks.set('charts', {
            type: 'feature',
            priority: 'medium',
            files: [
                '/static/js/features/charts.js',
                '/static/css/features/charts.css'
            ],
            dependencies: ['vendor-charts']
        });

        this.chunks.set('tables', {
            type: 'feature',
            priority: 'medium',
            files: [
                '/static/js/features/tables.js',
                '/static/css/features/tables.css'
            ],
            dependencies: ['vendor-tables']
        });

        this.chunks.set('forms', {
            type: 'feature',
            priority: 'high',
            files: [
                '/static/js/features/forms.js',
                '/static/css/features/forms.css'
            ],
            dependencies: ['vendor-validation']
        });

        // Chunks de vendor/librerías
        this.chunks.set('vendor-charts', {
            type: 'vendor',
            priority: 'medium',
            files: [
                'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js'
            ],
            dependencies: []
        });

        this.chunks.set('vendor-tables', {
            type: 'vendor',
            priority: 'medium',
            files: [
                'https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js',
                'https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css'
            ],
            dependencies: ['vendor-jquery']
        });

        this.chunks.set('vendor-pdf', {
            type: 'vendor',
            priority: 'low',
            files: [
                'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
            ],
            dependencies: []
        });

        // Chunks comunes
        this.chunks.set('common-forms', {
            type: 'common',
            priority: 'high',
            files: [
                '/static/js/common/form-validation.js',
                '/static/js/common/form-helpers.js'
            ],
            dependencies: []
        });

        this.chunks.set('common-filters', {
            type: 'common',
            priority: 'medium',
            files: [
                '/static/js/common/filters.js',
                '/static/css/common/filters.css'
            ],
            dependencies: []
        });

        console.log(`📦 ${this.chunks.size} chunks definidos`);
    }

    // 🛣️ Configurar splitting basado en rutas
    setupRouteBasedSplitting() {
        if (!this.options.enableRouteBasedSplitting) return;

        // Detectar cambios de ruta
        this.currentRoute = this.getCurrentRoute();
        
        // Cargar chunk de la ruta actual
        this.loadRouteChunk(this.currentRoute);

        // Escuchar cambios de ruta (para SPAs)
        window.addEventListener('popstate', () => {
            const newRoute = this.getCurrentRoute();
            if (newRoute !== this.currentRoute) {
                this.handleRouteChange(newRoute);
            }
        });

        // Interceptar enlaces para precargar chunks
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.isInternalLink(link.href)) {
                const route = this.extractRouteFromUrl(link.href);
                this.preloadRouteChunk(route);
            }
        });

        console.log('🛣️ Route-based splitting configurado');
    }

    // 🎯 Configurar splitting basado en funcionalidades
    setupFeatureBasedSplitting() {
        if (!this.options.enableFeatureBasedSplitting) return;

        // Observar elementos que requieren funcionalidades específicas
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.checkForFeatureRequirements(node);
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Verificar funcionalidades necesarias en el DOM actual
        this.checkForFeatureRequirements(document.body);

        console.log('🎯 Feature-based splitting configurado');
    }

    // 📚 Configurar splitting de vendors
    setupVendorSplitting() {
        if (!this.options.enableVendorSplitting) return;

        // Los vendors se cargan bajo demanda o con las funcionalidades
        console.log('📚 Vendor splitting configurado');
    }

    // ⚡ Precargar chunks críticos
    async preloadCriticalChunks() {
        if (!this.options.preloadCriticalRoutes) return;

        const criticalChunks = Array.from(this.chunks.entries())
            .filter(([name, chunk]) => chunk.priority === 'high')
            .map(([name]) => name);

        for (const chunkName of criticalChunks) {
            await this.preloadChunk(chunkName);
        }

        console.log(`⚡ ${criticalChunks.length} chunks críticos precargados`);
    }

    // 🎯 Verificar requisitos de funcionalidades
    checkForFeatureRequirements(element) {
        // Verificar si necesita charts
        if (element.querySelector('[data-chart], .chart-container, canvas[data-chart-type]')) {
            this.loadChunk('charts');
        }

        // Verificar si necesita tables avanzadas
        if (element.querySelector('[data-table], .data-table, .sortable-table')) {
            this.loadChunk('tables');
        }

        // Verificar si necesita formularios avanzados
        if (element.querySelector('[data-validation], .form-validation, .advanced-form')) {
            this.loadChunk('forms');
        }

        // Verificar funcionalidades específicas de módulos
        if (element.querySelector('[data-module="productos"]')) {
            this.loadChunk('productos');
        }

        if (element.querySelector('[data-module="inventario"]')) {
            this.loadChunk('inventario');
        }
    }

    // 📍 Obtener ruta actual
    getCurrentRoute() {
        return window.location.pathname.split('/')[1] || 'home';
    }

    // 🔗 Extraer ruta de URL
    extractRouteFromUrl(url) {
        try {
            const urlObj = new URL(url, window.location.origin);
            return urlObj.pathname.split('/')[1] || 'home';
        } catch {
            return 'home';
        }
    }

    // 🔍 Verificar si es enlace interno
    isInternalLink(href) {
        try {
            const url = new URL(href, window.location.origin);
            return url.origin === window.location.origin;
        } catch {
            return false;
        }
    }

    // 🔄 Manejar cambio de ruta
    async handleRouteChange(newRoute) {
        console.log(`🔄 Cambio de ruta: ${this.currentRoute} → ${newRoute}`);
        
        this.currentRoute = newRoute;
        await this.loadRouteChunk(newRoute);
    }

    // 🛣️ Cargar chunk de ruta
    async loadRouteChunk(route) {
        const chunkName = this.getChunkNameForRoute(route);
        if (chunkName) {
            await this.loadChunk(chunkName);
        }
    }

    // 🔮 Precargar chunk de ruta
    async preloadRouteChunk(route) {
        const chunkName = this.getChunkNameForRoute(route);
        if (chunkName && !this.loadedChunks.has(chunkName)) {
            await this.preloadChunk(chunkName);
        }
    }

    // 🎯 Obtener nombre de chunk para ruta
    getChunkNameForRoute(route) {
        // Mapeo de rutas a chunks
        const routeMapping = {
            'productos': 'productos',
            'inventario': 'inventario',
            'ventas': 'ventas',
            'reportes': 'reportes',
            'materias-primas': 'inventario', // Reutilizar chunk de inventario
        };

        return routeMapping[route];
    }

    // 📦 Cargar chunk específico
    async loadChunk(chunkName, forceReload = false) {
        if (!this.chunks.has(chunkName)) {
            console.warn(`⚠️ Chunk '${chunkName}' no encontrado`);
            return false;
        }

        if (this.loadedChunks.has(chunkName) && !forceReload) {
            console.log(`✅ Chunk '${chunkName}' ya cargado`);
            return true;
        }

        if (this.loadingChunks.has(chunkName)) {
            console.log(`⏳ Chunk '${chunkName}' ya se está cargando`);
            return false;
        }

        this.loadingChunks.add(chunkName);
        
        try {
            const startTime = performance.now();
            const chunk = this.chunks.get(chunkName);

            // Cargar dependencias primero
            for (const dependency of chunk.dependencies) {
                await this.loadChunk(dependency);
            }

            // Cargar archivos del chunk
            await this.loadChunkFiles(chunk.files);

            this.loadedChunks.add(chunkName);
            this.loadingChunks.delete(chunkName);
            this.failedChunks.delete(chunkName);

            const loadTime = performance.now() - startTime;
            console.log(`✅ Chunk '${chunkName}' cargado en ${loadTime.toFixed(2)}ms`);

            // Ejecutar callback de carga si existe
            this.executeChunkCallback(chunkName);

            return true;

        } catch (error) {
            this.loadingChunks.delete(chunkName);
            this.failedChunks.add(chunkName);
            console.error(`❌ Error cargando chunk '${chunkName}':`, error);
            return false;
        }
    }

    // 🔮 Precargar chunk
    async preloadChunk(chunkName) {
        if (this.preloadedChunks.has(chunkName)) return;

        const chunk = this.chunks.get(chunkName);
        if (!chunk) return;

        try {
            // Precargar con prioridad baja
            for (const file of chunk.files) {
                this.preloadResource(file, 'low');
            }

            this.preloadedChunks.add(chunkName);
            console.log(`🔮 Chunk '${chunkName}' precargado`);

        } catch (error) {
            console.error(`❌ Error precargando chunk '${chunkName}':`, error);
        }
    }

    // 📄 Cargar archivos de chunk
    async loadChunkFiles(files) {
        const loadPromises = files.map(file => this.loadFile(file));
        await Promise.all(loadPromises);
    }

    // 📄 Cargar archivo específico
    async loadFile(filePath) {
        return new Promise((resolve, reject) => {
            const extension = filePath.split('.').pop();
            let element;

            if (extension === 'js') {
                element = document.createElement('script');
                element.src = filePath;
                element.async = true;
            } else if (extension === 'css') {
                element = document.createElement('link');
                element.rel = 'stylesheet';
                element.href = filePath;
            } else {
                reject(new Error(`Tipo de archivo no soportado: ${extension}`));
                return;
            }

            element.onload = () => resolve(filePath);
            element.onerror = () => reject(new Error(`Error cargando: ${filePath}`));

            // Timeout para evitar cuelgues
            setTimeout(() => {
                reject(new Error(`Timeout cargando: ${filePath}`));
            }, this.options.chunkLoadTimeout);

            document.head.appendChild(element);
        });
    }

    // 🔮 Precargar recurso
    preloadResource(url, priority = 'low') {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = url;
        link.setAttribute('importance', priority);

        if (url.endsWith('.js')) {
            link.as = 'script';
        } else if (url.endsWith('.css')) {
            link.as = 'style';
        }

        document.head.appendChild(link);
    }

    // ⚡ Ejecutar callback de chunk
    executeChunkCallback(chunkName) {
        const callbackName = `onChunk${chunkName.charAt(0).toUpperCase() + chunkName.slice(1)}Loaded`;
        
        if (typeof window[callbackName] === 'function') {
            try {
                window[callbackName]();
                console.log(`⚡ Callback '${callbackName}' ejecutado`);
            } catch (error) {
                console.error(`❌ Error ejecutando callback '${callbackName}':`, error);
            }
        }
    }

    // 🚨 Configurar manejo de errores
    setupErrorHandling() {
        window.addEventListener('error', (event) => {
            const element = event.target;
            
            if (element.tagName === 'SCRIPT' || element.tagName === 'LINK') {
                const chunkName = this.findChunkByFile(element.src || element.href);
                if (chunkName) {
                    this.handleChunkError(chunkName, event.error);
                }
            }
        });
    }

    // 🔍 Encontrar chunk por archivo
    findChunkByFile(filePath) {
        for (const [chunkName, chunk] of this.chunks.entries()) {
            if (chunk.files.includes(filePath)) {
                return chunkName;
            }
        }
        return null;
    }

    // 🚨 Manejar error de chunk
    async handleChunkError(chunkName, error) {
        console.error(`🚨 Error en chunk '${chunkName}':`, error);
        
        this.failedChunks.add(chunkName);
        this.loadingChunks.delete(chunkName);

        // Intentar recargar si hay reintentos disponibles
        const retryKey = `${chunkName}_retries`;
        const retries = window[retryKey] || 0;

        if (retries < this.options.retryAttempts) {
            window[retryKey] = retries + 1;
            console.log(`🔄 Reintentando cargar chunk '${chunkName}' (${retries + 1}/${this.options.retryAttempts})`);
            
            setTimeout(() => {
                this.loadChunk(chunkName, true);
            }, 1000 * (retries + 1)); // Backoff exponencial
        }
    }

    // 📊 Obtener estadísticas
    getStats() {
        return {
            totalChunks: this.chunks.size,
            loadedChunks: this.loadedChunks.size,
            loadingChunks: this.loadingChunks.size,
            failedChunks: this.failedChunks.size,
            preloadedChunks: this.preloadedChunks.size,
            currentRoute: this.currentRoute,
            chunksByType: this.getChunksByType(),
            loadedChunksList: Array.from(this.loadedChunks),
            failedChunksList: Array.from(this.failedChunks)
        };
    }

    // 📊 Obtener chunks por tipo
    getChunksByType() {
        const byType = {};
        
        for (const [name, chunk] of this.chunks.entries()) {
            if (!byType[chunk.type]) {
                byType[chunk.type] = [];
            }
            byType[chunk.type].push(name);
        }
        
        return byType;
    }

    // 🔄 Recargar chunk fallido
    async reloadFailedChunk(chunkName) {
        if (this.failedChunks.has(chunkName)) {
            this.failedChunks.delete(chunkName);
            return await this.loadChunk(chunkName, true);
        }
        return false;
    }

    // 🧹 Cleanup
    destroy() {
        this.chunks.clear();
        this.loadedChunks.clear();
        this.loadingChunks.clear();
        this.failedChunks.clear();
        this.preloadedChunks.clear();
        console.log('🧹 Code Splitter destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoCodeSplitter = new LinoCodeSplitter();
    
    // Comandos globales
    window.loadChunk = (name) => window.LinoCodeSplitter.loadChunk(name);
    window.preloadChunk = (name) => window.LinoCodeSplitter.preloadChunk(name);
    window.getChunkStats = () => window.LinoCodeSplitter.getStats();
});
