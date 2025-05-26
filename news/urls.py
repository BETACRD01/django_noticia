from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articulo/<int:pk>/', views.ArticuloDetailView.as_view(), name='articulo_detail'),
    path('categoria/<slug:slug>/', views.CategoriaDetailView.as_view(), name='categoria_detail'),
    path('autor/<int:pk>/', views.AutorDetailView.as_view(), name='autor_detail'),
    path('autores/', views.AutoresListView.as_view(), name='autores_list'),
    path('buscar/', views.BusquedaView.as_view(), name='busqueda'),
    path('estadisticas/', views.estadisticas_view, name='estadisticas'),
    path('api/comentario/', views.agregar_comentario, name='agregar_comentario'),
]
