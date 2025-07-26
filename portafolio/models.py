from django.db import models

class Portafolio(models.Model):
    nombre = models.CharField(max_length=255, default='Accionista')
    dni = models.CharField(max_length=15, unique=True, default='00000000')
    acciones = models.IntegerField(default=0)
    valor_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_adquisicion = models.DateTimeField()

    def __str__(self):
        return f"{self.nombre} ({self.dni})"
