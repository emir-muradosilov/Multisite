
from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    website = forms.CharField(
    required=False,
    widget=forms.HiddenInput
)
    
    class Meta:
        model = Lead
        fields = [
            'name',
            'phone',
            'email',
            'service',
            'comment',
        ]

    def clean_phone(self):

        phone = self.cleaned_data['phone']

        digits = ''.join(
            filter(str.isdigit, phone)
        )

        if len(digits) < 10:
            raise forms.ValidationError(
                'Введите корректный телефон'
            )

        return phone