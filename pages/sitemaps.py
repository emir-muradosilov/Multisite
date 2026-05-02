from django.contrib.sitemaps import Sitemap
from .models import ServicePage


class ServicePageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ServicePage.objects.all()

    def location(self, obj):
        return f'/{obj.city.slug}/{obj.slug}/'