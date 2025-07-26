from django.shortcuts import render, redirect
from accounts.decorators import aprobado_required
from .models import InformeFinanciero
from .forms import InformeFinancieroForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.conf import settings
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from documentos.models import DocumentoLegal
from django.contrib.auth.decorators import login_required

aprobado_required = user_passes_test(lambda u: u.is_authenticated)

@aprobado_required
def informes_view(request):
    tipo = request.GET.get('tipo')
    anio = request.GET.get('anio')
    search = request.GET.get('search', '')
    informes = InformeFinanciero.objects.all().order_by('-fecha_publicacion')
    if tipo:
        informes = informes.filter(tipo_informe=tipo)
    if anio:
        informes = informes.filter(fecha_publicacion__year=anio)
    if search:
        informes = informes.filter(Q(titulo__icontains=search) | Q(archivo__icontains=search))
    anios = InformeFinanciero.objects.dates('fecha_publicacion', 'year', order='DESC')
    paginator = Paginator(informes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Solo administradores pueden registrar informes
    puede_registrar = request.user.is_superuser or getattr(request.user, 'rol', '') == 'admin'
    form = None
    if puede_registrar:
        if request.method == 'POST':
            form = InformeFinancieroForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Informe registrado correctamente.')
                return redirect('informes')
        else:
            form = InformeFinancieroForm()

    return render(request, 'informes/informes.html', {
        'informes': page_obj.object_list,
        'anios': anios,
        'tipo_actual': tipo,
        'anio_actual': anio,
        'search': search,
        'page_obj': page_obj,
        'form': form,
        'puede_registrar': puede_registrar,
    })

admin_required = user_passes_test(lambda u: u.is_superuser or getattr(u, 'rol', '') == 'admin')

@admin_required
def admin_informes_list(request):
    search = request.GET.get('search', '')
    informes = InformeFinanciero.objects.all().order_by('-fecha_publicacion')
    if search:
        informes = informes.filter(
            Q(titulo__icontains=search) |
            Q(tipo_informe__icontains=search) |
            Q(area__icontains=search) |
            Q(periodicidad__icontains=search) |
            Q(archivo__icontains=search)
        )
    paginator = Paginator(informes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'informes/admin_informes_list.html', {'informes': page_obj.object_list, 'search': search, 'page_obj': page_obj})

@admin_required
def admin_informes_create(request):
    if request.method == 'POST':
        form = InformeFinancieroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_informes_list')
    else:
        form = InformeFinancieroForm()
    return render(request, 'informes/admin_informes_form.html', {'form': form, 'accion': 'Crear'})

@admin_required
def admin_informes_edit(request, pk):
    informe = get_object_or_404(InformeFinanciero, pk=pk)
    if request.method == 'POST':
        form = InformeFinancieroForm(request.POST, request.FILES, instance=informe)
        if form.is_valid():
            form.save()
            return redirect('admin_informes_list')
    else:
        form = InformeFinancieroForm(instance=informe)
    return render(request, 'informes/admin_informes_form.html', {'form': form, 'accion': 'Editar'})

@admin_required
def admin_informes_delete(request, pk):
    informe = get_object_or_404(InformeFinanciero, pk=pk)
    if request.method == 'POST':
        informe.delete()
        return redirect('admin_informes_list')
    return render(request, 'informes/admin_informes_confirm_delete.html', {'informe': informe})

@login_required
def descargar_informe_pdf(request, pk):
    try:
        informe = InformeFinanciero.objects.get(pk=pk)
    except InformeFinanciero.DoesNotExist:
        raise Http404('Informe no encontrado')
    if not informe.archivo:
        raise Http404('Archivo no disponible')
    # Leer PDF original
    original_pdf = informe.archivo.open('rb')
    reader = PdfReader(original_pdf)
    writer = PdfWriter()
    dni = getattr(request.user, 'dni', 'XXXXXXXX')
    watermark_io = io.BytesIO()
    c = canvas.Canvas(watermark_io, pagesize=letter)
    width, height = letter
    logo_path = settings.BASE_DIR / 'static/img/logo.png'
    logo = ImageReader(str(logo_path))
    logo_w, logo_h = 340, 340
    c.saveState()
    c.translate(width/2, height/2)
    c.rotate(30)
    c.setFillAlpha(0.12)
    c.drawImage(logo, -logo_w/2, -logo_h/2, width=logo_w, height=logo_h, mask='auto')
    c.restoreState()
    c.saveState()
    c.setFont('Helvetica-Bold', 38)
    c.setFillColorRGB(0.1, 0.1, 0.1, alpha=0.18)
    c.drawCentredString(width/2, (height-logo_h)/2 + logo_h + 40, "CONFIDENCIAL")
    c.restoreState()
    c.saveState()
    c.setFont('Helvetica-Bold', 28)
    c.setFillColorRGB(0.1, 0.1, 0.1, alpha=0.18)
    c.drawCentredString(width/2, (height-logo_h)/2 - 30, f"{dni}")
    c.restoreState()
    c.save()
    watermark_io.seek(0)
    watermark_pdf = PdfReader(watermark_io)
    watermark_page = watermark_pdf.pages[0]
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)
    output_io = io.BytesIO()
    writer.write(output_io)
    output_io.seek(0)
    filename = f"{informe.titulo}_confidencial.pdf"
    as_attachment = request.GET.get('descargar') == '1'
    return FileResponse(output_io, as_attachment=as_attachment, filename=filename)
