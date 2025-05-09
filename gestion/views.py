from django.shortcuts import render, redirect, get_object_or_404
from .models import Archivo
from .forms import ArchivoForm

def archivo_list(request):
    archivos = Archivo.objects.all()
    return render(request, 'gestion/archivo_list.html', {'archivos': archivos})

def archivo_create(request):
    form = ArchivoForm(request.POST or request.FILES)
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

