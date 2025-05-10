from django.contrib import admin

from .models import Archivo, Asignatura

admin.site.register(Asignatura)

admin.site.register(Archivo)

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'asignatura', 'trimestre', 'fecha_subida', 'subido_por']
    list_filter = ['asignatura', 'trimestre']
    search_fields = ['archivo']



