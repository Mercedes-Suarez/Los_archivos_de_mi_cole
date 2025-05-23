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
    path('archivo/<int:id>/ver/', views.archivo_ver, name='archivo_ver'),
    path('archivo/editar/<int:pk>', views.archivo_editar, name='archivo_editar'),
    path('archivo/<int:pk>/eliminar/', archivo_delete, name='archivo_delete'),
    path('archivo/<int:pk>/solicitar_eliminacion_archivo/', views.solicitar_eliminacion_archivo, name='solicitar_eliminacion_archivo'),
  
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
    path('alumnos/<int:pk>/solicitar_eliminacion_alumno/', views.solicitar_eliminacion_alumno, name='solicitar_eliminacion_alumno'),
  
    path('panel/alumnos/', views.panel_admin_alumnos, name='panel_admin_alumnos'),

    # Gestion de padres

    path('padres/', views.padre_list, name='padre_list'),
    path('padres/crear/', views.padre_create, name='padre_create'),
    path('padres/<int:pk>/editar/', views.padre_update, name='padre_edit'),
    path('padres/<int:pk>/eliminar/', views.padre_delete, name='padre_delete'),

    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('alumnos/<int:pk>/solicitar-eliminacion/', views.solicitar_eliminacion_alumno, name='solicitar_eliminacion_alumno'),
    path('alumnos/<int:pk>/aprobar-eliminacion/', views.aprobar_eliminacion_alumno, name='aprobar_eliminacion_alumno'),
    path('alumnos/<int:pk>/rechazar-eliminacion/', views.rechazar_eliminacion_alumno, name='rechazar_eliminacion_alumno'),

]

