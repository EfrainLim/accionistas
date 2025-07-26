from django.db import models
from accounts.models import Usuario

# Create your models here.

class ContactoConfig(models.Model):
    direccion = models.CharField(max_length=255, default='')
    email = models.EmailField(default='')
    telefono = models.CharField(max_length=50, default='')
    horario = models.CharField(max_length=100, default='')
    mapa_url = models.URLField(default='')
    facebook = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    instagram = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    whatsapp = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        verbose_name = 'Configuración de Contacto'
        verbose_name_plural = 'Configuración de Contacto'

    def __str__(self):
        return 'Configuración de Contacto'

class MensajeSoporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_soporte', null=True, blank=True)
    nombre = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    asunto = models.CharField(max_length=150, default='')
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soporte de {self.nombre} - {self.fecha.date()}"
