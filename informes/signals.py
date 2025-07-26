from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
from .models import InformeFinanciero


@receiver(pre_delete, sender=InformeFinanciero)
def eliminar_archivos_informe(sender, instance, **kwargs):
    """
    Elimina los archivos físicos cuando se elimina un informe
    """
    # Eliminar archivo PDF
    if instance.archivo and instance.archivo.name:
        try:
            if default_storage.exists(instance.archivo.name):
                default_storage.delete(instance.archivo.name)
                print(f"Archivo PDF eliminado: {instance.archivo.name}")
        except Exception as e:
            print(f"Error eliminando archivo PDF {instance.archivo.name}: {e}")


@receiver(pre_save, sender=InformeFinanciero)
def eliminar_archivos_antiguos_informe(sender, instance, **kwargs):
    """
    Elimina los archivos antiguos cuando se edita un informe y se reemplaza el archivo
    """
    if instance.pk:  # Solo para informes existentes (edición)
        try:
            # Obtener la instancia original de la base de datos
            original = InformeFinanciero.objects.get(pk=instance.pk)
            
            # Verificar si se cambió el archivo PDF
            if original.archivo and instance.archivo and original.archivo != instance.archivo:
                try:
                    if default_storage.exists(original.archivo.name):
                        default_storage.delete(original.archivo.name)
                        print(f"Archivo PDF antiguo eliminado: {original.archivo.name}")
                except Exception as e:
                    print(f"Error eliminando archivo PDF antiguo {original.archivo.name}: {e}")
                    
        except InformeFinanciero.DoesNotExist:
            pass  # Es un nuevo informe
        except Exception as e:
            print(f"Error en pre_save signal de InformeFinanciero: {e}") 