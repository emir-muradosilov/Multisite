from django.shortcuts import render, get_object_or_404
from cities.models import City
from django.http import Http404

from .models import (
    ServicePage,
    FAQ,
    CityData,
    SEOBlock,
    PortfolioCase,
    Review,
    DistrictServicePage,
    FAQTemplate,
    GlobalFAQ
)

from pages.services.internal_linking import get_related_pages
from pages.services.faq_generator import generate_faqs
from pages.services.page_sections import build_page_sections, get_random_cta
from pages.services.page_quality import calculate_page_score
from pages.services.canonical import get_canonical_url
from pages.services.contacts import get_city_contacts
from pages.services.indexing import get_indexing_data

from core.models import SiteSettings
from cities.views import city_home


# =====================================================
# SERVICE PAGE
# =====================================================

def service_page(
    request,
    service_slug=None,
    city_slug=None,
    page_slug=None,
):
    print(
        f"city_slug={city_slug}",
        f"service_slug={service_slug}",
        f"page_slug={page_slug}",
    )
    # =====================================================
    # CITY
    # =====================================================

    if city_slug:

        city = get_object_or_404(
            City,
            slug=city_slug,
            is_active=True,
        )

    else:

        city = get_object_or_404(
            City,
            is_main=True,
            is_active=True,
        )
    if service_slug is None:
        raise Http404("Service slug is required.")

    # =====================================================
    # ГЛАВНАЯ СТРАНИЦА ГОРОДА
    # =====================================================

    
    # =====================================================
    # ПОДСТРАНИЦА
    # =====================================================

    if page_slug:

        page = get_object_or_404(
            ServicePage.objects.select_related(
                "parent",
                "city",
            ),
            city=city,
            parent__slug=service_slug,
            slug=page_slug,
            is_published=True,
        )

        parent = page.parent

    # =====================================================
    # РОДИТЕЛЬСКАЯ УСЛУГА
    # =====================================================

    else:

        page = get_object_or_404(
            ServicePage.objects.select_related("city"),
            city=city,
            slug=service_slug,
            parent__isnull=True,
            is_published=True,
        )

        parent = page

    # =====================================================
    # CHILDREN
    # =====================================================

    children = parent.children.filter(
        is_published=True,
        show_in_menu=True
    ).order_by(
        'sort_order',
        'title'
    )

    # =====================================================
    # RELATED SERVICES
    # =====================================================

    related_services = get_related_pages(
        page=page,
        city=city
    )

    # =====================================================
    # FAQ
    # =====================================================
    main_city = City.objects.get(
        is_main=True,
        is_active=True,
    )

    faqs = (
        FAQ.objects.filter(
            city=main_city,
            related_services__template=parent.template,
            is_published=True,
        )
        .distinct()[:8]
    )

    generated_faqs = generate_faqs(
        page,
        city,
    )

    if not faqs.exists():

        faqs = FAQ.objects.filter(
            city=main_city,
            is_published=True,
        )[:8]

    # чтобы ссылки строились для текущего города
    for faq in faqs:
        faq._current_city = city


    # =====================================================
    # CITY DATA
    # =====================================================

    city_data = CityData.objects.filter(
        city=city
    ).first()

    # =====================================================
    # OTHER CITIES
    # =====================================================

    other_cities = City.objects.filter(
        is_active=True
    ).exclude(
        id=city.id
    )[:12]

    # =====================================================
    # SEO CLUSTER
    # =====================================================

    seo_cluster = ServicePage.objects.filter(
        city=city,
        parent__isnull=True,
        is_published=True
    ).exclude(
        id=parent.id
    ).order_by(
        'sort_order'
    )[:8]

    # =====================================================
    # SEO BLOCKS
    # =====================================================

    seo_blocks = SEOBlock.objects.filter(
        is_active=True
    ).filter(
        cities=city
    ).distinct().order_by(
        'sort_order'
    )


    # =====================================================
    # Отзывы клиентов

    reviews = Review.objects.filter(is_published=True)
    service_reviews = reviews.filter(related_services=parent).distinct()

    if not service_reviews.exists():
        service_reviews = reviews.filter(city=city)
    if not service_reviews.exists():
        service_reviews = reviews.all()
    service_reviews = service_reviews[:2]

    # =====================================================
    # PORTFOLIO CASES
    # =====================================================

    portfolio_cases = PortfolioCase.objects.filter(
        is_published=True
    )

    portfolio_cases = portfolio_cases[:3]





    # =====================================================
    # PAGE QUALITY SCORE SYSTEM

    indexing_data = get_indexing_data(
    request=request,
    page=page,
    context={
        'faqs': faqs,
        'reviews': service_reviews,
        'portfolio_cases': portfolio_cases,
        'seo_blocks': seo_blocks,
        'children': children,
        'city_data': city_data,
    }
)


    # =====================================================
    # CANONICAL
    # =====================================================


    district_pages = DistrictServicePage.objects.filter(
        city=city,
        service_page=parent,
        is_published=True
    ).select_related(
        'district'
    )[:12]

    # Только страницы текущей услуги
    #district_pages = district_pages.filter(
    #    slug__startswith=parent.slug
    #)[:12]



    # Random block position
    page_sections = build_page_sections(page)
    cta_variant = get_random_cta(page)



    # =====================================================
    # Contacts
    # =====================================================

    contacts = get_city_contacts(city)


    # =====================================================
    # RENDER
    # =====================================================


    return render(
        request,
        'pages/service_page.html',
        {
            'page': page,
            'city': city,
            'parent': parent,
            'children': children,
            'related_services': related_services,
            'seo_cluster': seo_cluster,
            'faqs': faqs,
            'city_data': city_data,
            'other_cities': other_cities,
#            'canonical_url': canonical_url,
            'seo_blocks': seo_blocks,
            'generated_faqs': generated_faqs,
            'district_pages': district_pages,
            'portfolio_cases': portfolio_cases,
            'reviews': service_reviews,
            'page_sections': page_sections,
            'cta_variant': cta_variant,
#            'page_score': page_score,
#            'page_should_index': page_should_index,
            'contacts': contacts,

            'canonical_url': indexing_data['canonical_url'],
            'page_score': indexing_data['score'],
            'page_should_index': indexing_data['should_index'],
            'quality_level': indexing_data['quality_level'],
        }
    )


# =====================================================
# FAQ PAGE
# =====================================================

def faq_page(
    request,
    faq_slug,
    city_slug=None,
):

    if city_slug:

        city = get_object_or_404(
            City,
            slug=city_slug,
            is_active=True,
        )

    else:

        city = get_object_or_404(
            City,
            is_main=True,
            is_active=True,
        )

    main_city = City.objects.get(
        is_main=True,
        is_active=True,
    )

    faq = get_object_or_404(
        FAQ.objects.prefetch_related(
            "related_services",
        ),
        city=main_city,
        slug=faq_slug,
        is_published=True,
    )

    faq._current_city = city

    canonical_url = request.build_absolute_uri(
        request.path,
    )

    related_faqs = (
        FAQ.objects.filter(
            city=main_city,
            is_published=True,
        )
        .exclude(id=faq.id)[:6]
    )

    for item in related_faqs:
        item._current_city = city

    city_faq = GlobalFAQ.objects.filter(
        is_published=True
    )

    other_cities = (
        City.objects.filter(
            is_active=True
        )
        .exclude(id=city.id)
        .order_by("name")[:10]
    )

    seo_blocks = (
        SEOBlock.objects.filter(
            is_active=True,
            cities=city,
        )
        .distinct()
        .order_by("sort_order")
    )

    return render(
        request,
        "pages/faq_page.html",
        {
            "faq": faq,
            "city": city,
            "city_faq": city_faq,
            "canonical_url": canonical_url,
            "related_faqs": related_faqs,
            "other_cities": other_cities,
            "seo_blocks": seo_blocks,
        },
    )


# =====================================================
# HOME
# =====================================================

def home(request):

    main_city = get_object_or_404(
        City,
        is_main=True,
        is_active=True,
    )

    cities = (
        City.objects
        .filter(is_active=True)
        .exclude(id=main_city.id)
        .order_by("name")[:50]
    )

    popular_services = (
        ServicePage.objects
        .filter(
            city=main_city,
            is_published=True,
            parent__isnull=True,
            template__is_main=True,
        )
        .select_related("template")
        .order_by("sort_order")[:12]
    )

    portfolio_cases = PortfolioCase.objects.filter(
        city=main_city,
        is_published=True,
    )[:3]

    reviews = Review.objects.filter(
        city=main_city,
        is_published=True,
    )[:4]

    faqs = GlobalFAQ.objects.filter(
        is_published=True
    )

    contacts = get_city_contacts(main_city)

    return render(
        request,
        "home.html",
        {
            "city": main_city,
            "main_city": main_city,
            "cities": cities,
            "popular_services": popular_services,
            "portfolio_cases": portfolio_cases,
            "reviews": reviews,
            "faqs": faqs,
            "contacts": contacts,
        },
    )


def city_home(
    request,
    city_slug,
):

    city = get_object_or_404(
        City,
        slug=city_slug,
        is_active=True,
    )

    cities = (
        City.objects
        .filter(is_active=True)
        .exclude(id=city.id)
        .order_by("name")[:50]
    )

    popular_services = (
        ServicePage.objects
        .filter(
            city=city,
            is_published=True,
            parent__isnull=True,
            template__is_main=True,
        )
        .select_related("template")
        .order_by("sort_order")[:12]
    )

    portfolio_cases = PortfolioCase.objects.filter(
        city=city,
        is_published=True,
    )[:3]

    reviews = Review.objects.filter(
        city=city,
        is_published=True,
    )[:4]

    faqs = GlobalFAQ.objects.filter(
        is_published=True
    )

    contacts = get_city_contacts(city)

    seo_blocks = (
        SEOBlock.objects.filter(
            is_active=True,
            cities=city,
        )
        .distinct()
        .order_by("sort_order")
    )

    return render(
        request,
        "home.html",
        {
            "city": city,
            "main_city": city,
            "cities": cities,
            "popular_services": popular_services,
            "portfolio_cases": portfolio_cases,
            "reviews": reviews,
            "faqs": faqs,
            "contacts": contacts,
            "seo_blocks": seo_blocks,
        },
    )


def portfolio_case_page(
    request,
    city_slug,
    case_slug
):

    case = get_object_or_404(
        PortfolioCase,
        city__slug=city_slug,
        slug=case_slug,
        is_published=True
    )

    related_cases = PortfolioCase.objects.filter(
        city=case.city,
        is_published=True
    ).exclude(
        id=case.id
    )[:6]

    canonical_url = request.build_absolute_uri(
        request.path
    )

    return render(
        request,
        'pages/portfolio_case.html',
        {
            'case': case,
            'city': case.city,
            'related_cases': related_cases,
            'canonical_url': canonical_url,
        }
    )


def district_service_page(
    request,
    city_slug,
    district_slug,
    service_slug
):

    city = get_object_or_404(
        City,
        slug=city_slug
    )

    district_page = get_object_or_404(
        DistrictServicePage.objects.select_related(
            'city',
            'district',
            'service_page'
        ),
        city=city,
        district__slug=district_slug,
        service_page__slug=service_slug,
        is_published=True
    )

    page = district_page.service_page


    indexing_data = get_indexing_data(
        request=request,
        page=page,
        district_page=True,
        context={
            'faqs': [],
            'reviews': [],
            'portfolio_cases': [],
            'seo_blocks': [],
            'children': [],
            'city_data': True,
        }
    )

    return render(
        request,
        'pages/district_service_page.html',
        {
            'district_page': district_page,
            'page': page,
            'city': city,
            'district': district_page.district,
            'canonical_url': indexing_data['canonical_url'],
            'page_score': indexing_data['score'],
            'page_should_index': indexing_data['should_index'],
            'quality_level': indexing_data['quality_level'],
        }
    )



def city_or_service(request, slug):

    city = City.objects.filter(
        slug=slug,
        is_active=True,
        is_main=False
    ).first()

    if city:
        return city_home(
            request,
            city_slug=city.slug
        )

    return service_page(
        request,
        service_slug=slug
    )

def city_or_service_2level(request, first, second):

    city = City.objects.filter(
        slug=first,
        is_active=True
    ).first()

    # Если первый сегмент — город
    if city:
        return service_page(
            request,
            city_slug=first,
            service_slug=second,
        )

    # Иначе это Москва:
    # /demontaj/burenie-v-potolok/
    return service_page(
        request,
        service_slug=first,
        page_slug=second,
    )
