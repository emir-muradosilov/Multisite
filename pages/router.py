from django.http import Http404

from cities.models import City

from .views import (
    service_page,
    city_home,
)


SYSTEM_SLUGS = {
    "faq",
    "cases",
    "districts",
    "admin",
    "media",
    "static",
}


def resolve_one_level(request, slug):

    if slug in SYSTEM_SLUGS:
        raise Http404()

    city = City.objects.filter(
        slug=slug,
        is_active=True,
    ).first()

    if city:

        return city_home(
            request,
            city_slug=slug,
        )

    return service_page(
        request,
        service_slug=slug,
    )


def resolve_two_levels(
    request,
    first,
    second,
):
    print("resolve_two_levels:", first, second)
    if first in SYSTEM_SLUGS:
        raise Http404()

    city = City.objects.filter(
        slug=first,
        is_active=True,
    ).first()

    if city:

        return service_page(
            request,
            city_slug=first,
            service_slug=second,
        )

    return service_page(
        request,
        service_slug=first,
        page_slug=second,
    )



def resolve_three_levels(
    request,
    first,
    second,
    third,
):
    if first in SYSTEM_SLUGS:
        raise Http404()

    city = City.objects.filter(
        slug=first,
        is_active=True,
    ).first()

    # /krasnodar/almaznoe-burenie/podstranica/
    if city:

        return service_page(
            request,
            city_slug=first,
            service_slug=second,
            page_slug=third,
        )

    # На будущее.
    # Если позже появятся URL вида:
    # /service/category/page/
    raise Http404()

