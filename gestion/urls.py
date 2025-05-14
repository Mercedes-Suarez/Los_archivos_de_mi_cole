from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .views import archivo_delete

urlpatterns = [

    path('', views.inicio, name='home'),
    path('inicio', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro'),
    path('alumno/', views.acceso_alumno, name='acceso_alumno'),

    # Gestión de archivos

    path('nuevo/', views.archivo_create, name='archivo_create'),
    path('archivos/', views.archivo_list, name='archivo_list'),
    path('archivo/editar/<int:pk>', views.editar_archivo, name='editar_archivo'),
    path('archivo/<int:pk>/eliminar/', archivo_delete, name='archivo_delete'),
  
    # Gestión de asignaturas
    
    path('asignaturas/', views.asignatura_list, name='asignatura_list'),
    path('asignaturas/nueva/', views.asignatura_create, name='asignatura_create'),
    path('asignaturas/<int:pk>/editar/', views.asignatura_edit, name='asignatura_edit'),
    path('asignaturas/<int:pk>/eliminar/', views.asignatura_delete, name='asignatura_delete'),

    # Gestion de alumnos

    path('alumnos/', views.alumno_list, name='alumno_list'),
    path('alumnos/nuevo/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.alumno_edit, name='alumno_edit'),
    path('alumnos/<int:pk>/eliminar/', views.alumno_delete, name='alumno_delete'),

]

