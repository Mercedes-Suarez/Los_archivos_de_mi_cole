import os
from django import forms
from django.core.files import File
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render, redirect, get_object_or_404
from gestion.decorators import solo_admins_padres, solo_admins
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from win32com import client


from .models import (
    Archivo, Alumno, Asignatura, Padre,
    Usuario, 
    SolicitudEliminacionArchivo, 
    SolicitudEliminacionAlumno, 
    SolicitudEliminacionAsignatura, 
    CURSOS, TRIMESTRES
)
from .forms import ArchivoForm, AsignaturaForm, RegistroForm, AlumnoForm, PadreForm, Archivo

import os

class MiLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

Usuario = get_user_model()

# Solo permite acceso si el usuario es staff (admin)
def es_admin(user):
    return user.is_authenticated and user.tipo == 'admin'

def logout_with_message(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('/')

def inicio(request):
    return render(request, 'gestion/inicio.html')

def registro_padre(request):
    if request.method == 'POST':
        form = PadreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PadreForm()
    return render(request, 'gestion/registro.html', {'form': form})


# Listar padre
@solo_admins  

def padre_list(request):
    padres = Usuario.objects.filter(tipo='padre')
    return render(request, 'gestion/padre_list.html', {'padres': padres})

#  Crear padre
@solo_admins

def padre_create(request):
    if request.method == 'POST':
        form = PadreForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Padre.objects.create(usuario=usuario, nombre=usuario.username)
            
            return redirect('login')
    else:
        form = PadreForm()
    return render(request, 'gestion/registro.html', {'form': form})

#  Editar padre
def padre_edit(request, pk):
    padre = get_object_or_404(Usuario, pk=pk, tipo='padre')
    if request.method == 'POST':
      form = PadreForm(request.POST or None, instance=padre)
      if form.is_valid():
        form.save()
        return redirect('padre_list')
    else:
      form = PadreForm(instance=padre)  
    return render(request, 'gestion/padre_form.html', {'form': form})

#  Eliminar padre
@solo_admins
def padre_delete(request, pk):
    padre = get_object_or_404(Usuario, pk=pk, tipo='padre')
    if request.method == 'POST':
        padre.delete()
        return redirect('padre_list')
    return render(request, 'gestion/padre_confirm_delete.html', {'padre': padre})

@login_required
def acceso_alumno(request):
    if not hasattr(request.user, 'alumno'):
        messages.error(request, "Este acceso es solo para alumnos.")
        return redirect('inicio')

    alumno = request.user.alumno
    archivos = Archivo.objects.filter(curso=alumno.curso)

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

@login_required
@solo_admins_padres
def archivo_list(request):
    user = request.user
    is_padre = (user.tipo == 'padre')

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
 
    if is_padre and not user.is_staff:
        archivos = archivos.filter(subido_por=user)

    context = {
        'is_padre': is_padre,
        'archivos': archivos,
        'asignaturas': asignaturas,
        'asignatura_actual': asignatura_actual,
        'trimestre_actual': trimestre_actual,
        'curso_actual': curso_actual,
        'cursos_primaria': CURSOS_PRIMARIA,
        'cursos_secundaria': CURSOS_SECUNDARIA,
        
        'extensiones_embed': EXTENSIONES_EMBED
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

@login_required
@solo_admins_padres
def archivo_create(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid(): 
            archivo = form.save(commit=False)
            archivo.subido_por = request.user

            original = archivo.archivo

            if original and original.name.endswith('.ppsx'):
                import uuid
                from win32com import client
                from django.core.files import File

                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                temp_dir = os.path.join(BASE_DIR, 'temp_uploads')
                os.makedirs(temp_dir, exist_ok=True)

                filename = f"{uuid.uuid4()}.ppsx"
                temp_path = os.path.join(temp_dir, filename)

                try:
                    with open(temp_path, 'wb+') as temp_file:
                        for chunk in original.chunks():
                            temp_file.write(chunk)

                    ppt_app = client.Dispatch("PowerPoint.Application")
                    ppt_app.Visible = 1
                    presentation = ppt_app.Presentations.Open(temp_path, WithWindow=False)
                    ruta_convertido = temp_path.replace(".ppsx", ".pptx")
                    presentation.SaveAs(ruta_convertido, 24)
                    presentation.Close()
                    ppt_app.Quit()

                    with open(ruta_convertido, 'rb') as f:
                        archivo.archivo.save(original.name.replace('.ppsx', '.pptx'), File(f), save=False)

                except Exception as e:
                    # Opcional: registrar el error o mostrar mensaje
                    print(f"Error al convertir el archivo: {e}")
                    form.add_error('archivo', 'Error al convertir el archivo PPSX. Intente con un archivo válido.')
                    return render(request, 'gestion/archivo_form.html', {'form': form})

                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    if os.path.exists(ruta_convertido):
                        os.remove(ruta_convertido)

            archivo.save()
            return redirect('archivo_list')
        else:
            return render(request, 'gestion/archivo_form.html', {'form': form})
    else:
        form = ArchivoForm()
        return render(request, 'gestion/archivo_form.html', {'form': form})


@login_required
@solo_admins_padres

def archivo_editar(request, pk):
    if not request.user.is_staff and archivo.subido_por != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este archivo.")

    archivo = get_object_or_404(Archivo, pk=pk)
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('archivo_editar', args=[archivo.pk])}?success=edit")
    else:
        form = ArchivoForm(instance=archivo)
    return render(request, 'gestion/archivo_editar.html', {'form': form})

@login_required
@solo_admins_padres

def solicitar_eliminacion_archivo(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)

    if not request.user.is_staff and archivo.subido_por != request.user:
        return HttpResponseForbidden("No tienes permiso para solicitar la eliminación de este archivo.")

    ya_solicitada = SolicitudEliminacionArchivo.objects.filter(
        archivo=archivo,
        solicitante=request.user,
        procesado=False
    ).exists()

    if ya_solicitada:
        messages.warning(request, "Ya has solicitado la eliminación de este archivo.")
    else:
        SolicitudEliminacionArchivo.objects.create(
            archivo=archivo,
            solicitante=request.user,
        )

        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user and admin_user.email:
            send_mail(
                subject='Solicitud de eliminación de archivo',
                message=f'El usuario {request.user.username} ha solicitado eliminar el archivo "{archivo.nombre_archivo}".',
                from_email='noreply@micolegio.com',
                recipient_list=[admin_user.email],
                fail_silently=True,
            )

        messages.info(request, "Solicitud enviada al administrador.")

    return redirect('archivo_list')  # Asegúrate de tener esta vista/URL

@login_required
@solo_admins_padres

def aprobar_eliminacion_archivo(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    SolicitudEliminacionArchivo.objects.filter(archivo=archivo, procesado=False).update(procesado=True)
    archivo.delete()
    messages.success(request, "Archivo eliminado y solicitud procesada.")
    return redirect('panel_admin_archivos')  # Define esta URL

@login_required
@solo_admins_padres

def rechazar_eliminacion_archivo(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    SolicitudEliminacionArchivo.objects.filter(archivo=archivo, procesado=False).update(procesado=True)
    messages.info(request, "Solicitud de eliminación rechazada.")
    return redirect('panel_admin_archivos')

@login_required
@solo_admins_padres
def archivo_delete(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)

    if not request.user.is_staff and archivo.subido_por != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este archivo.")

    if request.method == 'POST':
        archivo.delete()
        messages.success(request, "Archivo eliminado correctamente.")
        return redirect('archivo_list')
    
    return render(request, 'gestion/archivo_confirm_delete.html', {'archivo': archivo})



@login_required
@solo_admins_padres

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

@login_required
@solo_admins_padres
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


@login_required
@solo_admins_padres
def asignatura_list(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'gestion/asignatura_list.html', {'asignaturas': asignaturas})


@login_required
@solo_admins_padres
def solicitar_eliminacion_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)

    ya_solicitada = SolicitudEliminacionAsignatura.objects.filter(
        asignatura=asignatura,
        solicitante=request.user,
        procesado=False
    ).exists()

    if ya_solicitada:
        messages.warning(request, "Ya has solicitado la eliminación de esta asignatura.")
    else:
        SolicitudEliminacionAsignatura.objects.create(
            asignatura=asignatura,
            solicitante=request.user,
        )

        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user and admin_user.email:
            send_mail(
                subject='Solicitud de eliminación de asignatura',
                message=f'El usuario {request.user.username} ha solicitado eliminar la asignatura "{asignatura.nombre}".',
                from_email='noreply@micolegio.com',
                recipient_list=[admin_user.email],
                fail_silently=True,
            )

        messages.info(request, "Solicitud enviada al administrador.")

    return redirect('asignatura_list')

@login_required
@solo_admins_padres

def aprobar_eliminacion_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    SolicitudEliminacionAsignatura.objects.filter(asignatura=asignatura, procesado=False).update(procesado=True)
    asignatura.delete()
    messages.success(request, "Asignatura eliminada y solicitud procesada.")
    return redirect('panel_admin_asignaturas')

@login_required
@solo_admins_padres

def rechazar_eliminacion_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    SolicitudEliminacionAsignatura.objects.filter(asignatura=asignatura, procesado=False).update(procesado=True)
    messages.info(request, "Solicitud de eliminación rechazada.")
    return redirect('panel_admin_asignaturas')


@login_required
@solo_admins_padres

def asignatura_delete(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        asignatura.delete()
        messages.success(request, "Asignatura eliminada correctamente.")
        return redirect('asignatura_list')

    return render(request, 'gestion/asignatura_confirm_delete.html', {'asignatura': asignatura})


User = get_user_model()

# Vistas para CRUD de Alumnos
@login_required
@solo_admins_padres
def alumno_create(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)

            # Crear nombre de usuario único
            username_base = alumno.nombre.lower().replace(" ", "_")
            username = username_base
            contador = 1
            while Usuario.objects.filter(username=username).exists():
                username = f"{username_base}_{contador}"
                contador += 1

            password = 'colegio123'

            usuario = Usuario.objects.create_user(
                username=username,
                password=password,
                email=""
            )

            usuario.tipo = 'alumno'
            usuario.is_active = True
            usuario.save()

            alumno.usuario = usuario

            if not request.user.is_staff:
                alumno.padre = request.user

            alumno.save()

            return redirect('alumno_list')
    else:
        form = AlumnoForm()

    return render(request, 'gestion/alumno_form.html', {'form': form})

@login_required
@solo_admins_padres

def alumno_list(request):
    curso_filtro = request.GET.get('curso')
    buscar = request.GET.get('buscar', '')
    
    if request.user.is_staff or request.user.is_superuser:
        alumnos = Alumno.objects.all()
    else:  # es padre
        alumnos = Alumno.objects.filter(padre=request.user)

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

@login_required
@solo_admins_padres

def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if not request.user.is_staff and alumno.padre != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este alumno.")

    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumno actualizado correctamente.")
            return redirect('alumno_list')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'gestion/alumno_form.html', {'form': form})

@login_required
@solo_admins_padres

def solicitar_eliminacion_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    # Solo el padre del alumno o el staff puede solicitar
    if not request.user.is_staff and alumno.padre != request.user:
        return HttpResponseForbidden("No tienes permiso para solicitar la eliminación de este alumno.")

    ya_solicitada = SolicitudEliminacionAlumno.objects.filter(
        alumno=alumno,
        solicitante=request.user,
        procesado=False
    ).exists()

    if ya_solicitada:
        messages.warning(request, "Ya has solicitado la eliminación de este alumno.")
    else:
        SolicitudEliminacionAlumno.objects.create(
            alumno=alumno,
            solicitante=request.user,
        )

        # Enviar correo al superusuario
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user and admin_user.email:
            send_mail(
                subject='Solicitud de eliminación de alumno',
                message=f'El usuario {request.user.username} ha solicitado eliminar al alumno "{alumno.nombre}".',
                from_email='noreply@micolegio.com',
                recipient_list=[admin_user.email],
                fail_silently=True,
            )

        messages.info(request, "Solicitud enviada al administrador.")

    return redirect('alumno_list')

@login_required
@solo_admins_padres

def enviar_notificacion(usuario, mensaje):
    if usuario.email:
        send_mail(
            subject="Nueva solicitud",
            message=mensaje,
            from_email="noreply@micolegio.com",
            recipient_list=[usuario.email],
            fail_silently=True,
        )


@login_required
@solo_admins_padres

def aprobar_eliminacion_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    SolicitudEliminacionAlumno.objects.filter(alumno=alumno, procesado=False).update(procesado=True)
    alumno.delete()
    messages.success(request, "Alumno eliminado y solicitud procesada.")
    return redirect('panel_admin_alumnos')

@login_required
@solo_admins

def rechazar_eliminacion_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    SolicitudEliminacionAlumno.objects.filter(alumno=alumno, procesado=False).update(procesado=True)
    messages.info(request, "Solicitud de eliminación rechazada.")
    return redirect('panel_admin_alumnos')


@login_required
@solo_admins_padres  # Antes: solo_admins

def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if not request.user.is_staff and alumno.padre != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este alumno.")

    if request.method == 'POST':
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect('alumno_list')
    return render(request, 'gestion/alumno_confirm_delete.html', {'alumno': alumno})

@login_required
@solo_admins

def panel_admin_padres(request):
    padres = Usuario.objects.filter(tipo='padre').prefetch_related('hijos')
    return render(request, 'gestion/panel_admin_padres.html', {
        'padres': padres
    })

@login_required
@solo_admins

def panel_admin_alumnos(request):
    alumnos = Alumno.objects.select_related('usuario').all()

    context = {
        'alumnos': alumnos,
    }
    return render(request, 'gestion/panel_admin_alumnos.html', context)

@login_required
@solo_admins

def lista_solicitudes(request):
    solicitudes_alumnos = SolicitudEliminacionAlumno.objects.all().order_by('-fecha_solicitud')
    solicitudes_archivos = SolicitudEliminacionArchivo.objects.all().order_by('-fecha_solicitud')
    solicitudes_asignaturas = SolicitudEliminacionAsignatura.objects.all().order_by('-fecha_solicitud')

    return render(request, 'gestion/lista_solicitudes.html', {
        'solicitudes_alumnos': solicitudes_alumnos,
        'solicitudes_archivos': solicitudes_archivos,
        'solicitudes_asignaturas': solicitudes_asignaturas,
    })