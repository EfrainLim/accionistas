from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ConfiguracionDashboard

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'dni', 'estado', 'rol', 'is_superuser', 'is_staff')
    list_filter = ('estado', 'rol', 'is_superuser', 'is_staff')
    search_fields = ('email', 'nombre', 'dni')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nombre', 'dni', 'estado', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined', 'fecha_registro', 'fecha_aprobacion')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'dni', 'password1', 'password2', 'estado', 'rol', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('fecha_registro', 'fecha_aprobacion', 'last_login', 'date_joined')

@admin.register(ConfiguracionDashboard)
class ConfiguracionDashboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'actualizado')
    readonly_fields = ('actualizado',)
