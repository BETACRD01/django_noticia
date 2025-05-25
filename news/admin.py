from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Categoria, Autor, Articulo, Comentario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'get_articulos_count', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'get_articulos_count']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'slug', 'descripcion')
        }),
        ('Estadísticas', {
            'fields': ('get_articulos_count', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_articulos_count(self, obj):
        count = obj.get_articulos_count()
        url = reverse('admin:news_articulo_changelist') + f'?categoria__id__exact={obj.id}'
        return format_html('<a href="{}">{} artículos</a>', url, count)
    get_articulos_count.short_description = 'Artículos'


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'get_foto_thumbnail', 'get_articulos_count', 'activo', 'fecha_ingreso']
    list_filter = ['activo', 'fecha_ingreso']
    search_fields = ['nombre', 'email', 'bio']
    readonly_fields = ['get_articulos_count', 'get_foto_preview']
    list_editable = ['activo']
    
    fieldsets = (
        ('Información personal', {
            'fields': ('nombre', 'email', 'bio')
        }),
        ('Foto', {
            'fields': ('foto', 'get_foto_preview')
        }),
        ('Configuración', {
            'fields': ('activo', 'fecha_ingreso')
        }),
        ('Estadísticas', {
            'fields': ('get_articulos_count',),
            'classes': ('collapse',)
        }),
    )
    
    def get_foto_thumbnail(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.foto.url)
        return "Sin foto"
    get_foto_thumbnail.short_description = 'Foto'
    
    def get_foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="200" height="200" style="border-radius: 10px;" />', obj.foto.url)
        return "No hay foto"
    get_foto_preview.short_description = 'Vista previa'
    
    def get_articulos_count(self, obj):
        count = obj.get_articulos_count()
        url = reverse('admin:news_articulo_changelist') + f'?autor__id__exact={obj.id}'
        return format_html('<a href="{}">{} artículos</a>', url, count)
    get_articulos_count.short_description = 'Artículos publicados'


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'fecha_publicacion', 'destacado', 'publicado', 'vistas']
    list_filter = ['categoria', 'autor', 'fecha_publicacion', 'destacado', 'publicado']
    search_fields = ['titulo', 'contenido', 'resumen']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    list_editable = ['destacado', 'publicado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'vistas', 'get_imagen_preview', 'get_comentarios_count']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'slug', 'autor', 'categoria')
        }),
        ('Contenido', {
            'fields': ('resumen', 'contenido')
        }),
        ('Imagen', {
            'fields': ('imagen', 'get_imagen_preview')
        }),
        ('Configuración', {
            'fields': ('fecha_publicacion', 'destacado', 'publicado')
        }),
        ('Estadísticas', {
            'fields': ('vistas', 'get_comentarios_count', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_destacado', 'quitar_destacado', 'publicar', 'despublicar']
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="300" style="border-radius: 10px;" />', obj.imagen.url)
        return "No hay imagen"
    get_imagen_preview.short_description = 'Vista previa de imagen'
    
    def get_comentarios_count(self, obj):
        count = obj.get_comentarios_count()
        url = reverse('admin:news_comentario_changelist') + f'?articulo__id__exact={obj.id}'
        return format_html('<a href="{}">{} comentarios</a>', url, count)
    get_comentarios_count.short_description = 'Comentarios'
    
    def marcar_como_destacado(self, request, queryset):
        updated = queryset.update(destacado=True)
        self.message_user(request, f'{updated} artículos marcados como destacados.')
    marcar_como_destacado.short_description = "Marcar como destacado"
    
    def quitar_destacado(self, request, queryset):
        updated = queryset.update(destacado=False)
        self.message_user(request, f'{updated} artículos ya no son destacados.')
    quitar_destacado.short_description = "Quitar destacado"
    
    def publicar(self, request, queryset):
        updated = queryset.update(publicado=True)
        self.message_user(request, f'{updated} artículos publicados.')
    publicar.short_description = "Publicar artículos"
    
    def despublicar(self, request, queryset):
        updated = queryset.update(publicado=False)
        self.message_user(request, f'{updated} artículos despublicados.')
    despublicar.short_description = "Despublicar artículos"


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_usuario', 'get_articulo_link', 'fecha', 'aprobado', 'get_texto_preview']
    list_filter = ['aprobado', 'fecha', 'articulo__categoria']
    search_fields = ['nombre_usuario', 'texto', 'articulo__titulo', 'email']
    readonly_fields = ['fecha']
    list_editable = ['aprobado']
    
    fieldsets = (
        ('Información del comentario', {
            'fields': ('articulo', 'nombre_usuario', 'email')
        }),
        ('Contenido', {
            'fields': ('texto',)
        }),
        ('Configuración', {
            'fields': ('aprobado', 'fecha')
        }),
    )
    
    actions = ['aprobar_comentarios', 'rechazar_comentarios']
    
    def get_articulo_link(self, obj):
        url = reverse('admin:news_articulo_change', args=[obj.articulo.id])
        return format_html('<a href="{}">{}</a>', url, obj.articulo.titulo[:50])
    get_articulo_link.short_description = 'Artículo'
    
    def get_texto_preview(self, obj):
        return obj.texto[:100] + "..." if len(obj.texto) > 100 else obj.texto
    get_texto_preview.short_description = 'Vista previa'
    
    def aprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=True)
        self.message_user(request, f'{updated} comentarios aprobados.')
    aprobar_comentarios.short_description = "Aprobar comentarios"
    
    def rechazar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=False)
        self.message_user(request, f'{updated} comentarios rechazados.')
    rechazar_comentarios.short_description = "Rechazar comentarios"


# Personalización del admin
admin.site.site_header = "Administración de Noticias Hoy"
admin.site.site_title = "Noticias Hoy Admin"
admin.site.index_title = "Panel de Administración"
