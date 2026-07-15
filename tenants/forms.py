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
            'max',
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
            'max': 'Max',
            'address': 'Адрес',
            'working_hours': 'Режим работы',
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['phone'].widget.attrs.update({
            'placeholder': '+7 (___) ___-__-__',
            'data-mask': 'phone'
        })

        self.fields['phone_secondary'].widget.attrs.update({
            'placeholder': '+7 (___) ___-__-__',
            'data-mask': 'phone'
        })

        self.fields['telegram'].widget.attrs.update({
            'placeholder': 'Your_nickname',
            'inputmode': 'str',
        })

        self.fields['whatsapp'].widget.attrs.update({
            'placeholder': '79780511856',
            'inputmode': 'numeric',
            'data-mask': 'digits'
        })

        self.fields['max'].widget.attrs.update({
            'placeholder': '79780511856',
            'inputmode': 'numeric',
            'data-mask': 'digits'
        })

        self.fields['working_hours'].widget.attrs.update({
            'placeholder': 'Пн-Пт, с 10:30 до 19:00',
            'inputmode': 'str',

        })
        self.fields['address'].widget.attrs.update({
            'placeholder': 'Москва, ул. Пушкина д. 12',
            'inputmode': 'str',

        })
