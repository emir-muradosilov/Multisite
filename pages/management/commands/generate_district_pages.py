from django.core.management.base import BaseCommand

from cities.models import City

from pages.models import (
    District,
    DistrictServicePage,
    DistrictPageTemplate,
    ServicePage,
)


class Command(BaseCommand):

    help = 'Generate district service pages'

    def handle(self, *args, **kwargs):

        created = 0

        districts = District.objects.select_related(
            'city'
        )

        templates = DistrictPageTemplate.objects.filter(
            is_active=True
        ).select_related(
            'service_template'
        )

        for district in districts:

            city = district.city

            for template in templates:

                parent_page = ServicePage.objects.filter(
                    city=city,
                    slug=template.service_template.slug,
                    parent__isnull=True,
                    is_published=True
                ).first()

                if not parent_page:
                    continue

                exists = DistrictServicePage.objects.filter(
                    district=district,
                    service_page=parent_page
                ).exists()

                if exists:
                    continue

                title = template.title_template.format(
                    city=city.name,
                    district=district.name
                )

                seo_title = (
                    template.seo_title_template.format(
                        city=city.name,
                        district=district.name
                    )
                )

                seo_description = (
                    template.seo_description_template.format(
                        city=city.name,
                        district=district.name
                    )
                )

                content = (
                    template.content_template.format(
                        city=city.name,
                        district=district.name
                    )
                )

                page = DistrictServicePage.objects.create(
                    city=city,
                    district=district,
                    service_page=parent_page,
                    seo_title=seo_title,
                    seo_description=seo_description,
                    content=content,
                    is_published=True
                )

                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created: {title}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDONE: {created}'
            )
        )