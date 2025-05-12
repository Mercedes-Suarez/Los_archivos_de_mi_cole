# gestion/forms.py
from django import forms
from .models import Archivo, Asignatura

class ArchivoForm(forms.ModelForm):
    nueva_asignatura = forms.CharField(
        required=False,
        label="Nueva asignatura",
        widget=forms.TextInput(attrs={
            'placeholder': 'Introduce una nueva asignatura si no aparece en la lista'
        })
    )
  #  enlace_externo = forms.URLField(
  #      required=False,
   #     label="Enlace externo",
   #     widget=forms.TextInput(attrs={
     #       'placeholder': 'https://drive.google.com/...',
     #   })
   # )

    class Meta:
        model = Archivo
        fields = ['archivo', 'enlace_externo', 'asignatura', 'trimestre']

    def clean(self):
        cleaned_data = super().clean()
        archivo = cleaned_data.get('archivo')
        enlace = cleaned_data.get('enlace_externo')

        if not archivo and not enlace:
            raise forms.ValidationError("Debes subir un archivo o proporcionar un enlace.")

        if archivo and archivo.size > 20 * 1024 * 1024:
            raise forms.ValidationError("El archivo es demasiado grande (20MB máx.). Usa un enlace externo.")
        
        return cleaned_data
