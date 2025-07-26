from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'categoria', 'imagen', 'contenido', 'archivo', 'autor', 'video_url', 'enlace_externo', 'destacada_en_dashboard', 'destacada_hasta']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'enlace_externo': forms.URLInput(attrs={'class': 'form-control'}),
            'destacada_en_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacada_hasta': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.destacada_hasta:
            self.initial['destacada_hasta'] = self.instance.destacada_hasta.strftime('%Y-%m-%dT%H:%M')

    def clean_destacada_hasta(self):
        data = self.cleaned_data['destacada_hasta']
        if isinstance(data, str):
            from datetime import datetime
            try:
                data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
            except Exception:
                pass
        return data 