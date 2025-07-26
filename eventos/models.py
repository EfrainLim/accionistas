from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha.strftime('%Y-%m-%d')}"
