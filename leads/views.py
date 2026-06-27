from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import JsonResponse

from cities.models import City

from .forms import LeadForm
from .models import Lead

from .services import send_telegram_message, is_duplicate_lead
#from ratelimit.decorators import ratelimit
from django_ratelimit.decorators import ratelimit
#from ratelimit.decorators import ratelimit

@ratelimit(
    key='ip',
    rate='5/m',
    block=True
)
def create_lead(request, city_slug=None):

    policy_accept = request.POST.get('policy_accept')

    if not policy_accept:
        return JsonResponse({
            'success': False,
            'error': 'Необходимо принять условия'
        })

    city = None

    # =====================================================
    # AJAX FORM
    # =====================================================

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        city_id = request.POST.get('city')

        city = get_object_or_404(
            City,
            id=city_id
        )

        form = LeadForm(request.POST)

        # =====================================================
        # HONEYPOT
        # =====================================================

        if request.POST.get('website'):

            return JsonResponse({
                'success': False
            })

        if form.is_valid():

            lead = form.save(commit=False)

            lead.city = city

            # =====================================================
            # UTM
            # =====================================================

            lead.utm_source = request.session.get(
                'utm_source'
            )

            lead.utm_medium = request.session.get(
                'utm_medium'
            )

            lead.utm_campaign = request.session.get(
                'utm_campaign'
            )

            lead.utm_term = request.session.get(
                'utm_term'
            )

            lead.utm_content = request.session.get(
                'utm_content'
            )

            # =====================================================
            # PAGE URL
            # =====================================================

            lead.page_url = request.POST.get(
                'page_url',
                ''
            )

            # =====================================================
            # USER AGENT
            # =====================================================

            lead.user_agent = request.META.get(
                'HTTP_USER_AGENT',
                ''
            )

            # =====================================================
            # IP
            # =====================================================

            x_forwarded_for = request.META.get(
                'HTTP_X_FORWARDED_FOR'
            )

            if x_forwarded_for:

                lead.ip_address = (
                    x_forwarded_for.split(',')[0]
                )

            else:

                lead.ip_address = request.META.get(
                    'REMOTE_ADDR'
                )

            # =====================================================
            # DUPLICATE CHECK
            # =====================================================

            if is_duplicate_lead(lead.phone):

                return JsonResponse({
                    'success': False,
                    'errors': {
                        'phone': [
                            'Заявка уже отправлена'
                        ]
                    }
                })

            lead.save()

            # =====================================================
            # TELEGRAM MESSAGE
            # =====================================================

            message = f"""
🔥 Новая заявка

🏙 Город: {city.name}

👤 Имя: {lead.name}

📞 Телефон: {lead.phone}

🛠 Услуга: {lead.service or 'Не указана'}

💬 Комментарий:
{lead.comment or '—'}

====================

🌐 Источник: {lead.utm_source or '—'}

📢 Кампания: {lead.utm_campaign or '—'}

🔑 Ключ: {lead.utm_term or '—'}

📄 Страница:
{lead.page_url or '—'}
"""

            tenant = getattr(
                city,
                'tenant_profile',
                None
            )

#            if (tenant and tenant.is_active and tenant.telegram_chat_id):

#                send_telegram_message( message, tenant.telegram_chat_id )

            return JsonResponse({
                'success': True
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        })

    # =====================================================
    # CLASSIC PAGE FORM
    # =====================================================

    city = get_object_or_404(
        City,
        slug=city_slug
    )

    canonical_url = request.build_absolute_uri(
        request.path
    )

    if request.method == 'POST':

        # =====================================================
        # HONEYPOT
        # =====================================================

        if request.POST.get('website'):

            return redirect('success')

        form = LeadForm(request.POST)

        if form.is_valid():

            lead = form.save(commit=False)

            lead.city = city

            # =====================================================
            # UTM
            # =====================================================

            lead.utm_source = request.session.get(
                'utm_source'
            )

            lead.utm_medium = request.session.get(
                'utm_medium'
            )

            lead.utm_campaign = request.session.get(
                'utm_campaign'
            )

            lead.utm_term = request.session.get(
                'utm_term'
            )

            lead.utm_content = request.session.get(
                'utm_content'
            )

            # =====================================================
            # PAGE URL
            # =====================================================

            lead.page_url = request.path

            # =====================================================
            # USER AGENT
            # =====================================================

            lead.user_agent = request.META.get(
                'HTTP_USER_AGENT',
                ''
            )

            # =====================================================
            # IP
            # =====================================================

            x_forwarded_for = request.META.get(
                'HTTP_X_FORWARDED_FOR'
            )

            if x_forwarded_for:

                lead.ip_address = (
                    x_forwarded_for.split(',')[0]
                )

            else:

                lead.ip_address = request.META.get(
                    'REMOTE_ADDR'
                )

            # =====================================================
            # DUPLICATE CHECK
            # =====================================================

            if is_duplicate_lead(lead.phone):

                return render(
                    request,
                    'leads/create_lead.html',
                    {
                        'form': form,
                        'city': city,
                        'canonical_url': canonical_url,
                        'duplicate_error': (
                            'Заявка уже отправлена'
                        )
                    }
                )

            lead.save()

            # =====================================================
            # TELEGRAM MESSAGE
            # =====================================================

            message = f"""
🔥 Новая заявка

🏙 Город: {city.name}

👤 Имя: {lead.name}

📞 Телефон: {lead.phone}

🛠 Услуга: {lead.service or 'Не указана'}

💬 Комментарий:
{lead.comment or '—'}

====================

🌐 Источник: {lead.utm_source or '—'}

📢 Кампания: {lead.utm_campaign or '—'}

🔑 Ключ: {lead.utm_term or '—'}

📄 Страница:
{lead.page_url or '—'}
"""

            tenant = getattr(
                city,
                'tenant_profile',
                None
            )

            if (
                tenant
                and tenant.is_active
                and tenant.telegram_chat_id
            ):

                send_telegram_message(
                    message,
                    tenant.telegram_chat_id
                )

            return redirect('success')

    else:

        form = LeadForm()

    return render(
        request,
        'leads/create_lead.html',
        {
            'form': form,
            'city': city,
            'canonical_url': canonical_url,
        }
    )

def success(request):

    return render(
        request,
        'leads/success.html'
    )