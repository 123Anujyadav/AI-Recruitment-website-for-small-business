from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    # Custom Admin Panel — served at /admin-panel/
    path('admin-panel/', TemplateView.as_view(template_name='admin.html')),
    path('admin-panel/api/', include('jobs.admin_urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
