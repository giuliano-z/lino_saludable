/**
 * 🧪 LINO FEATURE TESTS V3 - TESTS ESPECÍFICOS INTERACTIVOS
 * Tests detallados para validar funcionalidades específicas
 */

class LinoFeatureTests {
    constructor() {
        this.testResults = new Map();
        this.init();
    }

    init() {
        console.log('🧪 LINO Feature Tests V3 iniciado');
        this.setupInteractiveTests();
    }

    // 🔧 Configurar tests interactivos
    setupInteractiveTests() {
        // Crear botón de tests flotante
        this.createTestingFloatingButton();
        
        // Tests automáticos en ciertos eventos
        this.setupEventTests();
        
        console.log('🔧 Interactive tests configurados');
    }

    // 🎈 Crear botón flotante de tests
    createTestingFloatingButton() {
        const button = document.createElement('div');
        button.id = 'lino-test-button';
        button.innerHTML = '🧪';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            border-radius: 50%;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
            transition: all 0.3s ease;
            user-select: none;
        `;
        
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.1)';
            button.style.boxShadow = '0 6px 20px rgba(76, 175, 80, 0.4)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
            button.style.boxShadow = '0 4px 12px rgba(76, 175, 80, 0.3)';
        });
        
        button.addEventListener('click', () => {
            this.showTestingMenu();
        });
        
        document.body.appendChild(button);
        console.log('🎈 Botón de testing flotante creado');
    }

    // 📋 Mostrar menú de testing
    showTestingMenu() {
        const menu = document.createElement('div');
        menu.id = 'lino-test-menu';
        menu.style.cssText = `
            position: fixed;
            bottom: 90px;
            right: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            min-width: 300px;
            padding: 20px;
            border: 1px solid #e0e0e0;
        `;
        
        menu.innerHTML = `
            <div style="margin-bottom: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #333; font-size: 16px;">🧪 LINO Testing Menu</h3>
                <p style="margin: 0; color: #666; font-size: 12px;">Selecciona el tipo de test a ejecutar</p>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <button onclick="LinoFeatureTests.instance.testLazyLoadingDemo()" style="padding: 8px 12px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">🚀 Test Lazy Loading</button>
                
                <button onclick="LinoFeatureTests.instance.testCodeSplittingDemo()" style="padding: 8px 12px; border: 1px solid #2196F3; background: #2196F3; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">⚡ Test Code Splitting</button>
                
                <button onclick="LinoFeatureTests.instance.testCacheDemo()" style="padding: 8px 12px; border: 1px solid #FF9800; background: #FF9800; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">💾 Test Cache Strategy</button>
                
                <button onclick="LinoFeatureTests.instance.testPreloadingDemo()" style="padding: 8px 12px; border: 1px solid #9C27B0; background: #9C27B0; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">🎯 Test Preloading</button>
                
                <button onclick="LinoFeatureTests.instance.testSyncDemo()" style="padding: 8px 12px; border: 1px solid #795548; background: #795548; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">🔄 Test Background Sync</button>
                
                <button onclick="runLinoTests()" style="padding: 8px 12px; border: 1px solid #f44336; background: #f44336; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">🧪 Run All Tests</button>
                
                <button onclick="quickTestLino()" style="padding: 8px 12px; border: 1px solid #607D8B; background: #607D8B; color: white; border-radius: 6px; cursor: pointer; font-size: 12px;">⚡ Quick Test</button>
            </div>
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                <button onclick="this.parentElement.parentElement.remove()" style="padding: 6px 12px; border: 1px solid #ccc; background: white; color: #666; border-radius: 4px; cursor: pointer; font-size: 11px; width: 100%;">Cerrar</button>
            </div>
        `;
        
        // Remover menú existente
        const existingMenu = document.getElementById('lino-test-menu');
        if (existingMenu) {
            existingMenu.remove();
        }
        
        document.body.appendChild(menu);
        
        // Auto-cerrar después de 10 segundos
        setTimeout(() => {
            if (menu.parentElement) {
                menu.remove();
            }
        }, 10000);
    }

    // 🚀 Test demo de Lazy Loading
    testLazyLoadingDemo() {
        console.log('🧪 Testing Lazy Loading Demo...');
        
        // Crear elementos de prueba
        const testContainer = document.createElement('div');
        testContainer.id = 'lazy-test-container';
        testContainer.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 10001;
            max-width: 500px;
            border: 1px solid #e0e0e0;
        `;
        
        testContainer.innerHTML = `
            <h3>🚀 Lazy Loading Test</h3>
            <p>Scroll down to see lazy loading in action:</p>
            
            <div style="height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin: 10px 0;">
                <div style="height: 100px; background: #f0f0f0; margin: 10px 0; display: flex; align-items: center; justify-content: center;">Elemento 1</div>
                <div style="height: 100px; background: #f0f0f0; margin: 10px 0; display: flex; align-items: center; justify-content: center;">Elemento 2</div>
                
                <img data-src="https://via.placeholder.com/300x200/4CAF50/white?text=Lazy+Image+1" 
                     style="width: 100%; height: 200px; background: #ddd; margin: 10px 0; display: block;"
                     alt="Lazy Image 1">
                
                <div style="height: 100px; background: #f0f0f0; margin: 10px 0; display: flex; align-items: center; justify-content: center;">Elemento 3</div>
                
                <img data-src="https://via.placeholder.com/300x200/2196F3/white?text=Lazy+Image+2" 
                     style="width: 100%; height: 200px; background: #ddd; margin: 10px 0; display: block;"
                     alt="Lazy Image 2">
                
                <div data-lazy-component="chart" data-chart-data='{"type":"bar","data":[1,2,3,4,5]}' 
                     style="height: 200px; background: #f9f9f9; margin: 10px 0; display: flex; align-items: center; justify-content: center; border: 2px dashed #ccc;">
                     📊 Componente Lazy (Chart)
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; justify-content: flex-end;">
                <button onclick="console.log('Stats:', getLazyStats())" style="padding: 8px 16px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 6px; cursor: pointer;">Ver Stats</button>
                <button onclick="this.parentElement.parentElement.remove()" style="padding: 8px 16px; border: 1px solid #ccc; background: white; color: #666; border-radius: 6px; cursor: pointer;">Cerrar</button>
            </div>
        `;
        
        document.body.appendChild(testContainer);
        
        // Activar lazy loading en las nuevas imágenes
        if (window.LinoLazyLoader) {
            window.LinoLazyLoader.setupImageLazyLoading();
            window.LinoLazyLoader.setupComponentLazyLoading();
        }
    }

    // ⚡ Test demo de Code Splitting
    testCodeSplittingDemo() {
        console.log('🧪 Testing Code Splitting Demo...');
        
        this.showTestResult('Code Splitting', `
            📊 Chunks actuales: ${window.getChunkStats?.()?.totalChunks || 'N/A'}
            ⚡ Chunks cargados: ${window.getChunkStats?.()?.loadedChunks || 'N/A'}
            🔄 Chunks cargando: ${window.getChunkStats?.()?.loadingChunks || 'N/A'}
            ❌ Chunks fallidos: ${window.getChunkStats?.()?.failedChunks || 'N/A'}
            
            <div style="margin: 15px 0;">
                <button onclick="loadChunk('productos')" style="margin: 5px; padding: 6px 12px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 4px; cursor: pointer;">Cargar Chunk Productos</button>
                <button onclick="preloadChunk('charts')" style="margin: 5px; padding: 6px 12px; border: 1px solid #2196F3; background: #2196F3; color: white; border-radius: 4px; cursor: pointer;">Precargar Charts</button>
                <button onclick="console.log(getChunkStats())" style="margin: 5px; padding: 6px 12px; border: 1px solid #FF9800; background: #FF9800; color: white; border-radius: 4px; cursor: pointer;">Ver Stats</button>
            </div>
        `);
    }

    // 💾 Test demo de Cache
    testCacheDemo() {
        console.log('🧪 Testing Cache Demo...');
        
        const stats = window.getCacheStats?.() || {};
        
        this.showTestResult('Cache Strategy', `
            💾 Hit Rate: ${stats.hitRate || 'N/A'}%
            ✅ Hits: ${stats.hits || 'N/A'}
            ❌ Misses: ${stats.misses || 'N/A'}
            📦 Stores: ${stats.stores || 'N/A'}
            🧠 Memory Items: ${stats.memoryCacheItems || 'N/A'}
            💽 LocalStorage: ${((stats.localStorageUsage || 0) / 1024).toFixed(2)} KB
            
            <div style="margin: 15px 0;">
                <button onclick="fetch('/api/test').then(r=>console.log('Request test completed'))" style="margin: 5px; padding: 6px 12px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 4px; cursor: pointer;">Test Request</button>
                <button onclick="clearCache()" style="margin: 5px; padding: 6px 12px; border: 1px solid #f44336; background: #f44336; color: white; border-radius: 4px; cursor: pointer;">Clear Cache</button>
                <button onclick="console.log(getCacheStats())" style="margin: 5px; padding: 6px 12px; border: 1px solid #2196F3; background: #2196F3; color: white; border-radius: 4px; cursor: pointer;">Refresh Stats</button>
            </div>
        `);
    }

    // 🎯 Test demo de Preloading
    testPreloadingDemo() {
        console.log('🧪 Testing Preloading Demo...');
        
        const stats = window.getPreloadStats?.() || {};
        
        this.showTestResult('Resource Preloading', `
            🎯 Success Rate: ${stats.successRate || 'N/A'}%
            ✅ Successful: ${stats.successful || 'N/A'}
            ❌ Failed: ${stats.failed || 'N/A'}
            ⏳ Attempted: ${stats.attempted || 'N/A'}
            🔄 Current Preloads: ${stats.currentPreloads || 'N/A'}
            📊 Behavior Data Points: ${stats.userBehaviorDataPoints || 'N/A'}
            
            <div style="margin: 15px 0;">
                <button onclick="preloadResource('/static/css/test.css', 'style', 'high')" style="margin: 5px; padding: 6px 12px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 4px; cursor: pointer;">Preload CSS</button>
                <button onclick="preloadResource('/static/js/test.js', 'script', 'medium')" style="margin: 5px; padding: 6px 12px; border: 1px solid #2196F3; background: #2196F3; color: white; border-radius: 4px; cursor: pointer;">Preload JS</button>
                <button onclick="console.log(getPreloadStats())" style="margin: 5px; padding: 6px 12px; border: 1px solid #FF9800; background: #FF9800; color: white; border-radius: 4px; cursor: pointer;">Ver Stats</button>
            </div>
        `);
    }

    // 🔄 Test demo de Background Sync
    testSyncDemo() {
        console.log('🧪 Testing Background Sync Demo...');
        
        const stats = window.getSyncStats?.() || {};
        
        this.showTestResult('Background Sync', `
            🌐 Online: ${stats.isOnline ? '🟢 Sí' : '🔴 No'}
            ✅ Successful: ${stats.successful || 'N/A'}
            ❌ Failed: ${stats.failed || 'N/A'}
            🔄 Queue Size: ${stats.queueSize || 'N/A'}
            ⏰ Last Sync: ${stats.lastSyncTime || 'Nunca'}
            🔀 Conflicts: ${stats.conflicts || 'N/A'}
            
            <div style="margin: 15px 0;">
                <button onclick="forceSync()" style="margin: 5px; padding: 6px 12px; border: 1px solid #4CAF50; background: #4CAF50; color: white; border-radius: 4px; cursor: pointer;">Force Sync</button>
                <button onclick="clearSyncQueue()" style="margin: 5px; padding: 6px 12px; border: 1px solid #f44336; background: #f44336; color: white; border-radius: 4px; cursor: pointer;">Clear Queue</button>
                <button onclick="console.log(getSyncStats())" style="margin: 5px; padding: 6px 12px; border: 1px solid #2196F3; background: #2196F3; color: white; border-radius: 4px; cursor: pointer;">Ver Stats</button>
            </div>
        `);
    }

    // 📊 Mostrar resultado de test
    showTestResult(title, content) {
        const result = document.createElement('div');
        result.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 10001;
            max-width: 600px;
            border: 1px solid #e0e0e0;
        `;
        
        result.innerHTML = `
            <h3>🧪 ${title} Test Results</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; font-family: monospace; font-size: 12px; white-space: pre-line;">${content}</div>
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 15px;">
                <button onclick="this.parentElement.parentElement.remove()" style="padding: 8px 16px; border: 1px solid #ccc; background: white; color: #666; border-radius: 6px; cursor: pointer;">Cerrar</button>
            </div>
        `;
        
        document.body.appendChild(result);
        
        // Auto-cerrar después de 15 segundos
        setTimeout(() => {
            if (result.parentElement) {
                result.remove();
            }
        }, 15000);
    }

    // 🎯 Configurar tests de eventos
    setupEventTests() {
        // Test cuando se hace hover en un enlace
        document.addEventListener('mouseover', (e) => {
            const link = e.target.closest('a[href]');
            if (link) {
                console.log('🎯 Hover detected on link:', link.href);
                // Verificar si se activa preloading
            }
        });
        
        // Test cuando se scrollea
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                console.log('📜 Scroll event - Testing lazy loading trigger');
            }, 100);
        });
        
        // Test cuando cambia la conectividad
        window.addEventListener('online', () => {
            console.log('🌐 Network restored - Testing sync trigger');
        });
        
        window.addEventListener('offline', () => {
            console.log('📵 Network lost - Testing offline mode');
        });
    }

    // 📊 Performance benchmark
    async benchmarkAllSystems() {
        console.log('📊 Starting performance benchmark...');
        
        const benchmarks = {};
        
        // Benchmark cada sistema
        const systems = [
            'LinoLazyLoader',
            'LinoCodeSplitter',
            'LinoCriticalCSSOptimizer',
            'LinoCacheOptimizer',
            'LinoResourcePreloader',
            'LinoBackgroundSync',
            'LinoCommandCenter'
        ];
        
        for (const system of systems) {
            if (window[system]) {
                const startTime = performance.now();
                
                try {
                    // Test básico de cada sistema
                    if (window[system].getStats) {
                        window[system].getStats();
                    }
                    
                    const endTime = performance.now();
                    benchmarks[system] = {
                        duration: endTime - startTime,
                        status: 'OK'
                    };
                } catch (error) {
                    benchmarks[system] = {
                        duration: 0,
                        status: 'ERROR',
                        error: error.message
                    };
                }
            } else {
                benchmarks[system] = {
                    duration: 0,
                    status: 'NOT_FOUND'
                };
            }
        }
        
        console.log('📊 Performance Benchmark Results:', benchmarks);
        return benchmarks;
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        LinoFeatureTests.instance = new LinoFeatureTests();
        
        // Comandos globales adicionales
        window.benchmarkLino = () => LinoFeatureTests.instance.benchmarkAllSystems();
        window.testLazyDemo = () => LinoFeatureTests.instance.testLazyLoadingDemo();
        window.testCacheDemo = () => LinoFeatureTests.instance.testCacheDemo();
        
        console.log('🧪 LINO Feature Tests listos!');
        console.log('   Usa el botón flotante 🧪 para acceder a tests interactivos');
        
    }, 3000);
});
