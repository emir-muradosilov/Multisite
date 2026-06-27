from cities.models import City
from .models import ServicePage


def seo_context(request):

    city = None

    path_parts = request.path.strip('/').split('/')

    if len(path_parts) >= 1 and path_parts[0]:

        city = City.objects.filter(
            slug=path_parts[0],
            is_active=True
        ).first()

    # если URL без города (/)
    if not city:

        city = City.objects.filter(
            is_main=True,
            is_active=True
        ).first()

    menu_services = []

    if city:

        menu_services = ServicePage.objects.filter(
            city=city,
            parent__isnull=True,
            is_published=True,
            show_in_menu=True
        ).prefetch_related(
            'children'
        ).order_by(
            'sort_order',
            'title'
        )

    return {
        'menu_city': city,
        'menu_services': menu_services,
    }

