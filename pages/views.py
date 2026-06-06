from django.shortcuts import render, get_object_or_404
from cities.models import City

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

# =====================================================
# SERVICE PAGE
# =====================================================

def service_page(
    request,
    city_slug,
    service_slug,
    page_slug=None
):

    city = get_object_or_404(
        City,
        slug=city_slug
    )

    # =====================================================
    # PAGE
    # =====================================================

    if page_slug:

        # CHILD PAGE

        page = get_object_or_404(
            ServicePage.objects.select_related(
                'parent',
                'city'
            ),
            city=city,
            parent__slug=service_slug,
            slug=page_slug,
            is_published=True
        )

        parent = page.parent

    else:

        # PARENT PAGE

        page = get_object_or_404(
            ServicePage.objects.select_related(
                'city'
            ),
            city=city,
            slug=service_slug,
            parent__isnull=True,
            is_published=True
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

    faqs = FAQ.objects.filter(
        city=city,
        related_services=parent
    ).distinct()[:8]
    generated_faqs = generate_faqs(
    page,
    city
)

    # fallback

    if not faqs.exists():

        faqs = FAQ.objects.filter(
            city=city
        )[:8]

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
    city_slug,
    faq_slug
):

    faq = get_object_or_404(
        FAQ.objects.select_related('city'),
        city__slug=city_slug,
        slug=faq_slug
    )

    city = faq.city

    canonical_url = request.build_absolute_uri(
        request.path
    )

    # =====================================================
    # RELATED FAQ
    # =====================================================

    related_faqs = FAQ.objects.filter(
        city=city
    ).exclude(
        id=faq.id
    )[:6]

    # =====================================================
    # OTHER CITIES
    # =====================================================

    other_cities = City.objects.filter(
        is_active=True
    ).exclude(
        id=city.id
    )[:10]

    # =====================================================
    # SEO BLOCKS
    # =====================================================

    seo_blocks = SEOBlock.objects.filter(
        is_active=True,
        cities=city
    ).distinct().order_by(
        'sort_order'
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        'pages/faq_page.html',
        {
            'faq': faq,
            'city': city,
            'canonical_url': canonical_url,
            'related_faqs': related_faqs,
            'other_cities': other_cities,
            'seo_blocks': seo_blocks,
        }
    )


# =====================================================
# HOME
# =====================================================

def home(request):

    cities = City.objects.filter(
        is_active=True
    ).order_by(
        'name'
    )[:50]

    popular_services = ServicePage.objects.filter(
        is_published=True,
        parent__isnull=True,
        is_main=True
    ).select_related(
        'city'
    ).order_by(
        'sort_order'
    )[:12]

    portfolio_cases = PortfolioCase.objects.filter(
        is_published=True
    )
    portfolio_cases = portfolio_cases[:3]

    reviews = Review.objects.filter(is_published=True)
    service_reviews = reviews[:4]

    faqs = GlobalFAQ.objects.filter(is_published=True)


    return render(
        request,
        'home.html',
        {
            'cities': cities,
            'popular_services': popular_services,
            'reviews':reviews,
            'portfolio_cases':portfolio_cases,
            'faqs':faqs,
        }
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



