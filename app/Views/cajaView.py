
from django.shortcuts import render, render_to_response,redirect
from django.http import JsonResponse
from app.models import *
from app.fomularios.cajaForm import *
from datetime import datetime

from app.validacionUser import validacionUsuario

def registrarAperturacaja(request):
    if request.method == 'POST':
        Datos = request.POST
        hoy = datetime.today()
        print(Datos)
        usuario = request.user
        oEmpleado = Empleado.objects.get(usuario=usuario)

        oCaja = oEmpleado.caja
        monto = 0.0

        try:
            ultimoCierreCaja = Cierrecaja.objects.all().latest('pk')
            if ultimoCierreCaja:
                monto = ultimoCierreCaja.monto
            else:
                monto = 0.0
        except Exception as e:
            monto = 0.0

        oAperturaCaja = Aperturacaja(
            monto=monto,
            activo=True,
            estado=True,
            caja=oCaja
        )
        oAperturaCaja.save()

        return redirect('/Venta/nuevo/')

    else:

        if not validacionUsuario(request.user) == 5:
            return redirect('/error/')

        context = {}
        return render(request,'caja/apertura.html',context)

def registrarOperacion(request):
    if request.method == 'POST':
        usuario = request.user
        empleado = Empleado.objects.get(usuario_id=usuario)
        hoy = datetime.today()
        try:
            oCaja = Aperturacaja.objects.get(caja_id=empleado.caja_id,estado=1,fecha__year=hoy.year, fecha__month=hoy.month,fecha__day = hoy.day)
            Datos = request.POST
            print(Datos)
            oDetalletipooperacion = Detalletipooperacion.objects.get(id=Datos['cmbOperacion'])
            monto = float(Datos['monto'])
            if oDetalletipooperacion.tipooperacion_id == '2':
                monto = monto * -1
            oOperacion = Operacion(
                monto = monto,
                descripcion = Datos['descripcion'],
                estado = 1,
                caja_id = oCaja.caja_id,
                detalletipooperacion_id=Datos['cmbOperacion']
            )
            oOperacion.save()
            return redirect('/Pedido/listar/2/')
        except Exception as e:
            return redirect('/Caja/apertura/')
    else:

        if not validacionUsuario(request.user) == 5:
            return redirect('/error/')

        tipoOperaciones = Tipooperacion.objects.filter(estado=1)
        detalleOperaciones = Detalletipooperacion.objects.filter(estado=1)
        return render(request,'caja/operacion.html',{'tipoOperaciones':tipoOperaciones,'detalleOperaciones':detalleOperaciones})

# Reporte/caja/
def reporteCaja(request):
    if not validacionUsuario(request.user) == 5:
        return redirect('/error/')
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
