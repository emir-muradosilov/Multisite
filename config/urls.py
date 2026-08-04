"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.contrib.sitemaps.views import sitemap
#from cities.sitemaps import CitySitemap
from .views import robots_txt
from pages.sitemaps import (
    StaticSitemap,
    CitySitemap,
    ServicePageSitemap,
    FAQSitemap,
)

from django.conf import settings
from django.conf.urls.static import static



sitemaps = {
    'static': StaticSitemap,
#    'cities': CitySitemap,
    'services': ServicePageSitemap,
    'faq': FAQSitemap,
}

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('tenants.urls')),
    
    path('', include('leads.urls')),

    path('', include('pages.urls')),
    path('', include('cities.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
