# gestion/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Archivo, Asignatura, Usuario

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

        if not archivo and not enlace:
            raise forms.ValidationError("Debes subir un archivo o proporcionar un enlace.")

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