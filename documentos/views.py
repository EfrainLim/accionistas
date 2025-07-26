from django.shortcuts import render
from accounts.decorators import aprobado_required
from .models import DocumentoLegal
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .forms import DocumentoLegalForm
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.conf import settings
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from accounts.models import Usuario
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.cache import cache_page

from django.contrib.auth.decorators import login_required

@aprobado_required
def documentos_view(request):
    tipo = request.GET.get('tipo')
    search = request.GET.get('search', '')
    documentos = DocumentoLegal.objects.all().order_by('-fecha_publicacion')
    if tipo:
        documentos = documentos.filter(tipo=tipo)
    if search:
        documentos = documentos.filter(Q(titulo__icontains=search))
    paginator = Paginator(documentos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'documentos/documentos.html', {
        'documentos': page_obj.object_list,
        'tipo_actual': tipo,
        'search': search,
        'page_obj': page_obj,
    })

admin_required = user_passes_test(lambda u: u.is_superuser or getattr(u, 'rol', '') == 'admin')

@admin_required
def admin_documentos_list(request):
    search = request.GET.get('search', '')
    documentos = DocumentoLegal.objects.all().order_by('-fecha_publicacion')
    if search:
        documentos = documentos.filter(titulo__icontains=search)
    paginator = Paginator(documentos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'documentos/admin_documentos_list.html', {'documentos': page_obj.object_list, 'search': search, 'page_obj': page_obj})

@admin_required
def admin_documentos_create(request):
    if request.method == 'POST':
        form = DocumentoLegalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_documentos_list')
    else:
        form = DocumentoLegalForm()
    return render(request, 'documentos/admin_documentos_form.html', {'form': form, 'accion': 'Crear'})

@admin_required
def admin_documentos_edit(request, pk):
    documento = get_object_or_404(DocumentoLegal, pk=pk)
    if request.method == 'POST':
        form = DocumentoLegalForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('admin_documentos_list')
    else:
        form = DocumentoLegalForm(instance=documento)
    return render(request, 'documentos/admin_documentos_form.html', {'form': form, 'accion': 'Editar'})

@admin_required
def admin_documentos_delete(request, pk):
    documento = get_object_or_404(DocumentoLegal, pk=pk)
    if request.method == 'POST':
        documento.delete()
        return redirect('admin_documentos_list')
    return render(request, 'documentos/admin_documentos_confirm_delete.html', {'documento': documento})

@login_required
def descargar_documento_pdf(request, pk):
    try:
        documento = DocumentoLegal.objects.get(pk=pk)
    except DocumentoLegal.DoesNotExist:
        raise Http404('Documento no encontrado')
    if not documento.documento:
        raise Http404('Archivo no disponible')
    original_pdf = documento.documento.open('rb')
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
    filename = f"{documento.titulo}_confidencial.pdf"
    as_attachment = request.GET.get('descargar') == '1'
    return FileResponse(output_io, as_attachment=as_attachment, filename=filename)
