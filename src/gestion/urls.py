from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('api/productos/<int:pk>/', views.producto_precio, name='api_producto_precio'),
]
