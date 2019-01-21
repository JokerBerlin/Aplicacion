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

    hoy = datetime.today()
    usuario = request.user
    empleado = Empleado.objects.get(usuario_id=usuario)
    oAperturaCaja = Aperturacaja.objects.filter(caja_id=empleado.caja_id,fecha__year=hoy.year,fecha__month=hoy.month,fecha__day=hoy.day).latest('id')
    montoTotal = 0.0
    print(oAperturaCaja.estado)

    if oAperturaCaja:
        if oAperturaCaja.latest('pk').estado == True:
            oAperturaCaja = oAperturaCaja.latest('id')
            montoTotal += oAperturaCaja.monto
            oOperacions = Operacion.objects.filter(fecha__range=[oAperturaCaja.fecha,hoy])

            for oOperacion in oOperacions:
                print('monto total: %s' % montoTotal)
                montoTotal = montoTotal + float(oOperacion.monto)
        else:
            return redirect('/error/cierreCaja-efectuado/')

    else:
        return redirect('/Caja/apertura/')

    cierreCaja = Cierrecaja(
        fecha=datetime.now(),
        monto=montoTotal,
        estado=True,
        aperturacaja=oAperturaCaja
    )

    res = validarCierreCaja(cierreCaja)

    if res == 'Error ya se hizo el cierre de caja hoy':
        # print(res)
        context = {
            'msj': res
        }
        return redirect('/error/cierreCaja-efectuado/')
    else:
        # print(res)
        cierreCaja.save()
        oAperturaCaja.estado = False
        oAperturaCaja.save()
        context = {
            'msj': 'res'
        }
        return redirect('/Caja/exito-cierre')

def exitoCierreCaja(request):
    context = {
        'msj': 'Se Cerro la caja exitosamente'
    }
    return render(request, 'caja/exito.html')

def validarCierreCaja(cierreCaja):
    print('monto cierre Caja = %s' % cierreCaja.monto)
    ultimoCierreCaja = Cierrecaja.objects.all().latest('pk')
    print('fecha cierre caja %s' % ultimoCierreCaja.fecha.date())
    if cierreCaja.fecha.date() == ultimoCierreCaja.fecha.date():
        msj = 'Error ya se hizo el cierre de caja hoy'
    else:
        msj = 'Se cerró la caja'
    print(msj)
    return msj

def mostrarCierre(request):
    hoy = datetime.today()
    user = request.user
    empleado = Empleado.objects.get(usuario_id=user.id)
    fecha=''
    try:
        aperturaCaja = Aperturacaja.objects.filter(fecha__year=hoy.year,fecha__month=hoy.month,fecha__day=hoy.day,caja_id=empleado.caja_id)
        for apertura in aperturaCaja:
            fecha = apertura.fecha
    except Exception as e:
        fecha = ''

    return render(request,'caja/cierre.html',{'fecha':fecha})
