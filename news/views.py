from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q, Count
import json
from .models import Articulo, Categoria, Autor, Comentario


class HomeView(ListView):
    model = Articulo
    template_name = 'news/home.html'
    context_object_name = 'articulos'
    paginate_by = 9
    
    def get_queryset(self):
        return Articulo.objects.filter(
            publicado=True, 
            destacado=True
        ).select_related('autor', 'categoria').order_by('-fecha_publicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.annotate(
            articulos_count=Count('articulos', filter=Q(articulos__publicado=True))
        ).filter(articulos_count__gt=0)
        context['articulos_recientes'] = Articulo.objects.filter(
            publicado=True
        ).select_related('autor', 'categoria')[:6]
        context['autores_destacados'] = Autor.objects.filter(
            activo=True
        ).annotate(
            articulos_count=Count('articulos', filter=Q(articulos__publicado=True))
        ).filter(articulos_count__gt=0)[:4]
        return context


class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'news/articulo_detail.html'
    context_object_name = 'articulo'
    
    def get_queryset(self):
        return Articulo.objects.filter(publicado=True).select_related('autor', 'categoria')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Incrementar vistas
        obj.incrementar_vistas()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener comentarios aprobados ordenados por fecha (más recientes primero)
        context['comentarios'] = self.object.comentarios.filter(
            aprobado=True
        ).order_by('-fecha')
        
        context['articulos_relacionados'] = Articulo.objects.filter(
            categoria=self.object.categoria,
            publicado=True
        ).exclude(pk=self.object.pk).select_related('autor')[:3]
        return context


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'news/categoria_detail.html'
    context_object_name = 'categoria'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulos_list = self.object.articulos.filter(
            publicado=True
        ).select_related('autor').order_by('-fecha_publicacion')
        
        paginator = Paginator(articulos_list, 12)
        page_number = self.request.GET.get('page')
        context['articulos'] = paginator.get_page(page_number)
        return context


class AutorDetailView(DetailView):
    model = Autor
    template_name = 'news/autor_detail.html'
    context_object_name = 'autor'
    
    def get_queryset(self):
        return Autor.objects.filter(activo=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulos_list = self.object.articulos.filter(
            publicado=True
        ).select_related('categoria').order_by('-fecha_publicacion')
        
        paginator = Paginator(articulos_list, 12)
        page_number = self.request.GET.get('page')
        context['articulos'] = paginator.get_page(page_number)
        return context


class AutoresListView(ListView):
    model = Autor
    template_name = 'news/autores_list.html'
    context_object_name = 'autores'
    
    def get_queryset(self):
        return Autor.objects.filter(activo=True).annotate(
            articulos_count=Count('articulos', filter=Q(articulos__publicado=True))
        ).order_by('nombre')  # Removí el filtro que causaba el problema


class BusquedaView(ListView):
    model = Articulo
    template_name = 'news/busqueda.html'
    context_object_name = 'articulos'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Articulo.objects.filter(
                Q(titulo__icontains=query) | 
                Q(contenido__icontains=query) | 
                Q(resumen__icontains=query),
                publicado=True
            ).select_related('autor', 'categoria').order_by('-fecha_publicacion')
        return Articulo.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


@csrf_exempt
def agregar_comentario(request):
    """Vista para agregar comentarios vía AJAX"""
    if request.method == 'POST':
        try:
            # Obtener la IP del usuario
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip
            
            data = json.loads(request.body)
            articulo_id = data.get('articulo_id')
            nombre_usuario = data.get('nombre_usuario', '').strip()
            email = data.get('email', '').strip()
            texto = data.get('texto', '').strip()
            
            print(f"Datos recibidos: {data}")  # Debug
            
            # Validaciones
            if not articulo_id:
                return JsonResponse({
                    'error': 'ID del artículo es requerido'
                }, status=400)
            
            if not nombre_usuario:
                return JsonResponse({
                    'error': 'El nombre es requerido'
                }, status=400)
            
            if not texto:
                return JsonResponse({
                    'error': 'El comentario es requerido'
                }, status=400)
            
            if len(texto) < 10:
                return JsonResponse({
                    'error': 'El comentario debe tener al menos 10 caracteres'
                }, status=400)
            
            if len(nombre_usuario) > 100:
                return JsonResponse({
                    'error': 'El nombre no puede tener más de 100 caracteres'
                }, status=400)
            
            if len(texto) > 1000:
                return JsonResponse({
                    'error': 'El comentario no puede tener más de 1000 caracteres'
                }, status=400)
            
            # Validar email si se proporciona
            if email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return JsonResponse({
                        'error': 'El formato del email no es válido'
                    }, status=400)
            
            # Verificar que el artículo existe y está publicado
            try:
                articulo = Articulo.objects.get(id=articulo_id, publicado=True)
            except Articulo.DoesNotExist:
                return JsonResponse({
                    'error': 'El artículo no existe o no está publicado'
                }, status=404)
            
            # Crear el comentario
            comentario = Comentario.objects.create(
                articulo=articulo,
                nombre_usuario=nombre_usuario,
                email=email,
                texto=texto,
                aprobado=True,  # Los comentarios se aprueban automáticamente
                ip_address=get_client_ip(request)
            )
            
            print(f"Comentario creado: {comentario}")  # Debug
            
            return JsonResponse({
                'success': True,
                'comentario': {
                    'id': comentario.id,
                    'nombre_usuario': comentario.nombre_usuario,
                    'texto': comentario.texto,
                    'fecha': comentario.fecha.strftime('%d de %B de %Y, %H:%M')
                },
                'mensaje': 'Comentario agregado exitosamente'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Datos JSON inválidos'
            }, status=400)
        except Exception as e:
            print(f"Error al crear comentario: {str(e)}")  # Debug
            return JsonResponse({
                'error': f'Error interno del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'error': 'Método no permitido'
    }, status=405)


def estadisticas_view(request):
    """Vista para mostrar estadísticas del sitio"""
    context = {
        'total_articulos': Articulo.objects.filter(publicado=True).count(),
        'total_categorias': Categoria.objects.count(),
        'total_autores': Autor.objects.filter(activo=True).count(),
        'total_comentarios': Comentario.objects.filter(aprobado=True).count(),
        'articulos_mas_vistos': Articulo.objects.filter(
            publicado=True
        ).order_by('-vistas')[:5],
        'categorias_populares': Categoria.objects.annotate(
            articulos_count=Count('articulos', filter=Q(articulos__publicado=True))
        ).filter(articulos_count__gt=0).order_by('-articulos_count')[:5]
    }
    return render(request, 'news/estadisticas.html', context)
