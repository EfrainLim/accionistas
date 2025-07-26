from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha_publicacion', 'autor', 'destacada_en_dashboard', 'destacada_hasta')
    list_filter = ('categoria', 'fecha_publicacion', 'destacada_en_dashboard')
    search_fields = ('titulo', 'contenido', 'autor')
    readonly_fields = ('fecha_publicacion',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'categoria', 'imagen', 'contenido', 'archivo', 'autor', 'video_url', 'enlace_externo', 'destacada_en_dashboard', 'destacada_hasta')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',),
        }),
    )
