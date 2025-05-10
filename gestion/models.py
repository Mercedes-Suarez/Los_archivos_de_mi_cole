from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Usuario(AbstractUser):
    pass

class Asignatura(models.Model):
    nombre = models.CharField(max_length=255, default="Sin nombre")
   
    def __str__(self):
        return f"{self.nombre} - {self.curso}"

class Archivo(models.Model):
    TRIMESTRES = [(1, '1º Trimestre'), (2, '2º Trimestre'), (3, '3º Trimestre'), (4, 'Vacaciones'),]
    archivo = models.FileField(upload_to='archivos/')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=TRIMESTRES)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-fecha_subida']  # Orden descendente por fecha_subida

    @property
    def nombre_archivo(self):
        return self.archivo.name.split('/')[-1]
   
    def __str__(self):
        return f"{self.nombre_archivo} - {self.asignatura}"
    