import os
from django.core.files import File
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render, redirect, get_object_or_404
from gestion.decorators import solo_padres_y_admins
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.files.base import ContentFile
from win32com import client


from .models import Archivo,Alumno, Asignatura, CURSOS, TRIMESTRES
from .forms import ArchivoForm, AsignaturaForm, RegistroForm, AlumnoForm, Archivo

import os

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

@login_required
@solo_padres_y_admins
def acceso_alumno(request):
        usuario = request.user
        try:
            alumno = Alumno.objects.get(padre=usuario)
            archivos = Archivo.objects.filter(curso=alumno.curso)
        except Alumno.DoesNotExist:
            alumno = None
            archivos = None

        return render(request, 'gestion/acceso_alumno.html', {
             'alumno': alumno,
             'archivos': archivos
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

EXTENSIONES_EMBED = ["pptx", "docx"]

def archivo_ver(request, id):
    archivo = get_object_or_404(Archivo, id=id)

    enlace_modificado = None
    texto_contenido = None
 # Leer archivos de texto
    if archivo.archivo and archivo.extension == "txt":
        try:
            with archivo.archivo.open('r') as f:
                texto_contenido = f.read()
        except Exception as e:
            texto_contenido = f"⚠️ Error al leer el archivo: {str(e)}"
 
 # Archivos de Office locales (doc, ppt, etc.)   
    elif archivo.extension in EXTENSIONES_EMBED and archivo.archivo:
        enlace_modificado = f"https://view.officeapps.live.com/op/embed.aspx?src=http://127.0.0.1:8000{archivo.archivo.url}"

# Enlace externo de Google Drive
    elif archivo.enlace_externo and "drive.google.com" in archivo.enlace_externo:
        enlace_modificado = archivo.enlace_externo.replace("view?usp=sharing", "preview")

    return render(request, 'gestion/archivo_ver.html', {
        'archivo': archivo,
        'enlace_modificado': enlace_modificado,
        'extensiones_embed': EXTENSIONES_EMBED,
        'texto_contenido': texto_contenido
    })
def convertir_ppsx_a_pptx(ruta_ppsx):
    ppt_app = client.Dispatch("PowerPoint.Application")
    ppt_app.Visible = 1
    presentation = ppt_app.Presentations.Open(ruta_ppsx, WithWindow=False)
    
    ruta_salida = ruta_ppsx.replace(".ppsx", ".pptx")
    presentation.SaveAs(ruta_salida, 24)  # 24 = formato .pptx
    presentation.Close()
    ppt_app.Quit()
    return ruta_salida

@solo_padres_y_admins
def archivo_create(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid(): 
            archivo = form.save(commit=False)
            
            if archivo.archivo and archivo.archivo.name.endswith('.ppsx'):
                original = archivo.archivo
                
                # Ruta base del proyecto (donde está manage.py)
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                temp_dir = os.path.join(BASE_DIR, 'temp_uploads')

                # Crear carpeta si no existe
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Construir ruta temporal para guardar archivo subido
                temp_path = os.path.join(temp_dir, original.name)

                # Guardar el archivo temporalmente
                with open(temp_path, 'wb+') as temp_file:
                    for chunk in original.chunks():
                        temp_file.write(chunk)

                # Convertir .ppsx a .pptx con PowerPoint
                from win32com import client
                ppt_app = client.Dispatch("PowerPoint.Application")
                ppt_app.Visible = 1
                presentation = ppt_app.Presentations.Open(temp_path, WithWindow=False)
                ruta_convertido = temp_path.replace(".ppsx", ".pptx")
                presentation.SaveAs(ruta_convertido, 24)
                presentation.Close()
                ppt_app.Quit()

                from django.core.files import File
                with open(ruta_convertido, 'rb') as f:
                    archivo.archivo.save(original.name.replace('.ppsx', '.pptx'), File(f), save=False)

                # Eliminar archivos temporales
                os.remove(temp_path)
                os.remove(ruta_convertido)

            # Guardar el objeto final
            archivo.save()
            return redirect('archivo_list')
        
        else:
            return render(request, 'gestion/archivo_form.html', {'form': form})
    else:
        form = ArchivoForm()
        return render(request, 'gestion/archivo_form.html', {'form': form})

@solo_padres_y_admins
def archivo_editar(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('archivo_editar', args=[archivo.pk])}?success=edit")
    else:
        form = ArchivoForm(instance=archivo)
    return render(request, 'gestion/archivo_editar.html', {'form': form})

@solo_padres_y_admins
def archivo_delete(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == "POST":
        archivo.delete()
        messages.success(request, "Archivo eliminado con éxito.")
        return redirect('archivo_list')
    return render(request, 'gestion/archivo_confirm_delete.html', {'archivo': archivo})



@solo_padres_y_admins
def asignatura_list(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'gestion/asignatura_list.html', {'asignaturas': asignaturas})

@solo_padres_y_admins
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

@solo_padres_y_admins
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

@solo_padres_y_admins
def asignatura_delete(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        asignatura.delete()
        return redirect('asignatura_list')
    return render(request, 'gestion/asignatura_confirm_delete.html', {'asignatura': asignatura})

User = get_user_model()

# Vistas para CRUD de Alumnos
@solo_padres_y_admins
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

@solo_padres_y_admins
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

@solo_padres_y_admins
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

@solo_padres_y_admins
def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect('alumno_list')
    return render(request, 'gestion/alumno_confirm_delete.html', {'alumno': alumno})

@login_required
@solo_padres_y_admins
def panel_admin_alumnos(request):
    alumnos = Alumno.objects.select_related('usuario').all()

    context = {
        'alumnos': alumnos,
    }
    return render(request, 'gestion/panel_admin_alumnos.html', context)
