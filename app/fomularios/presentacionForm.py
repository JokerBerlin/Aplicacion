from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *

class PresentacionForm(ModelForm):
    class Meta:
        model = Presentacion
        exclude={'estado'}

        labels = {
            'nombre': 'Nombre presentacion',
            'codigo': 'Codigo presentacion',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control-p'}),
        }
