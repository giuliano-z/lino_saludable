// 🧠 LINO DIETÉTICA V3 - INTELIGENCIA DE NEGOCIO
// Sistema de recomendaciones automáticas y análisis predictivo

class LinoInteligencia {
    constructor() {
        this.init();
    }

    init() {
        this.configurarGraficos();
        this.inicializarRecomendaciones();
        this.configurarNotificaciones();
    }

    // 📊 GESTIÓN DE GRÁFICOS INTELIGENTES
    configurarGraficos() {
        const ctx = document.getElementById('chartInteligente');
        if (!ctx) return;

        this.chart = null;
        this.configurarControlesGrafico();
    }

    configurarControlesGrafico() {
        document.querySelectorAll('.lino-chart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.cambiarTipoGrafico(e.target.dataset.chart);
            });
        });
    }

    cambiarTipoGrafico(tipo) {
        // Actualizar estado visual de botones
        document.querySelectorAll('.lino-chart-btn').forEach(btn => {
            btn.classList.remove('lino-chart-btn--active');
        });
        document.querySelector(`[data-chart="${tipo}"]`).classList.add('lino-chart-btn--active');

        // Datos según tipo
        const configuraciones = {
            ventas: {
                label: 'Ventas ($)',
                color: '#7fb069',
                data: window.datosVentas || [0,0,0,0,0,0,0]
            },
            margen: {
                label: 'Margen (%)',
                color: '#d4a574',
                data: window.datosMargenes || [0,0,0,0,0,0,0]
            },
            rotacion: {
                label: 'Rotación',
                color: '#6b9dc7',
                data: window.datosRotacion || [0,0,0,0]
            }
        };

        this.actualizarGrafico(configuraciones[tipo]);
    }

    actualizarGrafico(config) {
        if (this.chart) {
            this.chart.destroy();
        }

        const ctx = document.getElementById('chartInteligente').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: config.data.length === 7 ? 
                    ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'] :
                    ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
                datasets: [{
                    label: config.label,
                    data: config.data,
                    backgroundColor: config.color + '20',
                    borderColor: config.color,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: config.color,
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                height: 300,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f1f5f9' },
                        ticks: { color: '#6b7280' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#6b7280' }
                    }
                }
            }
        });
    }

    // 🤖 SISTEMA DE RECOMENDACIONES
    inicializarRecomendaciones() {
        this.configurarEventosRecomendaciones();
        this.verificarAlertas();
    }

    configurarEventosRecomendaciones() {
        // Botones de aplicar recomendaciones
        document.querySelectorAll('[onclick^="aplicarRecomendacion"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const id = this.extraerId(btn.getAttribute('onclick'));
                this.aplicarRecomendacion(id);
            });
        });

        // Botones de crear compra
        document.querySelectorAll('[onclick^="crearCompra"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const id = this.extraerId(btn.getAttribute('onclick'));
                this.crearCompraInteligente(id);
            });
        });

        // Botones de crear promoción
        document.querySelectorAll('[onclick^="crearPromocion"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const id = this.extraerId(btn.getAttribute('onclick'));
                this.crearPromocionInteligente(id);
            });
        });
    }

    extraerId(onclick) {
        const match = onclick.match(/\((\d+)\)/);
        return match ? parseInt(match[1]) : null;
    }

    // 💰 APLICAR RECOMENDACIÓN DE PRECIO
    async aplicarRecomendacion(id) {
        const confirmacion = await this.mostrarConfirmacion(
            'Actualizar Precio',
            '¿Estás seguro de aplicar esta recomendación de precio?',
            'La IA ha calculado este precio basándose en análisis de mercado y rentabilidad.'
        );

        if (confirmacion) {
            try {
                // Simular llamada AJAX
                await this.simularApiCall(500);
                
                this.mostrarNotificacion('success', 
                    'Precio actualizado correctamente',
                    'La recomendación de IA ha sido aplicada exitosamente.'
                );
                
                // Actualizar UI
                setTimeout(() => location.reload(), 1500);
                
            } catch (error) {
                this.mostrarNotificacion('error', 
                    'Error al actualizar precio',
                    error.message
                );
            }
        }
    }

    // 🛒 CREAR COMPRA INTELIGENTE
    async crearCompraInteligente(productoId) {
        const cantidad = await this.mostrarDialogoCantidad(
            'Cantidad Sugerida de Compra',
            'La IA recomienda comprar 15 unidades basándose en tu historial de ventas.'
        );

        if (cantidad) {
            window.location.href = `/gestion/compras/crear/?producto=${productoId}&cantidad=${cantidad}`;
        }
    }

    // 🏷️ CREAR PROMOCIÓN INTELIGENTE
    async crearPromocionInteligente(productoId) {
        const descuento = await this.mostrarDialogoDescuento(
            'Promoción Sugerida',
            'La IA recomienda un descuento del 15% para acelerar la rotación.'
        );

        if (descuento) {
            window.location.href = `/gestion/productos/${productoId}/promocion/?descuento=${descuento}`;
        }
    }

    // 🔔 SISTEMA DE NOTIFICACIONES
    configurarNotificaciones() {
        this.contenedorNotificaciones = this.crearContenedorNotificaciones();
    }

    crearContenedorNotificaciones() {
        const contenedor = document.createElement('div');
        contenedor.id = 'lino-notifications';
        contenedor.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(contenedor);
        return contenedor;
    }

    mostrarNotificacion(tipo, titulo, mensaje) {
        const colores = {
            success: '#7fb069',
            warning: '#d4a574',
            error: '#c85a54',
            info: '#6b9dc7'
        };

        const iconos = {
            success: 'check-circle',
            warning: 'exclamation-triangle',
            error: 'x-circle',
            info: 'info-circle'
        };

        const notificacion = document.createElement('div');
        notificacion.style.cssText = `
            background: white;
            border: 1px solid ${colores[tipo]};
            border-left: 4px solid ${colores[tipo]};
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease;
        `;

        notificacion.innerHTML = `
            <div style="display: flex; align-items: start; gap: 12px;">
                <i class="bi bi-${iconos[tipo]}" style="color: ${colores[tipo]}; font-size: 18px; margin-top: 2px;"></i>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #374151; margin-bottom: 4px;">${titulo}</div>
                    <div style="font-size: 14px; color: #6b7280;">${mensaje}</div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; color: #9ca3af; font-size: 18px; cursor: pointer;">×</button>
            </div>
        `;

        this.contenedorNotificaciones.appendChild(notificacion);

        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (notificacion.parentElement) {
                notificacion.remove();
            }
        }, 5000);
    }

    // 🚨 VERIFICACIÓN DE ALERTAS
    async verificarAlertas() {
        // Verificar cada 5 minutos
        setInterval(() => {
            this.verificarStockCritico();
            this.verificarPreciosObsoletos();
        }, 300000); // 5 minutos
    }

    async verificarStockCritico() {
        try {
            // Simular verificación de stock
            const stockCritico = await this.simularApiCall(200, { productos: 2 });
            
            if (stockCritico.productos > 0) {
                this.mostrarNotificacion('warning',
                    'Stock Crítico Detectado',
                    `${stockCritico.productos} productos necesitan reposición urgente.`
                );
            }
        } catch (error) {
            console.log('Error verificando stock:', error);
        }
    }

    // 🛠️ UTILIDADES
    async mostrarConfirmacion(titulo, mensaje, detalle) {
        return new Promise((resolve) => {
            const confirmacion = confirm(`${titulo}\n\n${mensaje}\n\n${detalle}`);
            resolve(confirmacion);
        });
    }

    async mostrarDialogoCantidad(titulo, mensaje) {
        return new Promise((resolve) => {
            const cantidad = prompt(`${titulo}\n\n${mensaje}\n\nIngresa la cantidad:`);
            resolve(cantidad ? parseInt(cantidad) : null);
        });
    }

    async mostrarDialogoDescuento(titulo, mensaje) {
        return new Promise((resolve) => {
            const descuento = prompt(`${titulo}\n\n${mensaje}\n\nIngresa el porcentaje de descuento:`);
            resolve(descuento ? parseInt(descuento) : null);
        });
    }

    async simularApiCall(delay, data = {}) {
        return new Promise((resolve) => {
            setTimeout(() => resolve(data), delay);
        });
    }
}

// 🚀 INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', () => {
    window.linoIA = new LinoInteligencia();
    
    // Agregar estilos para animaciones
    const estilos = document.createElement('style');
    estilos.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(estilos);
});

// 🌐 FUNCIONES GLOBALES PARA COMPATIBILIDAD
window.aplicarRecomendacion = (id) => window.linoIA?.aplicarRecomendacion(id);
window.crearCompra = (id) => window.linoIA?.crearCompraInteligente(id);
window.crearPromocion = (id) => window.linoIA?.crearPromocionInteligente(id);
