# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import ContactMessage # Assuming ContactMessage model exists
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Fields displayed on the registration form
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email domain is correct
        if not email.endswith('@live.acibadem.edu.tr'):
            raise ValidationError(
                'Only email addresses ending with "@live.acibadem.edu.tr" can be registered.'
            )
        return email

class CustomAuthenticationForm(AuthenticationForm):
    # Change the label for the username field (which is email for us)
    username = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'autofocus': True}))

class ContactForm(forms.ModelForm):
    # Assuming you still need the ContactForm, kept as is.
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
     