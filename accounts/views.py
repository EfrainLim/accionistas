from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario, ConfiguracionDashboard
from django.urls import reverse
from portafolio.models import Portafolio
from transacciones.models import HistorialTransaccion
from noticias.models import Noticia
from eventos.models import Evento
from informes.models import InformeFinanciero
from documentos.models import DocumentoLegal
from django.db import models
from django.utils import timezone

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.estado = 'P'  # Pendiente de aprobación
            user.save()
            messages.info(request, 'Registro exitoso. Tu cuenta está pendiente de aprobación.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.estado == 'A':
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Tu cuenta está pendiente de aprobación.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.estado != 'A':
        messages.warning(request, 'Tu cuenta aún no ha sido aprobada.')
        return redirect('logout')
    ahora = timezone.now()
    noticia_destacada = Noticia.objects.filter(destacada_en_dashboard=True, destacada_hasta__gte=ahora).order_by('-fecha_publicacion').first()
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')[:4]
    if noticia_destacada:
        noticias = [noticia_destacada] + [n for n in noticias if n.pk != noticia_destacada.pk]
        noticias = noticias[:4]
    eventos = Evento.objects.all().order_by('fecha')[:3]
    informes = InformeFinanciero.objects.all().order_by('-fecha_publicacion')[:4]
    documentos = DocumentoLegal.objects.all().order_by('-fecha_publicacion')[:4]
    portafolio = None
    if request.user.rol == 'accionista':
        portafolio = Portafolio.objects.filter(dni=request.user.dni).first()
    else:
        total_acciones = Portafolio.objects.all().aggregate(total=models.Sum('acciones'))['total'] or 0
        portafolio = type('obj', (object,), {'acciones': total_acciones})()
    config_dashboard = ConfiguracionDashboard.objects.first()
    return render(request, 'accounts/dashboard.html', {
        'noticias': noticias,
        'noticia_destacada': noticia_destacada,
        'eventos': eventos,
        'informes': informes,
        'documentos': documentos,
        'portafolio': portafolio,
        'imagen_fondo_dashboard': config_dashboard.imagen_fondo.url if config_dashboard and config_dashboard.imagen_fondo else None,
    })

def landing_view(request):
    config_dashboard = ConfiguracionDashboard.objects.first()
    return render(request, 'accounts/landing.html', {
        'imagen_fondo_dashboard': config_dashboard.imagen_fondo.url if config_dashboard and config_dashboard.imagen_fondo else None,
    })
