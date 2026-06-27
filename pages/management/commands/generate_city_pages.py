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

        # =====================================
        # ЗАМЕНА ПЕРЕМЕННЫХ
        # =====================================

        def render_text(text):

            if not text:
                return ''

            return (
                text
                .replace('{{ city.name }}', city.name)
                .replace('{{ city.in_city }}', city.in_city)
                .replace('{{ city.oblast }}', city.oblast)
                .replace('{{ city.in_oblast }}', city.in_oblast)
            )

        title = render_text(
            template.title_template
        )

        h1 = render_text(
            template.h1_template
        )

        seo_title = render_text(
            template.seo_title_template
        )

        seo_description = render_text(
            template.seo_description_template
        )

        seo_keywords = render_text(
            template.seo_keywords_template
        )

        city_data = CityData.objects.filter(
            city=city
        ).first()

        content = render_text(
            spin_text(
                template.content_template
            )
        )

        if city_data:

            content = content.format(
                districts=city_data.districts or '',
                industrial_zones=city_data.industrial_zones or '',
                typical_concrete=city_data.typical_concrete or '',
                typical_thickness=city_data.typical_thickness or '',
                price_range=city_data.price_range or '',
            )

        page = ServicePage.objects.create(
            city=city,
            template=template,
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

        def render_text(text):

            if not text:
                return ''
            
            return (
                text
                .replace('{{ city.name }}', city.name)
                .replace('{{ city.in_city }}', city.in_city)
                .replace('{{ city.oblast }}', city.oblast)
                .replace('{{ city.in_oblast }}', city.in_oblast)
            )

        question = render_text(
            template.question_template
        )

        answer = render_text(
            spin_text(
                template.answer_template
            )
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

        # =====================================
        # СВЯЗЫВАЕМ FAQ С УСЛУГАМИ
        # =====================================

        for service_template in template.related_service_templates.all():

            service_page = ServicePage.objects.filter(
                city=city,
                template=service_template,
                is_published=True
            ).first()

            if service_page:
                faq.related_services.add(service_page)

        self.stdout.write(
            self.style.SUCCESS(
                f'Created FAQ: {faq.question}'
            )
        )

        return faq