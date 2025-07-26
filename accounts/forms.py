from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from portafolio.models import Portafolio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegistroForm(UserCreationForm):
    dni = forms.CharField(max_length=15, label='DNI', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}))

    class Meta:
        model = Usuario
        fields = ('nombre', 'dni', 'email', 'password1', 'password2')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrarse'))

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        # Verificar que el DNI exista en Portafolio
        if not Portafolio.objects.filter(dni=dni).exists():
            raise forms.ValidationError('El DNI ingresado no está registrado como accionista.')
        # Verificar que no haya otro usuario con ese DNI
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un usuario registrado con este DNI.')
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.dni = self.cleaned_data['dni']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Iniciar sesión')) 