from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, HttpResponseNotFound, HttpResponse
import os
from django.conf import settings
import zipfile
import io

@staff_member_required
def descargar_backup_sqlite(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if os.path.exists(db_path):
        return FileResponse(open(db_path, 'rb'), as_attachment=True, filename='backup_db.sqlite3')
    else:
        return HttpResponseNotFound("No se encontró la base de datos.")

@staff_member_required
def descargar_media_zip(request):
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        return HttpResponseNotFound("No se encontró la carpeta media.")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(media_root):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, media_root)
                zip_file.write(abs_path, rel_path)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='media_backup.zip') 