from django.db import models

# Create your models here.

class InformeFinanciero(models.Model):
    TIPO_INFORME_CHOICES = [
        ('financiero', 'Financiero'),
        ('area', 'Área'),
        ('gestion', 'Gestión'),
        ('auditoria', 'Auditoría'),
        ('proyecto', 'Proyecto'),
        ('otro', 'Otro'),
    ]
    PERIODICIDAD_CHOICES = [
        ('mensual', 'Mensual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral'),
        ('anual', 'Anual'),
        ('otro', 'Otro'),
    ]
    AREAS_CHOICES = [
        ('contabilidad', 'Contabilidad'),
        ('tesoreria', 'Tesorería'),
        ('operaciones', 'Operaciones'),
        ('comercial', 'Comercial'),
        ('rrhh', 'Recursos Humanos'),
        ('legal', 'Legal'),
        ('laboratorio', 'Laboratorio'),
        ('secretaria', 'Secretaría'),
        ('finanzas', 'Finanzas'),
        ('produccion', 'Producción'),
        ('administrativo', 'Administrativo'),
        ('seguridad', 'Seguridad'),
        ('ambiental', 'Ambiental'),
        ('planta', 'Planta'),
        ('secretaria', 'Secretaría'),
        ('gerencia', 'Gerencia'),
        ('gerencia_general', 'Gerencia General'),
        ('gerencia_administrativa', 'Gerencia Administrativa'),
        ('compras', 'Compras'),
        ('ventas', 'Ventas'),
        ('logistica', 'Logística'),
        ('sistemas', 'Sistemas'),
        ('otros', 'Otros'),
    ]
    titulo = models.CharField(max_length=255, default='')
    tipo_informe = models.CharField(max_length=20, choices=TIPO_INFORME_CHOICES, default='financiero')
    area = models.CharField(max_length=30, choices=AREAS_CHOICES, blank=True, null=True)
    periodicidad = models.CharField(max_length=15, choices=PERIODICIDAD_CHOICES, default='anual')
    archivo = models.FileField(upload_to='informes/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_informe_display()} - {self.get_periodicidad_display()} - {self.fecha_publicacion.date()})"
