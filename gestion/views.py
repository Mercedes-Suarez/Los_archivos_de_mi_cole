from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, get_user_model
from django.contrib import messages


from .models import Archivo,Alumno, Asignatura
from .forms import ArchivoForm, AsignaturaForm, RegistroForm

Usuario = get_user_model()

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'gestion/registro.html', {'form': form})

# Solo permite acceso si el usuario es staff (admin)
def es_admin(user):
    return user.is_staff

def logout_with_message(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('/')

def inicio(request):
    return render(request, 'gestion/inicio.html')

def acceso_alumno(request):
    archivos = None
    alumno = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            alumno = Alumno.objects.get(nombre__iexact=nombre)
            archivos = Archivo.objects.filter(curso=alumno.curso)
        except Alumno.DoesNotExist:
            alumno = None

    return render(request, 'gestion/acceso_alumno.html', {
        'archivos': archivos,
        'alumno': alumno
    })

def archivo_list(request):
    curso_actual = request.GET.get('curso', '')
    trimestre_actual = request.GET.get('trimestre', '')
    asignatura_actual = request.GET.get('asignatura', '')

    archivos = Archivo.objects.all()

    if asignatura_actual:
        archivos = archivos.filter(asignatura_id=asignatura_actual)
    if trimestre_actual:
        archivos = archivos.filter(trimestre=trimestre_actual)
    if curso_actual:
        archivos = archivos.filter(curso=curso_actual)

    context = {
         "archivos": archivos,
         "asignaturas": Asignatura.objects.all(),
         "curso_actual": curso_actual,
         "trimestre_actual": trimestre_actual,
         "asignatura_actual": asignatura_actual,
    }
    
    return render(request, 'gestion/archivo_list.html', context)
    
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