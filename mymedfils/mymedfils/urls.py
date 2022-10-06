"""mymedfils URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
}



handler404 = 'ecommerce.views.handler404'
""" handler400 = 'ecommerce.views.bad_request'
handler403 = 'ecommerce.views.permission_denied'
handler500 = 'ecommerce.views.server_error' """

admin.site.site_header = "Medfils Admin"
admin.site.site_title = "Medfils Admin Portal"
admin.site.index_title = "Welcome to Medfils"


urlpatterns = [
    path('', include('ecommerce.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('consultation/', include('consultation.urls')),
    path('products/', include('products.urls')),
    path('exercise/', include('exercise.urls')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
