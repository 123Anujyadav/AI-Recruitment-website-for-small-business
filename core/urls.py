from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    # Custom Admin Panel — served at /admin-panel/
    path('admin-panel/', TemplateView.as_view(template_name='admin.html')),
    path('admin-panel/api/', include('jobs.admin_urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]
