from django import forms
from cities.models import City
from .models import TenantProfile

class CityContactForm(forms.ModelForm):
    class Meta:
        model = TenantProfile

        fields = [
            'company_name',
            'phone',
            'phone_secondary',
            'email',
            'telegram',
            'whatsapp',
            'website',
            'address',
            'working_hours',
        ]

        labels = {
            'company_name': 'Название компании',
            'phone': 'Основной телефон',
            'phone_secondary': 'Дополнительный телефон',
            'email': 'Email',
            'telegram': 'Telegram',
            'whatsapp': 'WhatsApp',
            'website': 'Сайт',
            'address': 'Адрес',
            'working_hours': 'Режим работы',
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

