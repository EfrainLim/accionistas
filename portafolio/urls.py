from django.urls import path
from .views import portafolio_view

urlpatterns = [
    path('', portafolio_view, name='portafolio'),
] 