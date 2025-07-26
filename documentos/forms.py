from django import forms
from .models import DocumentoLegal

class DocumentoLegalForm(forms.ModelForm):
    class Meta:
        model = DocumentoLegal
        fields = ['titulo', 'tipo', 'documento', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_documento(self):
        archivo = self.cleaned_data.get('documento')
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