from django.contrib import admin
from .models import ContactoConfig, MensajeSoporte
from django.urls import reverse
from django.utils.html import format_html

@admin.register(ContactoConfig)
class ContactoConfigAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'email', 'telefono', 'horario', 'backup_link', 'media_link')
    fieldsets = (
        (None, {
            'fields': ('direccion', 'email', 'telefono', 'horario', 'mapa_url', 'facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp')
        }),
    )

    def backup_link(self, obj):
        url = reverse('descargar_backup_sqlite')
        return format_html('<a class="button" href="{}" target="_blank">Descargar Backup DB</a>', url)
    backup_link.short_description = 'Backup DB SQLite'

    def media_link(self, obj):
        url = reverse('descargar_media_zip')
        return format_html('<a class="button" href="{}" target="_blank">Descargar Media ZIP</a>', url)
    media_link.short_description = 'Backup Carpeta Media'

@admin.register(MensajeSoporte)
class MensajeSoporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('fecha',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'email', 'asunto', 'mensaje', 'usuario')
        }),
        ('Fechas', {
            'fields': ('fecha',),
        }),
    )
