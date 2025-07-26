import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Noticia

@receiver(pre_save, sender=Noticia)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Es una noticia nueva
    try:
        old_instance = Noticia.objects.get(pk=instance.pk)
    except Noticia.DoesNotExist:
        return
    # Para imagen
    if hasattr(old_instance, 'imagen') and old_instance.imagen and old_instance.imagen != instance.imagen:
        if os.path.isfile(old_instance.imagen.path):
            os.remove(old_instance.imagen.path)
    # Para archivo
    if hasattr(old_instance, 'archivo') and old_instance.archivo and old_instance.archivo != instance.archivo:
        if os.path.isfile(old_instance.archivo.path):
            os.remove(old_instance.archivo.path)

@receiver(post_delete, sender=Noticia)
def delete_file_on_delete(sender, instance, **kwargs):
    if hasattr(instance, 'imagen') and instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)
    if hasattr(instance, 'archivo') and instance.archivo and os.path.isfile(instance.archivo.path):
        os.remove(instance.archivo.path) 