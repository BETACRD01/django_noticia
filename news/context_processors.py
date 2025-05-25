from .models import Categoria, Articulo
from django.db.models import Count, Q


def global_context(request):
    """Context processor para variables globales disponibles en todas las plantillas"""
    return {
        'categorias_menu': Categoria.objects.annotate(
            articulos_count=Count('articulos', filter=Q(articulos__publicado=True))
        ).filter(articulos_count__gt=0)[:6],
        'articulos_sidebar': Articulo.objects.filter(
            publicado=True
        ).order_by('-vistas')[:5],
        'site_name': 'Noticias Hoy',
        'site_description': 'Tu fuente de información confiable'
    }
