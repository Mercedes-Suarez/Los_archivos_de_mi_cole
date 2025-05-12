from django.contrib import admin

from .models import Archivo, Asignatura

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'asignatura', 'trimestre', 'fecha_subida', ]
    list_filter = ['asignatura', 'trimestre']
    search_fields = ['archivo']

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

