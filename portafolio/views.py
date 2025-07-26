from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import aprobado_required
from .models import Portafolio
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .forms import PortafolioForm
from django.shortcuts import get_object_or_404, redirect

@login_required
@aprobado_required
def portafolio_view(request):
    search = request.GET.get('search', '')
    accionistas = Portafolio.objects.all().order_by('nombre')
    if search:
        accionistas = accionistas.filter(Q(nombre__icontains=search) | Q(dni__icontains=search))
    total_acciones = sum(a.acciones for a in accionistas)
    return render(request, 'portafolio/portafolio.html', {
        'accionistas': accionistas,
        'total_acciones': total_acciones,
        'search': search,
    })

# Decorador para admin
admin_required = user_passes_test(lambda u: u.is_superuser or getattr(u, 'rol', '') == 'admin')

@admin_required
def admin_portafolio_list(request):
    search = request.GET.get('search', '')
    accionistas = Portafolio.objects.all().order_by('nombre')
    if search:
        accionistas = accionistas.filter(Q(nombre__icontains=search) | Q(dni__icontains=search))
    return render(request, 'portafolio/admin_portafolio_list.html', {'accionistas': accionistas, 'search': search})

@admin_required
def admin_portafolio_create(request):
    if request.method == 'POST':
        form = PortafolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_portafolio_list')
    else:
        form = PortafolioForm()
    return render(request, 'portafolio/admin_portafolio_form.html', {'form': form, 'accion': 'Crear'})

@admin_required
def admin_portafolio_edit(request, pk):
    accionista = get_object_or_404(Portafolio, pk=pk)
    if request.method == 'POST':
        form = PortafolioForm(request.POST, instance=accionista)
        if form.is_valid():
            form.save()
            return redirect('admin_portafolio_list')
    else:
        form = PortafolioForm(instance=accionista)
    return render(request, 'portafolio/admin_portafolio_form.html', {'form': form, 'accion': 'Editar'})

@admin_required
def admin_portafolio_delete(request, pk):
    accionista = get_object_or_404(Portafolio, pk=pk)
    if request.method == 'POST':
        accionista.delete()
        return redirect('admin_portafolio_list')
    return render(request, 'portafolio/admin_portafolio_confirm_delete.html', {'accionista': accionista})
