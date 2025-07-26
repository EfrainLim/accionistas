from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
    ]
    ROL_CHOICES = [
        ('accionista', 'Accionista'),
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    ]
    nombre = models.CharField(max_length=255)
    dni = models.CharField(max_length=15, unique=True, default='00000000')
    email = models.EmailField(unique=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='accionista')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']

    def __str__(self):
        return self.email

class ConfiguracionDashboard(models.Model):
    imagen_fondo = models.ImageField(upload_to='dashboard/', null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Configuración Dashboard'
        verbose_name_plural = 'Configuración Dashboard'
    def __str__(self):
        return 'Configuración Dashboard'
