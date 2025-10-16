# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import ContactMessage
from users.models import CustomUser  # Yeni kullanıcı modelini import edin

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@live.acibadem.edu.tr'):
            raise ValidationError(
                'Sadece "@live.acibadem.edu.tr" uzantılı e-posta adresleri ile kayıt olunabilir.'
            )
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='E-posta Adresi', widget=forms.EmailInput(attrs={'autofocus': True}))


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label='Doğrulama Kodu',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'E-postanıza gelen kodu girin'})
    )

class ContactForm(forms.ModelForm):
    # ... bu form aynı kalabilir ...
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']