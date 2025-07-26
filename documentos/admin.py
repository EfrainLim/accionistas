from django.contrib import admin
from .models import DocumentoLegal

@admin.register(DocumentoLegal)
class DocumentoLegalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_publicacion', 'documento')
    list_filter = ('tipo', 'fecha_publicacion')
    search_fields = ('titulo', 'tipo')
    readonly_fields = ('fecha_publicacion',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'tipo', 'imagen', 'documento')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',),
        }),
    )
