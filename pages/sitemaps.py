from django.contrib.sitemaps import Sitemap
from .models import ServicePage, FAQ


class ServicePageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ServicePage.objects.filter(is_published=True)

    def location(self, obj):
        if obj.parent:
            return f"/{obj.city.slug}/{obj.parent.slug}/{obj.slug}/"
        return f"/{obj.city.slug}/{obj.slug}/"


class FAQSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return FAQ.objects.all()

    def location(self, obj):
        return f"/{obj.city.slug}/faq/{obj.slug}/"