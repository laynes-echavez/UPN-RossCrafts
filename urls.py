"""
URL configuration for ross_crafts project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('stock/', include('apps.stock.urls')),
    path('', include('apps.customers.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('', include('apps.sales.urls')),
    path('reports/', include('apps.reports.urls')),
    path('dashboard/auditoria/', include('apps.audit.urls')),  # Auditoría
    path('', include('apps.payments.urls')),  # Checkout en raíz
    path('', include('apps.ecommerce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
