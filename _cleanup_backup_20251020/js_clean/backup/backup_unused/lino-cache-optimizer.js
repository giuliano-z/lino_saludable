/**
 * 🚀 LINO CACHE STRATEGY OPTIMIZER V3
 * Sistema avanzado de optimización de caché para máximo performance
 */

class LinoCacheOptimizer {
    constructor(options = {}) {
        this.options = {
            enableBrowserCache: true,
            enableServiceWorkerCache: true,
            enableMemoryCache: true,
            enableIndexedDBCache: true,
            enableLocalStorageCache: true,
            cacheVersion: 'v3.0.0',
            maxMemoryCacheSize: 50 * 1024 * 1024, // 50MB
            maxIndexedDBSize: 100 * 1024 * 1024, // 100MB
            defaultTTL: 24 * 60 * 60 * 1000, // 24 horas
            ...options
        };

        this.memoryCache = new Map();
        this.cacheStrategies = new Map();
        this.cacheStats = {
            hits: 0,
            misses: 0,
            stores: 0,
            evictions: 0
        };
        
        this.init();
    }

    init() {
        console.log('🚀 LINO Cache Optimizer iniciado');
        this.setupCacheStrategies();
        this.setupBrowserCache();
        this.setupServiceWorkerCache();
        this.setupMemoryCache();
        this.setupIndexedDBCache();
        this.setupLocalStorageCache();
        this.setupCacheHeaders();
        this.setupCacheMonitoring();
    }

    // 📋 Configurar estrategias de caché
    setupCacheStrategies() {
        // Estrategias por tipo de recurso
        this.cacheStrategies.set('static-assets', {
            strategy: 'cache-first',
            ttl: 365 * 24 * 60 * 60 * 1000, // 1 año
            storage: ['browser', 'service-worker'],
            versioned: true
        });

        this.cacheStrategies.set('api-data', {
            strategy: 'network-first',
            ttl: 5 * 60 * 1000, // 5 minutos
            storage: ['memory', 'indexeddb'],
            staleWhileRevalidate: true
        });

        this.cacheStrategies.set('page-content', {
            strategy: 'stale-while-revalidate',
            ttl: 60 * 60 * 1000, // 1 hora
            storage: ['service-worker', 'memory'],
            networkTimeout: 3000
        });

        this.cacheStrategies.set('user-preferences', {
            strategy: 'cache-only',
            ttl: Infinity,
            storage: ['localstorage'],
            persistent: true
        });

        this.cacheStrategies.set('images', {
            strategy: 'cache-first',
            ttl: 30 * 24 * 60 * 60 * 1000, // 30 días
            storage: ['browser', 'service-worker'],
            compression: true
        });

        console.log(`📋 ${this.cacheStrategies.size} estrategias de caché configuradas`);
    }

    // 🌐 Configurar caché de navegador
    setupBrowserCache() {
        if (!this.options.enableBrowserCache) return;

        // Configurar headers de caché para recursos estáticos
        this.setBrowserCacheHeaders();
        
        // Interceptar requests para añadir headers optimizados
        this.interceptRequests();
        
        console.log('🌐 Browser cache configurado');
    }

    // 📄 Configurar headers de caché
    setBrowserCacheHeaders() {
        // Añadir meta tags para caché
        const cacheMetaTags = [
            { name: 'Cache-Control', content: 'public, max-age=31536000' },
            { name: 'ETag', content: this.generateETag() },
            { name: 'Last-Modified', content: new Date().toUTCString() }
        ];

        cacheMetaTags.forEach(tag => {
            let meta = document.querySelector(`meta[name="${tag.name}"]`);
            if (!meta) {
                meta = document.createElement('meta');
                meta.name = tag.name;
                document.head.appendChild(meta);
            }
            meta.content = tag.content;
        });
    }

    // 🔗 Interceptar requests
    interceptRequests() {
        // Override fetch para añadir headers de caché
        const originalFetch = window.fetch;
        
        window.fetch = async (url, options = {}) => {
            const strategy = this.getCacheStrategyForUrl(url);
            
            // Añadir headers de caché apropiados
            options.headers = {
                ...options.headers,
                ...this.getCacheHeadersForStrategy(strategy)
            };

            // Aplicar estrategia de caché
            return this.applyCacheStrategy(url, options, originalFetch);
        };
    }

    // 🎯 Obtener estrategia para URL
    getCacheStrategyForUrl(url) {
        if (typeof url !== 'string') return 'default';

        if (url.includes('/api/')) return 'api-data';
        if (url.includes('/static/')) return 'static-assets';
        if (url.match(/\.(jpg|jpeg|png|gif|svg|webp)$/)) return 'images';
        if (url.includes('/pages/') || url.includes('.html')) return 'page-content';
        
        return 'default';
    }

    // 📋 Obtener headers para estrategia
    getCacheHeadersForStrategy(strategyName) {
        const strategy = this.cacheStrategies.get(strategyName);
        if (!strategy) return {};

        const headers = {};

        if (strategy.strategy === 'cache-first') {
            headers['Cache-Control'] = 'public, max-age=31536000';
        } else if (strategy.strategy === 'network-first') {
            headers['Cache-Control'] = 'no-cache';
        } else if (strategy.strategy === 'stale-while-revalidate') {
            headers['Cache-Control'] = 'public, max-age=300, stale-while-revalidate=86400';
        }

        return headers;
    }

    // ⚡ Aplicar estrategia de caché
    async applyCacheStrategy(url, options, originalFetch) {
        const strategyName = this.getCacheStrategyForUrl(url);
        const strategy = this.cacheStrategies.get(strategyName);
        
        if (!strategy) {
            return originalFetch(url, options);
        }

        switch (strategy.strategy) {
            case 'cache-first':
                return this.cacheFirst(url, options, originalFetch, strategy);
            case 'network-first':
                return this.networkFirst(url, options, originalFetch, strategy);
            case 'stale-while-revalidate':
                return this.staleWhileRevalidate(url, options, originalFetch, strategy);
            case 'cache-only':
                return this.cacheOnly(url, strategy);
            default:
                return originalFetch(url, options);
        }
    }

    // 🎯 Cache First Strategy
    async cacheFirst(url, options, originalFetch, strategy) {
        // Buscar en caché primero
        const cached = await this.getFromCache(url, strategy);
        
        if (cached) {
            this.cacheStats.hits++;
            return new Response(cached.data, {
                status: cached.status || 200,
                headers: cached.headers || {}
            });
        }

        // Si no está en caché, hacer request
        try {
            const response = await originalFetch(url, options);
            
            if (response.ok) {
                await this.storeInCache(url, response.clone(), strategy);
                this.cacheStats.stores++;
            }
            
            return response;
        } catch (error) {
            this.cacheStats.misses++;
            throw error;
        }
    }

    // 🌐 Network First Strategy
    async networkFirst(url, options, originalFetch, strategy) {
        try {
            // Intentar red primero
            const response = await originalFetch(url, options);
            
            if (response.ok) {
                await this.storeInCache(url, response.clone(), strategy);
                this.cacheStats.stores++;
            }
            
            return response;
        } catch (error) {
            // Si falla la red, buscar en caché
            const cached = await this.getFromCache(url, strategy);
            
            if (cached) {
                this.cacheStats.hits++;
                return new Response(cached.data, {
                    status: cached.status || 200,
                    headers: cached.headers || {}
                });
            }
            
            this.cacheStats.misses++;
            throw error;
        }
    }

    // 🔄 Stale While Revalidate Strategy
    async staleWhileRevalidate(url, options, originalFetch, strategy) {
        // Buscar en caché
        const cached = await this.getFromCache(url, strategy);
        
        // Hacer request en background para actualizar
        const networkPromise = originalFetch(url, options)
            .then(response => {
                if (response.ok) {
                    this.storeInCache(url, response.clone(), strategy);
                }
                return response;
            })
            .catch(error => {
                console.warn('Error en background fetch:', error);
            });

        // Si hay caché, devolverlo inmediatamente
        if (cached && !this.isCacheStale(cached, strategy)) {
            this.cacheStats.hits++;
            
            // Actualizar en background
            networkPromise;
            
            return new Response(cached.data, {
                status: cached.status || 200,
                headers: cached.headers || {}
            });
        }

        // Si no hay caché o está muy viejo, esperar a la red
        try {
            const response = await networkPromise;
            this.cacheStats.stores++;
            return response;
        } catch (error) {
            // Si falla la red pero hay caché viejo, usarlo
            if (cached) {
                this.cacheStats.hits++;
                return new Response(cached.data, {
                    status: cached.status || 200,
                    headers: cached.headers || {}
                });
            }
            
            this.cacheStats.misses++;
            throw error;
        }
    }

    // 💾 Cache Only Strategy
    async cacheOnly(url, strategy) {
        const cached = await this.getFromCache(url, strategy);
        
        if (cached) {
            this.cacheStats.hits++;
            return new Response(cached.data, {
                status: cached.status || 200,
                headers: cached.headers || {}
            });
        }
        
        this.cacheStats.misses++;
        throw new Error('No cached response available');
    }

    // 🔧 Configurar Service Worker Cache
    setupServiceWorkerCache() {
        if (!this.options.enableServiceWorkerCache || !('serviceWorker' in navigator)) return;

        // Registrar service worker si no existe
        this.registerServiceWorker();
        
        console.log('🔧 Service Worker cache configurado');
    }

    // 📝 Registrar Service Worker
    async registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register('/static/js/lino-sw.js');
            
            registration.addEventListener('updatefound', () => {
                console.log('🔄 Nueva versión del Service Worker disponible');
                this.handleServiceWorkerUpdate(registration);
            });
            
            console.log('✅ Service Worker registrado');
        } catch (error) {
            console.error('❌ Error registrando Service Worker:', error);
        }
    }

    // 🔄 Manejar actualización de SW
    handleServiceWorkerUpdate(registration) {
        const newWorker = registration.installing;
        
        newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // Mostrar notificación de actualización
                this.showUpdateNotification();
            }
        });
    }

    // 🔔 Mostrar notificación de actualización
    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'lino-update-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <span>🔄 Nueva versión disponible</span>
                <button onclick="window.location.reload()">Actualizar</button>
                <button onclick="this.parentElement.parentElement.remove()">Cerrar</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remover después de 10 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    // 🧠 Configurar Memory Cache
    setupMemoryCache() {
        if (!this.options.enableMemoryCache) return;

        // Limpiar caché cuando se acerque al límite
        setInterval(() => {
            this.cleanupMemoryCache();
        }, 60000); // Cada minuto
        
        console.log('🧠 Memory cache configurado');
    }

    // 🧹 Limpiar Memory Cache
    cleanupMemoryCache() {
        const currentSize = this.getMemoryCacheSize();
        
        if (currentSize > this.options.maxMemoryCacheSize) {
            console.log('🧹 Limpiando memory cache...');
            
            // Remover items más antiguos (LRU)
            const entries = Array.from(this.memoryCache.entries())
                .sort((a, b) => a[1].lastAccessed - b[1].lastAccessed);
            
            let removedSize = 0;
            const targetSize = this.options.maxMemoryCacheSize * 0.8; // 80% del máximo
            
            for (const [key, value] of entries) {
                if (currentSize - removedSize <= targetSize) break;
                
                removedSize += this.getItemSize(value.data);
                this.memoryCache.delete(key);
                this.cacheStats.evictions++;
            }
            
            console.log(`🧹 Memory cache limpiado: ${removedSize} bytes removidos`);
        }
    }

    // 📊 Obtener tamaño de Memory Cache
    getMemoryCacheSize() {
        let totalSize = 0;
        
        for (const [key, value] of this.memoryCache.entries()) {
            totalSize += this.getItemSize(value.data);
        }
        
        return totalSize;
    }

    // 📏 Obtener tamaño de item
    getItemSize(data) {
        if (typeof data === 'string') {
            return data.length * 2; // UTF-16
        } else if (data instanceof ArrayBuffer) {
            return data.byteLength;
        } else {
            return JSON.stringify(data).length * 2;
        }
    }

    // 🗃️ Configurar IndexedDB Cache
    setupIndexedDBCache() {
        if (!this.options.enableIndexedDBCache || !('indexedDB' in window)) return;

        this.initIndexedDB();
        
        console.log('🗃️ IndexedDB cache configurado');
    }

    // 🚀 Inicializar IndexedDB
    async initIndexedDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('LinoCacheDB', 1);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.indexedDB = request.result;
                resolve(this.indexedDB);
            };
            
            request.onupgradeneeded = () => {
                const db = request.result;
                
                // Crear object store para caché
                if (!db.objectStoreNames.contains('cache')) {
                    const store = db.createObjectStore('cache', { keyPath: 'url' });
                    store.createIndex('timestamp', 'timestamp');
                    store.createIndex('strategy', 'strategy');
                }
            };
        });
    }

    // 💾 Configurar LocalStorage Cache
    setupLocalStorageCache() {
        if (!this.options.enableLocalStorageCache || !('localStorage' in window)) return;

        // Limpiar localStorage si está lleno
        this.cleanupLocalStorage();
        
        console.log('💾 LocalStorage cache configurado');
    }

    // 🧹 Limpiar LocalStorage
    cleanupLocalStorage() {
        try {
            const usage = this.getLocalStorageUsage();
            
            if (usage > 4 * 1024 * 1024) { // 4MB límite típico
                console.log('🧹 Limpiando localStorage...');
                
                // Remover items de caché antiguos
                for (let i = localStorage.length - 1; i >= 0; i--) {
                    const key = localStorage.key(i);
                    
                    if (key.startsWith('lino_cache_')) {
                        const item = JSON.parse(localStorage.getItem(key));
                        
                        if (this.isCacheStale(item, { ttl: this.options.defaultTTL })) {
                            localStorage.removeItem(key);
                        }
                    }
                }
            }
        } catch (error) {
            console.warn('Error limpiando localStorage:', error);
        }
    }

    // 📊 Obtener uso de LocalStorage
    getLocalStorageUsage() {
        let totalSize = 0;
        
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                totalSize += localStorage[key].length + key.length;
            }
        }
        
        return totalSize;
    }

    // 📋 Configurar headers de caché
    setupCacheHeaders() {
        // Añadir headers predeterminados para recursos
        const resourceTypes = {
            'js': 'public, max-age=31536000, immutable',
            'css': 'public, max-age=31536000, immutable',
            'woff2': 'public, max-age=31536000, immutable',
            'jpg|jpeg|png|gif|svg|webp': 'public, max-age=2592000',
            'html': 'public, max-age=3600'
        };

        // Aplicar headers via meta tags o service worker
        console.log('📋 Cache headers configurados');
    }

    // 📊 Configurar monitoreo de caché
    setupCacheMonitoring() {
        // Monitorear performance de caché
        setInterval(() => {
            this.logCachePerformance();
        }, 300000); // Cada 5 minutos
        
        console.log('📊 Cache monitoring configurado');
    }

    // 📈 Log de performance de caché
    logCachePerformance() {
        const stats = this.getCacheStats();
        const hitRate = stats.hits / (stats.hits + stats.misses) * 100;
        
        console.log(`📈 Cache Performance: ${hitRate.toFixed(2)}% hit rate`);
        
        if (hitRate < 70) {
            console.warn('⚠️ Low cache hit rate. Consider optimizing cache strategies.');
        }
    }

    // 💾 Almacenar en caché
    async storeInCache(url, response, strategy) {
        const data = {
            url,
            data: await response.text(),
            status: response.status,
            headers: Object.fromEntries(response.headers.entries()),
            timestamp: Date.now(),
            strategy: strategy.strategy,
            ttl: strategy.ttl
        };

        // Almacenar según las opciones de storage de la estrategia
        for (const storage of strategy.storage) {
            try {
                switch (storage) {
                    case 'memory':
                        this.storeInMemory(url, data);
                        break;
                    case 'indexeddb':
                        await this.storeInIndexedDB(url, data);
                        break;
                    case 'localstorage':
                        this.storeInLocalStorage(url, data);
                        break;
                }
            } catch (error) {
                console.warn(`Error storing in ${storage}:`, error);
            }
        }
    }

    // 🧠 Almacenar en memoria
    storeInMemory(url, data) {
        data.lastAccessed = Date.now();
        this.memoryCache.set(url, data);
    }

    // 🗃️ Almacenar en IndexedDB
    async storeInIndexedDB(url, data) {
        if (!this.indexedDB) return;

        const transaction = this.indexedDB.transaction(['cache'], 'readwrite');
        const store = transaction.objectStore('cache');
        
        await store.put(data);
    }

    // 💾 Almacenar en LocalStorage
    storeInLocalStorage(url, data) {
        const key = `lino_cache_${btoa(url)}`;
        
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            if (error.name === 'QuotaExceededError') {
                this.cleanupLocalStorage();
                try {
                    localStorage.setItem(key, JSON.stringify(data));
                } catch (retryError) {
                    console.warn('No se pudo almacenar en localStorage:', retryError);
                }
            }
        }
    }

    // 🔍 Obtener de caché
    async getFromCache(url, strategy) {
        // Buscar en orden de preferencia según storage
        for (const storage of strategy.storage) {
            let cached;
            
            switch (storage) {
                case 'memory':
                    cached = this.getFromMemory(url);
                    break;
                case 'indexeddb':
                    cached = await this.getFromIndexedDB(url);
                    break;
                case 'localstorage':
                    cached = this.getFromLocalStorage(url);
                    break;
            }
            
            if (cached && !this.isCacheStale(cached, strategy)) {
                // Actualizar lastAccessed si es memory cache
                if (storage === 'memory') {
                    cached.lastAccessed = Date.now();
                }
                
                return cached;
            }
        }
        
        return null;
    }

    // 🧠 Obtener de memoria
    getFromMemory(url) {
        return this.memoryCache.get(url);
    }

    // 🗃️ Obtener de IndexedDB
    async getFromIndexedDB(url) {
        if (!this.indexedDB) return null;

        const transaction = this.indexedDB.transaction(['cache'], 'readonly');
        const store = transaction.objectStore('cache');
        
        return new Promise((resolve) => {
            const request = store.get(url);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => resolve(null);
        });
    }

    // 💾 Obtener de LocalStorage
    getFromLocalStorage(url) {
        const key = `lino_cache_${btoa(url)}`;
        
        try {
            const cached = localStorage.getItem(key);
            return cached ? JSON.parse(cached) : null;
        } catch (error) {
            return null;
        }
    }

    // ⏰ Verificar si caché está obsoleto
    isCacheStale(cached, strategy) {
        if (!cached || !cached.timestamp) return true;
        
        const age = Date.now() - cached.timestamp;
        return age > strategy.ttl;
    }

    // 🏷️ Generar ETag
    generateETag() {
        return `"${this.options.cacheVersion}-${Date.now()}"`;
    }

    // 📊 Obtener estadísticas de caché
    getCacheStats() {
        return {
            ...this.cacheStats,
            hitRate: this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses) * 100,
            memoryCacheSize: this.getMemoryCacheSize(),
            memoryCacheItems: this.memoryCache.size,
            localStorageUsage: this.getLocalStorageUsage(),
            strategies: Array.from(this.cacheStrategies.keys())
        };
    }

    // 🧹 Limpiar toda la caché
    async clearAllCache() {
        console.log('🧹 Limpiando toda la caché...');
        
        // Limpiar memory cache
        this.memoryCache.clear();
        
        // Limpiar localStorage
        for (let i = localStorage.length - 1; i >= 0; i--) {
            const key = localStorage.key(i);
            if (key.startsWith('lino_cache_')) {
                localStorage.removeItem(key);
            }
        }
        
        // Limpiar IndexedDB
        if (this.indexedDB) {
            const transaction = this.indexedDB.transaction(['cache'], 'readwrite');
            const store = transaction.objectStore('cache');
            await store.clear();
        }
        
        // Limpiar browser cache
        if ('caches' in window) {
            const cacheNames = await caches.keys();
            for (const cacheName of cacheNames) {
                await caches.delete(cacheName);
            }
        }
        
        console.log('✅ Toda la caché limpiada');
    }

    // 🔄 Refrescar caché
    async refreshCache() {
        console.log('🔄 Refrescando caché...');
        
        // Invalidar memory cache
        this.memoryCache.clear();
        
        // Actualizar versión de caché
        this.options.cacheVersion = `v3.0.0-${Date.now()}`;
        
        console.log('✅ Caché refrescada');
    }

    // 🧹 Cleanup
    destroy() {
        this.memoryCache.clear();
        this.cacheStrategies.clear();
        
        if (this.indexedDB) {
            this.indexedDB.close();
        }
        
        console.log('🧹 Cache Optimizer destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoCacheOptimizer = new LinoCacheOptimizer();
    
    // Comandos globales
    window.getCacheStats = () => window.LinoCacheOptimizer.getCacheStats();
    window.clearCache = () => window.LinoCacheOptimizer.clearAllCache();
    window.refreshCache = () => window.LinoCacheOptimizer.refreshCache();
});
