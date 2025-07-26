from django.db import models

# Create your models here.

class Noticia(models.Model):
    CATEGORIA_CHOICES = [
        ('business', 'Negocios'),
        ('economy', 'Economía'),
        ('politics', 'Política'),
        ('life', 'Vida'),
        ('world', 'Mundo'),
        ('other', 'Otro'),
    ]
    titulo = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='other')
    imagen = models.ImageField(upload_to='noticias/imagenes/', null=True, blank=True)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='noticias/', null=True, blank=True)
    autor = models.CharField(max_length=100, null=True, blank=True)
    video_url = models.URLField(max_length=300, null=True, blank=True, help_text='Enlace a video externo (YouTube, Vimeo, etc.)')
    enlace_externo = models.URLField(max_length=300, null=True, blank=True, help_text='Enlace externo relacionado (fuente, leer más, etc.)')
    destacada_en_dashboard = models.BooleanField(default=False, verbose_name='Destacar en Dashboard')
    destacada_hasta = models.DateTimeField(null=True, blank=True, verbose_name='Destacar hasta')

    def __str__(self):
        return self.titulo
