from django.shortcuts import render, get_object_or_404
from .models import ServicePage, FAQ, CityData
from cities.models import City


def service_page(request, city_slug, service_slug, page_slug=None):
    city = get_object_or_404(City, slug=city_slug)

    # 🔹 Определяем страницу
    if page_slug:
        page = get_object_or_404(
            ServicePage.objects.select_related('parent'),
            city=city,
            parent__slug=service_slug,
            slug=page_slug,
            is_published=True
        )
        parent = page.parent
    else:
        page = get_object_or_404(
            ServicePage,
            city=city,
            slug=service_slug,
            parent__isnull=True,
            is_published=True
        )
        parent = page

    # 🔹 Подуслуги
    children = parent.children.filter(
        is_published=True,
        show_in_menu=True
    )

    # 🔹 Другие услуги
    related = ServicePage.objects.filter(
        city=city,
        parent__isnull=True,
        is_published=True
    ).exclude(id=parent.id)

    # 🔹 FAQ
    faqs = FAQ.objects.filter(city=city)[:5]

    # 🔹 SEO данные города
    city_data = CityData.objects.filter(city=city).first()

    # 🔹 Перелинковка городов
    other_cities = City.objects.filter(is_active=True).exclude(id=city.id)[:10]

    canonical_url = request.build_absolute_uri(request.path)

    return render(request, 'pages/service_page.html', {
        'page': page,
        'city': city,
        'parent': parent,
        'children': children,
        'related_services': related,
        'faqs': faqs,
        'city_data': city_data,
        'canonical_url': canonical_url,
        'other_cities': other_cities,
    })


def faq_page(request, city_slug, faq_slug):
    faq = get_object_or_404(
        FAQ,
        city__slug=city_slug,
        slug=faq_slug
    )

    return render(request, 'pages/faq_page.html', {
        'faq': faq,
        'city': faq.city,
    })