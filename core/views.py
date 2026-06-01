# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password 
from .models import Persona, Usuario
from .forms import PersonaForm, UsuarioForm

# ==========================================
# HELPER: Memoria Frontend (Cookies)
# ==========================================
def get_user_role(request):
    """
    Lee una cookie del navegador para recordar el rol sin usar la base de datos.
    ¡Truco perfecto para probar diseños y maquetas!
    """
    rol = request.COOKIES.get('vibe_rol', 'oyente')
    return {
        'es_admin': rol == 'admin',
        'es_artista': rol == 'artista'
    }

# ==========================================
# VISTAS DE AUTENTICACIÓN
# ==========================================
def login_view(request):
    response = render(request, 'core/login.html')
    response.delete_cookie('vibe_rol') # Limpiamos la memoria al entrar al login
    return response


# ==========================================
# VISTAS DE OYENTE
# ==========================================
def oyente_dashboard_view(request):
    context = get_user_role(request)
    context.update({'es_admin': False, 'es_artista': False})
    
    response = render(request, 'core/oyente_dashboard.html', context)
    response.set_cookie('vibe_rol', 'oyente') # Guardamos el rol en el navegador
    return response

def explorar_view(request):
    context = get_user_role(request)
    query = request.GET.get('q', '')
    
    context.update({
        'historial_busquedas': [
            {'tipo_ui': 'cancion', 'titulo': 'Synthwave Andino Mix', 'subtitulo': 'Canción • VibeSync', 'inicial': 'S', 'color': '1e2a38'},
            {'tipo_ui': 'artista', 'titulo': 'Guardarraya', 'subtitulo': 'Artista', 'inicial': 'G', 'color': '50e3c2'},
            {'tipo_ui': 'album', 'titulo': 'Noches de Quito', 'subtitulo': 'Álbum', 'inicial': 'N', 'color': 'f5a623'}
        ],
        'resultado_principal': {
            'titulo': query, 'tipo': 'Canción', 'subtitulo': 'Artista Local • Álbum VibeSync'
        },
        'canciones': [
            {'titulo': f'{query} (Remix Oficial)' if query else '', 'artista': 'Artista Relacionado', 'duracion': '3:45'},
            {'titulo': f'{query} (Acústico)' if query else '', 'artista': 'Artista Relacionado', 'duracion': '4:10'},
        ],
        'albumes_relacionados': [{'titulo': 'El Primer Disco', 'tipo': 'Álbum'}, {'titulo': 'Lados B', 'tipo': 'EP'}],
        'artistas_genero': [{'nombre': 'La Máquina Camaleón', 'tipo': 'Artista'}, {'nombre': 'Lolabum', 'tipo': 'Artista'}]
    })
    return render(request, 'core/explorar.html', context)

def gamificacion_view(request):
    context = get_user_role(request)
    context.update({
        'progreso': {'nivel': 12, 'xp_faltante': 350, 'porcentaje': 65},
        'insignias': [
            {'icono': '🎧', 'nombre': 'Primer Play', 'descripcion': 'Escuchaste tu primera canción.', 'obtenida': True},
            {'icono': '🎟️', 'nombre': 'Apoyo Local', 'descripcion': 'Compra tu primer boleto.', 'obtenida': False},
            {'icono': '🔥', 'nombre': 'En Llamas', 'descripcion': 'Escuchaste música 7 días seguidos.', 'obtenida': False},
        ]
    })
    return render(request, 'core/gamificacion.html', context)

def biblioteca_view(request):
    context = get_user_role(request)
    context.update({
        'me_gusta': {
            'canciones': [{'titulo': 'Crimen Perfecto', 'artista': 'Soda Stereo'}],
            'albumes': [{'titulo': 'Signos', 'artista': 'Soda Stereo'}],
            'artistas': [{'nombre': 'Guardarraya', 'genero': 'Rock Andino'}]
        },
        'albums_alfabetico': [{'titulo': 'Chiste Cruel', 'artista': 'Lolabum'}, {'titulo': 'Roja', 'artista': 'Da Pawn'}],
        'playlists_alfabetico': [{'nombre': 'Clásicos del Rock', 'total_canciones': 42}]
    })
    return render(request, 'core/biblioteca.html', context)

def eventos_view(request):
    context = get_user_role(request)
    return render(request, 'core/eventos.html', context)


# ==========================================
# DETALLES (Compartidos)
# ==========================================
def artista_view(request):
    context = get_user_role(request)
    context.update({
        'artista': {'nombre': 'La Máquina Camaleón', 'oyentes_mensuales': '145,892', 'color_hero': 'linear-gradient(135deg, #2c3e50 0%, #1a1a1d 100%)', 'imagen': 'https://placehold.co/400x400/2c3e50/ffffff?text=LMC'},
        'canciones_populares': [{'numero': 1, 'titulo': 'El Gran Retorno', 'reproducciones': '1,204,500', 'duracion': '3:45'}],
        'albumes': [{'titulo': 'Amarilla', 'anio': '2017', 'color': 'f5a623'}]
    })
    return render(request, 'core/artista.html', context)

def album_view(request):
    context = get_user_role(request)
    context.update({
        'album': {'titulo': 'Noches de Quito', 'artista': 'Guardarraya', 'anio': '2023', 'total_canciones': 8, 'duracion_total': '32 min', 'color_hero': 'linear-gradient(135deg, #8e44ad 0%, #1a1a1d 100%)', 'imagen': 'https://placehold.co/400x400/8e44ad/ffffff?text=NDQ'},
        'canciones': [{'numero': 1, 'titulo': '1537', 'artistas': 'Guardarraya', 'duracion': '4:05'}]
    })
    return render(request, 'core/album.html', context)

def playlist_view(request):
    context = get_user_role(request)
    context.update({
        'playlist': {'nombre': 'Vibra Local 🇪🇨', 'creador': 'VibeSync', 'descripcion': 'Lo mejor del talento ecuatoriano.', 'likes': '4,500', 'total_canciones': 45, 'color_hero': 'linear-gradient(135deg, #16a085 0%, #1a1a1d 100%)', 'imagen': 'https://placehold.co/400x400/151b29/00e5ff?text=VL'},
        'canciones': [{'numero': 1, 'titulo': 'Crimen Perfecto', 'album': 'Signos', 'fecha_agregada': 'Hace 2 días', 'duracion': '3:15'}]
    })
    return render(request, 'core/playlist.html', context)


# ==========================================
# VISTAS DE ARTISTA
# ==========================================
def artista_dashboard_view(request):
    context = get_user_role(request)
    context.update({
        'es_artista': True, 'es_admin': False,
        'estadisticas': {'oyentes_mensuales': '45,230', 'reproducciones_totales': '1,204,500', 'seguidores': '12,400'},
        'top_canciones': [{'numero': 1, 'titulo': 'Amanecer Neón', 'album': 'Sintético', 'reproducciones': '540,000', 'color': '1e2a38'}],
        'top_albumes': [{'titulo': 'Sintético', 'anio': '2023', 'reproducciones': '860,100', 'color': 'f5a623'}]
    })
    
    response = render(request, 'core/artista_dashboard.html', context)
    response.set_cookie('vibe_rol', 'artista') # Guardamos el rol
    return response

def crear_album_view(request):
    context = get_user_role(request)
    return render(request, 'core/crear_album.html', context)

def subir_sencillo_view(request):
    context = get_user_role(request)
    return render(request, 'core/subir_sencillo.html', context)

def regalias_view(request):
    context = get_user_role(request)
    context.update({
        'resumen': {
            'mes_actual': 'Mayo 2026',
            'total_reproducciones': '975,500',
            'ganancias_estimadas': '$3,902.00',
            'tasa_por_stream': '$0.004'
        },
        'desglose': [
            {'cancion': 'Amanecer Neón', 'reproducciones': '540,000', 'ganancia': '$2,160.00'},
            {'cancion': 'Vuelo Nocturno', 'reproducciones': '320,100', 'ganancia': '$1,280.40'},
            {'cancion': 'Ecos del Valle', 'reproducciones': '115,400', 'ganancia': '$461.60'},
        ]
    })
    return render(request, 'core/regalias.html', context)


# ==========================================
# VISTAS DE ADMINISTRADOR
# ==========================================
# 1. READ (Leer)
def administrar_usuarios_view(request):
    context = get_user_role(request)
    # select_related optimiza la consulta cruzando Persona y Usuario en un solo llamado a SQL
    usuarios_db = Usuario.objects.select_related('persona').all()
    context['usuarios'] = usuarios_db
    return render(request, 'core/administrar_usuarios.html', context)

# 2. CREATE (Crear)
def crear_usuario_view(request):
    context = get_user_role(request)
    if request.method == 'POST':
        form_persona = PersonaForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        
        if form_persona.is_valid() and form_usuario.is_valid():
            # Guardamos la Persona primero, sin enviar a DB (commit=False)
            nueva_persona = form_persona.save(commit=False)
            # Encriptamos la contraseña por seguridad antes de guardar en SQL Server
            nueva_persona.contrasenaPersona = make_password(nueva_persona.contrasenaPersona)
            nueva_persona.save() # Ahora sí guardamos en SQL Server
            
            # Guardamos el Usuario
            nuevo_usuario = form_usuario.save(commit=False)
            nuevo_usuario.persona = nueva_persona # Enlazamos el OneToOneField
            nuevo_usuario.save()
            
            return redirect('administrar_usuarios')
    else:
        form_persona = PersonaForm()
        form_usuario = UsuarioForm()

    context.update({'form_persona': form_persona, 'form_usuario': form_usuario, 'accion': 'Crear'})
    return render(request, 'core/usuario_form.html', context)

# 3. UPDATE (Actualizar)
def editar_usuario_view(request, id):
    context = get_user_role(request)
    # Buscamos al usuario por su Primary Key (que es idPersona)
    usuario = get_object_or_404(Usuario, pk=id)
    persona = usuario.persona
    
    if request.method == 'POST':
        form_persona = PersonaForm(request.POST, instance=persona)
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        
        if form_persona.is_valid() and form_usuario.is_valid():
            persona_actualizada = form_persona.save(commit=False)
            # Solo re-encriptar si el administrador escribió una nueva contraseña
            if 'contrasenaPersona' in form_persona.changed_data:
                persona_actualizada.contrasenaPersona = make_password(persona_actualizada.contrasenaPersona)
            persona_actualizada.save()
            form_usuario.save()
            return redirect('administrar_usuarios')
    else:
        form_persona = PersonaForm(instance=persona)
        form_usuario = UsuarioForm(instance=usuario)

    context.update({'form_persona': form_persona, 'form_usuario': form_usuario, 'accion': 'Editar'})
    return render(request, 'core/usuario_form.html', context)

# 4. DELETE (Eliminar)
def eliminar_usuario_view(request, id):
    context = get_user_role(request)
    usuario = get_object_or_404(Usuario, pk=id)
    persona = usuario.persona
    
    if request.method == 'POST':
        # Primero eliminamos el hijo (Usuario) y luego el padre (Persona) para no violar llaves foráneas
        usuario.delete()
        persona.delete()
        return redirect('administrar_usuarios')
        
    context.update({'usuario': usuario})
    return render(request, 'core/usuario_confirm_delete.html', context)

def admin_dashboard_view(request):
    context = get_user_role(request)
    total_usuarios_reales = Usuario.objects.count()
    context.update({
        'es_admin': True, 'es_artista': False,
        'metricas_globales': {
            # Usamos el dato real
            'usuarios_totales': f"{total_usuarios_reales:,}", 
            
            # Estos se mantienen simulados por ahora:
            'usuarios_activos_hoy': '342,100', 
            'nuevos_registros_mes': '+12,400'  
        },
        'generos_top': [
            {'nombre': 'Indie Rock', 'porcentaje': 85},
            {'nombre': 'Pop Latino', 'porcentaje': 70},
            {'nombre': 'Alternativo Andino', 'porcentaje': 65},
            {'nombre': 'Urbano', 'porcentaje': 40},
        ],
        'eventos_top': [
            {'nombre': 'Quito Fest 2026', 'ventas': '15,000 tickets', 'estado': 'Agotado'},
            {'nombre': 'VibeSync Live UI', 'ventas': '8,500 tickets', 'estado': 'En venta'},
            {'nombre': 'FestivalFFF', 'ventas': '5,200 tickets', 'estado': 'En venta'},
        ],
        'artistas_top': [
            {'nombre': 'La Máquina Camaleón', 'reproducciones': '2.5M'},
            {'nombre': 'Guardarraya', 'reproducciones': '1.8M'},
            {'nombre': 'Lolabum', 'reproducciones': '1.2M'},
        ],
        'albumes_top': [
            {'titulo': 'Noches de Quito', 'artista': 'Guardarraya', 'reproducciones': '1.5M'},
            {'titulo': 'Amarilla', 'artista': 'La Máquina Camaleón', 'reproducciones': '1.1M'},
        ],
        'canciones_top': [
            {'numero': 1, 'titulo': '1537', 'artista': 'Guardarraya', 'streams': '850K'},
            {'numero': 2, 'titulo': 'Amanecer Neón', 'artista': 'Sintético', 'streams': '540K'},
            {'numero': 3, 'titulo': 'El Gran Retorno', 'artista': 'La Máquina Camaleón', 'streams': '420K'},
        ]
    })
    
    response = render(request, 'core/admin_dashboard.html', context)
    response.set_cookie('vibe_rol', 'admin') # Guardamos el rol
    return response

def administrar_usuarios_view(request):
    context = get_user_role(request)
    
    # Esta es la línea clave: Le pedimos a SQL Server TODOS los usuarios
    # y usamos select_related para traer también los datos de la Persona asociada
    usuarios_db = Usuario.objects.select_related('persona').all()
    
    # Inyectamos los usuarios reales al contexto
    context['usuarios'] = usuarios_db
    
    return render(request, 'core/administrar_usuarios.html', context)

def admin_eventos_view(request):
    context = get_user_role(request)
    context.update({
        'eventos': [
            {'id': 1, 'nombre': 'Quito Fest 2026', 'fecha': '12 Ago 2026', 'lugar': 'Parque Bicentenario', 'estado': 'Publicado'},
            {'id': 2, 'nombre': 'VibeSync Live UI', 'fecha': '05 Sep 2026', 'lugar': 'Teatro Sucre', 'estado': 'Publicado'},
            {'id': 3, 'nombre': 'FestivalFFF', 'fecha': '20 Nov 2026', 'lugar': 'Ambato', 'estado': 'Borrador'},
        ]
    })
    return render(request, 'core/admin_eventos.html', context)

def admin_insignias_view(request):
    context = get_user_role(request)
    context.update({
        'insignias': [
            {'id': 1, 'icono': '🎧', 'nombre': 'Primer Play', 'descripcion': 'Escuchaste tu primera canción.'},
            {'id': 2, 'icono': '🎟️', 'nombre': 'Apoyo Local', 'descripcion': 'Compraste tu primer boleto.'},
            {'id': 3, 'icono': '🔥', 'nombre': 'En Llamas', 'descripcion': 'Escuchaste música 7 días seguidos.'},
        ]
    })
    return render(request, 'core/admin_insignias.html', context)


# ==========================================
# OTRAS VISTAS (Perfil, Ajustes Compartidos)
# ==========================================
def perfil_view(request):
    context = get_user_role(request)
    return render(request, 'core/perfil.html', context)

def suscripcion_view(request):
    context = get_user_role(request)
    return render(request, 'core/suscripcion.html', context)

def ajustes_view(request):
    context = get_user_role(request)
    return render(request, 'core/ajustes.html', context)