from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

CURSOS = [
        ('1P', '1º Primaria'), ('2P', '2º Primaria'), ('3P', '3º Primaria'),
        ('4P', '4º Primaria'), ('5P', '5º Primaria'), ('6P', '6º Primaria'),
        ('1S', '1º Secundaria'), ('2S', '2º Secundaria'),
        ('3S', '3º Secundaria'), ('4S', '4º Secundaria'),
]

TRIMESTRES = [
    (1, '1º Trimestre'), (2, '2º Trimestre'),
    (3, '3º Trimestre'), (4, 'Vacaciones'),
]

class Usuario(AbstractUser):

    tipo = models.CharField(max_length=10, choices=[('alumno', 'Alumno'), ('padre', 'Padre'), ('admin', 'Administrador')])
    fecha_creacion = models.DateTimeField(default=timezone.now)

# Padre vinculado al usuario
class Padre(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='padre')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    usuario = models.OneToOneField('gestion.Usuario', on_delete=models.CASCADE, null=True, blank=True)
    padre = models.ForeignKey('gestion.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='hijos')
    nombre = models.CharField(max_length=100)
    curso = models.CharField(max_length=2, choices=CURSOS)

    def __str__(self):
        return f"{self.nombre} ({self.get_curso_display()})"

class Asignatura(models.Model):

    nombre = models.CharField(max_length=100, default="Sin nombre")
   
    def __str__(self):
        return f"{self.nombre}"

class Archivo(models.Model):    
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)
    enlace_externo = models.URLField(blank=True, null=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=TRIMESTRES)
    curso = models.CharField(max_length=2, choices=CURSOS)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-fecha_subida']

    @property
    def nombre_archivo(self):
        return self.archivo.name.split('/')[-1] if self.archivo else "Enlace"
    
    @property
    def extension(self):
        if self.archivo and hasattr(self.archivo, 'name'):
            return self.archivo.name.split('.')[-1].lower()
        return ''

    def __str__(self):
        return f"{self.nombre_archivo} - {self.asignatura}"

class SolicitudEliminacionBase(models.Model):
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True)  # Nuevo campo para explicar el motivo

    class Meta:
        abstract = True

class SolicitudEliminacionAlumno(SolicitudEliminacionBase):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

class SolicitudEliminacionArchivo(SolicitudEliminacionBase):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)

class SolicitudEliminacionAsignatura(SolicitudEliminacionBase):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)