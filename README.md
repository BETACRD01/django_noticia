# Sitio de Noticias - Django

Un sitio web completo de noticias desarrollado con Django 4+, que incluye gestión de artículos, categorías, autores y comentarios con un diseño moderno y responsivo.

## 🚀 Características

### Backend (Django)
- ✅ **Modelos bien estructurados**: Categoria, Autor, Articulo, Comentario
- ✅ **Panel de administración personalizado** con Django Admin
- ✅ **Vistas basadas en clases** siguiendo buenas prácticas
- ✅ **URLs organizadas** por aplicación
- ✅ **Base de datos SQLite** (fácil migración a PostgreSQL)
- ✅ **API REST** para comentarios con AJAX
- ✅ **Sistema de búsqueda** avanzado
- ✅ **Contador de vistas** automático
- ✅ **Validaciones** robustas en modelos

### Frontend
- ✅ **Diseño responsivo** con Bootstrap 5
- ✅ **Plantilla base** reutilizable y moderna
- ✅ **Páginas dinámicas**: inicio, detalle, categorías, autores
- ✅ **Sistema de comentarios** interactivo con AJAX
- ✅ **Navegación intuitiva** con menús desplegables
- ✅ **Búsqueda en tiempo real**
- ✅ **Paginación** elegante
- ✅ **Breadcrumbs** para navegación
- ✅ **Sidebar** con contenido relacionado

## 📋 Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Descargar el proyecto
Descarga todos los archivos del proyecto usando el botón "Download Code"

### 2. Crear entorno virtual
\`\`\`bash
cd django-news-site
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Ejecutar migraciones
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 5. Crear superusuario
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 6. Cargar datos de ejemplo (opcional)
\`\`\`bash
python manage.py shell
\`\`\`

Luego ejecutar:
\`\`\`python
from news.models import Categoria, Autor, Articulo

# Crear categorías
tech = Categoria.objects.create(nombre="Tecnología", descripcion="Noticias sobre tecnología e innovación")
env = Categoria.objects.create(nombre="Medio Ambiente", descripcion="Noticias ambientales y sostenibilidad")
sports = Categoria.objects.create(nombre="Deportes", descripcion="Noticias deportivas y competiciones")

# Crear autores
autor1 = Autor.objects.create(
    nombre="Ana García",
    bio="Periodista especializada en tecnología con más de 10 años de experiencia cubriendo innovaciones en Silicon Valley.",
    email="ana.garcia@noticiashoy.com"
)

autor2 = Autor.objects.create(
    nombre="Carlos López",
    bio="Reportero ambiental enfocado en cambio climático y políticas de sostenibilidad.",
    email="carlos.lopez@noticiashoy.com"
)

# Crear artículos de ejemplo
Articulo.objects.create(
    titulo="Avances en Inteligencia Artificial transforman la industria",
    contenido="Los últimos desarrollos en inteligencia artificial están revolucionando múltiples sectores de la economía global...",
    resumen="La IA está cambiando la forma en que trabajamos y vivimos.",
    categoria=tech,
    autor=autor1,
    destacado=True
)

Articulo.objects.create(
    titulo="Nuevas políticas ambientales buscan reducir emisiones",
    contenido="El gobierno anuncia un paquete de medidas para combatir el cambio climático...",
    resumen="Políticas ambientales para un futuro sostenible.",
    categoria=env,
    autor=autor2,
    destacado=True
)

print("Datos de ejemplo creados exitosamente!")
\`\`\`

### 7. Ejecutar servidor de desarrollo
\`\`\`bash
python manage.py runserver
\`\`\`

### 8. Acceder a la aplicación
- **Sitio web**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

\`\`\`
django-news-site/
├── manage.py                 # Comando principal de Django
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Este archivo
├── news_site/               # Configuración principal
│   ├── __init__.py
│   ├── settings.py          # Configuraciones de Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── news/                    # Aplicación principal
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Configuración del admin
│   └── context_processors.py # Procesadores de contexto
└── templates/              # Plantillas HTML
    ├── base.html           # Plantilla base
    └── news/               # Plantillas específicas
        └── home.html       # Página principal
\`\`\`

## 🎯 **¡Proyecto Django Completo!**

Este proyecto incluye:

### ✅ **Características Implementadas:**
- **Backend Django completo** con modelos, vistas, admin
- **Frontend moderno** con Bootstrap 5 y diseño responsivo
- **Sistema de comentarios** con AJAX
- **Panel de administración** personalizado
- **Búsqueda avanzada** y paginación
- **Contador de vistas** automático
- **Validaciones** robustas

### 🚀 **Para usar el proyecto:**

1. **Descarga** todos los archivos usando el botón "Download Code"
2. **Instala** las dependencias: `pip install -r requirements.txt`
3. **Ejecuta** las migraciones: `python manage.py migrate`
4. **Crea** un superusuario: `python manage.py createsuperuser`
5. **Inicia** el servidor: `python manage.py runserver`

¡El proyecto está completamente funcional y listo para usar! 🎉

---

**¡Desarrollado con ❤️ usando Django 4+ y Bootstrap 5!** 🚀📰
