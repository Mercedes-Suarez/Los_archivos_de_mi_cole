from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib import messages


from .models import Archivo, Asignatura
from .forms import ArchivoForm, AsignaturaForm

# Solo permite acceso si el usuario es staff (admin)
def es_admin(user):
    return user.is_staff

def logout_with_message(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('/')

def inicio(request):
    return render(request, 'inicio.html')

def archivo_list(request):
    asignaturas = Asignatura.objects.all()
    archivos = Archivo.objects.all()
    cursos = Archivo.objects.all()

    asignatura_id = request.GET.get('asignatura')
    trimestre = request.GET.get('trimestre')
    curso = request.GET.get('curso')

    if asignatura_id:
        archivos = archivos.filter(asignatura_id=asignatura_id)
    if trimestre:
        archivos = archivos.filter(trimestre=trimestre)
    if curso:
        archivos = archivos.filter(curso=curso)

    return render(request, 'gestion/archivo_list.html', {
        'archivos': archivos,
        'asignaturas': asignaturas,
        'curso': cursos,
    })
    
@user_passes_test(lambda u: u.is_staff)
def archivo_create(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_asignatura = form.cleaned_data.get('nueva_asignatura')
            archivo = form.save(commit=False)
            if nueva_asignatura:
                asignatura_obj, _ = Asignatura.objects.get_or_create(nombre=nueva_asignatura)
                archivo.asignatura = asignatura_obj
            archivo.subido_por = request.user
            archivo.save()
            messages.success(request, "Archivo subido con éxito.")
            return redirect('archivo_list')  # Aquí rediriges al listado u otra vista de inicio admin
    else:
        form = ArchivoForm()
    return render(request, 'gestion/archivo_form.html', {'form': form})

@user_passes_test(es_admin)
def editar_archivo(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return redirect('archivo_list')  # o la vista que tengas
    else:
        form = ArchivoForm(instance=archivo)
    return render(request, 'gestion/archivo_form.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def archivo_delete(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == "POST":
        archivo.delete()
        messages.success(request, "Archivo eliminado con éxito.")
        return redirect('archivo_list')
    return render(request, 'gestion/archivo_confirm_delete.html', {'archivo': archivo})



@user_passes_test(lambda u: u.is_staff)
def asignatura_list(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'gestion/asignatura_list.html', {'asignaturas': asignaturas})

@user_passes_test(lambda u: u.is_staff)
def asignatura_create(request):
        if request.method == 'POST':
         form = AsignaturaForm(request.POST)
         if form.is_valid():
               form.save()
               messages.success(request, "Asignatura creada correctamente.")
               return render(request, "gestion/asignatura_crear.html", {"form": form})
         else:
            messages.error(request, "Corrige los errores del formulario.")
        else:
           form = AsignaturaForm()
        return render(request, "gestion/asignatura_crear.html", {"form": form})

@user_passes_test(lambda u: u.is_staff)
def asignatura_edit(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == "POST":
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignatura modificada correctamente.")
            return render(request, "gestion/asignatura_editar.html", {
                "form": form,
                "asignatura": asignatura,
            })
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = AsignaturaForm(instance=asignatura)
    return render(request, "gestion/asignatura_editar.html", {
        "form": form,
        "asignatura": asignatura,
    })

@user_passes_test(lambda u: u.is_staff)
def asignatura_delete(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        asignatura.delete()
        return redirect('asignatura_list')
    return render(request, 'gestion/asignatura_confirm_delete.html', {'asignatura': asignatura})