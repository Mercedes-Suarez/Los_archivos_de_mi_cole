from django.urls import path
from .views import ArchivoListView, ArchivoCreateView, ArchivoDeleteView

urlpatterns = [
    path('archivos/', ArchivoListView.as_view(), name='archivo-list'),
    path('archivos/nuevo/', ArchivoCreateView.as_view(), name='archivo-create'),
    path('archivos/borrar/<int:pk>/', ArchivoDeleteView.as_view(), name='archivo-delete'),
]
