from django.urls import path
from .views import archivo_list, archivo_create, archivo_delete

urlpatterns = [
    path('', archivo_list, name='archivo_list'),
    path('nuevo/', archivo_create, name='archivo_create'),
    path('borrar/<int:pk>/', archivo_delete, name='archivo_delete'),
]
