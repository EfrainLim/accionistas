from django.urls import path
from .views import noticias_view, noticia_detalle_view

urlpatterns = [
    path('', noticias_view, name='noticias'),
    path('<int:noticia_id>/', noticia_detalle_view, name='noticia_detalle'),
] 