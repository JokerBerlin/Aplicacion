# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.cierrecajaForm import *
from datetime import date, datetime

from app.validacionUser import validacionUsuario

perfiles_correctos = [1, 4]

@login_required
def cierreCaja(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    fechaHoraActual = datetime.today()
    usuario = request.user
    empleado = Empleado.objects.get(usuario_id=usuario)
    oAperturaCaja = Aperturacaja.objects.filter(estado=1,caja_id=empleado.caja_id)
    montoTotal = 0.0

    if oAperturaCaja:
        oAperturaCaja = oAperturaCaja.latest('id')
        oOperacions = Operacion.objects.filter(fecha__range=[oAperturaCaja.fecha,fechaHoraActual])
        
        for oOperacion in oOperacions:
            montoTotal = montoTotal + float(oOperacion.monto)
    else:
        oAperturaCaja = Aperturacaja(
            monto=0.0,
            activo=True,
            estado=True,
            caja=empleado.caja
        )
        oAperturaCaja.save()
    
    cierreCaja = Cierrecaja(
        fecha=datetime.now(),
        monto=montoTotal,
        estado=True,
        aperturacaja=oAperturaCaja
    )

    res = validarCierreCaja(cierreCaja)

    if res == 'Error ya se hizo el cierre de caja hoy':
        context = {
            'msj': 'res' 
        }
        return redirect('/Venta/nuevo/')
    else:
        cierreCaja.save()
        oAperturaCaja.estado = False
        oAperturaCaja.save()
        context = {
            'msj': 'res'
        }
        return redirect('/Venta/nuevo/')

def validarCierreCaja(cierreCaja):
    hoy = date.today()
    print('fecha cierre caja %s' % cierreCaja.fecha.date())
    if cierreCaja.fecha.date() == hoy:
        msj = 'Error ya se hizo el cierre de caja hoy'
        # print(msj)
        # return msj
    else:
        msj = 'Se cerró la caja'
        # print(msj)
        # return msj
    print(msj)
    return msj