from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

CURSOS = [
        ('1P', '1º Primaria'), ('2P', '2º Primaria'), ('3P', '3º Primaria'),
        ('4P', '4º Primaria'), ('5P', '5º Primaria'), ('6P', '6º Primaria'),
        ('1S', '1º Secundaria'), ('2S', '2º Secundaria'),
        ('3S', '3º Secundaria'), ('4S', '4º Secundaria'),
]

TRIMESTRES = [
    (1, '1º Trimestre'), (2, '2º Trimestre'),
    (3, '3º Trimestre'), (4, 'Vacaciones'),]

class Usuario(AbstractUser):
    pass

class Alumno(models.Model):
    usuario = models.OneToOneField('gestion.Usuario', on_delete=models.CASCADE, null=True, blank=True)
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
        if self.archivo:
            return self.archivo.name.split('.')[-1].lower()
        return None

    def __str__(self):
        return f"{self.nombre_archivo} - {self.asignatura}"
