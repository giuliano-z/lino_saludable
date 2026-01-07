from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gestion.views import index
# Importar funciones API para LINO V3
from gestion.api import api_productos, api_inventario, api_ventas
# ⚠️  TEMPORAL: Vista para reset de producción
from gestion.views_reset_temp import reset_database_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('gestion/', include('gestion.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # APIs LINO V3 - Endpoints para sincronización
    path('api/productos/', api_productos, name='api_productos'),
    path('api/inventario/', api_inventario, name='api_inventario'),
    path('api/ventas/', api_ventas, name='api_ventas'),
    # ⚠️  TEMPORAL: Endpoint para resetear base de datos
    path('__reset_db_temp__/', reset_database_view, name='reset_db_temp'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalización del panel de administración
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Lino Administración')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Lino Administración')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Panel de Control')
