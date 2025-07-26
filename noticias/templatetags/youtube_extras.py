from django import template
import re

register = template.Library()

def youtube_embed_url(url):
    """
    Convierte una URL de YouTube a formato embed.
    """
    if not url:
        return ''
    # Soporta enlaces tipo https://www.youtube.com/watch?v=ID o https://youtu.be/ID
    patterns = [
        r'youtube\.com/watch\?v=([\w-]+)',
        r'youtu\.be/([\w-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    return url  # Si no es YouTube, retorna la original

@register.filter
def youtube_embed(url):
    return youtube_embed_url(url)

@register.filter
def youtube_id(url):
    """
    Extrae solo el ID del video de YouTube de una URL.
    """
    if not url:
        return ''
    patterns = [
        r'youtube\.com/watch\?v=([\w-]+)',
        r'youtu\.be/([\w-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return '' 