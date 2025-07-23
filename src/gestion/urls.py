from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/exportar/', views.exportar_productos, name='exportar_productos'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/<int:pk>/eliminar/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/exportar/', views.exportar_ventas, name='exportar_ventas'),
    path('api/productos/<int:pk>/precio/', views.producto_precio, name='producto_precio'),
    path('reportes/', views.reportes, name='reportes'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('reportes/', views.reportes, name='reportes'),
]