from django.shortcuts import render, get_object_or_404
from .models import City
from leads.forms import LeadForm
from .forms import CityContactForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from pages.models import ServicePage
from pages.services.page_quality import calculate_page_score
from django.shortcuts import redirect
from pages.services.contacts import get_city_contacts
from pages.models import (
    ServicePage,
    FAQ,
    PortfolioCase,
    Review,
    GlobalFAQ
)


def city_home(request, city_slug):
    city = get_object_or_404(City, slug = city_slug)
    if city.is_main:
        return redirect('/', permanent=True)
    
    main_services = ServicePage.objects.filter(city=city, is_published=True, template__is_main=True, parent__isnull=True).select_related('template')[:6]

    cities = City.objects.filter(is_active=True).exclude(id=city.id).order_by('name')[:50]
    
    contacts = get_city_contacts(city)

    portfolio_cases = PortfolioCase.objects.filter(is_published=True)[:3]
    reviews = Review.objects.filter(is_published=True)[:2]
    faqs = GlobalFAQ.objects.filter(is_published=True)
    popular_faqs = FAQ.objects.filter(is_published=True)



    form = LeadForm
    canonical_url = request.build_absolute_uri(request.path)

    return render(request, 'cities/city_home.html', {
        'city': city,
        'cities':cities,
        'contacts':contacts,
        'portfolio_cases':portfolio_cases,
        'reviews': reviews,
        'faqs':popular_faqs,
        'form': form,
        'canonical_url':canonical_url,
        'main_services': main_services,
    })



@login_required
def tenant_dashboard(request):

    user = request.user

    city = user.city

    leads = city.leads.all().order_by(
        '-created_at'
    )

    # =====================================================
    # CONTACT FORM
    # =====================================================

    if request.method == 'POST':

        form = CityContactForm(
            request.POST,
            instance=city
        )

        if form.is_valid():
            form.save()

    else:

        form = CityContactForm(
            instance=city
        )

    # =====================================================
    # SEO STATS
    # =====================================================

    pages = ServicePage.objects.filter(
        city=city,
        is_published=True
    )

    total_pages = pages.count()

    indexed_pages = pages.filter(
        no_index=False
    ).count()

    noindex_pages = pages.filter(
        no_index=True
    ).count()

    weak_pages = 0

    seo_scores = []

    for page in pages:

        score = calculate_page_score(
            page,
            {
                'faqs': [],
                'reviews': [],
                'portfolio_cases': [],
                'seo_blocks': [],
                'children': [],
                'city_data': True,
            }
        )

        seo_scores.append(score)

        if score < 40:
            weak_pages += 1

    avg_seo_score = 0

    if seo_scores:

        avg_seo_score = int(
            sum(seo_scores) / len(seo_scores)
        )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        'tenants/dashboard.html',
        {
            'city': city,
            'leads': leads,
            'form': form,

            'total_pages': total_pages,
            'indexed_pages': indexed_pages,
            'noindex_pages': noindex_pages,
            'weak_pages': weak_pages,
            'avg_seo_score': avg_seo_score,
        }
    )