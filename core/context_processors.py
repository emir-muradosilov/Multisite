from pages.models import ServicePage
from cities.models import City
from .models import SiteSettings
from tenants.models import TenantProfile
from django.core.exceptions import ObjectDoesNotExist

from core.models import WorkType


def menu_services(request):

    path_parts = request.path.strip('/').split('/')

    if not path_parts or not path_parts[0]:

        return {
            'menu_services': [],
            'menu_city': None,
            'city': None,
            'contacts': None,
        }

    city_slug = path_parts[0]

    try:

        city = City.objects.get(
            slug=city_slug,
            is_active=True
        )

    except City.DoesNotExist:

        return {
            'menu_services': [],
            'menu_city': None,
            'city': None,
            'contacts': None,
        }

    services = ServicePage.objects.filter(
        city=city,
        parent__isnull=True,
        is_published=True,
        show_in_menu=True
    ).prefetch_related(
        'children'
    )

    contacts = None

    try:

        tenant = city.tenant_profile

        if tenant.is_active:
            contacts = tenant

    except ObjectDoesNotExist:

        contacts = None

    return {
        'menu_services': services,
        'menu_city': city,
        'city': city,
        'contacts': contacts,
    }


def global_cities(request):

    return {
        'all_cities': City.objects.filter(
            is_active=True
        ).order_by('name')
    }


def site_settings(request):

    return {
        'site_settings': SiteSettings.load()
    }


def homepage_data(request):

    return {
        'work_types': WorkType.objects.filter(
            is_published=True
        )
    }


'''
def current_contacts(request):

    path_parts = request.path.strip('/').split('/')

    if not path_parts or not path_parts[0]:

        return {
            'contacts': None
        }

    city_slug = path_parts[0]

    city = City.objects.filter(
        slug=city_slug,
        is_active=True
    ).first()

    if not city:

        return {
            'contacts': None
        }

    tenant = TenantProfile.objects.filter(
        city=city,
        is_active=True
    ).first()

    return {
        'contacts': tenant
    }

'''

