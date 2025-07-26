from django.shortcuts import render, get_object_or_404
from accounts.decorators import aprobado_required
from .models import Noticia
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .forms import NoticiaForm
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator

@aprobado_required
def noticias_view(request):
    search = request.GET.get('search', '')
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    if search:
        noticias = noticias.filter(Q(titulo__icontains=search) | Q(contenido__icontains=search))
    paginator = Paginator(noticias, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'noticias/noticias.html', {'noticias': page_obj.object_list, 'search': search, 'page_obj': page_obj})

@aprobado_required
def noticia_detalle_view(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    recientes = Noticia.objects.exclude(id=noticia.id).order_by('-fecha_publicacion')[:4]
    return render(request, 'noticias/detalle.html', {'noticia': noticia, 'recientes': recientes})

admin_required = user_passes_test(lambda u: u.is_superuser or getattr(u, 'rol', '') == 'admin')

@admin_required
def admin_noticias_list(request):
    search = request.GET.get('search', '')
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    if search:
        noticias = noticias.filter(Q(titulo__icontains=search) | Q(contenido__icontains=search))
    paginator = Paginator(noticias, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'noticias/admin_noticias_list.html', {'noticias': page_obj.object_list, 'search': search, 'page_obj': page_obj})

@admin_required
def admin_noticias_create(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            print('Fecha destacada:', form.cleaned_data.get('destacada_hasta'))
            form.save()
            return redirect('admin_noticias_list')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/admin_noticias_form.html', {'form': form, 'accion': 'Crear'})

@admin_required
def admin_noticias_edit(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('admin_noticias_list')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticias/admin_noticias_form.html', {'form': form, 'accion': 'Editar'})

@admin_required
def admin_noticias_delete(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('admin_noticias_list')
    return render(request, 'noticias/admin_noticias_confirm_delete.html', {'noticia': noticia})
