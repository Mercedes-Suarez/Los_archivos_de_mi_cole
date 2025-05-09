from django import forms
from .models import Archivo

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['nombre', 'tipo', 'ruta', 'trimestre']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if " " in nombre:
            raise forms.ValidationError("El nombre no debe tener espacios")
        return nombre