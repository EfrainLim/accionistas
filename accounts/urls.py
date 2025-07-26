from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
] 