from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cities.models import City
from .models import ServicePage, FAQ
from pages.services.page_quality import calculate_page_score
from .models import DistrictServicePage

# =========================
# ГОРОДА
# =========================

class CitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        pages = DistrictServicePage.objects.filter(is_published=True )
        valid_pages = []
        for page in pages:
            score = calculate_page_score(
                page.service_page,
                {
                    'faqs': [],
                    'reviews': [],
                    'portfolio_cases': [],
                    'seo_blocks': [],
                    'children': [],
                    'city_data': True,
                }
            )
            if score >= 70:
                valid_pages.append(page)
        return valid_pages


    def location(self, obj):
        return f"/{obj.slug}/"


# =========================
# СТРАНИЦЫ УСЛУГ
# =========================

class ServicePageSitemap(Sitemap):

    changefreq = "weekly"

    def items(self):

        pages = ServicePage.objects.filter(
            is_published=True
        ).select_related(
            "city",
            "parent"
        )

        valid_pages = []

        for page in pages:

            score = calculate_page_score(
                page,
                {
                    'faqs': [],
                    'reviews': [],
                    'portfolio_cases': [],
                    'seo_blocks': [],
                    'children': [],
                    'city_data': True,
                }
            )

            if score >= 40:
                valid_pages.append(page)

        return valid_pages

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):

        # MAIN PAGES
        if obj.is_main:
            return 1.0

        # PARENT
        if obj.parent is None:
            return 0.9

        # CHILD
        return 0.7


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


class StaticSitemap(Sitemap):

    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class DistrictPageSitemap(Sitemap):

    changefreq = "monthly"

    priority = 0.6

    def items(self):

        return DistrictServicePage.objects.filter(
            is_published=True
        ).select_related(
            'city',
            'district',
            'service_page'
        )

    def location(self, obj):

        return obj.get_absolute_url()

