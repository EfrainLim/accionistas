from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import aprobado_required
from django.contrib import messages
from accounts.models import Usuario, ConfiguracionDashboard
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django import forms
from django.http import HttpResponseForbidden

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'readonly': 'readonly'}),
        }

class ConfiguracionDashboardForm(forms.ModelForm):
    limpiar_imagen = forms.BooleanField(
        required=False, 
        label='Limpiar imagen actual',
        help_text='Marcar esta casilla para eliminar la imagen actual sin subir una nueva'
    )
    
    class Meta:
        model = ConfiguracionDashboard
        fields = ['imagen_fondo']
        widgets = {
            'imagen_fondo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        imagen_fondo = cleaned_data.get('imagen_fondo')
        limpiar_imagen = cleaned_data.get('limpiar_imagen')
        
        if limpiar_imagen and imagen_fondo:
            raise forms.ValidationError('No puedes subir una nueva imagen y limpiar la actual al mismo tiempo.')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('limpiar_imagen'):
            # Si se marca limpiar, eliminar la imagen actual
            if instance.imagen_fondo:
                instance.imagen_fondo.delete(save=False)
            instance.imagen_fondo = None
        
        if commit:
            instance.save()
        return instance

@login_required
@aprobado_required
def configuracion_view(request):
    user = request.user
    perfil_form = PerfilForm(instance=user)
    password_form = PasswordChangeForm(user)
    if request.method == 'POST':
        if 'perfil_submit' in request.POST:
            perfil_form = PerfilForm(request.POST, instance=user)
            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('configuracion')
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('configuracion')
    return render(request, 'configuracion/configuracion.html', {
        'perfil_form': perfil_form,
        'password_form': password_form,
    })

@login_required
@aprobado_required
def administrar_view(request):
    if not (request.user.is_superuser or getattr(request.user, 'rol', '') != 'accionista'):
        return HttpResponseForbidden('No tienes permisos para acceder a esta sección.')
    return render(request, 'configuracion/administrar.html')

@login_required
@aprobado_required
def admin_dashboard_config(request):
    if not (request.user.is_superuser or getattr(request.user, 'rol', '') != 'accionista'):
        return HttpResponseForbidden('No tienes permisos para acceder a esta sección.')
    
    config, created = ConfiguracionDashboard.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = ConfiguracionDashboardForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración del dashboard actualizada correctamente.')
            return redirect('admin_dashboard_config')
    else:
        form = ConfiguracionDashboardForm(instance=config)
    
    return render(request, 'configuracion/dashboard_config.html', {
        'form': form,
        'config': config,
    })
