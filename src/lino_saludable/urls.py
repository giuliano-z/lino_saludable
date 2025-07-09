from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gestion.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('gestion/', include('gestion.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalización del panel de administración
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Lino Administración')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Lino Administración')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Panel de Control')
