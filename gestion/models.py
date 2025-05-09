from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
class Usuario(AbstractUser):
    pass

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    año = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.año})"
    
class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.curso}"

class Archivo(models.Model):
    TRIMESTRES = [(1, '1º'), (2, '2º'), (3, '3º')]
    archivo = models.FileField(upload_to='archivos/')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=TRIMESTRES)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.archivo.name} - {self.asignatura}"
    