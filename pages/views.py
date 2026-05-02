from django.shortcuts import render, get_object_or_404

from .models import ServicePage
from .models import FAQ
from cities.models import City

def service_page(request, city_slug, page_slug):
    page = get_object_or_404(
        ServicePage,
        city__slug=city_slug,
        slug=page_slug
    )
    canonical_url = request.build_absolute_uri(request.path)

    return render(request, 'pages/service_page.html', {
        'page': page,
        'canonical_url':canonical_url,
    })

def faq_page(request, city_slug, faq_slug):
    faq = get_object_or_404(
        FAQ,
        city__slug=city_slug,
        slug=faq_slug
    )

    canonical_url = request.build_absolute_uri(request.path)

    return render(request, 'pages/faq_page.html', {
        'faq': faq,
        'canonical_url': canonical_url
    })

def city_home(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)

    return render(request, 'pages/city_home.html', {
        'city': city
    })