from django.urls import path
from .views import documentos_view, descargar_documento_pdf

urlpatterns = [
    path('', documentos_view, name='documentos'),
    path('descargar/<int:pk>/', descargar_documento_pdf, name='descargar_documento_pdf'),
] 