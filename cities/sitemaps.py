from django.contrib.sitemaps import Sitemap
from .models import City


class CitySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return City.objects.filter(is_active=True)

    def location(self, obj):
        return f'/{obj.slug}/'