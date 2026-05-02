from django.shortcuts import render, get_object_or_404
from .models import City
from leads.forms import LeadForm
from .forms import CityContactForm
from django.contrib.auth.decorators import login_required
# Create your views here.


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
    leads = city.leads.all().order_by('-created_at')

    if request.method == 'POST':
        form = CityContactForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
    else:
        form = CityContactForm(instance=city)

    return render(request, 'tenants/dashboard.html', {
        'city': city,
        'leads': leads,
        'form': form,
    })