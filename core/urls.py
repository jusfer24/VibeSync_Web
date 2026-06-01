from django.urls import path
from . import views

urlpatterns = [
    # ==========================
    # AUTENTICACIÓN
    # ==========================
    path('', views.login_view, name='login'),

    # ==========================
    # RUTAS DE OYENTE
    # ==========================
    path('dashboard/', views.oyente_dashboard_view, name='oyente_dashboard'),
    path('explorar/', views.explorar_view, name='explorar'),
    path('eventos/', views.eventos_view, name='eventos'),
    path('gamificacion/', views.gamificacion_view, name='gamificacion'),
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),

    # ==========================
    # RUTAS DE DETALLE (Páginas internas)
    # ==========================
    path('artista/', views.artista_view, name='artista'),
    path('album/', views.album_view, name='album'),
    path('playlist/', views.playlist_view, name='playlist'),

    # ==========================
    # RUTAS DE ARTISTA
    # ==========================
    path('mi-musica/', views.artista_dashboard_view, name='artista_dashboard'),
    path('crear-album/', views.crear_album_view, name='crear_album'),
    path('subir-sencillo/', views.subir_sencillo_view, name='subir_sencillo'),
    path('regalias/', views.regalias_view, name='regalias'),

    # ==========================
    # RUTAS DE USUARIO (Globales)
    # ==========================
    path('perfil/', views.perfil_view, name='perfil'),
    path('suscripcion/', views.suscripcion_view, name='suscripcion'),
    path('ajustes/', views.ajustes_view, name='ajustes'),
    
    # ==========================
    # RUTAS DE ADMINISTRADOR
    # ==========================
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'), # <-- Ya no está duplicado
    path('admin-usuarios/', views.administrar_usuarios_view, name='administrar_usuarios'),
    path('admin-eventos/', views.admin_eventos_view, name='admin_eventos'),
    path('admin-insignias/', views.admin_insignias_view, name='admin_insignias'),
]