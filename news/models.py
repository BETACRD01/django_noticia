from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinLengthValidator


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Nombre de la categoría (ej: Tecnología, Deportes)"
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        blank=True,
        help_text="URL amigable generada automáticamente"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción opcional de la categoría"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('categoria_detail', kwargs={'slug': self.slug})
    
    def get_articulos_count(self):
        return self.articulos.count()


class Autor(models.Model):
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre completo del autor"
    )
    bio = models.TextField(
        validators=[MinLengthValidator(50)],
        help_text="Biografía del autor (mínimo 50 caracteres)"
    )
    foto = models.ImageField(
        upload_to='autores/', 
        blank=True, 
        null=True,
        help_text="Foto de perfil del autor"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email de contacto del autor"
    )
    fecha_ingreso = models.DateField(
        default=timezone.now,
        help_text="Fecha de ingreso al equipo"
    )
    activo = models.BooleanField(
        default=True,
        help_text="¿El autor está activo?"
    )
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('autor_detail', kwargs={'pk': self.pk})
    
    def get_articulos_count(self):
        return self.articulos.filter(publicado=True).count()
    
    def get_articulos_recientes(self, limit=5):
        return self.articulos.filter(publicado=True)[:limit]


class Articulo(models.Model):
    titulo = models.CharField(
        max_length=200,
        help_text="Título del artículo"
    )
    contenido = models.TextField(
        validators=[MinLengthValidator(100)],
        help_text="Contenido completo del artículo (mínimo 100 caracteres)"
    )
    resumen = models.TextField(
        max_length=300,
        blank=True,
        help_text="Resumen corto del artículo (máximo 300 caracteres)"
    )
    fecha_publicacion = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora de publicación"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(
        upload_to='articulos/', 
        blank=True, 
        null=True,
        help_text="Imagen principal del artículo"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='articulos',
        help_text="Categoría del artículo"
    )
    autor = models.ForeignKey(
        Autor, 
        on_delete=models.CASCADE, 
        related_name='articulos',
        help_text="Autor del artículo"
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True,
        help_text="URL amigable generada automáticamente"
    )
    destacado = models.BooleanField(
        default=False,
        help_text="¿Mostrar en artículos destacados?"
    )
    publicado = models.BooleanField(
        default=True,
        help_text="¿El artículo está publicado?"
    )
    vistas = models.PositiveIntegerField(
        default=0,
        help_text="Número de vistas del artículo"
    )
    
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_publicacion']
        indexes = [
            models.Index(fields=['-fecha_publicacion']),
            models.Index(fields=['categoria', '-fecha_publicacion']),
            models.Index(fields=['autor', '-fecha_publicacion']),
        ]
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if not self.resumen:
            self.resumen = self.contenido[:297] + "..."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('articulo_detail', kwargs={'pk': self.pk})
    
    def get_comentarios_count(self):
        return self.comentarios.count()
    
    def incrementar_vistas(self):
        self.vistas += 1
        self.save(update_fields=['vistas'])


class Comentario(models.Model):
    articulo = models.ForeignKey(
        Articulo, 
        on_delete=models.CASCADE, 
        related_name='comentarios',
        help_text="Artículo al que pertenece el comentario"
    )
    nombre_usuario = models.CharField(
        max_length=100,
        help_text="Nombre del usuario que comenta"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email del usuario (opcional)"
    )
    texto = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text="Contenido del comentario (mínimo 10 caracteres)"
    )
    fecha = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora del comentario"
    )
    aprobado = models.BooleanField(
        default=True,
        help_text="¿El comentario está aprobado?"
    )
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['fecha']
        indexes = [
            models.Index(fields=['articulo', 'fecha']),
        ]
    
    def __str__(self):
        return f'Comentario de {self.nombre_usuario} en {self.articulo.titulo}'
