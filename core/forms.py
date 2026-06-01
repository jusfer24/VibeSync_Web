# core/forms.py
from django import forms
from .models import Persona, Usuario

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        # Excluimos idPersona y campos automáticos/foráneos complejos por ahora
        fields = ['nombrePersona', 'apellidoPersona', 'correoPersona', 'sexoPersona', 'anioNacimientoPersona', 'tipoPersona', 'contrasenaPersona']
        # Aquí puedes agregar widgets de HTML para que luzcan mejor con CSS (ej. Tailwind/Bootstrap)
        widgets = {
            'anioNacimientoPersona': forms.DateInput(attrs={'type': 'date'}),
            'contrasenaPersona': forms.PasswordInput(),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Excluimos la llave foránea 'persona' porque la inyectaremos en la vista
        fields = ['usernameUsuario', 'ciudadUsuario', 'metodoPago', 'estadoSuscripcion', 'paisOrigenUsuario', 'paisResidenciaUsuario']