from django.db import models

# Create your models here.

class DocumentoLegal(models.Model):
    TIPO_CHOICES = [
        ('auditoria', 'Auditoría'),
        ('contrato', 'Contrato'),
        ('estatutario', 'Estatuto'),
        ('resoluciones', 'Resoluciones'),
        ('acuerdos', 'Acuerdos'),
        ('declaraciones', 'Declaraciones'),
        ('politica', 'Política'),
        ('procedimiento', 'Procedimiento'),
        ('reglamento', 'Reglamento'),
        ('otros', 'Otros'),
    ]
    titulo = models.CharField(max_length=255, default='')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    documento = models.FileField(upload_to='documentos/%Y/%m/')
    imagen = models.ImageField(upload_to='documentos/imagenes/%Y/%m/', null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()} - {self.fecha_publicacion.date()})"
