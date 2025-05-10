from django.urls import path

from .views import archivo_list, archivo_create, editar_archivo, archivo_delete, CustomLogoutView

urlpatterns = [
    path('', archivo_list, name='archivo_list'),
    path('nuevo/', archivo_create, name='archivo_create'),
    path('archivo/editar/<int:pk>', editar_archivo, name='editar_archivo'),
    path('borrar/<int:pk>/', archivo_delete, name='archivo_delete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
]
