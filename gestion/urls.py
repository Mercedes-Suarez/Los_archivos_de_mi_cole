from django.urls import path
from . import views

urlpatterns = [
    path('', views.archivo_list, name='archivo_list'),
    path('crear/', views.archivo_create, name='archivo_create'),
    path('eliminar/<int:pk>/', views.archivo_delete, name='archivo_delete'),
]
