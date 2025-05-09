# gestion/forms.py
from django import forms
from .models import Archivo

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['archivo', 'asignatura', 'trimestre']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo.size > 10*1024*1024:  # 10MB
            raise forms.ValidationError("El archivo es demasiado grande.")
        return archivo
