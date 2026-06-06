from .models import City


def all_cities(request):

    return {
        'all_cities': City.objects.filter(
            is_active=True
        ).order_by('name')
    }