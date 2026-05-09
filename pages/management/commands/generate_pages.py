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

    help = 'Generate service pages for all cities'

    def handle(self, *args, **kwargs):

        templates = ServiceTemplate.objects.all()
        cities = City.objects.all()

        created_count = 0

        for city in cities:

            city_data = CityData.objects.filter(city=city).first()

            for template in templates:

                if ServicePage.objects.filter(
                    city=city,
                    slug=template.slug,
                    parent__isnull=True
                ).exists():
                    continue

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

                ServicePage.objects.create(
                    city=city,

                    title=title,

                    slug=template.slug,

                    content=content,

                    seo_title=seo_title,

                    seo_description=seo_description,

                    seo_keywords=seo_keywords,
                )

                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано страниц: {created_count}'
            )
        )