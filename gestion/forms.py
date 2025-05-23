# gestion/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from gestion.models import Usuario
from .models import Archivo, Asignatura, Alumno

class PadreForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        user.tipo = 'padre'
        user.is_staff = False
        if commit:
            user.save()
        return user

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'curso']
        exclude = ['padre', 'usuario']
        labels = {
            'nombre': 'Nombre del alumno',
            'curso': 'Curso',
        }

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

class ArchivoForm(forms.ModelForm):
    nueva_asignatura = forms.CharField(required=False, label='Nueva Asignatura')

    class Meta:
        model = Archivo
        fields = ['archivo', 'enlace_externo', 'asignatura', 'trimestre', 'curso']

    def clean(self):
     cleaned_data = super().clean()
     archivo = cleaned_data.get('archivo')
     enlace = cleaned_data.get('enlace_externo')
     curso = cleaned_data.get('curso')
     asignatura = cleaned_data.get('asignatura')
     nueva_asignatura = cleaned_data.get('nueva_asignatura')

     if not archivo and not enlace:
        raise forms.ValidationError("Debes subir un archivo o proporcionar un enlace.")

     if asignatura == '__nueva__':
        if nueva_asignatura:
            asignatura_obj, _ = Asignatura.objects.get_or_create(nombre=nueva_asignatura)
            cleaned_data['asignatura'] = asignatura_obj
        else:
            self.add_error('nueva_asignatura', "Debes indicar un nombre para la nueva asignatura.")
    # 🟡 Si el usuario no elige __nueva__, no se hace nada — correcto

     if not archivo and not curso:
        raise forms.ValidationError("Debes señalar un curso.")

     if archivo and archivo.size > 20 * 1024 * 1024:
        raise forms.ValidationError("El archivo es demasiado grande (20MB máx.). Usa un enlace externo.")
    
     return cleaned_data


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la asignatura',
        }