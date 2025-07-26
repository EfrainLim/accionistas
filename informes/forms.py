from django import forms
from .models import InformeFinanciero

class InformeFinancieroForm(forms.ModelForm):
    class Meta:
        model = InformeFinanciero
        fields = ['titulo', 'tipo_informe', 'area', 'periodicidad', 'archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del informe'}),
            'tipo_informe': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'periodicidad': forms.Select(attrs={'class': 'form-select'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_informe = cleaned_data.get('tipo_informe')
        area = cleaned_data.get('area')
        if tipo_informe == 'area' and not area:
            self.add_error('area', 'Debes seleccionar un área para informes de área.')
        if tipo_informe == 'financiero':
            cleaned_data['area'] = None
        return cleaned_data

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Verificar si es un archivo nuevo (tiene content_type) o existente
            if hasattr(archivo, 'content_type'):
                # Es un archivo nuevo
                if not archivo.name.lower().endswith('.pdf') or archivo.content_type != 'application/pdf':
                    raise forms.ValidationError('Solo se permiten archivos PDF.')
            else:
                # Es un archivo existente, verificar solo la extensión
                if not archivo.name.lower().endswith('.pdf'):
                    raise forms.ValidationError('Solo se permiten archivos PDF.')
        return archivo 