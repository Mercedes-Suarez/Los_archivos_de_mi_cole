from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Usuario(AbstractUser):
    pass

class Asignatura(models.Model):

    nombre = models.CharField(max_length=100, default="Sin nombre")
   
    def __str__(self):
        return f"{self.nombre}"

class Archivo(models.Model):
    TRIMESTRES = [(1, '1º Trimestre'), (2, '2º Trimestre'), (3, '3º Trimestre'), (4, 'Vacaciones'),]

    CURSOS = [
        ('1P', '1º Primaria'), ('2P', '2º Primaria'), ('3P', '3º Primaria'),
        ('4P', '4º Primaria'), ('5P', '5º Primaria'), ('6P', '6º Primaria'),
        ('1S', '1º Secundaria'), ('2S', '2º Secundaria'),
        ('3S', '3º Secundaria'), ('4S', '4º Secundaria'),
    ]
    
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
    
    def __str__(self):
        return f"{self.nombre_archivo} - {self.asignatura}"
