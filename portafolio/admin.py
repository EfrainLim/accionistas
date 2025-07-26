from django.contrib import admin
from .models import Portafolio

class PortafolioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'acciones', 'valor_actual', 'fecha_adquisicion')
    search_fields = ('nombre', 'dni')
    list_filter = ('fecha_adquisicion',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'dni', 'acciones', 'valor_actual', 'fecha_adquisicion')
        }),
    )

admin.site.register(Portafolio, PortafolioAdmin)
