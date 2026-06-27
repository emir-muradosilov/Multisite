from django import forms
from cities.models import City


class CityContactForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['phone', 'address', 'price_text']




class CityAdminForm(forms.ModelForm):

    copy_structure = forms.BooleanField(
        required=False,
        label='Скопировать структуру Москвы'
    )

    class Meta:
        model = City
        fields = '__all__'
