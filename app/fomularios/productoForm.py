from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        exclude={'estado', 'presentacions','valor'}

        labels = {
            'nombre': 'Nombre producto',
            'codigo': 'Codigo de producto',
            'imagen': 'Imagen',
            'url': 'Url',
        }

        widgets = {
        #    'password': forms.PasswordInput(),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control-p'}),
            'imagen': forms.FileInput(),
            'url': forms.TextInput(attrs={'class': 'form-control-p'}),
        }
