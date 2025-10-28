/**
 * 🎯 LINO COMMAND CENTER V3
 * Sistema unificado de control y monitoreo de todas las features avanzadas
 */

class LinoCommandCenter {
    constructor() {
        this.systems = new Map();
        this.isInitialized = false;
        this.commandHistory = [];
        this.shortcuts = new Map();
        
        this.init();
    }

    init() {
        console.log('🎯 LINO Command Center iniciado');
        this.registerSystems();
        this.setupKeyboardShortcuts();
        this.setupGlobalCommands();
        this.createCommandInterface();
        this.setupAutoReporting();
        this.isInitialized = true;
    }

    // 📋 Registrar sistemas
    registerSystems() {
        // Registrar sistemas cuando estén disponibles
        this.waitForSystem('LinoLazyLoader', 'lazy-loader');
        this.waitForSystem('LinoCodeSplitter', 'code-splitter');
        this.waitForSystem('LinoCriticalCSSOptimizer', 'critical-css');
        this.waitForSystem('LinoCacheOptimizer', 'cache-optimizer');
        this.waitForSystem('LinoResourcePreloader', 'resource-preloader');
        this.waitForSystem('LinoBackgroundSync', 'background-sync');
        this.waitForSystem('LinoTestingConsole', 'testing-console');
        this.waitForSystem('LinoPerformanceAudit', 'performance-audit');
        this.waitForSystem('LinoCSSAnalyzer', 'css-analyzer');
    }

    // ⏳ Esperar por sistema
    waitForSystem(windowProperty, systemId) {
        const checkSystem = () => {
            if (window[windowProperty]) {
                this.systems.set(systemId, window[windowProperty]);
                console.log(`✅ Sistema registrado: ${systemId}`);
            } else {
                setTimeout(checkSystem, 100);
            }
        };
        checkSystem();
    }

    // ⌨️ Configurar atajos de teclado
    setupKeyboardShortcuts() {
        // Ctrl/Cmd + Shift + L = Command Center
        this.shortcuts.set('ctrl+shift+l', () => this.toggleCommandCenter());
        
        // Ctrl/Cmd + Shift + P = Performance Report
        this.shortcuts.set('ctrl+shift+p', () => this.generatePerformanceReport());
        
        // Ctrl/Cmd + Shift + S = System Status
        this.shortcuts.set('ctrl+shift+s', () => this.showSystemStatus());
        
        // Ctrl/Cmd + Shift + C = Clear All Cache
        this.shortcuts.set('ctrl+shift+c', () => this.clearAllCache());
        
        // Ctrl/Cmd + Shift + R = Refresh All Systems
        this.shortcuts.set('ctrl+shift+r', () => this.refreshAllSystems());

        document.addEventListener('keydown', (e) => {
            const key = this.buildKeyString(e);
            const command = this.shortcuts.get(key);
            
            if (command) {
                e.preventDefault();
                command();
            }
        });

        console.log('⌨️ Keyboard shortcuts configurados');
    }

    // 🔧 Construir string de tecla
    buildKeyString(event) {
        const parts = [];
        
        if (event.ctrlKey || event.metaKey) parts.push('ctrl');
        if (event.shiftKey) parts.push('shift');
        if (event.altKey) parts.push('alt');
        
        parts.push(event.key.toLowerCase());
        
        return parts.join('+');
    }

    // 🌐 Configurar comandos globales
    setupGlobalCommands() {
        // Comandos globales para consola
        window.LinoCommand = {
            status: () => this.getSystemsStatus(),
            performance: () => this.generatePerformanceReport(),
            cache: {
                clear: () => this.clearAllCache(),
                stats: () => this.getCacheStats(),
                refresh: () => this.refreshCache()
            },
            sync: {
                status: () => this.getSyncStatus(),
                force: () => this.forceSync(),
                clear: () => this.clearSyncQueue()
            },
            preload: {
                stats: () => this.getPreloadStats(),
                resource: (url, type, priority) => this.preloadResource(url, type, priority)
            },
            test: {
                run: () => this.runAllTests(),
                performance: () => this.testPerformance(),
                css: () => this.analyzeCSSUsage()
            },
            optimize: {
                lazy: () => this.optimizeLazyLoading(),
                css: () => this.optimizeCriticalCSS(),
                cache: () => this.optimizeCache()
            },
            help: () => this.showHelp()
        };

        console.log('🌐 Global commands configurados');
    }

    // 🎛️ Crear interfaz de comando
    createCommandInterface() {
        // Solo crear si no existe
        if (document.getElementById('lino-command-center')) return;

        const commandCenter = document.createElement('div');
        commandCenter.id = 'lino-command-center';
        commandCenter.className = 'lino-command-center hidden';
        commandCenter.innerHTML = `
            <div class="command-center-content">
                <div class="command-header">
                    <h3>🎯 LINO Command Center V3</h3>
                    <button class="close-btn" onclick="LinoCommandCenter.instance.toggleCommandCenter()">×</button>
                </div>
                
                <div class="command-tabs">
                    <button class="tab-btn active" data-tab="dashboard">📊 Dashboard</button>
                    <button class="tab-btn" data-tab="performance">⚡ Performance</button>
                    <button class="tab-btn" data-tab="cache">💾 Cache</button>
                    <button class="tab-btn" data-tab="sync">🔄 Sync</button>
                    <button class="tab-btn" data-tab="console">💻 Console</button>
                </div>
                
                <div class="command-content">
                    <div id="dashboard-tab" class="tab-content active">
                        <div class="system-grid">
                            <div class="system-card" data-system="lazy-loader">
                                <h4>🚀 Lazy Loader</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="LinoCommand.optimize.lazy()">Optimizar</button>
                                </div>
                            </div>
                            
                            <div class="system-card" data-system="code-splitter">
                                <h4>⚡ Code Splitter</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="getChunkStats()">Ver Stats</button>
                                </div>
                            </div>
                            
                            <div class="system-card" data-system="critical-css">
                                <h4>🎯 Critical CSS</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="LinoCommand.optimize.css()">Optimizar</button>
                                </div>
                            </div>
                            
                            <div class="system-card" data-system="cache-optimizer">
                                <h4>💾 Cache Optimizer</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="LinoCommand.cache.clear()">Limpiar</button>
                                </div>
                            </div>
                            
                            <div class="system-card" data-system="resource-preloader">
                                <h4>🎯 Resource Preloader</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="getPreloadStats()">Ver Stats</button>
                                </div>
                            </div>
                            
                            <div class="system-card" data-system="background-sync">
                                <h4>🔄 Background Sync</h4>
                                <div class="system-status">Inicializando...</div>
                                <div class="system-actions">
                                    <button onclick="LinoCommand.sync.force()">Sync Now</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="performance-tab" class="tab-content">
                        <div class="performance-metrics">
                            <div class="metric-card">
                                <h4>⚡ Performance Score</h4>
                                <div class="metric-value">--</div>
                            </div>
                            <div class="metric-card">
                                <h4>🚀 Load Time</h4>
                                <div class="metric-value">--</div>
                            </div>
                            <div class="metric-card">
                                <h4>💾 Cache Hit Rate</h4>
                                <div class="metric-value">--</div>
                            </div>
                            <div class="metric-card">
                                <h4>🔄 Sync Status</h4>
                                <div class="metric-value">--</div>
                            </div>
                        </div>
                        
                        <div class="performance-actions">
                            <button onclick="LinoCommand.performance()" class="primary-btn">🔍 Generar Reporte</button>
                            <button onclick="LinoCommand.test.run()" class="secondary-btn">🧪 Ejecutar Tests</button>
                        </div>
                        
                        <div class="performance-log">
                            <h4>📋 Log de Performance</h4>
                            <div id="performance-log-content">
                                <p>Ejecuta un reporte para ver métricas detalladas...</p>
                            </div>
                        </div>
                    </div>
                    
                    <div id="cache-tab" class="tab-content">
                        <div class="cache-overview">
                            <div class="cache-stats">
                                <h4>📊 Estadísticas de Cache</h4>
                                <div id="cache-stats-content">Cargando estadísticas...</div>
                            </div>
                            
                            <div class="cache-actions">
                                <button onclick="LinoCommand.cache.clear()" class="danger-btn">🗑️ Limpiar Todo</button>
                                <button onclick="LinoCommand.cache.refresh()" class="primary-btn">🔄 Refrescar</button>
                                <button onclick="LinoCommand.cache.stats()" class="secondary-btn">📊 Ver Stats</button>
                            </div>
                        </div>
                    </div>
                    
                    <div id="sync-tab" class="tab-content">
                        <div class="sync-overview">
                            <div class="sync-status">
                                <h4>🔄 Estado de Sincronización</h4>
                                <div id="sync-status-content">Verificando estado...</div>
                            </div>
                            
                            <div class="sync-actions">
                                <button onclick="LinoCommand.sync.force()" class="primary-btn">🚀 Forzar Sync</button>
                                <button onclick="LinoCommand.sync.clear()" class="secondary-btn">🗑️ Limpiar Queue</button>
                                <button onclick="LinoCommand.sync.status()" class="info-btn">📊 Ver Estado</button>
                            </div>
                        </div>
                    </div>
                    
                    <div id="console-tab" class="tab-content">
                        <div class="console-interface">
                            <div class="console-output" id="console-output">
                                <div class="console-line">🎯 LINO Command Center V3 - Usa 'LinoCommand.help()' para ver comandos disponibles</div>
                            </div>
                            
                            <div class="console-input-group">
                                <span class="console-prompt">></span>
                                <input type="text" id="console-input" placeholder="Ejecutar comando..." autocomplete="off">
                                <button onclick="LinoCommandCenter.instance.executeCommand()">▶</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Estilos del Command Center
        const styles = document.createElement('style');
        styles.textContent = `
            .lino-command-center {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.8);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: opacity 0.3s ease;
            }
            
            .lino-command-center.hidden {
                opacity: 0;
                pointer-events: none;
            }
            
            .command-center-content {
                background: #1a1a1a;
                border-radius: 12px;
                width: 90vw;
                max-width: 1200px;
                height: 80vh;
                max-height: 800px;
                color: white;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .command-header {
                padding: 20px;
                border-bottom: 1px solid #333;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #2a2a2a;
            }
            
            .command-header h3 {
                margin: 0;
                color: #4CAF50;
            }
            
            .close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .close-btn:hover {
                background: #ff4444;
            }
            
            .command-tabs {
                display: flex;
                background: #333;
                border-bottom: 1px solid #444;
            }
            
            .tab-btn {
                background: none;
                border: none;
                color: #ccc;
                padding: 15px 20px;
                cursor: pointer;
                border-bottom: 2px solid transparent;
                transition: all 0.3s ease;
            }
            
            .tab-btn:hover,
            .tab-btn.active {
                color: #4CAF50;
                border-bottom-color: #4CAF50;
                background: #2a2a2a;
            }
            
            .command-content {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }
            
            .tab-content {
                display: none;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .system-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            
            .system-card {
                background: #2a2a2a;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #444;
            }
            
            .system-card h4 {
                margin: 0 0 10px 0;
                color: #4CAF50;
            }
            
            .system-status {
                margin: 10px 0;
                padding: 8px 12px;
                border-radius: 4px;
                background: #333;
                font-size: 14px;
            }
            
            .system-actions {
                margin-top: 15px;
            }
            
            .system-actions button {
                background: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
                font-size: 12px;
            }
            
            .performance-metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .metric-card {
                background: #2a2a2a;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                border: 1px solid #444;
            }
            
            .metric-card h4 {
                margin: 0 0 10px 0;
                color: #4CAF50;
                font-size: 14px;
            }
            
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            
            .performance-actions {
                text-align: center;
                margin: 20px 0;
            }
            
            .primary-btn {
                background: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                margin: 0 10px;
                font-size: 14px;
            }
            
            .secondary-btn {
                background: #2196F3;
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                margin: 0 10px;
                font-size: 14px;
            }
            
            .danger-btn {
                background: #f44336;
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                margin: 0 10px;
                font-size: 14px;
            }
            
            .info-btn {
                background: #FF9800;
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                margin: 0 10px;
                font-size: 14px;
            }
            
            .performance-log,
            .cache-overview,
            .sync-overview {
                background: #2a2a2a;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #444;
            }
            
            .console-interface {
                height: 400px;
                display: flex;
                flex-direction: column;
            }
            
            .console-output {
                flex: 1;
                background: #000;
                border-radius: 4px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                overflow-y: auto;
                border: 1px solid #444;
            }
            
            .console-line {
                margin: 5px 0;
                color: #4CAF50;
            }
            
            .console-input-group {
                display: flex;
                align-items: center;
                margin-top: 10px;
                background: #000;
                border-radius: 4px;
                padding: 5px;
                border: 1px solid #444;
            }
            
            .console-prompt {
                color: #4CAF50;
                margin-right: 10px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
            }
            
            .console-input-group input {
                flex: 1;
                background: none;
                border: none;
                color: white;
                font-family: 'Courier New', monospace;
                outline: none;
                padding: 8px;
            }
            
            .console-input-group button {
                background: #4CAF50;
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                cursor: pointer;
                margin-left: 10px;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(commandCenter);

        // Configurar eventos de tabs
        this.setupTabEvents();
        
        // Configurar input de consola
        this.setupConsoleInput();

        console.log('🎛️ Command Center UI creado');
    }

    // 📑 Configurar eventos de tabs
    setupTabEvents() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.dataset.tab;
                
                // Remover active de todos
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Activar seleccionado
                button.classList.add('active');
                document.getElementById(`${tabName}-tab`).classList.add('active');
                
                // Cargar datos del tab
                this.loadTabData(tabName);
            });
        });
    }

    // 💻 Configurar input de consola
    setupConsoleInput() {
        const input = document.getElementById('console-input');
        
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.executeCommand();
                }
            });
        }
    }

    // 🔄 Alternar Command Center
    toggleCommandCenter() {
        const commandCenter = document.getElementById('lino-command-center');
        
        if (commandCenter) {
            commandCenter.classList.toggle('hidden');
            
            if (!commandCenter.classList.contains('hidden')) {
                this.loadTabData('dashboard');
            }
        }
    }

    // 📊 Cargar datos del tab
    loadTabData(tabName) {
        switch (tabName) {
            case 'dashboard':
                this.updateSystemStatus();
                break;
            case 'performance':
                this.updatePerformanceMetrics();
                break;
            case 'cache':
                this.updateCacheStats();
                break;
            case 'sync':
                this.updateSyncStatus();
                break;
        }
    }

    // 🔄 Actualizar estado de sistemas
    updateSystemStatus() {
        this.systems.forEach((system, systemId) => {
            const card = document.querySelector(`[data-system="${systemId}"]`);
            if (card) {
                const statusEl = card.querySelector('.system-status');
                
                try {
                    let status = '✅ Activo';
                    
                    if (system.getStats) {
                        const stats = system.getStats();
                        status = `✅ Activo - ${Object.keys(stats).length} métricas`;
                    } else if (system.isInitialized !== undefined) {
                        status = system.isInitialized ? '✅ Inicializado' : '⏳ Inicializando';
                    }
                    
                    statusEl.textContent = status;
                    statusEl.style.color = '#4CAF50';
                } catch (error) {
                    statusEl.textContent = '❌ Error';
                    statusEl.style.color = '#f44336';
                }
            }
        });
    }

    // ⚡ Actualizar métricas de performance
    updatePerformanceMetrics() {
        const metrics = document.querySelectorAll('.metric-value');
        
        if (this.systems.has('performance-audit')) {
            try {
                const perfSystem = this.systems.get('performance-audit');
                const stats = perfSystem.getStats();
                
                metrics[0].textContent = `${stats.overallScore || '--'}/100`;
                metrics[1].textContent = `${stats.loadTime || '--'}ms`;
            } catch (error) {
                console.warn('Error getting performance stats:', error);
            }
        }
        
        if (this.systems.has('cache-optimizer')) {
            try {
                const cacheSystem = this.systems.get('cache-optimizer');
                const stats = cacheSystem.getStats();
                
                metrics[2].textContent = `${stats.hitRate || '--'}%`;
            } catch (error) {
                console.warn('Error getting cache stats:', error);
            }
        }
        
        if (this.systems.has('background-sync')) {
            try {
                const syncSystem = this.systems.get('background-sync');
                const stats = syncSystem.getStats();
                
                metrics[3].textContent = stats.isOnline ? '🟢 Online' : '🔴 Offline';
            } catch (error) {
                console.warn('Error getting sync stats:', error);
            }
        }
    }

    // 💾 Actualizar stats de cache
    updateCacheStats() {
        const content = document.getElementById('cache-stats-content');
        
        if (content && this.systems.has('cache-optimizer')) {
            try {
                const cacheSystem = this.systems.get('cache-optimizer');
                const stats = cacheSystem.getStats();
                
                content.innerHTML = `
                    <div>Hit Rate: ${stats.hitRate || 0}%</div>
                    <div>Hits: ${stats.hits || 0}</div>
                    <div>Misses: ${stats.misses || 0}</div>
                    <div>Stores: ${stats.stores || 0}</div>
                    <div>Memory Cache: ${stats.memoryCacheItems || 0} items</div>
                `;
            } catch (error) {
                content.innerHTML = '<div>Error obteniendo estadísticas de cache</div>';
            }
        }
    }

    // 🔄 Actualizar estado de sync
    updateSyncStatus() {
        const content = document.getElementById('sync-status-content');
        
        if (content && this.systems.has('background-sync')) {
            try {
                const syncSystem = this.systems.get('background-sync');
                const stats = syncSystem.getStats();
                
                content.innerHTML = `
                    <div>Estado: ${stats.isOnline ? '🟢 Online' : '🔴 Offline'}</div>
                    <div>Exitosos: ${stats.successful || 0}</div>
                    <div>Fallidos: ${stats.failed || 0}</div>
                    <div>Queue: ${stats.queueSize || 0} items</div>
                    <div>Último Sync: ${stats.lastSyncTime || 'Nunca'}</div>
                `;
            } catch (error) {
                content.innerHTML = '<div>Error obteniendo estado de sync</div>';
            }
        }
    }

    // 💻 Ejecutar comando
    executeCommand() {
        const input = document.getElementById('console-input');
        const output = document.getElementById('console-output');
        
        if (!input || !output) return;
        
        const command = input.value.trim();
        if (!command) return;
        
        // Añadir comando al historial
        this.commandHistory.push(command);
        
        // Mostrar comando en output
        const commandLine = document.createElement('div');
        commandLine.className = 'console-line';
        commandLine.textContent = `> ${command}`;
        output.appendChild(commandLine);
        
        // Ejecutar comando
        try {
            const result = eval(command);
            
            const resultLine = document.createElement('div');
            resultLine.className = 'console-line';
            resultLine.style.color = '#4CAF50';
            resultLine.textContent = typeof result === 'object' ? JSON.stringify(result, null, 2) : result;
            output.appendChild(resultLine);
            
        } catch (error) {
            const errorLine = document.createElement('div');
            errorLine.className = 'console-line';
            errorLine.style.color = '#f44336';
            errorLine.textContent = `Error: ${error.message}`;
            output.appendChild(errorLine);
        }
        
        // Limpiar input y scroll
        input.value = '';
        output.scrollTop = output.scrollHeight;
    }

    // 📊 Configurar auto-reporte
    setupAutoReporting() {
        // Reporte automático cada 5 minutos
        setInterval(() => {
            this.generateSystemReport();
        }, 300000);
        
        console.log('📊 Auto-reporting configurado');
    }

    // 📋 Generar reporte del sistema
    generateSystemReport() {
        const report = {
            timestamp: new Date().toISOString(),
            systems: {},
            summary: {}
        };
        
        // Recopilar datos de todos los sistemas
        this.systems.forEach((system, systemId) => {
            try {
                if (system.getStats) {
                    report.systems[systemId] = system.getStats();
                }
            } catch (error) {
                report.systems[systemId] = { error: error.message };
            }
        });
        
        // Calcular resumen
        report.summary = {
            activeSystems: this.systems.size,
            totalErrors: Object.values(report.systems).filter(s => s.error).length,
            timestamp: Date.now()
        };
        
        console.log('📋 System Report Generated:', report);
        return report;
    }

    // Métodos de comando delegados
    getSystemsStatus() {
        return this.generateSystemReport();
    }

    generatePerformanceReport() {
        if (this.systems.has('performance-audit')) {
            return this.systems.get('performance-audit').generateReport();
        }
        return 'Performance Audit system not available';
    }

    clearAllCache() {
        if (this.systems.has('cache-optimizer')) {
            return this.systems.get('cache-optimizer').clearAllCache();
        }
        return 'Cache Optimizer system not available';
    }

    getCacheStats() {
        if (this.systems.has('cache-optimizer')) {
            return this.systems.get('cache-optimizer').getStats();
        }
        return 'Cache Optimizer system not available';
    }

    refreshCache() {
        if (this.systems.has('cache-optimizer')) {
            return this.systems.get('cache-optimizer').refreshCache();
        }
        return 'Cache Optimizer system not available';
    }

    getSyncStatus() {
        if (this.systems.has('background-sync')) {
            return this.systems.get('background-sync').getStats();
        }
        return 'Background Sync system not available';
    }

    forceSync() {
        if (this.systems.has('background-sync')) {
            return this.systems.get('background-sync').forceSync();
        }
        return 'Background Sync system not available';
    }

    clearSyncQueue() {
        if (this.systems.has('background-sync')) {
            return this.systems.get('background-sync').clearQueue();
        }
        return 'Background Sync system not available';
    }

    getPreloadStats() {
        if (this.systems.has('resource-preloader')) {
            return this.systems.get('resource-preloader').getStats();
        }
        return 'Resource Preloader system not available';
    }

    preloadResource(url, type, priority) {
        if (this.systems.has('resource-preloader')) {
            return this.systems.get('resource-preloader').preloadResource(url, type, priority);
        }
        return 'Resource Preloader system not available';
    }

    runAllTests() {
        if (this.systems.has('testing-console')) {
            return this.systems.get('testing-console').runFullTest();
        }
        return 'Testing Console system not available';
    }

    testPerformance() {
        if (this.systems.has('performance-audit')) {
            return this.systems.get('performance-audit').measureLoadTime();
        }
        return 'Performance Audit system not available';
    }

    analyzeCSSUsage() {
        if (this.systems.has('css-analyzer')) {
            return this.systems.get('css-analyzer').analyzeUnusedCSS();
        }
        return 'CSS Analyzer system not available';
    }

    optimizeLazyLoading() {
        if (this.systems.has('lazy-loader')) {
            return this.systems.get('lazy-loader').getStats();
        }
        return 'Lazy Loader system not available';
    }

    optimizeCriticalCSS() {
        if (this.systems.has('critical-css')) {
            return this.systems.get('critical-css').getStats();
        }
        return 'Critical CSS Optimizer system not available';
    }

    optimizeCache() {
        return this.clearAllCache();
    }

    showHelp() {
        return `
🎯 LINO Command Center V3 - Comandos Disponibles:

📊 Estado del Sistema:
- LinoCommand.status() - Estado de todos los sistemas
- LinoCommand.performance() - Reporte de performance

💾 Cache:
- LinoCommand.cache.clear() - Limpiar toda la cache
- LinoCommand.cache.stats() - Estadísticas de cache
- LinoCommand.cache.refresh() - Refrescar cache

🔄 Sincronización:
- LinoCommand.sync.status() - Estado de sync
- LinoCommand.sync.force() - Forzar sincronización
- LinoCommand.sync.clear() - Limpiar queue de sync

🎯 Preloading:
- LinoCommand.preload.stats() - Estadísticas de preload
- LinoCommand.preload.resource(url, type, priority) - Precargar recurso

🧪 Testing:
- LinoCommand.test.run() - Ejecutar todos los tests
- LinoCommand.test.performance() - Test de performance
- LinoCommand.test.css() - Analizar CSS

⚡ Optimización:
- LinoCommand.optimize.lazy() - Optimizar lazy loading
- LinoCommand.optimize.css() - Optimizar CSS crítico
- LinoCommand.optimize.cache() - Optimizar cache

⌨️ Atajos de Teclado:
- Ctrl+Shift+L - Abrir/Cerrar Command Center
- Ctrl+Shift+P - Reporte de Performance
- Ctrl+Shift+S - Estado del Sistema
- Ctrl+Shift+C - Limpiar Cache
- Ctrl+Shift+R - Refrescar Sistemas
        `;
    }

    refreshAllSystems() {
        console.log('🔄 Refrescando todos los sistemas...');
        
        this.systems.forEach((system, systemId) => {
            try {
                if (system.refresh) {
                    system.refresh();
                    console.log(`✅ ${systemId} refrescado`);
                }
            } catch (error) {
                console.error(`❌ Error refrescando ${systemId}:`, error);
            }
        });
        
        return 'Sistemas refrescados';
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoCommandCenter = LinoCommandCenter.instance = new LinoCommandCenter();
    
    // Comando global para abrir
    window.openLinoCommandCenter = () => LinoCommandCenter.instance.toggleCommandCenter();
});
