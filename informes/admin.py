from django.contrib import admin
from .models import InformeFinanciero

@admin.register(InformeFinanciero)
class InformeFinancieroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_informe', 'periodicidad', 'area', 'fecha_publicacion', 'archivo')
    list_filter = ('tipo_informe', 'periodicidad', 'area', 'fecha_publicacion')
    search_fields = ('titulo', 'tipo_informe', 'area')
    readonly_fields = ('fecha_publicacion',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'tipo_informe', 'periodicidad', 'area', 'archivo')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',),
        }),
    )
