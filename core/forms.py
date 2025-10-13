# core/forms.py

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        # Formda gösterilecek alanları belirtiyoruz
        fields = ['name', 'email', 'subject', 'message']