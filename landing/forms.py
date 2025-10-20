from django import forms
from .models import ContactForm

class ContactFormForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(
        required=True,
        label="Отправляя заявку вы соглашаетесь с политикой конфиденциальности",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = ContactForm
        fields = ['full_name', 'phone', 'email', 'organization_name', 'package', 'comment', 'privacy_policy_accepted']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше ФИО'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7(999)999-99-99'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@example.com'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Организация'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий', 'rows': 3}),
        }
