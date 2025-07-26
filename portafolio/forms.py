from django import forms
from .models import Portafolio

class PortafolioForm(forms.ModelForm):
    class Meta:
        model = Portafolio
        fields = ['nombre', 'dni', 'acciones', 'valor_actual', 'fecha_adquisicion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'acciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha_adquisicion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        } 