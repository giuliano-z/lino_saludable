/**
 * 🔍 LINO PERFORMANCE AUDIT SYSTEM V3
 * Sistema avanzado de auditoría de performance
 */

class LinoPerformanceAudit {
    constructor() {
        this.metrics = {};
        this.startTime = performance.now();
        this.init();
    }

    init() {
        console.log('🔍 LINO Performance Audit iniciado');
        this.measureLoadTime();
        this.measureCSSPerformance();
        this.measureJSPerformance();
        this.measureDOMMetrics();
        this.measureNetworkMetrics();
        this.measureUserExperience();
    }

    // 📊 Medición de tiempo de carga
    measureLoadTime() {
        const navigation = performance.getEntriesByType('navigation')[0];
        
        this.metrics.loadTime = {
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            firstByte: navigation.responseStart - navigation.requestStart,
            domInteractive: navigation.domInteractive - navigation.navigationStart
        };
    }

    // 🎨 Medición de performance CSS
    measureCSSPerformance() {
        const cssResources = performance.getEntriesByType('resource').filter(resource => 
            resource.name.includes('.css')
        );

        let totalCSSSize = 0;
        let totalCSSLoadTime = 0;

        cssResources.forEach(css => {
            totalCSSSize += css.transferSize || 0;
            totalCSSLoadTime += css.duration;
        });

        this.metrics.css = {
            files: cssResources.length,
            totalSize: totalCSSSize,
            totalLoadTime: totalCSSLoadTime,
            averageLoadTime: totalCSSLoadTime / cssResources.length || 0,
            resources: cssResources.map(css => ({
                name: css.name.split('/').pop(),
                size: css.transferSize,
                loadTime: css.duration
            }))
        };
    }

    // ⚡ Medición de performance JavaScript
    measureJSPerformance() {
        const jsResources = performance.getEntriesByType('resource').filter(resource => 
            resource.name.includes('.js')
        );

        let totalJSSize = 0;
        let totalJSLoadTime = 0;

        jsResources.forEach(js => {
            totalJSSize += js.transferSize || 0;
            totalJSLoadTime += js.duration;
        });

        this.metrics.javascript = {
            files: jsResources.length,
            totalSize: totalJSSize,
            totalLoadTime: totalJSLoadTime,
            averageLoadTime: totalJSLoadTime / jsResources.length || 0,
            resources: jsResources.map(js => ({
                name: js.name.split('/').pop(),
                size: js.transferSize,
                loadTime: js.duration
            }))
        };
    }

    // 🌳 Medición de métricas DOM
    measureDOMMetrics() {
        this.metrics.dom = {
            elements: document.querySelectorAll('*').length,
            depth: this.getDOMDepth(),
            images: document.querySelectorAll('img').length,
            stylesheets: document.querySelectorAll('link[rel="stylesheet"]').length,
            scripts: document.querySelectorAll('script').length,
            linoCssClasses: document.querySelectorAll('[class*="lino-"]').length,
            v3Components: {
                cards: document.querySelectorAll('.lino-card').length,
                kpis: document.querySelectorAll('.lino-kpi-card, .lino-kpi-mini').length,
                buttons: document.querySelectorAll('.lino-button').length,
                forms: document.querySelectorAll('.lino-form').length,
                grids: document.querySelectorAll('.lino-row').length
            }
        };
    }

    // 🌐 Medición de métricas de red
    measureNetworkMetrics() {
        const allResources = performance.getEntriesByType('resource');
        
        let totalSize = 0;
        let totalRequests = allResources.length;

        allResources.forEach(resource => {
            totalSize += resource.transferSize || 0;
        });

        this.metrics.network = {
            totalRequests: totalRequests,
            totalSize: totalSize,
            averageSize: totalSize / totalRequests,
            cacheHits: allResources.filter(r => r.transferSize === 0).length,
            cacheRate: (allResources.filter(r => r.transferSize === 0).length / totalRequests) * 100
        };
    }

    // 👤 Medición de experiencia de usuario
    measureUserExperience() {
        // First Contentful Paint
        const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0];
        
        // Largest Contentful Paint
        let largestContentfulPaint = 0;
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            largestContentfulPaint = entries[entries.length - 1].startTime;
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        this.metrics.userExperience = {
            firstContentfulPaint: fcpEntry ? fcpEntry.startTime : 0,
            largestContentfulPaint: largestContentfulPaint,
            darkModeSupport: document.documentElement.hasAttribute('data-theme'),
            animationsActive: window.AOS ? true : false,
            tooltipsActive: window.LinoTooltips ? true : false,
            themeSystemActive: window.LinoTheme ? true : false
        };
    }

    // 📏 Calcular profundidad del DOM
    getDOMDepth() {
        let maxDepth = 0;
        
        function calculateDepth(element, depth = 0) {
            maxDepth = Math.max(maxDepth, depth);
            for (let child of element.children) {
                calculateDepth(child, depth + 1);
            }
        }
        
        calculateDepth(document.documentElement);
        return maxDepth;
    }

    // 📊 Generar score de performance
    calculatePerformanceScore() {
        let score = 100;
        
        // Penalizar tiempo de carga lento
        if (this.metrics.loadTime.domContentLoaded > 1000) score -= 20;
        if (this.metrics.loadTime.loadComplete > 2000) score -= 15;
        
        // Penalizar muchos recursos CSS/JS
        if (this.metrics.css.files > 10) score -= 10;
        if (this.metrics.javascript.files > 15) score -= 10;
        
        // Penalizar DOM complejo
        if (this.metrics.dom.elements > 1000) score -= 10;
        if (this.metrics.dom.depth > 15) score -= 5;
        
        // Bonificar características V3
        if (this.metrics.userExperience.darkModeSupport) score += 5;
        if (this.metrics.userExperience.animationsActive) score += 5;
        if (this.metrics.dom.v3Components.cards > 0) score += 5;
        
        return Math.max(0, Math.min(100, score));
    }

    // 📈 Generar reporte completo
    generateReport() {
        const performanceScore = this.calculatePerformanceScore();
        const totalTime = performance.now() - this.startTime;

        const report = {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            userAgent: navigator.userAgent,
            performanceScore: performanceScore,
            auditTime: totalTime,
            metrics: this.metrics,
            recommendations: this.generateRecommendations()
        };

        return report;
    }

    // 💡 Generar recomendaciones
    generateRecommendations() {
        const recommendations = [];

        if (this.metrics.loadTime.domContentLoaded > 1000) {
            recommendations.push({
                type: 'performance',
                priority: 'high',
                message: 'DOM Content Loaded toma más de 1 segundo',
                solution: 'Optimizar CSS crítico y diferir recursos no esenciales'
            });
        }

        if (this.metrics.css.totalSize > 100000) {
            recommendations.push({
                type: 'css',
                priority: 'medium',
                message: 'Tamaño total de CSS mayor a 100KB',
                solution: 'Implementar tree-shaking y minificación avanzada'
            });
        }

        if (this.metrics.network.cacheRate < 50) {
            recommendations.push({
                type: 'caching',
                priority: 'medium',
                message: 'Tasa de cache baja (< 50%)',
                solution: 'Implementar headers de cache más agresivos'
            });
        }

        if (!this.metrics.userExperience.darkModeSupport) {
            recommendations.push({
                type: 'feature',
                priority: 'low',
                message: 'Dark mode no detectado',
                solution: 'Verificar implementación del sistema de temas'
            });
        }

        return recommendations;
    }

    // 🖨️ Imprimir reporte en consola
    printReport() {
        const report = this.generateReport();
        
        console.group('🔍 LINO V3 Performance Audit Report');
        console.log(`📅 Timestamp: ${report.timestamp}`);
        console.log(`🌐 URL: ${report.url}`);
        console.log(`⭐ Performance Score: ${report.performanceScore}/100`);
        console.log(`⏱️ Audit Time: ${report.auditTime.toFixed(2)}ms`);
        
        console.group('📊 Load Time Metrics');
        console.table(report.metrics.loadTime);
        console.groupEnd();
        
        console.group('🎨 CSS Performance');
        console.table(report.metrics.css);
        console.groupEnd();
        
        console.group('⚡ JavaScript Performance');
        console.table(report.metrics.javascript);
        console.groupEnd();
        
        console.group('🌳 DOM Metrics');
        console.table(report.metrics.dom);
        console.groupEnd();
        
        console.group('🌐 Network Metrics');
        console.table(report.metrics.network);
        console.groupEnd();
        
        console.group('👤 User Experience');
        console.table(report.metrics.userExperience);
        console.groupEnd();
        
        if (report.recommendations.length > 0) {
            console.group('💡 Recommendations');
            report.recommendations.forEach((rec, index) => {
                console.log(`${index + 1}. [${rec.priority.toUpperCase()}] ${rec.message}`);
                console.log(`   💡 Solution: ${rec.solution}`);
            });
            console.groupEnd();
        }
        
        console.groupEnd();
        
        return report;
    }
}

// 🚀 Auto-inicializar si estamos en modo debug
if (window.location.search.includes('debug=performance') || 
    localStorage.getItem('lino-debug-performance') === 'true') {
    
    window.addEventListener('load', () => {
        setTimeout(() => {
            const audit = new LinoPerformanceAudit();
            window.LinoAudit = audit;
            audit.printReport();
            
            console.log('💡 Comandos disponibles:');
            console.log('  • LinoAudit.printReport() - Imprimir reporte completo');
            console.log('  • LinoAudit.generateReport() - Obtener datos del reporte');
            console.log('  • LinoAudit.calculatePerformanceScore() - Solo el score');
        }, 1000);
    });
}

// 🌐 Exponer globalmente
window.LinoPerformanceAudit = LinoPerformanceAudit;
