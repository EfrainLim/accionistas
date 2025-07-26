from django.urls import path
from . import views
from .admin_backup import descargar_backup_sqlite, descargar_media_zip

urlpatterns = [
    path('', views.soporte_view, name='soporte'),
    path('admin/backup/', descargar_backup_sqlite, name='descargar_backup_sqlite'),
    path('admin/backup-media/', descargar_media_zip, name='descargar_media_zip'),
] 