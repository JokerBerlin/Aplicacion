from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *

class AperturaCajaForm(ModelForm):
    class Meta:
        model = Aperturacaja
        exclude={'estado', 'caja','activo'}

        labels = {
            'monto': 'Monto de apertura',

        }

        widgets = {
        #    'password': forms.PasswordInput(),
            'monto': forms.NumberInput(attrs={'class': 'form-control-p'}),
            }
