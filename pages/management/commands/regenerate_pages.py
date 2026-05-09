from django.core.management.base import BaseCommand

from cities.models import City

from pages.models import (
    ServiceTemplate,
    ServicePage,
    CityData
)

import random


INTRO = [
    "Профессионально выполняем",
    "Оказываем услуги",
    "Выполняем работы"
]


class Command(BaseCommand):

    help = 'Regenerate all service pages'

    def handle(self, *args, **kwargs):

        templates = ServiceTemplate.objects.all()

        updated_count = 0

        for page in ServicePage.objects.all():

            template = templates.filter(
                slug=page.slug
            ).first()

            if not template:
                continue

            city = page.city

            city_data = CityData.objects.filter(
                city=city
            ).first()

            intro = random.choice(INTRO)

            title = template.title_template.format(
                city=city.name
            )

            seo_title = template.seo_title_template.format(
                city=city.name
            )

            seo_description = template.seo_description_template.format(
                city=city.name
            )

            seo_keywords = ''

            if template.seo_keywords_template:
                seo_keywords = template.seo_keywords_template.format(
                    city=city.name
                )

            content = f"""
{intro} {title.lower()}.

Мы работаем по всему городу, включая районы:
{city_data.districts if city_data else "все районы города"}.

Основные объекты:
{city_data.industrial_zones if city_data else "жилые и коммерческие здания"}.

Средняя стоимость:
{city_data.price_range if city_data else "рассчитывается индивидуально"}.
"""

            page.title = title
            page.content = content

            page.seo_title = seo_title
            page.seo_description = seo_description
            page.seo_keywords = seo_keywords

            page.save()

            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Обновлено страниц: {updated_count}'
            )
        )