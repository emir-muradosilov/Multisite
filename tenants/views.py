from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CityContactForm
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from leads.models import Lead

# Create your views here.

@login_required
def tenant_dashboard(request):
    if request.user.role != 'tenant':
        return HttpResponseForbidden("Нет доступа")

    city = request.user.city
    leads = city.leads.all()

    today = timezone.now().date()
    month_ago = today - timedelta(days=30)

    total_leads = leads.count()
    today_leads = leads.filter(created_at__date=today).count()
    month_leads = leads.filter(created_at__date__gte=month_ago).count()

    utm_stats = (
    leads
    .values('utm_source')
    .annotate(count=Count('id'))
    .order_by('-count'))

    status_stats = (
    leads
    .values('status')
    .annotate(count=Count('id')))


    status_dict = {item['status']: item['count'] for item in status_stats}
    new_count = status_dict.get('new', 0)
    target_count = status_dict.get('target', 0)
    spam_count = status_dict.get('spam', 0)
    no_answer_count = status_dict.get('no_answer', 0)
    conversion = 0
    if total_leads > 0:
        conversion = round((target_count / total_leads) * 100, 2)
    

    return render(request, 'tenants/dashboard.html', {
        'city': city,

        'total_leads': total_leads,
        'today_leads': today_leads,
        'month_leads': month_leads,

        'target_count': target_count,
        'spam_count': spam_count,
        'no_answer_count': no_answer_count,

        'conversion': conversion,

        'utm_stats': utm_stats,
    })


class TenantLoginView(LoginView):
    template_name = 'tenants/login.html'

@login_required
def tenant_leads(request):
    if request.user.role != 'tenant':
        return HttpResponseForbidden("Нет доступа")

    city = request.user.city
    leads = city.leads.all().order_by('-created_at')

    # --- фильтр по дате ---
    date_filter = request.GET.get('date')

    if date_filter == 'today':
        today = timezone.now().date()
        leads = leads.filter(created_at__date=today)

    # --- фильтр по источнику ---
    source_filter = request.GET.get('source')

    if source_filter:
        leads = leads.filter(utm_source=source_filter)

    sources = (
    city.leads
    .values_list('utm_source', flat=True)
    .distinct()
)

    return render(request, 'tenants/leads.html', {
        'city': city,
        'leads': leads,
        'date_filter': date_filter,
        'source_filter': source_filter,
        'sources': sources,
        'status_choices': Lead.STATUS_CHOICES,
    })


@login_required
def tenant_settings(request):
    if request.user.role != 'tenant':
        return HttpResponseForbidden("Нет доступа")

    city = request.user.city

    if request.method == 'POST':
        form = CityContactForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
    else:
        form = CityContactForm(instance=city)

    return render(request, 'tenants/settings.html', {
        'city': city,
        'form': form
    })


@login_required
def update_lead_status(request, lead_id):
    if request.user.role != 'tenant':
        return HttpResponseForbidden("Нет доступа")

    lead = get_object_or_404(Lead, id=lead_id, city=request.user.city)

    new_status = request.POST.get('status')
    if new_status in dict(Lead.STATUS_CHOICES):
        lead.status = new_status
        lead.save()

    return redirect('tenant_leads')

