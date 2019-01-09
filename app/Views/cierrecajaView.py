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
    oAperturaCaja = Aperturacaja.objects.filter(caja_id=empleado.caja_id)
    montoTotal = 0.0

    if oAperturaCaja:
        if oAperturaCaja.estado == True:   
            oAperturaCaja = oAperturaCaja.latest('id')
            montoTotal += oAperturaCaja.monto
            oOperacions = Operacion.objects.filter(fecha__range=[oAperturaCaja.fecha,fechaHoraActual])
        
            for oOperacion in oOperacions:
                print('monto total: %s' % montoTotal)
                montoTotal = montoTotal + float(oOperacion.monto)
        else:
            res == 'Error ya se hizo el cierre de caja hoy'
            context = {
                'msj': res
            }
            return redirect('/error/cierreCaja-efectuado/')
        
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
        # print(res)
        context = {
            'msj': res
        }
        return redirect('/Venta/nuevo/')
    else:
        # print(res)
        cierreCaja.save()
        oAperturaCaja.estado = False
        oAperturaCaja.save()
        context = {
            'msj': 'res'
        }
        return redirect('/Venta/nuevo/')

def validarCierreCaja(cierreCaja):
    print('monto cierre Caja = %s' % cierreCaja.monto)
    ultimoCierreCaja = Cierrecaja.objects.all().latest('pk')
    print('fecha cierre caja %s' % ultimoCierreCaja.fecha.date())
    if cierreCaja.fecha.date() == ultimoCierreCaja.fecha.date():
        msj = 'Error ya se hizo el cierre de caja hoy'
        # print(msj)
        # return msj
    else:
        msj = 'Se cerró la caja'
        # print(msj)
        # return msj
    print(msj)
    return msj