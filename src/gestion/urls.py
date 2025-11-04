from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Dashboard principal - ahora usa la versión inteligente verde
    path('', views.dashboard_inteligente, name='panel_control'),
    # Versiones alternativas del dashboard
    path('dashboard-original/', views.panel_control_original, name='panel_control_original'),
    path('dashboard-clean/', views.panel_control_clean, name='panel_control_clean'),
    path('dashboard-minimal/', views.panel_control_minimal, name='panel_control_minimal'),
    path('dashboard-inteligente/', views.dashboard_inteligente, name='dashboard_inteligente'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/exportar/', views.exportar_productos, name='exportar_productos'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta_v3, name='crear_venta'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/<int:pk>/eliminar/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/exportar/', views.exportar_ventas, name='exportar_ventas'),
    path('api/productos/<int:pk>/precio/', views.producto_precio, name='producto_precio'),
    # REPORTES - Vista enterprise unificada
    path('reportes/', views.reportes_lino, name='reportes'),
    path('gastos-inversiones/', views.gastos_inversiones, name='gastos_inversiones'),
    path('usuarios/', views.usuarios, name='usuarios'),
    # Demo de componentes - Solo para desarrollo
    path('demo/componentes/', views.demo_componentes, name='demo_componentes'),
    path('configuracion/', views.configuracion, name='configuracion'),
    # NUEVAS URLs - COMPRAS (Ahora principales)
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/crear/', views.crear_compra_v3, name='crear_compra'),
    path('compras/<int:pk>/', views.detalle_compra, name='detalle_compra'),
    path('compras/<int:pk>/eliminar/', views.eliminar_compra, name='eliminar_compra'),
    # NUEVAS URLs - MATERIAS PRIMAS (Ahora principales)
    path('materias-primas/', views.lista_materias_primas, name='lista_materias_primas'),
    path('materias-primas/crear/', views.crear_materia_prima, name='crear_materia_prima'),
    path('materias-primas/<int:pk>/editar/', views.editar_materia_prima, name='editar_materia_prima'),
    path('materias-primas/<int:pk>/detalle/', views.detalle_materia_prima, name='detalle_materia_prima'),
    path('materias-primas/<int:pk>/movimiento/', views.movimiento_materia_prima, name='movimiento_materia_prima'),
    # NUEVAS URLs - RECETAS
    path('recetas/', views.lista_recetas, name='lista_recetas'),
    path('recetas/crear/', views.crear_receta_v3, name='crear_receta'),
    path('recetas/<int:pk>/', views.detalle_receta, name='detalle_receta'),
    path('recetas/<int:pk>/editar/', views.editar_receta, name='editar_receta'),
    path('recetas/<int:pk>/eliminar/', views.eliminar_receta, name='eliminar_receta'),
    # NUEVAS URLs - VENTAS AVANZADAS
    path('ventas/con-materias/', views.crear_venta_con_materias, name='crear_venta_con_materias'),
    # NUEVAS URLs - REPORTES AVANZADOS
    path('reportes/stock-materias-primas/', views.reporte_stock_materias_primas, name='reporte_stock_materias_primas'),
    path('reportes/costos-produccion/', views.reporte_costos_produccion, name='reporte_costos_produccion'),
    # NUEVAS URLs - EXPORTACIÓN
    path('exportar/materias-primas/excel/', views.exportar_materias_primas_excel, name='exportar_materias_primas_excel'),
    path('exportar/reporte/<str:tipo_reporte>/pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),
    # NUEVAS URLs - API
    path('api/verificar-stock/<int:producto_id>/', views.api_verificar_stock_producto, name='api_verificar_stock_producto'),
    path('api/receta/<int:pk>/costo/', views.api_costo_receta, name='api_costo_receta'),
    # APIs para sincronización LINO V3
    path('api/productos/', views.api_productos, name='api_productos'),
    path('api/inventario/', views.api_inventario, name='api_inventario'), 
    path('api/ventas/', views.api_ventas, name='api_ventas'),
    
    # NUEVAS URLs - CONTROL DE RENTABILIDAD Y ANALYTICS
    path('rentabilidad/', views.dashboard_rentabilidad, name='dashboard_rentabilidad'),
    path('rentabilidad/producto/<int:producto_id>/', views.detalle_rentabilidad_producto, name='detalle_rentabilidad_producto'),
    path('api/alertas-rentabilidad/', views.alertas_rentabilidad_ajax, name='alertas_rentabilidad_ajax'),
    path('api/recomendaciones-precios/', views.recomendaciones_precios_ajax, name='recomendaciones_precios_ajax'),
    path('api/aplicar-precio/<int:producto_id>/', views.aplicar_precio_sugerido, name='aplicar_precio_sugerido'),
    
    # NUEVAS URLs - VISTAS MIGRADAS AL SISTEMA LINO (OPCIONALES)
    path('productos/lino/', views.lista_productos_lino, name='lista_productos_lino'),
    path('ventas/lino/', views.lista_ventas_lino, name='lista_ventas_lino'),
    # path('materias-primas/lino/', views.lista_materias_primas_lino, name='lista_materias_primas_lino'),  # OBSOLETA - usar lista_materias_primas
    path('compras/lino/', views.lista_compras_lino, name='lista_compras_lino'),
    # Vista de inventario optimizada
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    
    # ============================================
    # FASE 3: SISTEMA DE ALERTAS UI
    # ============================================
    # API Endpoints
    path('api/alertas/count/', views.alertas_count_api, name='alertas_count'),
    path('api/alertas/no-leidas/', views.alertas_no_leidas_api, name='alertas_no_leidas'),
    path('api/alertas/<int:alerta_id>/marcar-leida/', views.marcar_alerta_leida, name='marcar_alerta_leida'),
    
    # UI Endpoints
    path('alertas/', views.alertas_lista, name='alertas_lista'),
]