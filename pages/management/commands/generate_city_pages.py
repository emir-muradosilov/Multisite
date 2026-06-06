from django.core.management.base import BaseCommand

from cities.models import City

from pages.models import (
    ServiceTemplate,
    ServicePage,
    FAQTemplate,
    FAQ,
)

from pages.models import CityData
from pages.utils import spin_text


class Command(BaseCommand):

    help = 'Generate service pages and FAQ for all cities'

    def handle(self, *args, **kwargs):

        cities = City.objects.all()

        parent_templates = ServiceTemplate.objects.filter(
            parent__isnull=True
        ).order_by('sort_order')

        created_pages = 0
        created_faq = 0

        for city in cities:

            created_parents = {}

            # =====================================
            # PARENT PAGES
            # =====================================

            for template in parent_templates:

                page = self.create_page(
                    city=city,
                    template=template,
                    parent=None
                )

                if page:
                    created_pages += 1
                    created_parents[template.id] = page

            # =====================================
            # CHILD PAGES
            # =====================================

            child_templates = ServiceTemplate.objects.filter(
                parent__isnull=False
            ).order_by('sort_order')

            for template in child_templates:

                parent_page = created_parents.get(
                    template.parent.id
                )

                if not parent_page:
                    continue

                page = self.create_page(
                    city=city,
                    template=template,
                    parent=parent_page
                )

                if page:
                    created_pages += 1

            # =====================================
            # FAQ
            # =====================================

            faq_templates = FAQTemplate.objects.all()

            for template in faq_templates:

                faq = self.create_faq(
                    city=city,
                    template=template
                )

                if faq:
                    created_faq += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDONE.\n'
                f'Created pages: {created_pages}\n'
                f'Created FAQ: {created_faq}'
            )
        )

    # =====================================
    # CREATE PAGE
    # =====================================

    def create_page(self, city, template, parent=None):

        exists = ServicePage.objects.filter(
            city=city,
            parent=parent,
            slug=template.slug
        ).exists()

        if exists:
            return None

        title = template.title_template.format(
            city=city.name
        )

        h1 = template.h1_template.format(
            city=city.name
        )

        seo_title = template.seo_title_template.format(
            city=city.name
        )

        seo_description = template.seo_description_template.format(
            city=city.name
        )

        seo_keywords = template.seo_keywords_template.format(
            city=city.name
        )

        city_data = CityData.objects.filter(city=city.first())
        
        content = spin_text(template.content_template).format(
            city=city.name,
            districts=city_data.districts if city_data else '',
            industrial_zones=city_data.industrial_zones if city_data else '',
            typical_concrete=city_data.typical_concrete if city_data else '',
            typical_thickness=city_data.typical_thickness if city_data else '',
            price_range=city_data.price_range if city_data else '',
        )

        page = ServicePage.objects.create(
            city=city,
            parent=parent,
            title=title,
            slug=template.slug,
            h1_title=h1,
            content=content,
            seo_title=seo_title,
            seo_description=seo_description,
            seo_keywords=seo_keywords,
            is_published=True,
            show_in_menu=template.show_in_menu,
            is_main=template.is_main,
            sort_order=template.sort_order,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Created page: {page.title}'
            )
        )

        return page

    # =====================================
    # CREATE FAQ
    # =====================================

    def create_faq(self, city, template):

        exists = FAQ.objects.filter(
            city=city,
            slug=template.slug
        ).exists()

        if exists:
            return None

        question = template.question_template.format(
            city=city.name
        )

        answer = spin_text(template.answer_template).format(
            city=city.name
        )

        faq = FAQ.objects.create(
            city=city,
            question=question,
            slug=template.slug,
            answer=answer,
            seo_title=question,
            seo_description=answer[:160],
            seo_keywords=f"{question}, {city.name}",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Created FAQ: {faq.question}'
            )
        )

        return faq