from django.shortcuts import render, redirect
from accounts.decorators import aprobado_required
from .forms import SoporteForm
from .models import ContactoConfig
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import MensajeSoporte
from django.shortcuts import get_object_or_404, redirect
from .forms import ContactoConfigForm
from django.core.paginator import Paginator

admin_required = user_passes_test(lambda u: u.is_superuser or getattr(u, 'rol', '') == 'admin')

# Create your views here.

@aprobado_required
def soporte_view(request):
    config = ContactoConfig.objects.first()
    datos_contacto = {
        'direccion': config.direccion if config else '',
        'email': config.email if config else '',
        'telefono': config.telefono if config else '',
        'horario': config.horario if config else '',
        'mapa_url': config.mapa_url if config else '',
        'redes': [
            {'icon': 'bi-facebook', 'url': config.facebook} if config and config.facebook else None,
            {'icon': 'bi-twitter', 'url': config.twitter} if config and config.twitter else None,
            {'icon': 'bi-instagram', 'url': config.instagram} if config and config.instagram else None,
            {'icon': 'bi-linkedin', 'url': config.linkedin} if config and config.linkedin else None,
            {'icon': 'bi-whatsapp', 'url': config.whatsapp} if config and config.whatsapp else None,
        ]
    }
    datos_contacto['redes'] = [r for r in datos_contacto['redes'] if r]
    if request.method == 'POST':
        form = SoporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu mensaje ha sido enviado exitosamente!')
            return redirect('soporte')
    else:
        form = SoporteForm()
    return render(request, 'soporte/soporte.html', {'form': form, 'datos': datos_contacto})

@admin_required
def admin_soporte_list(request):
    search = request.GET.get('search', '')
    mensajes = MensajeSoporte.objects.all().order_by('-fecha')
    if search:
        mensajes = mensajes.filter(nombre__icontains=search)
    paginator = Paginator(mensajes, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'soporte/admin_soporte_list.html', {'mensajes': page_obj.object_list, 'search': search, 'page_obj': page_obj})

@admin_required
def admin_soporte_detail(request, pk):
    mensaje = get_object_or_404(MensajeSoporte, pk=pk)
    return render(request, 'soporte/admin_soporte_detail.html', {'mensaje': mensaje})

@admin_required
def admin_soporte_delete(request, pk):
    mensaje = get_object_or_404(MensajeSoporte, pk=pk)
    if request.method == 'POST':
        mensaje.delete()
        return redirect('admin_soporte_list')
    return render(request, 'soporte/admin_soporte_confirm_delete.html', {'mensaje': mensaje})

@admin_required
def admin_contacto_config(request):
    config = ContactoConfig.objects.first()
    if request.method == 'POST':
        form = ContactoConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('admin_contacto_config')
    else:
        form = ContactoConfigForm(instance=config)
    return render(request, 'soporte/admin_contacto_config.html', {'form': form})
