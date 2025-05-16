from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages


from .models import Archivo,Alumno, Asignatura, CURSOS, TRIMESTRES
from .forms import ArchivoForm, AsignaturaForm, RegistroForm, AlumnoForm, Archivo

import re

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

CURSOS_PRIMARIA = [
       ('1P', '1º Primaria'),
       ('2P', '2º Primaria'),
       ('3P', '3º Primaria'),
       ('4P', '4º Primaria'),
       ('5P', '5º Primaria'),
       ('6P', '6º Primaria'),
    ]
CURSOS_SECUNDARIA = [
       ('1S', '1º Secundaria'),
       ('2S', '2º Secundaria'),
       ('3S', '3º Secundaria'),
       ('4S', '4º Secundaria'),
    ]
TRIMESTRES = [
    (1, '1º Trimestre'), (2, '2º Trimestre'),
    (3, '3º Trimestre'), (4, 'Vacaciones'),
]

def archivo_list(request):

    archivos = Archivo.objects.all()
    asignaturas = Asignatura.objects.all()

    asignatura_actual = request.GET.get('asignatura', '')
    trimestre_actual = request.GET.get('trimestre', '')
    curso_actual = request.GET.get('curso', '')
    
    if asignatura_actual:
        archivos = archivos.filter(asignatura_id=asignatura_actual)
    if trimestre_actual:
        archivos = archivos.filter(trimestre=trimestre_actual)
    if curso_actual:
        archivos = archivos.filter(curso=curso_actual)
    
    context = {

        'archivos': archivos,
        'asignaturas': asignaturas,
        'asignatura_actual': asignatura_actual,
        'trimestre_actual': trimestre_actual,
        'curso_actual': curso_actual,
        'cursos_primaria': CURSOS_PRIMARIA,
        'cursos_secundaria': CURSOS_SECUNDARIA
           
    }
    return render(request, 'gestion/archivo_list.html', context)

def archivo_ver(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)

     # Validar que el enlace externo sea seguro (solo dominios permitidos)
    if archivo.enlace_externo and not re.match(r'^https?:\/\/(drive\.google\.com|youtube\.com|youtu\.be|dropbox\.com|onedrive\.live\.com|yourdomain\.com)', archivo.enlace_externo):
        archivo.enlace_externo = None  # O marca como no confiable

    return render(request, 'gestion/archivo_ver.html', {'archivo': archivo})

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

User = get_user_model()

# Vistas para CRUD de Alumnos
@user_passes_test(lambda u: u.is_staff)
def alumno_create(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)

            # Crear usuario asociado
            username = alumno.nombre.lower().replace(" ", "_")
            password = User.objects.make_random_password()  # O asigna una fija tipo 'colegio123'

            usuario = User.objects.create(
                username=username,
                password=make_password(password),
                email="",  # Opcional
            )

            # Marcar como alumno
            usuario.es_alumno = True
            usuario.save()

            # Enlazar con el alumno
            alumno.usuario = usuario
            alumno.save()
            return redirect('alumno_list')
    else:
        form = AlumnoForm()
    return render(request, 'gestion/alumno_form.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def alumno_list(request):
    curso_filtro = request.GET.get('curso')
    buscar = request.GET.get('buscar', '')

    alumnos = Alumno.objects.all()
    if curso_filtro:
        alumnos = alumnos.filter(curso=curso_filtro)
    if buscar:
        alumnos = alumnos.filter(nombre__icontains=buscar)

    cursos = Alumno._meta.get_field('curso').choices

    return render(request, 'gestion/alumno_list.html', {
        'alumnos': alumnos,
        'cursos': cursos,
        'curso_filtro': curso_filtro,
        'buscar': buscar,
    })

@user_passes_test(lambda u: u.is_staff)
def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumno actualizado correctamente.")
            return redirect('alumno_list')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'gestion/alumno_form.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect('alumno_list')
    return render(request, 'gestion/alumno_confirm_delete.html', {'alumno': alumno})

@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_admin_alumnos(request):
    alumnos = Alumno.objects.select_related('usuario').all()

    context = {
        'alumnos': alumnos,
    }
    return render(request, 'gestion/panel_admin_alumnos.html', context)
