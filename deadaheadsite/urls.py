"""deadaheadsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', include('deadahead_app.urls')),
    path('admin/', admin.site.urls),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^tests/400/$', TemplateView.as_view(template_name='400.html'), name='test404'),
        url(r'^tests/403/$', TemplateView.as_view(template_name='403.html'), name='test404'),
        url(r'^tests/404/$', TemplateView.as_view(template_name='404.html'), name='test404'),
        url(r'^tests/500/$', TemplateView.as_view(template_name='500.html'), name='test404'),
    ]