/**
 * ⚡ LINO CSS BUNDLE ANALYZER V3
 * Analizador avanzado de CSS para optimización
 */

class LinoCSSAnalyzer {
    constructor() {
        this.stylesheets = [];
        this.rules = [];
        this.selectors = [];
        this.unusedRules = [];
        this.duplicateRules = [];
        this.init();
    }

    async init() {
        console.log('⚡ LINO CSS Analyzer iniciado');
        await this.loadStylesheets();
        this.analyzeCSS();
        this.detectUnusedCSS();
        this.detectDuplicates();
        this.analyzeLinoV3Coverage();
    }

    // 📄 Cargar todas las hojas de estilo
    async loadStylesheets() {
        const styleSheets = Array.from(document.styleSheets);
        
        for (const sheet of styleSheets) {
            try {
                const rules = Array.from(sheet.cssRules || sheet.rules);
                this.stylesheets.push({
                    href: sheet.href,
                    title: sheet.title,
                    disabled: sheet.disabled,
                    media: sheet.media.mediaText,
                    rulesCount: rules.length,
                    rules: rules
                });
                this.rules.push(...rules);
            } catch (e) {
                console.warn('No se pudo acceder a:', sheet.href, e.message);
            }
        }
    }

    // 🔍 Analizar CSS general
    analyzeCSS() {
        this.rules.forEach(rule => {
            if (rule.selectorText) {
                this.selectors.push({
                    selector: rule.selectorText,
                    cssText: rule.cssText,
                    isLino: rule.selectorText.includes('lino-'),
                    isV3: this.isV3Selector(rule.selectorText),
                    specificity: this.calculateSpecificity(rule.selectorText)
                });
            }
        });
    }

    // 🎯 Detectar si es selector V3
    isV3Selector(selector) {
        const v3Patterns = [
            'lino-card',
            'lino-kpi-',
            'lino-button',
            'lino-form',
            'lino-row',
            'lino-col-',
            'lino-gradient-',
            'lino-alert',
            'lino-breadcrumb',
            'lino-page-header'
        ];
        
        return v3Patterns.some(pattern => selector.includes(pattern));
    }

    // 📊 Calcular especificidad CSS
    calculateSpecificity(selector) {
        // Simplificado: contar IDs, clases, elementos
        const ids = (selector.match(/#/g) || []).length;
        const classes = (selector.match(/\./g) || []).length;
        const elements = (selector.match(/[a-zA-Z]/g) || []).length - classes;
        
        return {
            ids: ids,
            classes: classes,
            elements: elements,
            score: ids * 100 + classes * 10 + elements
        };
    }

    // 🚫 Detectar CSS no utilizado
    detectUnusedCSS() {
        this.selectors.forEach(selectorObj => {
            try {
                const elements = document.querySelectorAll(selectorObj.selector);
                if (elements.length === 0) {
                    this.unusedRules.push(selectorObj);
                }
            } catch (e) {
                // Selector inválido o complejo
            }
        });
    }

    // 🔄 Detectar reglas duplicadas
    detectDuplicates() {
        const seenRules = new Map();
        
        this.selectors.forEach(selectorObj => {
            const key = selectorObj.cssText;
            if (seenRules.has(key)) {
                this.duplicateRules.push({
                    original: seenRules.get(key),
                    duplicate: selectorObj
                });
            } else {
                seenRules.set(key, selectorObj);
            }
        });
    }

    // 🚀 Analizar cobertura LINO V3
    analyzeLinoV3Coverage() {
        const v3Components = {
            cards: document.querySelectorAll('.lino-card').length,
            kpiCards: document.querySelectorAll('.lino-kpi-card').length,
            kpiMinis: document.querySelectorAll('.lino-kpi-mini').length,
            buttons: document.querySelectorAll('.lino-button').length,
            forms: document.querySelectorAll('.lino-form').length,
            grids: document.querySelectorAll('.lino-row').length,
            cols: document.querySelectorAll('[class*="lino-col-"]').length,
            alerts: document.querySelectorAll('.lino-alert').length,
            breadcrumbs: document.querySelectorAll('.lino-breadcrumb').length,
            pageHeaders: document.querySelectorAll('.lino-page-header').length
        };

        const v3Selectors = this.selectors.filter(s => s.isV3);
        const linoSelectors = this.selectors.filter(s => s.isLino);

        this.v3Coverage = {
            components: v3Components,
            totalV3Selectors: v3Selectors.length,
            totalLinoSelectors: linoSelectors.length,
            v3Ratio: (v3Selectors.length / linoSelectors.length) * 100,
            activeComponents: Object.keys(v3Components).filter(key => v3Components[key] > 0),
            inactiveComponents: Object.keys(v3Components).filter(key => v3Components[key] === 0)
        };
    }

    // 📈 Calcular métricas de optimización
    calculateOptimizationMetrics() {
        const totalSelectors = this.selectors.length;
        const unusedCount = this.unusedRules.length;
        const duplicateCount = this.duplicateRules.length;
        const linoCount = this.selectors.filter(s => s.isLino).length;
        const v3Count = this.selectors.filter(s => s.isV3).length;

        // Calcular tamaño estimado
        let totalSize = 0;
        this.stylesheets.forEach(sheet => {
            if (sheet.href && sheet.href.includes('lino')) {
                // Estimación basada en número de reglas
                totalSize += sheet.rulesCount * 50; // ~50 bytes por regla promedio
            }
        });

        return {
            totalSelectors: totalSelectors,
            unusedSelectors: unusedCount,
            duplicateSelectors: duplicateCount,
            linoSelectors: linoCount,
            v3Selectors: v3Count,
            unusedPercentage: (unusedCount / totalSelectors) * 100,
            duplicatePercentage: (duplicateCount / totalSelectors) * 100,
            v3AdoptionRate: (v3Count / linoCount) * 100,
            estimatedSize: totalSize,
            potentialSavings: ((unusedCount + duplicateCount) / totalSelectors) * 100,
            optimizationScore: Math.max(0, 100 - (unusedCount + duplicateCount) / totalSelectors * 100)
        };
    }

    // 💡 Generar recomendaciones específicas
    generateCSSRecommendations() {
        const metrics = this.calculateOptimizationMetrics();
        const recommendations = [];

        if (metrics.unusedPercentage > 20) {
            recommendations.push({
                type: 'cleanup',
                priority: 'high',
                message: `${metrics.unusedPercentage.toFixed(1)}% de selectores no utilizados`,
                solution: 'Eliminar selectores no utilizados para reducir bundle size',
                impact: 'Reducción estimada: ' + (metrics.estimatedSize * metrics.unusedPercentage / 100 / 1024).toFixed(1) + 'KB'
            });
        }

        if (metrics.duplicatePercentage > 10) {
            recommendations.push({
                type: 'deduplication',
                priority: 'medium',
                message: `${metrics.duplicatePercentage.toFixed(1)}% de reglas duplicadas`,
                solution: 'Consolidar reglas duplicadas y usar mixins/variables',
                impact: 'Mejor mantenibilidad y menor complejidad'
            });
        }

        if (metrics.v3AdoptionRate < 80) {
            recommendations.push({
                type: 'migration',
                priority: 'medium',
                message: `Solo ${metrics.v3AdoptionRate.toFixed(1)}% de componentes usan V3`,
                solution: 'Completar migración a componentes LINO V3',
                impact: 'Mejor consistencia y mantenibilidad'
            });
        }

        if (this.v3Coverage.inactiveComponents.length > 3) {
            recommendations.push({
                type: 'treeshaking',
                priority: 'low',
                message: `${this.v3Coverage.inactiveComponents.length} componentes V3 no utilizados`,
                solution: 'Implementar tree-shaking para eliminar CSS no utilizado',
                impact: 'Reducción de bundle size'
            });
        }

        return recommendations;
    }

    // 📊 Generar reporte completo
    generateReport() {
        const metrics = this.calculateOptimizationMetrics();
        const recommendations = this.generateCSSRecommendations();

        return {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            stylesheets: this.stylesheets.map(s => ({
                href: s.href,
                rulesCount: s.rulesCount,
                disabled: s.disabled
            })),
            metrics: metrics,
            v3Coverage: this.v3Coverage,
            recommendations: recommendations,
            topUnusedSelectors: this.unusedRules.slice(0, 10),
            topDuplicates: this.duplicateRules.slice(0, 5)
        };
    }

    // 🖨️ Imprimir reporte en consola
    printReport() {
        const report = this.generateReport();
        
        console.group('⚡ LINO CSS Bundle Analysis Report');
        console.log(`📅 Timestamp: ${report.timestamp}`);
        console.log(`🌐 URL: ${report.url}`);
        
        console.group('📊 CSS Metrics');
        console.table(report.metrics);
        console.groupEnd();
        
        console.group('🚀 LINO V3 Coverage');
        console.table(report.v3Coverage.components);
        console.log(`V3 Adoption Rate: ${report.v3Coverage.v3Ratio.toFixed(1)}%`);
        console.log(`Active Components: ${report.v3Coverage.activeComponents.join(', ')}`);
        if (report.v3Coverage.inactiveComponents.length > 0) {
            console.log(`Inactive Components: ${report.v3Coverage.inactiveComponents.join(', ')}`);
        }
        console.groupEnd();
        
        console.group('📄 Stylesheets');
        console.table(report.stylesheets);
        console.groupEnd();
        
        if (report.topUnusedSelectors.length > 0) {
            console.group('🚫 Top Unused Selectors');
            console.table(report.topUnusedSelectors.map(s => ({
                selector: s.selector,
                isLino: s.isLino,
                isV3: s.isV3
            })));
            console.groupEnd();
        }
        
        if (report.recommendations.length > 0) {
            console.group('💡 CSS Optimization Recommendations');
            report.recommendations.forEach((rec, index) => {
                console.log(`${index + 1}. [${rec.priority.toUpperCase()}] ${rec.message}`);
                console.log(`   💡 Solution: ${rec.solution}`);
                console.log(`   📈 Impact: ${rec.impact}`);
            });
            console.groupEnd();
        }
        
        console.groupEnd();
        
        return report;
    }
}

// 🌐 Exponer globalmente
window.LinoCSSAnalyzer = LinoCSSAnalyzer;

// 🚀 Comando rápido para análisis
window.runCSSAnalysis = async function() {
    const analyzer = new LinoCSSAnalyzer();
    // Esperar a que se complete la inicialización
    await new Promise(resolve => setTimeout(resolve, 500));
    return analyzer.printReport();
};
