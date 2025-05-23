from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from gestion.views import (
    acceso_alumno,
    asignatura_create,
    asignatura_edit,
    asignatura_list,
    solicitar_eliminacion_asignatura,
    asignatura_delete,
    aprobar_eliminacion_asignatura,
    rechazar_eliminacion_asignatura,
)

urlpatterns = [

    path('', views.inicio, name='home'),
    path('inicio', views.inicio, name='inicio'),
    path('registro/', views.registro_padre, name='registro'),
    path('alumno/', views.acceso_alumno, name='acceso_alumno'),

    # Gestión de archivos

    path('nuevo/', views.archivo_create, name='archivo_create'),
    path('archivos/', views.archivo_list, name='archivo_list'),
    path('archivo/<int:id>/ver/', views.archivo_ver, name='archivo_ver'),
    path('archivo/editar/<int:id>', views.archivo_editar, name='archivo_editar'),
    path('archivo/<int:pk>/eliminar/', views.archivo_delete, name='archivo_delete'),
    path('archivo/solicitar-eliminacion/<int:pk>/', views.solicitar_eliminacion_archivo, name='solicitar_eliminacion_archivo'),
 
    # Gestión de asignaturas
    
    path('asignaturas/', views.asignatura_list, name='asignatura_list'),
    path('asignaturas/nueva/', views.asignatura_create, name='asignatura_create'),
    path('asignaturas/<int:pk>/editar/', views.asignatura_edit, name='asignatura_edit'),
    path('asignaturas/<int:pk>/eliminar/', views.asignatura_delete, name='asignatura_delete'),
    path('asignaturas/solicitar-eliminacion/<int:pk>/', views.solicitar_eliminacion_asignatura, name='solicitar_eliminacion_asignatura'),

    # Gestion de alumnos

    path('alumno/archivos/', acceso_alumno, name='acceso_alumno'),
    path('alumnos/', views.alumno_list, name='alumno_list'),
    path('alumnos/nuevo/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.alumno_edit, name='alumno_edit'),
    path('alumnos/<int:pk>/eliminar/', views.alumno_delete, name='alumno_delete'),
    path('alumnos/solicitar-eliminacion/<int:pk>/', views.solicitar_eliminacion_alumno, name='solicitar_eliminacion_alumno'),
 
    path('panel/alumnos/', views.panel_admin_alumnos, name='panel_admin_alumnos'),

    # Gestion de padres

    path('padres/', views.padre_list, name='padre_list'),
    path('padres/crear/', views.padre_create, name='padre_create'),
    path('padres/<int:pk>/editar/', views.padre_edit, name='padre_edit'),
    path('padres/<int:pk>/eliminar/', views.padre_delete, name='padre_delete'),

    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),

    path('archivo/<int:pk>/aprobar-eliminacion/', views.aprobar_eliminacion_archivo, name='aprobar_eliminacion_archivo'),
    path('archivo/<int:pk>/rechazar-eliminacion/', views.rechazar_eliminacion_archivo, name='rechazar_eliminacion_archivo'),

    path('alumnos/<int:pk>/aprobar-eliminacion/', views.aprobar_eliminacion_alumno, name='aprobar_eliminacion_alumno'),
    path('alumnos/<int:pk>/rechazar-eliminacion/', views.rechazar_eliminacion_alumno, name='rechazar_eliminacion_alumno'),

    path('asignatura/<int:pk>/aprobar-eliminacion/', views.aprobar_eliminacion_asignatura, name='aprobar_eliminacion_asignatura'),
    path('asignatura/<int:pk>/rechazar-eliminacion/', views.rechazar_eliminacion_asignatura, name='rechazar_eliminacion_asignatura'),

]

