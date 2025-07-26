from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
from .models import ConfiguracionDashboard

@receiver(pre_save, sender=ConfiguracionDashboard)
def eliminar_imagen_antigua_dashboard(sender, instance, **kwargs):
    """
    Elimina la imagen anterior cuando se actualiza la configuración del dashboard
    """
    if instance.pk:
        try:
            original = ConfiguracionDashboard.objects.get(pk=instance.pk)
            
            # Si hay una imagen anterior y es diferente a la nueva
            if original.imagen_fondo and instance.imagen_fondo and original.imagen_fondo != instance.imagen_fondo:
                try:
                    if default_storage.exists(original.imagen_fondo.name):
                        default_storage.delete(original.imagen_fondo.name)
                        print(f"Imagen anterior del dashboard eliminada: {original.imagen_fondo.name}")
                except Exception as e:
                    print(f"Error eliminando imagen anterior del dashboard {original.imagen_fondo.name}: {e}")
            
            # Si se limpia la imagen (se deja en blanco)
            elif original.imagen_fondo and not instance.imagen_fondo:
                try:
                    if default_storage.exists(original.imagen_fondo.name):
                        default_storage.delete(original.imagen_fondo.name)
                        print(f"Imagen del dashboard eliminada por limpieza: {original.imagen_fondo.name}")
                except Exception as e:
                    print(f"Error eliminando imagen del dashboard por limpieza {original.imagen_fondo.name}: {e}")
                    
        except ConfiguracionDashboard.DoesNotExist:
            pass
        except Exception as e:
            print(f"Error en pre_save signal de ConfiguracionDashboard: {e}")

@receiver(pre_delete, sender=ConfiguracionDashboard)
def eliminar_imagen_dashboard(sender, instance, **kwargs):
    """
    Elimina la imagen cuando se elimina la configuración del dashboard
    """
    if instance.imagen_fondo and instance.imagen_fondo.name:
        try:
            if default_storage.exists(instance.imagen_fondo.name):
                default_storage.delete(instance.imagen_fondo.name)
                print(f"Imagen del dashboard eliminada: {instance.imagen_fondo.name}")
        except Exception as e:
            print(f"Error eliminando imagen del dashboard {instance.imagen_fondo.name}: {e}") 