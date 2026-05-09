from pages.models import ServicePage
from cities.models import City


def menu_services(request):
    path_parts = request.path.strip('/').split('/')

    if not path_parts or not path_parts[0]:
        return {}

    city_slug = path_parts[0]

    try:
        city = City.objects.get(slug=city_slug)
    except City.DoesNotExist:
        return {}

    services = ServicePage.objects.filter(
        city=city,
        parent__isnull=True,
        is_published=True,
        show_in_menu=True
    ).prefetch_related('children')

    return {
        'menu_services': services,
        'menu_city': city
    }