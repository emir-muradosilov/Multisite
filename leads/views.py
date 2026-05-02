from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import LeadForm
from .services import send_telegram_message

# Create your views here.

def create_lead(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)

    canonical_url = request.build_absolute_uri(request.path)

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.city = city

            # UTM из session
            lead.utm_source = request.session.get('utm_source')
            lead.utm_medium = request.session.get('utm_medium')
            lead.utm_campaign = request.session.get('utm_campaign')
            lead.utm_term = request.session.get('utm_term')
            lead.utm_content = request.session.get('utm_content')

            lead.save()

            # telegram message Lead
            message = f"""
            Новая заявка!

            Город: {city.name}
            Имя: {lead.name}
            Телефон: {lead.phone}
            Услуга: {lead.service}

            Источник: {lead.utm_source}
            Ключ: {lead.utm_term}
            """

            chat_id = city.telegram_chat_id
            if chat_id:
                send_telegram_message(message, chat_id)

            return redirect('success')

    else:
        form = LeadForm()

    return render(request, 'leads/create_lead.html', {
        'form': form,
        'city': city,
        'canonical_url': canonical_url
    })


def success(request):
    return render(request, 'leads/success.html')