
from django.shortcuts import render, render_to_response,redirect
from django.http import JsonResponse
from app.models import *
from app.fomularios.cajaForm import *
from datetime import datetime


def registrarAperturacaja(request):
    if request.method == 'POST':
        Datos = request.POST
        hoy = datetime.today()
        print(Datos)
        usuario = request.user
        oEmpleado = Empleado.objects.get(usuario=usuario)

        oCaja = oEmpleado.caja
<<<<<<< HEAD
        montoInicial = 0.0
        try:
            oAperturaCaja = Aperturacaja.objects.filter(fecha__day=hoy.day, fecha__month=hoy.month, fecha__year=hoy.year)
            nuevo = float(oAperturaCaja.latest('pk').monto) + float(Datos['monto'])
            print(nuevo)
            if Datos['cmbTipo'] == '1':
                print(Datos['monto'])
                montoInicial = float(oAperturaCaja.latest('pk').monto) + float(Datos['monto'])
                print(montoInicial)
            elif Datos['cmbTipo'] == '2':
                montoInicial = oAperturaCaja.latest('pk').monto - float(Datos['monto'])
        except Exception as e:
            if Datos['cmbTipo'] == '1':
                montoInicial = 0 + float(Datos['monto'])
            elif Datos['cmbTipo'] == '2':
                montoInicial = 0 - float(Datos['monto'])

        apCaja = Aperturacaja(
            monto=montoInicial,
            estado=True,
            caja=oCaja,
            activo=True
        )
        apCaja.save()
=======
        monto = 0.0

        ultimoCierreCaja = Cierrecaja.objects.all().latest('pk')
>>>>>>> 966e2efb062b2758cb549d855bd2111214a99404

        monto = ultimoCierreCaja.monto

        oAperturaCaja = Aperturacaja(
            monto=monto,
            activo=True,
            estado=True,
            caja=oCaja
        )
        oAperturaCaja.save()
        
        return redirect('/Venta/nuevo/')

    else:
        
        context = {
        }
        return render(request,'caja/apertura.html',context)

def registrarOperacion(request):
    oDetalletipooperacions = Detalletipooperacion.objects.filter(estado=1)
    oCajas = Caja.objects.filter(estado=1)
    return render(request,'caja/operacion.html',{'oDetalletipooperacions':oDetalletipooperacions,'oCajas':oCajas})

# Reporte/caja/
def reporteCaja(request):
    cajas = Caja.objects.all()
    context = {
        'cajas': cajas
    }
    return render(request, 'reporte/caja.html', context)

# Reporte/caja/(?P<cajaId>\d+)/(?P<añoActual>\d+)/(?P<mesActual>\d+)/
def movimientosCaja(request, cajaId, añoActual, mesActual):
    caja = Caja.objects.get(id=cajaId)
    aperturaCaja = Aperturacaja.objects.filter(
        caja=caja,
        fecha__month=mesActual,
        fecha__year=añoActual
    )
    jsonFinal = []

    for apertura in aperturaCaja:
        jsonCaja = {}
        jsonCaja['fecha'] = apertura.fecha
        jsonCaja['monto'] = apertura.monto

        jsonFinal.append(jsonCaja)

    return JsonResponse(jsonFinal, safe=False)

# Reporte/caja/(?P<añoActual>\d+)/(?P<mesActual>\d+)/
def montoCajaActual(request, añoActual, mesActual):
    cajas = Caja.objects.all()
    jsonFinal = []
    monto = 0

    for caja in cajas:
        jsonMontoCaja = {}
        aperturaCaja = Aperturacaja.objects.filter(
            caja=caja,
            fecha__month=mesActual,
            fecha__year=añoActual
        )

        if aperturaCaja:
            aperturaCaja = aperturaCaja.latest('pk')
            monto += aperturaCaja.monto
            jsonMontoCaja['cajaId'] = caja.id
            jsonMontoCaja['caja'] = caja.nombre
            jsonMontoCaja['montoFinalCaja'] = monto
            jsonFinal.append(jsonMontoCaja)
        else:
            jsonMontoCaja['cajaId'] = caja.id
            jsonMontoCaja['caja'] = caja.nombre
            jsonMontoCaja['montoFinalCaja'] = '0.0'
            jsonFinal.append(jsonMontoCaja)

    return JsonResponse(jsonFinal, safe=False)
