/**
 * 🔄 LINO BACKGROUND SYNC SYSTEM V3
 * Sistema avanzado de sincronización en segundo plano para máxima disponibilidad
 */

class LinoBackgroundSync {
    constructor(options = {}) {
        this.options = {
            enableBackgroundSync: true,
            enableOfflineQueue: true,
            enablePeriodicSync: true,
            enableConflictResolution: true,
            syncInterval: 30000, // 30 segundos
            retryAttempts: 3,
            retryDelay: 5000,
            maxQueueSize: 100,
            syncEndpoints: ['/api/productos/', '/api/inventario/', '/api/ventas/'],
            ...options
        };

        this.syncQueue = [];
        this.syncInProgress = false;
        this.lastSyncTime = 0;
        this.syncStats = {
            successful: 0,
            failed: 0,
            conflicts: 0,
            queued: 0
        };
        
        this.offlineData = new Map();
        this.conflictResolutions = new Map();
        this.init();
    }

    init() {
        console.log('🔄 LINO Background Sync iniciado');
        this.setupBackgroundSync();
        this.setupOfflineQueue();
        this.setupPeriodicSync();
        this.setupNetworkMonitoring();
        this.setupConflictResolution();
        this.restoreQueueFromStorage();
        this.setupVisibilityChangeSync();
    }

    // 🔄 Configurar Background Sync
    setupBackgroundSync() {
        if (!this.options.enableBackgroundSync) return;

        // Registrar para background sync si está disponible
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            this.registerBackgroundSync();
        } else {
            // Fallback a sync manual
            this.setupManualSync();
        }

        console.log('🔄 Background Sync configurado');
    }

    // 📝 Registrar Background Sync
    async registerBackgroundSync() {
        try {
            const registration = await navigator.serviceWorker.ready;
            
            // Registrar sync para diferentes tipos de datos
            await registration.sync.register('lino-data-sync');
            await registration.sync.register('lino-offline-queue');
            
            console.log('📝 Background Sync registrado');
        } catch (error) {
            console.warn('Error registrando Background Sync:', error);
            this.setupManualSync();
        }
    }

    // 🔧 Configurar sync manual
    setupManualSync() {
        // Sync cuando la página se enfoca
        window.addEventListener('focus', () => {
            this.performSync();
        });

        // Sync cuando se restablece la conexión
        window.addEventListener('online', () => {
            this.performSync();
        });

        console.log('🔧 Sync manual configurado');
    }

    // 📱 Configurar queue offline
    setupOfflineQueue() {
        if (!this.options.enableOfflineQueue) return;

        // Interceptar requests cuando estamos offline
        this.interceptOfflineRequests();
        
        // Procesar queue cuando volvemos online
        window.addEventListener('online', () => {
            this.processOfflineQueue();
        });

        console.log('📱 Offline queue configurado');
    }

    // 🔄 Configurar sync periódico
    setupPeriodicSync() {
        if (!this.options.enablePeriodicSync) return;

        // Sync periódico solo cuando la página está visible
        setInterval(() => {
            if (!document.hidden && navigator.onLine) {
                this.performPeriodicSync();
            }
        }, this.options.syncInterval);

        console.log('🔄 Sync periódico configurado');
    }

    // 📡 Configurar monitoreo de red
    setupNetworkMonitoring() {
        // Detectar cambios de conectividad
        window.addEventListener('online', () => {
            console.log('🌐 Conexión restablecida - iniciando sync');
            this.onNetworkRestore();
        });

        window.addEventListener('offline', () => {
            console.log('📵 Conexión perdida - activando modo offline');
            this.onNetworkLost();
        });

        // Monitorear calidad de conexión
        if ('connection' in navigator) {
            navigator.connection.addEventListener('change', () => {
                this.onConnectionChange(navigator.connection);
            });
        }

        console.log('📡 Network monitoring configurado');
    }

    // 🔀 Configurar resolución de conflictos
    setupConflictResolution() {
        if (!this.options.enableConflictResolution) return;

        // Estrategias de resolución de conflictos
        this.conflictResolutions.set('timestamp', (local, remote) => {
            return local.timestamp > remote.timestamp ? local : remote;
        });

        this.conflictResolutions.set('user-priority', (local, remote) => {
            return local.userPriority > remote.userPriority ? local : remote;
        });

        this.conflictResolutions.set('merge', (local, remote) => {
            return { ...remote, ...local, merged: true };
        });

        console.log('🔀 Conflict resolution configurado');
    }

    // 👁️ Configurar sync por visibilidad
    setupVisibilityChangeSync() {
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                // Página visible - hacer sync rápido
                this.performQuickSync();
            }
        });
    }

    // 🔄 Realizar sincronización
    async performSync() {
        if (this.syncInProgress || !navigator.onLine) return;

        this.syncInProgress = true;
        console.log('🔄 Iniciando sincronización completa...');

        try {
            // Sincronizar cada endpoint
            for (const endpoint of this.options.syncEndpoints) {
                await this.syncEndpoint(endpoint);
            }

            // Procesar queue offline
            await this.processOfflineQueue();

            this.lastSyncTime = Date.now();
            console.log('✅ Sincronización completada');

        } catch (error) {
            console.error('❌ Error en sincronización:', error);
            this.syncStats.failed++;
        } finally {
            this.syncInProgress = false;
        }
    }

    // ⚡ Realizar sync rápido
    async performQuickSync() {
        if (this.syncInProgress || !navigator.onLine) return;

        console.log('⚡ Iniciando sync rápido...');

        try {
            // Solo sincronizar datos críticos y queue
            await this.syncCriticalData();
            await this.processOfflineQueue();

        } catch (error) {
            console.warn('⚠️ Error en sync rápido:', error);
        }
    }

    // 🔄 Realizar sync periódico
    async performPeriodicSync() {
        const timeSinceLastSync = Date.now() - this.lastSyncTime;
        
        if (timeSinceLastSync < this.options.syncInterval) return;

        console.log('🔄 Iniciando sync periódico...');
        await this.performSync();
    }

    // 🎯 Sincronizar endpoint específico
    async syncEndpoint(endpoint) {
        try {
            const response = await fetch(endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const remoteData = await response.json();
            await this.reconcileData(endpoint, remoteData);
            
            this.syncStats.successful++;
            console.log(`✅ Endpoint sincronizado: ${endpoint}`);

        } catch (error) {
            console.error(`❌ Error sincronizando ${endpoint}:`, error);
            this.syncStats.failed++;
        }
    }

    // 📊 Sincronizar datos críticos
    async syncCriticalData() {
        const criticalEndpoints = [
            '/api/productos/modified/',
            '/api/inventario/alerts/',
            '/api/ventas/pending/'
        ];

        for (const endpoint of criticalEndpoints) {
            try {
                await this.syncEndpoint(endpoint);
            } catch (error) {
                console.warn(`⚠️ Error en sync crítico ${endpoint}:`, error);
            }
        }
    }

    // 🔀 Reconciliar datos
    async reconcileData(endpoint, remoteData) {
        const localData = this.getLocalData(endpoint);
        
        if (!localData) {
            // No hay datos locales, usar remotos
            this.setLocalData(endpoint, remoteData);
            return;
        }

        // Detectar conflictos
        const conflicts = this.detectConflicts(localData, remoteData);
        
        if (conflicts.length > 0) {
            console.log(`🔀 Detectados ${conflicts.length} conflictos en ${endpoint}`);
            const resolvedData = await this.resolveConflicts(conflicts, localData, remoteData);
            this.setLocalData(endpoint, resolvedData);
            this.syncStats.conflicts += conflicts.length;
        } else {
            // No hay conflictos, usar datos más recientes
            const mergedData = this.mergeData(localData, remoteData);
            this.setLocalData(endpoint, mergedData);
        }
    }

    // 🔍 Detectar conflictos
    detectConflicts(localData, remoteData) {
        const conflicts = [];
        
        if (Array.isArray(localData) && Array.isArray(remoteData)) {
            // Comparar arrays de objetos
            localData.forEach(localItem => {
                const remoteItem = remoteData.find(r => r.id === localItem.id);
                
                if (remoteItem && this.hasConflict(localItem, remoteItem)) {
                    conflicts.push({
                        id: localItem.id,
                        local: localItem,
                        remote: remoteItem
                    });
                }
            });
        } else if (typeof localData === 'object' && typeof remoteData === 'object') {
            // Comparar objetos
            if (this.hasConflict(localData, remoteData)) {
                conflicts.push({
                    local: localData,
                    remote: remoteData
                });
            }
        }
        
        return conflicts;
    }

    // ⚔️ Verificar si hay conflicto
    hasConflict(local, remote) {
        // Verificar timestamps
        if (local.modified && remote.modified) {
            const localTime = new Date(local.modified).getTime();
            const remoteTime = new Date(remote.modified).getTime();
            
            // Conflicto si ambos fueron modificados en ventana de tiempo pequeña
            const timeDiff = Math.abs(localTime - remoteTime);
            return timeDiff < 5000; // 5 segundos
        }
        
        // Verificar checksums si están disponibles
        if (local.checksum && remote.checksum) {
            return local.checksum !== remote.checksum;
        }
        
        // Fallback: comparar contenido
        return JSON.stringify(local) !== JSON.stringify(remote);
    }

    // 🛠️ Resolver conflictos
    async resolveConflicts(conflicts, localData, remoteData) {
        const resolutionStrategy = this.getResolutionStrategy();
        const resolver = this.conflictResolutions.get(resolutionStrategy);
        
        if (!resolver) {
            console.warn('⚠️ Estrategia de resolución no encontrada, usando timestamp');
            return this.conflictResolutions.get('timestamp')(localData, remoteData);
        }

        let resolvedData = { ...remoteData };
        
        for (const conflict of conflicts) {
            const resolved = resolver(conflict.local, conflict.remote);
            
            if (Array.isArray(resolvedData)) {
                const index = resolvedData.findIndex(item => item.id === conflict.id);
                if (index !== -1) {
                    resolvedData[index] = resolved;
                }
            } else {
                resolvedData = resolved;
            }
        }
        
        return resolvedData;
    }

    // 📋 Obtener estrategia de resolución
    getResolutionStrategy() {
        // Obtener estrategia de configuración o preferencias del usuario
        return localStorage.getItem('lino_conflict_resolution') || 'timestamp';
    }

    // 🔗 Combinar datos
    mergeData(localData, remoteData) {
        if (Array.isArray(localData) && Array.isArray(remoteData)) {
            // Merge arrays manteniendo items únicos
            const merged = [...remoteData];
            
            localData.forEach(localItem => {
                const exists = merged.find(item => item.id === localItem.id);
                if (!exists) {
                    merged.push(localItem);
                }
            });
            
            return merged;
        }
        
        // Para objetos, usar remote como base
        return { ...localData, ...remoteData };
    }

    // 🔗 Interceptar requests offline
    interceptOfflineRequests() {
        const originalFetch = window.fetch;
        
        window.fetch = async (url, options = {}) => {
            if (!navigator.onLine) {
                return this.handleOfflineRequest(url, options);
            }
            
            try {
                const response = await originalFetch(url, options);
                
                // Si la respuesta es exitosa, remover de queue si estaba
                this.removeFromQueue(url, options);
                
                return response;
            } catch (error) {
                // Si falla, añadir a queue offline
                if (this.shouldQueueRequest(url, options)) {
                    this.addToQueue(url, options);
                }
                throw error;
            }
        };
    }

    // 📵 Manejar request offline
    async handleOfflineRequest(url, options) {
        console.log('📵 Request offline detectado:', url);
        
        // Verificar si hay datos en caché
        const cachedData = this.getCachedData(url);
        
        if (cachedData) {
            console.log('💾 Devolviendo datos de caché');
            return new Response(JSON.stringify(cachedData), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Añadir a queue si es un request que modifica datos
        if (this.shouldQueueRequest(url, options)) {
            this.addToQueue(url, options);
            
            // Devolver respuesta simulada
            return new Response(JSON.stringify({ queued: true }), {
                status: 202,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Para requests GET sin caché, fallar
        throw new Error('No network connection and no cached data available');
    }

    // ❓ Verificar si debe hacer queue del request
    shouldQueueRequest(url, options) {
        const method = options.method || 'GET';
        
        // Solo hacer queue de requests que modifican datos
        return ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method.toUpperCase());
    }

    // ➕ Añadir a queue
    addToQueue(url, options) {
        if (this.syncQueue.length >= this.options.maxQueueSize) {
            console.warn('⚠️ Queue offline llena, removiendo item más antiguo');
            this.syncQueue.shift();
        }
        
        const queueItem = {
            id: Date.now() + Math.random(),
            url,
            options: {
                ...options,
                headers: { ...(options.headers || {}) }
            },
            timestamp: Date.now(),
            attempts: 0
        };
        
        this.syncQueue.push(queueItem);
        this.saveQueueToStorage();
        this.syncStats.queued++;
        
        console.log(`➕ Request añadido a queue offline: ${url}`);
    }

    // ➖ Remover de queue
    removeFromQueue(url, options) {
        const initialLength = this.syncQueue.length;
        
        this.syncQueue = this.syncQueue.filter(item => {
            return !(item.url === url && item.options.method === (options.method || 'GET'));
        });
        
        if (this.syncQueue.length < initialLength) {
            this.saveQueueToStorage();
            console.log(`➖ Request removido de queue: ${url}`);
        }
    }

    // 🔄 Procesar queue offline
    async processOfflineQueue() {
        if (!navigator.onLine || this.syncQueue.length === 0) return;

        console.log(`🔄 Procesando queue offline: ${this.syncQueue.length} items`);
        
        const itemsToProcess = [...this.syncQueue];
        
        for (const item of itemsToProcess) {
            try {
                await this.processQueueItem(item);
                this.removeQueueItem(item.id);
                
            } catch (error) {
                console.error(`❌ Error procesando item de queue:`, error);
                item.attempts++;
                
                if (item.attempts >= this.options.retryAttempts) {
                    console.error(`❌ Item de queue falló después de ${this.options.retryAttempts} intentos`);
                    this.removeQueueItem(item.id);
                } else {
                    console.log(`🔄 Reintentando item de queue (${item.attempts}/${this.options.retryAttempts})`);
                }
            }
        }
        
        this.saveQueueToStorage();
    }

    // ⚙️ Procesar item de queue
    async processQueueItem(item) {
        console.log(`⚙️ Procesando: ${item.options.method} ${item.url}`);
        
        const response = await fetch(item.url, item.options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        console.log(`✅ Item de queue procesado exitosamente`);
        return response;
    }

    // 🗑️ Remover item de queue
    removeQueueItem(itemId) {
        this.syncQueue = this.syncQueue.filter(item => item.id !== itemId);
    }

    // 🌐 Manejar restauración de red
    onNetworkRestore() {
        console.log('🌐 Red restaurada');
        
        // Procesar queue inmediatamente
        this.processOfflineQueue();
        
        // Hacer sync completo
        setTimeout(() => {
            this.performSync();
        }, 1000);
    }

    // 📵 Manejar pérdida de red
    onNetworkLost() {
        console.log('📵 Red perdida - modo offline activo');
        
        // Notificar al usuario
        this.showOfflineNotification();
    }

    // 📶 Manejar cambio de conexión
    onConnectionChange(connection) {
        console.log(`📶 Conexión cambió: ${connection.effectiveType}`);
        
        // Ajustar estrategia de sync según calidad de conexión
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
            this.options.syncInterval = 60000; // Reducir frecuencia
        } else {
            this.options.syncInterval = 30000; // Frecuencia normal
        }
    }

    // 🔔 Mostrar notificación offline
    showOfflineNotification() {
        const notification = document.createElement('div');
        notification.className = 'lino-offline-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <span>📵 Sin conexión - trabajando offline</span>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remover cuando se restaure la conexión
        const removeOnOnline = () => {
            if (notification.parentElement) {
                notification.remove();
            }
            window.removeEventListener('online', removeOnOnline);
        };
        
        window.addEventListener('online', removeOnOnline);
    }

    // 💾 Obtener datos locales
    getLocalData(endpoint) {
        try {
            const data = localStorage.getItem(`lino_sync_${btoa(endpoint)}`);
            return data ? JSON.parse(data) : null;
        } catch {
            return null;
        }
    }

    // 💾 Establecer datos locales
    setLocalData(endpoint, data) {
        try {
            localStorage.setItem(`lino_sync_${btoa(endpoint)}`, JSON.stringify(data));
        } catch (error) {
            console.warn('Error guardando datos locales:', error);
        }
    }

    // 💾 Obtener datos en caché
    getCachedData(url) {
        return this.offlineData.get(url);
    }

    // 💾 Guardar queue en storage
    saveQueueToStorage() {
        try {
            localStorage.setItem('lino_sync_queue', JSON.stringify(this.syncQueue));
        } catch (error) {
            console.warn('Error guardando queue:', error);
        }
    }

    // 💾 Restaurar queue de storage
    restoreQueueFromStorage() {
        try {
            const stored = localStorage.getItem('lino_sync_queue');
            if (stored) {
                this.syncQueue = JSON.parse(stored);
                console.log(`💾 Queue restaurada: ${this.syncQueue.length} items`);
            }
        } catch (error) {
            console.warn('Error restaurando queue:', error);
            this.syncQueue = [];
        }
    }

    // 📊 Obtener estadísticas
    getStats() {
        return {
            ...this.syncStats,
            queueSize: this.syncQueue.length,
            lastSyncTime: new Date(this.lastSyncTime).toLocaleString(),
            syncInProgress: this.syncInProgress,
            isOnline: navigator.onLine,
            conflictResolutionStrategy: this.getResolutionStrategy()
        };
    }

    // 🧹 Limpiar queue
    clearQueue() {
        this.syncQueue = [];
        this.saveQueueToStorage();
        console.log('🧹 Queue offline limpiada');
    }

    // 🔄 Forzar sync
    async forceSync() {
        console.log('🔄 Forzando sincronización...');
        this.syncInProgress = false; // Reset flag
        await this.performSync();
    }

    // 🧹 Cleanup
    destroy() {
        this.syncQueue = [];
        this.offlineData.clear();
        this.conflictResolutions.clear();
        
        console.log('🧹 Background Sync destruido');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoBackgroundSync = new LinoBackgroundSync();
    
    // Comandos globales
    window.getSyncStats = () => window.LinoBackgroundSync.getStats();
    window.forceSync = () => window.LinoBackgroundSync.forceSync();
    window.clearSyncQueue = () => window.LinoBackgroundSync.clearQueue();
});
