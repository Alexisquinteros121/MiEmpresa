from django import forms
from .models import Contacto, Persona

class FormPersona(forms.ModelForm):
    class Meta:
        model=Persona
        fields='__all__'

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'}),
        }
