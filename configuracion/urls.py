from django.urls import path
from .views import configuracion_view
from .views import administrar_view, admin_dashboard_config
from portafolio.views import admin_portafolio_list, admin_portafolio_create, admin_portafolio_edit, admin_portafolio_delete
from noticias.views import admin_noticias_list, admin_noticias_create, admin_noticias_edit, admin_noticias_delete
from informes.views import admin_informes_list, admin_informes_create, admin_informes_edit, admin_informes_delete
from documentos.views import admin_documentos_list, admin_documentos_create, admin_documentos_edit, admin_documentos_delete
from soporte.views import admin_soporte_list, admin_soporte_detail, admin_soporte_delete, admin_contacto_config

urlpatterns = [
    path('', configuracion_view, name='configuracion'),
    path('administrar/', administrar_view, name='administrar'),
    path('administrar/dashboard/', admin_dashboard_config, name='admin_dashboard_config'),
    path('administrar/accionistas/', admin_portafolio_list, name='admin_portafolio_list'),
    path('administrar/accionistas/crear/', admin_portafolio_create, name='admin_portafolio_create'),
    path('administrar/accionistas/<int:pk>/editar/', admin_portafolio_edit, name='admin_portafolio_edit'),
    path('administrar/accionistas/<int:pk>/eliminar/', admin_portafolio_delete, name='admin_portafolio_delete'),
    path('administrar/noticias/', admin_noticias_list, name='admin_noticias_list'),
    path('administrar/noticias/crear/', admin_noticias_create, name='admin_noticias_create'),
    path('administrar/noticias/<int:pk>/editar/', admin_noticias_edit, name='admin_noticias_edit'),
    path('administrar/noticias/<int:pk>/eliminar/', admin_noticias_delete, name='admin_noticias_delete'),
    path('administrar/informes/', admin_informes_list, name='admin_informes_list'),
    path('administrar/informes/crear/', admin_informes_create, name='admin_informes_create'),
    path('administrar/informes/<int:pk>/editar/', admin_informes_edit, name='admin_informes_edit'),
    path('administrar/informes/<int:pk>/eliminar/', admin_informes_delete, name='admin_informes_delete'),
    path('administrar/documentos/', admin_documentos_list, name='admin_documentos_list'),
    path('administrar/documentos/crear/', admin_documentos_create, name='admin_documentos_create'),
    path('administrar/documentos/<int:pk>/editar/', admin_documentos_edit, name='admin_documentos_edit'),
    path('administrar/documentos/<int:pk>/eliminar/', admin_documentos_delete, name='admin_documentos_delete'),
    path('administrar/soporte/', admin_soporte_list, name='admin_soporte_list'),
    path('administrar/soporte/<int:pk>/', admin_soporte_detail, name='admin_soporte_detail'),
    path('administrar/soporte/<int:pk>/eliminar/', admin_soporte_delete, name='admin_soporte_delete'),
    path('administrar/soporte/configuracion/', admin_contacto_config, name='admin_contacto_config'),
] 