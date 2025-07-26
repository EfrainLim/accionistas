from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
from .models import DocumentoLegal


@receiver(pre_delete, sender=DocumentoLegal)
def eliminar_archivos_documento(sender, instance, **kwargs):
    """
    Elimina los archivos físicos cuando se elimina un documento
    """
    # Eliminar archivo PDF
    if instance.documento and instance.documento.name:
        try:
            if default_storage.exists(instance.documento.name):
                default_storage.delete(instance.documento.name)
                print(f"Archivo PDF eliminado: {instance.documento.name}")
        except Exception as e:
            print(f"Error eliminando archivo PDF {instance.documento.name}: {e}")
    
    # Eliminar imagen
    if instance.imagen and instance.imagen.name:
        try:
            if default_storage.exists(instance.imagen.name):
                default_storage.delete(instance.imagen.name)
                print(f"Imagen eliminada: {instance.imagen.name}")
        except Exception as e:
            print(f"Error eliminando imagen {instance.imagen.name}: {e}")


@receiver(pre_save, sender=DocumentoLegal)
def eliminar_archivos_antiguos_documento(sender, instance, **kwargs):
    """
    Elimina los archivos antiguos cuando se edita un documento y se reemplazan los archivos
    También elimina la imagen si se limpia (se borra desde el admin o formulario)
    """
    if instance.pk:  # Solo para documentos existentes (edición)
        try:
            # Obtener la instancia original de la base de datos
            original = DocumentoLegal.objects.get(pk=instance.pk)
            
            # Verificar si se cambió el archivo PDF
            if original.documento and instance.documento and original.documento != instance.documento:
                try:
                    if default_storage.exists(original.documento.name):
                        default_storage.delete(original.documento.name)
                        print(f"Archivo PDF antiguo eliminado: {original.documento.name}")
                except Exception as e:
                    print(f"Error eliminando archivo PDF antiguo {original.documento.name}: {e}")
            
            # Verificar si se cambió la imagen
            if original.imagen and instance.imagen and original.imagen != instance.imagen:
                try:
                    if default_storage.exists(original.imagen.name):
                        default_storage.delete(original.imagen.name)
                        print(f"Imagen antigua eliminada: {original.imagen.name}")
                except Exception as e:
                    print(f"Error eliminando imagen antigua {original.imagen.name}: {e}")
            # Eliminar imagen si se limpió (se dejó en blanco)
            if original.imagen and not instance.imagen:
                try:
                    if default_storage.exists(original.imagen.name):
                        default_storage.delete(original.imagen.name)
                        print(f"Imagen eliminada por limpieza: {original.imagen.name}")
                except Exception as e:
                    print(f"Error eliminando imagen por limpieza {original.imagen.name}: {e}")
        except DocumentoLegal.DoesNotExist:
            pass  # Es un nuevo documento
        except Exception as e:
            print(f"Error en pre_save signal de DocumentoLegal: {e}") 