from django.urls import path
from django.contrib.sitemaps.views import sitemap

from pages.sitemaps import ServicePageSitemap, FAQSitemap
from .views import robots_txt

# ✅ ОБЯЗАТЕЛЬНО сначала объявить
urlpatterns = []

sitemaps = {
    'services': ServicePageSitemap,
    'faq': FAQSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', robots_txt),
]