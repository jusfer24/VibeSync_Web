from django.db import models

class Persona(models.Model):
    idPersona = models.AutoField(primary_key=True, db_column='idPersona')
    nombrePersona = models.CharField(max_length=50, db_column='nombrePersona')
    apellidoPersona = models.CharField(max_length=50, null=True, blank=True, db_column='apellidoPersona')
    sexoPersona = models.CharField(max_length=20, default='Prefiero no Decirlo', db_column='sexoPersona')
    anioNacimientoPersona = models.DateField(db_column='anioNacimientoPersona')
    correoPersona = models.EmailField(unique=True, max_length=75, db_column='correoPersona')
    tipoPersona = models.CharField(max_length=10, db_column='tipoPersona')
    
    # Almacena el hash criptográfico generado por el sistema
    contrasenaPersona = models.CharField(max_length=255, db_column='contrasenaPersona')
    fotoPerfilPersona = models.BinaryField(null=True, blank=True, db_column='fotoPerfilPersona')

    class Meta:
        managed = False
        db_table = '[Identidad].[Persona]'

    def __str__(self):
        return f"{self.nombrePersona} ({self.tipoPersona})"


class Usuario(models.Model):
    persona = models.OneToOneField(
        Persona, 
        on_delete=models.DO_NOTHING, 
        primary_key=True, 
        db_column='idPersona',
        related_name='perfil_usuario'
    )
    usernameUsuario = models.CharField(max_length=75, unique=True, db_column='usernameUsuario')
    ciudadUsuario = models.CharField(max_length=50, db_column='ciudadUsuario')
    metodoPago = models.CharField(max_length=25, null=True, blank=True, db_column='metodoPago')
    estadoSuscripcion = models.CharField(max_length=10, null=True, blank=True, db_column='estadoSuscripcion')
    
    # Catálogos y claves foráneas físicas
    paisOrigenUsuario = models.IntegerField(db_column='paisOrigenUsuario')
    paisResidenciaUsuario = models.IntegerField(db_column='paisResidenciaUsuario')
    Suscripcion_idSuscripcion = models.IntegerField(null=True, blank=True, db_column='Suscripcion_idSuscripcion')
    Genero_idGenero = models.IntegerField(null=True, blank=True, db_column='Genero_idGenero')
    Emocion_idEmocion = models.IntegerField(null=True, blank=True, db_column='Emocion_idEmocion')

    class Meta:
        managed = False
        db_table = '[Identidad].[Usuario]'

    def __str__(self):
        return self.usernameUsuario