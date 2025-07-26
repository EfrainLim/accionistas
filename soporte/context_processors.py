from .models import ContactoConfig

def contacto_config(request):
    config = ContactoConfig.objects.first()
    return {'contacto_config': config} 