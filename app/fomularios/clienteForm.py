from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre','direccion','numerodocumento','precio','longitud','latitud')

        labels={
            'nombre':'Nombre de cliente',
            'numerodocumento':'Dni',
            'direccion':'Residencia cliente',
            'precio':'Tipo de cliente',
            'longitud':'Longitud',
            'latitud':'latitud',

            }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numerodocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.Select(attrs={'class': 'form-control'}),
            'longitud': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'latitud': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
        }
