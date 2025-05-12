from django.urls import path

from . import views
from .views import logout_with_message, archivo_delete

urlpatterns = [

    path('inicio/', views.inicio, name='inicio'),
    path('logout/', logout_with_message, name='logout'), 
    path('', views.archivo_list, name='archivo_list'),
    path('nuevo/', views.archivo_create, name='archivo_create'),
    path('archivo/editar/<int:pk>', views.editar_archivo, name='editar_archivo'),
    path('archivo/<int:pk>/eliminar/', archivo_delete, name='archivo_delete'),
  
    path('asignaturas/', views.asignatura_list, name='asignatura_list'),
    path('asignaturas/nueva/', views.asignatura_create, name='asignatura_create'),
    path('asignaturas/<int:pk>/editar/', views.asignatura_edit, name='asignatura_edit'),
    path('asignaturas/<int:pk>/eliminar/', views.asignatura_delete, name='asignatura_delete'),


]

