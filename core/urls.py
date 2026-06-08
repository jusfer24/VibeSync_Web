from django.urls import path
from . import views

# ─────────────────────────────────────────────
# URL PATTERNS — VibeSync
# ─────────────────────────────────────────────
urlpatterns = [

    # ── AUTENTICACIÓN ──────────────────────────
    path("",            views.login_view, name="login"),
    path("logout/",     views.login_view, name="logout"),   # simple redirect al login

    # ── OYENTE ─────────────────────────────────
    path("dashboard/",    views.oyente_dashboard_view, name="oyente_dashboard"),
    path("explorar/",     views.explorar_view,         name="explorar"),
    path("eventos/",      views.eventos_view,          name="eventos"),
    path("gamificacion/", views.gamificacion_view,     name="gamificacion"),
    path("biblioteca/",   views.biblioteca_view,       name="biblioteca"),

    # ── DETALLE ────────────────────────────────
    path("artista/",  views.artista_view,  name="artista"),
    path("album/",    views.album_view,    name="album"),
    path("playlist/", views.playlist_view, name="playlist"),

    # ── ARTISTA ────────────────────────────────
    path("mi-musica/",      views.artista_dashboard_view, name="artista_dashboard"),
    path("crear-album/",    views.crear_album_view,       name="crear_album"),
    path("subir-sencillo/", views.subir_sencillo_view,    name="subir_sencillo"),
    path("regalias/",       views.regalias_view,          name="regalias"),

    # ── ADMINISTRADOR ──────────────────────────
    path("admin-panel/",    views.admin_dashboard_view,    name="admin_dashboard"),
    path("admin-usuarios/", views.administrar_usuarios_view, name="administrar_usuarios"),
    path("admin-eventos/",  views.admin_eventos_view,      name="admin_eventos"),
    path("admin-insignias/",views.admin_insignias_view,    name="admin_insignias"),

    # ── GLOBALES ───────────────────────────────
    path("perfil/",       views.perfil_view,       name="perfil"),
    path("suscripcion/",  views.suscripcion_view,  name="suscripcion"),
    path("ajustes/",      views.ajustes_view,      name="ajustes"),

    # ── PÁGINAS DE ERROR (acceso directo) ──────
    path("404/", views.error_404_view,  name="error_404"),
    path("500/", views.error_500_view,  name="error_500"),
    path("403/", views.error_403_view,  name="error_403"),
    path("400/", views.error_400_view,  name="error_400"),
]

# ── HANDLERS GLOBALES (Django los usa automáticamente) ──
handler400 = "core.views.error_400_view"
handler403 = "core.views.error_403_view"
handler404 = "core.views.error_404_view"
handler500 = "core.views.error_500_view"