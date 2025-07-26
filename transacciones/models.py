from django.db import models
from accounts.models import Usuario

# Create your models here.

class HistorialTransaccion(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateTimeField()

    def __str__(self):
        return f"{self.tipo.title()} de {self.cantidad} acciones por {self.usuario.email} el {self.fecha_transaccion.strftime('%Y-%m-%d')}"
