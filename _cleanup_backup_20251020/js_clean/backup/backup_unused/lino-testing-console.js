/**
 * 🧪 LINO TESTING CONSOLE V3
 * Consola avanzada de testing y debugging
 */

class LinoTestingConsole {
    constructor() {
        this.version = '3.0.0';
        this.testResults = {};
        this.isDebugMode = window.location.search.includes('debug=true') || 
                          localStorage.getItem('lino-debug') === 'true';
        this.init();
    }

    init() {
        console.log('🧪 LINO Testing Console V3 iniciada');
        this.createDebugPanel();
        this.registerGlobalCommands();
        this.runStartupTests();
    }

    // 🎛️ Crear panel de debug visual
    createDebugPanel() {
        if (!this.isDebugMode) return;

        const panel = document.createElement('div');
        panel.id = 'lino-debug-panel';
        panel.innerHTML = `
            <div style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(0,0,0,0.9);
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                z-index: 10000;
                max-width: 300px;
                backdrop-filter: blur(10px);
            ">
                <div style="font-weight: bold; margin-bottom: 10px;">
                    🧪 LINO Testing Console V3
                </div>
                <div id="debug-status"></div>
                <div style="margin-top: 10px;">
                    <button onclick="window.LinoTesting.runFullTest()" style="
                        background: #007bff;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        margin: 2px;
                        cursor: pointer;
                    ">Full Test</button>
                    <button onclick="window.LinoTesting.runPerformanceTest()" style="
                        background: #28a745;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        margin: 2px;
                        cursor: pointer;
                    ">Performance</button>
                    <button onclick="window.LinoTesting.runCSSTest()" style="
                        background: #ffc107;
                        color: black;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        margin: 2px;
                        cursor: pointer;
                    ">CSS Analysis</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(panel);
        this.updateDebugStatus('Consola iniciada ✅');
    }

    // 📊 Actualizar estado del panel
    updateDebugStatus(message) {
        const statusEl = document.getElementById('debug-status');
        if (statusEl) {
            statusEl.innerHTML = `${new Date().toLocaleTimeString()}: ${message}`;
        }
    }

    // 🌐 Registrar comandos globales
    registerGlobalCommands() {
        window.LinoTesting = {
            // Comandos principales
            runFullTest: () => this.runFullTest(),
            runPerformanceTest: () => this.runPerformanceTest(),
            runCSSTest: () => this.runCSSTest(),
            runComponentTest: () => this.runComponentTest(),
            runAccessibilityTest: () => this.runAccessibilityTest(),
            
            // Comandos de debugging
            enableDebug: () => this.enableDebugMode(),
            disableDebug: () => this.disableDebugMode(),
            showResults: () => this.showTestResults(),
            clearResults: () => this.clearTestResults(),
            
            // Comandos de utilidad
            version: () => this.version,
            help: () => this.showHelp()
        };

        // Atajos de teclado
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+T = Testing Console
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.toggleDebugMode();
            }
            
            // Ctrl+Shift+P = Performance Test
            if (e.ctrlKey && e.shiftKey && e.key === 'P') {
                e.preventDefault();
                this.runPerformanceTest();
            }
        });

        console.log('🎮 Comandos LINO Testing disponibles:');
        console.log('  • LinoTesting.runFullTest() - Test completo');
        console.log('  • LinoTesting.runPerformanceTest() - Solo performance');
        console.log('  • LinoTesting.runCSSTest() - Solo CSS analysis');
        console.log('  • LinoTesting.help() - Ver todos los comandos');
        console.log('  • Ctrl+Shift+T - Toggle debug panel');
        console.log('  • Ctrl+Shift+P - Quick performance test');
    }

    // 🚀 Test completo del sistema
    async runFullTest() {
        console.group('🧪 LINO V3 Full System Test');
        this.updateDebugStatus('Ejecutando test completo...');
        
        const startTime = performance.now();
        const results = {};

        try {
            // 1. Test de componentes V3
            console.log('1️⃣ Testing V3 Components...');
            results.components = await this.runComponentTest();
            
            // 2. Test de performance
            console.log('2️⃣ Testing Performance...');
            results.performance = await this.runPerformanceTest();
            
            // 3. Test de CSS
            console.log('3️⃣ Testing CSS...');
            results.css = await this.runCSSTest();
            
            // 4. Test de accesibilidad
            console.log('4️⃣ Testing Accessibility...');
            results.accessibility = await this.runAccessibilityTest();
            
            // 5. Test de features V3
            console.log('5️⃣ Testing V3 Features...');
            results.features = await this.runV3FeaturesTest();

            const totalTime = performance.now() - startTime;
            
            this.testResults = {
                timestamp: new Date().toISOString(),
                totalTime: totalTime,
                results: results,
                overall: this.calculateOverallScore(results)
            };

            console.log(`✅ Test completo finalizado en ${totalTime.toFixed(2)}ms`);
            this.printFullResults();
            this.updateDebugStatus(`Test completo ✅ Score: ${this.testResults.overall.score}/100`);
            
        } catch (error) {
            console.error('❌ Error en test completo:', error);
            this.updateDebugStatus('Test completo ❌ Error');
        }
        
        console.groupEnd();
        return this.testResults;
    }

    // 📊 Test de performance
    async runPerformanceTest() {
        if (!window.LinoPerformanceAudit) {
            console.warn('LinoPerformanceAudit no disponible');
            return null;
        }

        const audit = new window.LinoPerformanceAudit();
        await new Promise(resolve => setTimeout(resolve, 100));
        
        const report = audit.generateReport();
        console.log('📊 Performance Test completado');
        
        return {
            score: report.performanceScore,
            loadTime: report.metrics.loadTime.domContentLoaded,
            recommendations: report.recommendations.length,
            report: report
        };
    }

    // 🎨 Test de CSS
    async runCSSTest() {
        if (!window.LinoCSSAnalyzer) {
            console.warn('LinoCSSAnalyzer no disponible');
            return null;
        }

        const analyzer = new window.LinoCSSAnalyzer();
        await new Promise(resolve => setTimeout(resolve, 200));
        
        const report = analyzer.generateReport();
        console.log('🎨 CSS Test completado');
        
        return {
            optimizationScore: report.metrics.optimizationScore,
            v3AdoptionRate: report.metrics.v3AdoptionRate,
            potentialSavings: report.metrics.potentialSavings,
            recommendations: report.recommendations.length,
            report: report
        };
    }

    // 🧩 Test de componentes V3
    async runComponentTest() {
        const components = {
            cards: document.querySelectorAll('.lino-card').length,
            kpiCards: document.querySelectorAll('.lino-kpi-card').length,
            kpiMinis: document.querySelectorAll('.lino-kpi-mini').length,
            buttons: document.querySelectorAll('.lino-button').length,
            forms: document.querySelectorAll('.lino-form').length,
            grids: document.querySelectorAll('.lino-row').length,
            alerts: document.querySelectorAll('.lino-alert').length,
            breadcrumbs: document.querySelectorAll('.lino-breadcrumb').length,
            pageHeaders: document.querySelectorAll('.lino-page-header').length
        };

        const activeComponents = Object.keys(components).filter(key => components[key] > 0);
        const totalComponents = Object.values(components).reduce((a, b) => a + b, 0);
        
        // Test de sistemas JavaScript
        const jsFeatures = {
            darkMode: !!window.LinoTheme,
            animations: !!window.AOS,
            tooltips: !!window.LinoTooltips,
            cssOptimizer: !!window.LinoCSSOptimizer,
            performanceAudit: !!window.LinoPerformanceAudit
        };

        const activeFeatures = Object.keys(jsFeatures).filter(key => jsFeatures[key]);

        console.log('🧩 Component Test completado');
        
        return {
            components: components,
            totalComponents: totalComponents,
            activeComponentTypes: activeComponents.length,
            jsFeatures: jsFeatures,
            activeFeatures: activeFeatures.length,
            score: Math.min(100, (activeComponents.length / 9) * 50 + (activeFeatures.length / 5) * 50)
        };
    }

    // ♿ Test de accesibilidad
    async runAccessibilityTest() {
        const checks = {
            altTexts: document.querySelectorAll('img:not([alt])').length === 0,
            headingHierarchy: this.checkHeadingHierarchy(),
            colorContrast: document.documentElement.hasAttribute('data-theme'),
            keyboardNavigation: document.querySelectorAll('[tabindex]').length > 0,
            ariaLabels: document.querySelectorAll('[aria-label], [aria-labelledby]').length > 0,
            semanticHTML: document.querySelectorAll('nav, main, section, article, aside, header, footer').length > 0
        };

        const passedChecks = Object.values(checks).filter(Boolean).length;
        const totalChecks = Object.keys(checks).length;
        
        console.log('♿ Accessibility Test completado');
        
        return {
            checks: checks,
            passedChecks: passedChecks,
            totalChecks: totalChecks,
            score: (passedChecks / totalChecks) * 100
        };
    }

    // 🚀 Test de features V3
    async runV3FeaturesTest() {
        const features = {
            darkModeToggle: !!window.toggleTheme,
            animatedCounters: document.querySelectorAll('.lino-counter').length > 0,
            tooltipSystem: document.querySelectorAll('[data-tooltip]').length > 0,
            responsiveGrid: document.querySelectorAll('.lino-row .lino-col-md-6, .lino-row .lino-col-lg-4').length > 0,
            gradientCards: document.querySelectorAll('.lino-gradient-success, .lino-gradient-primary').length > 0
        };

        const activeFeatures = Object.keys(features).filter(key => features[key]);
        
        console.log('🚀 V3 Features Test completado');
        
        return {
            features: features,
            activeFeatures: activeFeatures.length,
            score: (activeFeatures.length / Object.keys(features).length) * 100
        };
    }

    // 📊 Calcular score general
    calculateOverallScore(results) {
        let totalScore = 0;
        let testCount = 0;

        Object.values(results).forEach(result => {
            if (result && result.score !== undefined) {
                totalScore += result.score;
                testCount++;
            }
        });

        const averageScore = testCount > 0 ? totalScore / testCount : 0;
        
        return {
            score: Math.round(averageScore),
            grade: this.getGrade(averageScore),
            testCount: testCount,
            breakdown: Object.keys(results).map(key => ({
                test: key,
                score: results[key]?.score || 0
            }))
        };
    }

    // 🏆 Obtener calificación
    getGrade(score) {
        if (score >= 90) return 'A+';
        if (score >= 80) return 'A';
        if (score >= 70) return 'B';
        if (score >= 60) return 'C';
        return 'D';
    }

    // 🔍 Verificar jerarquía de headings
    checkHeadingHierarchy() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        if (headings.length === 0) return false;
        
        let currentLevel = 0;
        for (const heading of headings) {
            const level = parseInt(heading.tagName[1]);
            if (level > currentLevel + 1) return false;
            currentLevel = level;
        }
        return true;
    }

    // 🖨️ Imprimir resultados completos
    printFullResults() {
        if (!this.testResults) return;

        console.group('🎯 LINO V3 Testing Results Summary');
        console.log(`📅 Timestamp: ${this.testResults.timestamp}`);
        console.log(`⏱️ Total Time: ${this.testResults.totalTime.toFixed(2)}ms`);
        console.log(`⭐ Overall Score: ${this.testResults.overall.score}/100 (${this.testResults.overall.grade})`);
        
        console.group('📊 Test Breakdown');
        this.testResults.overall.breakdown.forEach(test => {
            console.log(`${test.test}: ${test.score.toFixed(1)}/100`);
        });
        console.groupEnd();
        
        console.groupEnd();
    }

    // 🎛️ Toggle modo debug
    toggleDebugMode() {
        this.isDebugMode = !this.isDebugMode;
        localStorage.setItem('lino-debug', this.isDebugMode.toString());
        
        if (this.isDebugMode) {
            this.createDebugPanel();
        } else {
            const panel = document.getElementById('lino-debug-panel');
            if (panel) panel.remove();
        }
    }

    // 📋 Mostrar ayuda
    showHelp() {
        console.group('🆘 LINO Testing Console V3 - Comandos Disponibles');
        console.log('🧪 Testing Commands:');
        console.log('  • LinoTesting.runFullTest() - Ejecuta todos los tests');
        console.log('  • LinoTesting.runPerformanceTest() - Solo test de performance');
        console.log('  • LinoTesting.runCSSTest() - Solo análisis de CSS');
        console.log('  • LinoTesting.runComponentTest() - Solo test de componentes');
        console.log('  • LinoTesting.runAccessibilityTest() - Solo test de accesibilidad');
        
        console.log('\n🎛️ Debug Commands:');
        console.log('  • LinoTesting.enableDebug() - Activar modo debug');
        console.log('  • LinoTesting.disableDebug() - Desactivar modo debug');
        console.log('  • LinoTesting.showResults() - Mostrar últimos resultados');
        console.log('  • LinoTesting.clearResults() - Limpiar resultados');
        
        console.log('\n⌨️ Keyboard Shortcuts:');
        console.log('  • Ctrl+Shift+T - Toggle debug panel');
        console.log('  • Ctrl+Shift+P - Quick performance test');
        
        console.log('\n🔗 URL Parameters:');
        console.log('  • ?debug=true - Activar modo debug');
        console.log('  • ?debug=performance - Solo performance audit');
        
        console.groupEnd();
    }

    // Tests startup
    runStartupTests() {
        if (this.isDebugMode) {
            console.log('🚀 Running startup tests...');
            setTimeout(() => {
                this.runComponentTest().then(results => {
                    this.updateDebugStatus(`Componentes: ${results.totalComponents} detectados`);
                });
            }, 1000);
        }
    }

    // Métodos auxiliares
    enableDebugMode() { 
        this.isDebugMode = true; 
        this.createDebugPanel();
        localStorage.setItem('lino-debug', 'true');
    }
    
    disableDebugMode() { 
        this.isDebugMode = false; 
        const panel = document.getElementById('lino-debug-panel');
        if (panel) panel.remove();
        localStorage.setItem('lino-debug', 'false');
    }
    
    showTestResults() { 
        if (this.testResults) {
            console.table(this.testResults.overall.breakdown);
        } else {
            console.log('No hay resultados de tests disponibles');
        }
    }
    
    clearTestResults() { 
        this.testResults = {};
        console.log('Resultados de tests eliminados');
    }
}

// 🚀 Auto-inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.LinoTestingConsole = new LinoTestingConsole();
});
