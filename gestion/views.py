from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LogoutView
from .models import Archivo
from .forms import ArchivoForm

# Solo permite acceso si el usuario es staff (admin)
def es_admin(user):
    return user.is_staff

class CustomLogoutView(LogoutView):
    next_page = '/' 

@user_passes_test(es_admin)
def editar_archivo(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return redirect('lista_archivos')  # o la vista que tengas
    else:
        form = ArchivoForm(instance=archivo)
    return render(request, 'gestion/editar_archivo.html', {'form': form})

def inicio(request):
    return render(request, 'inicio.html')

def archivo_list(request):
    archivos = Archivo.objects.all()
    return render(request, 'gestion/archivo_list.html', {'archivos': archivos})

@require_http_methods(["GET", "POST"])
def archivo_create(request):
    form = ArchivoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('archivo_list')
    return render(request, 'gestion/archivo_form.html', {'form': form})

def archivo_delete(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == "POST":
        archivo.delete()
        return redirect('archivo_list')
    return render(request, 'gestion/archivo_confirm_delete.html', {'archivo': archivo})

