from django.core.management.base import BaseCommand

from cities.models import City
from pages.models import District

from slugify import slugify

import json
import os


class Command(BaseCommand):

    help = 'Import districts from local JSON files'

    def handle(self, *args, **kwargs):

        cities = City.objects.filter(
            is_active=True
        )

        total_created = 0

        for city in cities:

            filename = (
                f"data/districts/"
                f"{city.slug}.json"
            )

            if not os.path.exists(filename):

                self.stdout.write(
                    self.style.ERROR(
                        f'FILE NOT FOUND: {filename}'
                    )
                )

                continue

            self.stdout.write(
                self.style.WARNING(
                    f'\nIMPORTING: {city.name}'
                )
            )

            with open(
                filename,
                'r',
                encoding='utf-8'
            ) as f:

                districts = json.load(f)

            created = 0

            for district_name in districts:

                slug = slugify(district_name)

                exists = District.objects.filter(
                    city=city,
                    slug=slug
                ).exists()

                if exists:
                    continue

                District.objects.create(
                    city=city,
                    name=district_name,
                    slug=slug,
                    description=(
                        f'Район {district_name} '
                        f'в городе {city.name}'
                    )
                )

                created += 1
                total_created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created: {district_name}'
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Imported: {created}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDONE. Total created: {total_created}'
            )
        )