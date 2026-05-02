from django import forms
from cities.models import City


class CityContactForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['phone', 'address', 'price_text', 'telegram_chat_id']