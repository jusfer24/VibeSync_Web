from django.contrib.auth.hashers import check_password
from .models import Persona

class VibeSyncBusinessBackend:
    """
    Backend de autenticación personalizado para validar usuarios del negocio
    contra el esquema Identidad.Persona de SQL Server.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # En nuestro diseño, 'username' recibe el correo electrónico de la persona
        correo = username 
        try:
            # Buscamos la entidad en la base de datos gestionada
            persona = Persona.objects.get(correoPersona=correo)
            
            # Validamos si el password en texto plano coincide con el hash de la base de datos
            if check_password(password, persona.contrasenaPersona):
                return persona  # Retorna el objeto Persona si la credencial es válida
        except Persona.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Persona.objects.get(pk=user_id)
        except Persona.DoesNotExist:
            return None