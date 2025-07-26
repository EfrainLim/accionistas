from django.urls import path
from .views import informes_view, descargar_informe_pdf

urlpatterns = [
    path('', informes_view, name='informes'),
    path('descargar/<int:pk>/', descargar_informe_pdf, name='descargar_informe_pdf'),
] 