from django.db import models
from django.contrib.auth.models import AbstractUser

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
        return self.nombre

class Trimestre(models.Model):
    OPCIONES = [
        ('1', 'Primer Trimestre'),
        ('2', 'Segundo Trimestre'),
        ('3', 'Tercer Trimestre'),
    ]   
    nombre = models.CharField(max_length=1, choices=OPCIONES)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_nombre_display()} - {self.asignatura.nombre}"

class Archivo(models.Model):
    TIPO_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('img', 'Imagen'),
        ('txt', 'Texto'),
    ]
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    ruta = models.FileField(upload_to='media/')
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre