from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cities.models import City
from .models import ServicePage, FAQ


# =========================
# ГОРОДА
# =========================

class CitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return City.objects.filter(is_published=True)

    def location(self, obj):
        return f"/{obj.slug}/"


# =========================
# СТРАНИЦЫ УСЛУГ
# =========================

class ServicePageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ServicePage.objects.filter(
            is_published=True
        ).select_related(
            "city",
            "parent"
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):

        if obj.parent:
            return (
                f"/{obj.city.slug}/"
                f"{obj.parent.slug}/"
                f"{obj.slug}/"
            )

        return (
            f"/{obj.city.slug}/"
            f"{obj.slug}/"
        )


# =========================
# FAQ
# =========================

class FAQSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return FAQ.objects.filter(
            is_published=True
        ).select_related("city")

    def location(self, obj):
        return f"/{obj.city.slug}/faq/{obj.slug}/"