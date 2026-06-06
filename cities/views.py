from django.shortcuts import render, get_object_or_404
from .models import City
from leads.forms import LeadForm
from .forms import CityContactForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from pages.models import ServicePage
from pages.services.page_quality import calculate_page_score



def city_home(request, city_slug):
    city = get_object_or_404(City, slug = city_slug)
    form = LeadForm
    canonical_url = request.build_absolute_uri(request.path)

    return render(request, 'cities/city_home.html', {
        'city': city,
        'form': form,
        'canonical_url':canonical_url

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