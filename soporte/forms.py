from django import forms
from .models import MensajeSoporte, ContactoConfig

class SoporteForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, label='Tu Nombre')
    email = forms.EmailField(label='Tu Email')
    asunto = forms.CharField(max_length=150, label='Asunto')
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Mensaje')

    class Meta:
        model = MensajeSoporte
        fields = ['nombre', 'email', 'asunto', 'mensaje']

class ContactoConfigForm(forms.ModelForm):
    class Meta:
        model = ContactoConfig
        fields = ['direccion', 'email', 'telefono', 'horario', 'mapa_url', 'facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'mapa_url': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+'}),
        }

    def clean_whatsapp(self):
        numero = self.cleaned_data.get('whatsapp', '').strip()
        if numero and not numero.isdigit():
            raise forms.ValidationError('Solo se permiten números (sin espacios, guiones ni +).')
        return numero 