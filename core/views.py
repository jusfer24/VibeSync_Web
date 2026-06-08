from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.db import connection, OperationalError
import logging

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _fetch(sql, params=()):
    """Run a raw SQL query safely and return rows as dicts."""
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    except OperationalError as e:
        logger.error("DB error: %s", e)
        return []

def _get_artistas_locales(pais_id=1, limit=8):
    return _fetch(
        """SELECT TOP(%(lim)s)
               a.apodoArtista, a.tipoArtista,
               p.nombrePersona + \' \' + p.apellidoPersona AS nombreCompleto
           FROM Identidad.Artista a
           INNER JOIN Identidad.Persona p ON a.idPersona = p.idPersona
           WHERE a.paisResidencia = %(pais)s""",
        {"lim": limit, "pais": pais_id}
    )

def _get_tendencias(limit=6):
    return _fetch(
        """SELECT TOP(%(lim)s)
               c.nombreCancion AS nombre,
               COUNT(r.idReproduccion) AS total_plays
           FROM Musica.Cancion c
           LEFT JOIN Actividad.Reproduccion r ON r.Cancion_ISRC_Cancion = c.ISRC_Cancion
           GROUP BY c.nombreCancion, c.ISRC_Cancion
           ORDER BY total_plays DESC""",
        {"lim": limit}
    )

# ─────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────
def login_view(request):
    if request.method == "POST":
        user = request.POST.get("usuario", "").lower()
        if "admin" in user:
            return redirect("admin_dashboard")
        elif "artista" in user or "banda" in user:
            return redirect("artista_dashboard")
        else:
            return redirect("oyente_dashboard")
    return render(request, "core/login.html")

# ─────────────────────────────────────────────
# OYENTE
# ─────────────────────────────────────────────
def oyente_dashboard_view(request):
    artistas = _get_artistas_locales()
    tendencias = _get_tendencias()
    context = {
        "nombre_usuario": request.session.get("username", "Oyente"),
        "pais_usuario": "Ecuador",
        "artistas_locales": artistas,
        "tendencias": [{"nombre": t["nombre"]} for t in tendencias],
        "historial": [],
        "stats": {"horas": "4.2", "canciones": "28", "racha": "7"},
    }
    return render(request, "core/oyente_dashboard.html", context)

def explorar_view(request):
    q = request.GET.get("q", "").strip()
    context = {
        "historial_busquedas": [
            {"tipo_ui": "cancion", "titulo": "Synthwave Andino Mix",
             "subtitulo": "Canción · VibeSync", "inicial": "S", "color": "0d1422"},
            {"tipo_ui": "artista", "titulo": "Guardarraya",
             "subtitulo": "Artista",            "inicial": "G", "color": "0d2210"},
            {"tipo_ui": "album",   "titulo": "Noches de Quito",
             "subtitulo": "Álbum",              "inicial": "N", "color": "1c1000"},
        ],
        "resultado_principal": {
            "titulo": q or "VibeSync", "tipo": "Canción",
            "subtitulo": "Artista Local · Álbum VibeSync",
        },
        "canciones": [
            {"titulo": f"{q} (Remix)"   if q else "Remix",    "artista": "Artista", "duracion": "3:45"},
            {"titulo": f"{q} (Acústico)"if q else "Acústico", "artista": "Artista", "duracion": "4:10"},
        ],
        "albumes_relacionados": [
            {"titulo": "El Primer Disco", "tipo": "Álbum"},
            {"titulo": "Lados B",         "tipo": "EP"},
        ],
        "artistas_genero": [
            {"nombre": "La Máquina Camaleón", "tipo": "Artista"},
            {"nombre": "Guardarraya",         "tipo": "Artista"},
        ],
    }
    return render(request, "core/explorar.html", context)

def gamificacion_view(request):
    context = {
        "progreso": {"nivel": 12, "xp_faltante": 350,
                     "porcentaje": 65, "xp_total": "12,400"},
        "insignias": [
            {"icono": "🎧", "nombre": "Primer Play",
             "descripcion": "Reprodujiste tu primera canción.", "obtenida": True, "fecha": "Hace 45 días"},
            {"icono": "🌙", "nombre": "Noctámbulo",
             "descripcion": "Escuchaste +10 canciones nocturnas.", "obtenida": True, "fecha": "Hace 12 días"},
            {"icono": "🏔️", "nombre": "Explorador Andino",
             "descripcion": "Descubriste 5 artistas ecuatorianos.", "obtenida": True, "fecha": "Hace 5 días"},
            {"icono": "🎭", "nombre": "Mood Master",
             "descripcion": "Registra 5 estados de ánimo distintos.", "obtenida": False},
            {"icono": "⭐", "nombre": "Fan Destacado",
             "descripcion": "Escucha un álbum +20 veces.", "obtenida": False},
            {"icono": "🔥", "nombre": "En Llamas",
             "descripcion": "Escucha música 7 días seguidos.", "obtenida": False},
        ],
    }
    return render(request, "core/gamificacion.html", context)

def biblioteca_view(request):
    context = {
        "me_gusta": {
            "canciones": [{"titulo": "Crimen Perfecto", "artista": "Guardarraya"}],
            "albumes":   [{"titulo": "Signos",          "artista": "Guardarraya"}],
            "artistas":  [{"nombre": "Guardarraya",     "genero": "Rock Andino"}],
        },
        "albums_alfabetico": [
            {"titulo": "Noches de Quito", "artista": "Guardarraya"},
            {"titulo": "Ecos del Cotopaxi", "artista": "MatS"},
        ],
        "playlists_alfabetico": [
            {"nombre": "Vibra Local 🇪🇨", "total_canciones": 45},
            {"nombre": "Clásicos del Rock", "total_canciones": 42},
        ],
    }
    return render(request, "core/biblioteca.html", context)

def eventos_view(request):
    return render(request, "core/eventos.html", {"eventos": []})

# ─────────────────────────────────────────────
# DETALLE (Álbum / Artista / Playlist)
# ─────────────────────────────────────────────
def artista_view(request):
    context = {
        "artista": {
            "nombre": "La Máquina Camaleón",
            "oyentes_mensuales": "145,892",
            "color_hero": "linear-gradient(135deg,#2c3e50,#0d1422)",
            "imagen": "https://placehold.co/400x400/2c3e50/ffffff?text=LMC",
            "biografia": "Un proyecto sonoro nacido entre los páramos andinos.",
        },
        "canciones_populares": [
            {"numero": 1, "titulo": "El Gran Retorno",
             "reproducciones": "1,204,500", "duracion": "3:45"},
            {"numero": 2, "titulo": "Amarilla",
             "reproducciones": "985,200",   "duracion": "4:10"},
        ],
        "albumes": [
            {"titulo": "Amarilla",  "anio": "2017", "color": "f5a623"},
            {"titulo": "Camaleón",  "anio": "2020", "color": "2c3e50"},
        ],
    }
    return render(request, "core/artista.html", context)

def album_view(request):
    context = {
        "album": {
            "titulo": "Noches de Quito",
            "artista": "Guardarraya",
            "anio": "2023",
            "total_canciones": 8,
            "duracion_total": "32 min",
            "color_hero": "linear-gradient(135deg,#8e44ad,#0d1422)",
            "imagen": "https://placehold.co/400x400/8e44ad/ffffff?text=NDQ",
            "discografica": "Quito Play Music S.A.",
        },
        "canciones": [
            {"numero": 1, "titulo": "1537",          "artistas": "Guardarraya",            "duracion": "4:05"},
            {"numero": 2, "titulo": "Volcán",        "artistas": "Guardarraya",            "duracion": "3:50"},
            {"numero": 3, "titulo": "Cotopaxi",      "artistas": "Guardarraya",            "duracion": "5:12"},
            {"numero": 4, "titulo": "Tungurahua",    "artistas": "Guardarraya ft. ValeCruz","duracion": "3:33"},
            {"numero": 5, "titulo": "Quito de Noche","artistas": "Guardarraya",            "duracion": "4:28"},
            {"numero": 6, "titulo": "Mitad del Mundo","artistas": "Guardarraya",           "duracion": "3:45"},
            {"numero": 7, "titulo": "La Sequía",     "artistas": "Guardarraya",            "duracion": "4:58"},
            {"numero": 8, "titulo": "Fin de Ciclo",  "artistas": "Guardarraya",            "duracion": "6:02"},
        ],
    }
    return render(request, "core/album.html", context)

def playlist_view(request):
    context = {
        "playlist": {
            "nombre": "Vibra Local 🇪🇨",
            "creador": "VibeSync",
            "descripcion": "Lo mejor del talento ecuatoriano, curado por VibeSync.",
            "likes": "4,500",
            "total_canciones": 5,
            "color_hero": "linear-gradient(135deg,#16a085,#0d1422)",
            "imagen": "https://placehold.co/400x400/0d0d20/a855f7?text=⚡",
        },
        "canciones": [
            {"numero": 1, "titulo": "Crimen Perfecto",
             "album": "Signos",          "fecha_agregada": "Hace 2 días",   "duracion": "3:15"},
            {"numero": 2, "titulo": "1537",
             "album": "Noches de Quito", "fecha_agregada": "Hace 5 días",   "duracion": "4:05"},
            {"numero": 3, "titulo": "Amanecer Neón",
             "album": "Sintético",       "fecha_agregada": "Hace 1 semana", "duracion": "3:52"},
            {"numero": 4, "titulo": "El Gran Retorno",
             "album": "Camaleón",        "fecha_agregada": "Hace 2 semanas","duracion": "3:45"},
            {"numero": 5, "titulo": "Volcán",
             "album": "Noches de Quito", "fecha_agregada": "Hace 1 mes",    "duracion": "3:50"},
        ],
    }
    return render(request, "core/playlist.html", context)

# ─────────────────────────────────────────────
# ARTISTA (panel)
# ─────────────────────────────────────────────
def artista_dashboard_view(request):
    context = {
        "es_artista": True,
        "estadisticas": {
            "oyentes_mensuales":    "45,230",
            "reproducciones_totales": "1,204,500",
            "seguidores":           "12,400",
        },
        "top_canciones": [
            {"numero": 1, "titulo": "Amanecer Neón",  "album": "Sintético",
             "reproducciones": "540,000", "color": "1a0d2e"},
            {"numero": 2, "titulo": "Vuelo Nocturno", "album": "Sintético",
             "reproducciones": "320,100", "color": "001a1a"},
            {"numero": 3, "titulo": "Ecos del Valle", "album": "Sintético",
             "reproducciones": "115,400", "color": "0d1422"},
        ],
        "top_albumes": [
            {"titulo": "Sintético",       "anio": "2023",
             "reproducciones": "860,100", "color": "f5a623"},
            {"titulo": "Ecos del Cotopaxi","anio": "2022",
             "reproducciones": "344,000", "color": "1a0d2e"},
        ],
    }
    return render(request, "core/artista_dashboard.html", context)

def crear_album_view(request):
    return render(request, "core/crear_album.html", {"es_artista": True})

def subir_sencillo_view(request):
    return render(request, "core/subir_sencillo.html", {"es_artista": True})

def regalias_view(request):
    context = {
        "es_artista": True,
        "resumen": {
            "mes_actual": "Mayo 2026",
            "total_reproducciones": "975,500",
            "ganancias_estimadas":  "$3,902.00",
            "tasa_por_stream":      "$0.004",
        },
        "desglose": [
            {"cancion": "Amanecer Neón",  "reproducciones": "540,000", "ganancia": "$2,160.00"},
            {"cancion": "Vuelo Nocturno", "reproducciones": "320,100", "ganancia": "$1,280.40"},
            {"cancion": "Ecos del Valle", "reproducciones": "115,400", "ganancia": "$461.60"},
        ],
    }
    return render(request, "core/regalias.html", context)

# ─────────────────────────────────────────────
# ADMINISTRADOR
# ─────────────────────────────────────────────
def admin_dashboard_view(request):
    # Intentar obtener datos reales de la BD
    usuarios_totales = _fetch("SELECT COUNT(*) AS total FROM Identidad.Persona")
    usuarios_total_val = usuarios_totales[0]["total"] if usuarios_totales else 1_245_890

    artistas_db = _fetch(
        """SELECT TOP(3)
               p.nombrePersona + \' \' + p.apellidoPersona AS nombre,
               COUNT(r.idReproduccion) AS reproducciones
           FROM Identidad.Artista a
           INNER JOIN Identidad.Persona p ON a.idPersona = p.idPersona
           LEFT JOIN Musica.ArtistaCancion ac ON ac.Artista_idPersona = a.idPersona
           LEFT JOIN Actividad.Reproduccion r ON r.Cancion_ISRC_Cancion = ac.Cancion_ISRC_Cancion
           GROUP BY p.nombrePersona, p.apellidoPersona
           ORDER BY reproducciones DESC"""
    )

    canciones_db = _fetch(
        """SELECT TOP(3)
               c.nombreCancion AS titulo,
               p.nombrePersona + \' \' + p.apellidoPersona AS artista,
               COUNT(r.idReproduccion) AS streams
           FROM Musica.Cancion c
           INNER JOIN Musica.ArtistaCancion ac ON ac.Cancion_ISRC_Cancion = c.ISRC_Cancion
           INNER JOIN Identidad.Persona p ON p.idPersona = ac.Artista_idPersona
           LEFT JOIN Actividad.Reproduccion r ON r.Cancion_ISRC_Cancion = c.ISRC_Cancion
           GROUP BY c.nombreCancion, p.nombrePersona, p.apellidoPersona
           ORDER BY streams DESC"""
    )

    context = {
        "es_admin": True,
        "metricas_globales": {
            "usuarios_totales":     f"{usuarios_total_val:,}",
            "usuarios_activos_hoy": "342,100",
            "nuevos_registros_mes": "+12,400",
        },
        "generos_top": [
            {"nombre": "Indie Rock",         "porcentaje": 85},
            {"nombre": "Pop Latino",         "porcentaje": 70},
            {"nombre": "Synthwave Andino",   "porcentaje": 65},
            {"nombre": "Urbano",             "porcentaje": 40},
        ],
        "eventos_top": [
            {"nombre": "Quito Fest 2026",  "ventas": "15,000 tickets", "estado": "Agotado"},
            {"nombre": "VibeSync Live UI", "ventas": "8,500 tickets",  "estado": "En venta"},
            {"nombre": "FestivalFFF",      "ventas": "5,200 tickets",  "estado": "En venta"},
        ],
        "artistas_top": artistas_db or [
            {"nombre": "La Máquina Camaleón", "reproducciones": "2.5M"},
            {"nombre": "Guardarraya",         "reproducciones": "1.8M"},
            {"nombre": "DJ Santi",            "reproducciones": "1.2M"},
        ],
        "albumes_top": [
            {"titulo": "Noches de Quito", "artista": "Guardarraya", "reproducciones": "1.5M"},
            {"titulo": "Amarilla",        "artista": "La Máq. Camaleón", "reproducciones": "1.1M"},
        ],
        "canciones_top": canciones_db or [
            {"numero": 1, "titulo": "1537",           "artista": "Guardarraya",          "streams": "850K"},
            {"numero": 2, "titulo": "Amanecer Neón",  "artista": "DJ Santi",             "streams": "540K"},
            {"numero": 3, "titulo": "El Gran Retorno","artista": "La Máquina Camaleón",  "streams": "420K"},
        ],
    }
    return render(request, "core/admin_dashboard.html", context)

def administrar_usuarios_view(request):
    # Intentar datos reales
    users_db = _fetch(
        """SELECT TOP(20)
               p.idPersona AS id,
               p.nombrePersona + \' \' + p.apellidoPersona AS username,
               p.correoPersona AS email,
               p.tipoPersona AS rol,
               \'Activo\' AS estado,
               \'success\' AS color
           FROM Identidad.Persona p
           ORDER BY p.idPersona"""
    )
    usuarios_fallback = [
        {"id": 1, "username": "mateo_dev",           "email": "mateo@vibesync.com",       "rol": "Administrador", "estado": "Activo",    "color": "success"},
        {"id": 2, "username": "guardarraya_oficial",  "email": "banda@guardarraya.ec",     "rol": "Artista",       "estado": "Activo",    "color": "success"},
        {"id": 3, "username": "juan_oyente99",        "email": "juan99@gmail.com",         "rol": "Oyente",        "estado": "Bloqueado", "color": "danger"},
        {"id": 4, "username": "indie_fan",            "email": "indie@hotmail.com",        "rol": "Oyente",        "estado": "Activo",    "color": "success"},
        {"id": 5, "username": "dj_santi_ec",          "email": "santi@music.com",          "rol": "Artista",       "estado": "Activo",    "color": "success"},
        {"id": 6, "username": "paula_v",              "email": "pvargas@email.com",        "rol": "Oyente",        "estado": "Inactivo",  "color": "warning"},
    ]
    context = {
        "es_admin": True,
        "usuarios": users_db or usuarios_fallback,
    }
    return render(request, "core/administrar_usuarios.html", context)

def admin_eventos_view(request):
    eventos_db = _fetch(
        """SELECT
               c.idConcierto AS id,
               c.nombreConcierto AS nombre,
               CONVERT(VARCHAR(10), c.fechaConcierto, 103) AS fecha,
               c.ciudadConcierto + \', \' + p.nombrePais AS lugar,
               c.aforoConcierto AS aforo,
               \'Publicado\' AS estado
           FROM Eventos.Concierto c
           INNER JOIN Identidad.Pais p ON p.idPais = c.Pais_idPais"""
    )
    context = {
        "es_admin": True,
        "eventos": eventos_db or [],
    }
    return render(request, "core/admin_eventos.html", context)

def admin_insignias_view(request):
    badges_db = _fetch(
        """SELECT idInsignia, nombreInsignia AS nombre, detalleInsignia AS descripcion
           FROM Gamificacion.Insignia"""
    )
    context = {
        "es_admin": True,
        "insignias": badges_db or [],
    }
    return render(request, "core/admin_insignias.html", context)

# ─────────────────────────────────────────────
# OTRAS VISTAS (Perfil, Ajustes, Suscripción)
# ─────────────────────────────────────────────
def perfil_view(request):
    context = {
        "persona": {
            "nombrePersona":         "Mateo",
            "apellidoPersona":       "Sánchez",
            "correoPersona":         "mateo@vibesync.com",
            "anioNacimientoPersona": "2000-01-01",
        },
        "usuario": {
            "usernameUsuario": "mateo_dev",
            "ciudadUsuario":   "Quito",
        },
    }
    return render(request, "core/perfil.html", context)

def suscripcion_view(request):
    context = {
        "usuario": {
            "tipoSuscripcion":  "Premium",
            "metodoPago":       "Tarjeta •••• 4242",
            "estadoSuscripcion":"Activo",
        }
    }
    return render(request, "core/suscripcion.html", context)

def ajustes_view(request):
    return render(request, "core/ajustes.html")

# ─────────────────────────────────────────────
# MANEJO DE ERRORES
# ─────────────────────────────────────────────
def error_404_view(request, exception=None):
    context = {
        "error_code":    "404",
        "error_message": "Página no encontrada",
    }
    return render(request, "core/error.html", context, status=404)

def error_500_view(request):
    context = {
        "error_code":    "500",
        "error_message": "Error interno del servidor",
    }
    return render(request, "core/error.html", context, status=500)

def error_403_view(request, exception=None):
    context = {
        "error_code":    "403",
        "error_message": "Acceso denegado",
    }
    return render(request, "core/error.html", context, status=403)

def error_400_view(request, exception=None):
    context = {
        "error_code":    "400",
        "error_message": "Solicitud incorrecta",
    }
    return render(request, "core/error.html", context, status=400)