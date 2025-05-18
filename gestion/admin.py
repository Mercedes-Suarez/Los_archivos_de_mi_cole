from django.contrib import admin

from .models import Archivo, Asignatura, Alumno, Usuario

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'asignatura', 'trimestre', 'fecha_subida', ]
    list_filter = ['asignatura', 'trimestre']
    search_fields = ['archivo']

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso')
    list_filter = ('curso',)
    search_fields = ('nombre',)
    ordering = ('curso', 'nombre')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']

