
from django.shortcuts import render, render_to_response,redirect
from django.http import JsonResponse
from app.models import *
from app.fomularios.cajaForm import *


def registrarAperturacaja(request):
    if request.method == 'POST':
        Datos = request.POST
        form = AperturaCajaForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            print('esto')
            oCaja = Caja.objects.get(id = int(Datos['cmbCaja']))
            print(oCaja.id)
            form.estado=1
            form.activo=1
            form.caja_id = oCaja.id
            print('esta')
            print(form.caja_id)
            print(form)
            form.save()
            return redirect('/Producto/listar/')
        else:
            return render(request,'caja/apertura.html',{})

    else:
        form = AperturaCajaForm()
        oCajas = Caja.objects.filter(estado=1)

        return render(request,'caja/apertura.html',{'form': form,'cajas':oCajas,})

def registrarOperacion(request):
    oDetalletipooperacions = Detalletipooperacion.objects.filter(estado=1)
    oCajas = Caja.objects.filter(estado=1)
    return render(request,'caja/operacion.html',{'oDetalletipooperacions':oDetalletipooperacions,'oCajas':oCajas,})

def movimientosCaja(request, cajaId, añoActual, mesActual):
    caja = Caja.objects.get(id=cajaId)
    aperturaCajas = Aperturacaja.objects.filter(
        caja=caja,
        fecha__month=mesActual,
        fecha__year=añoActual
    )
    print(aperturaCajas)
    cierreCajas = Cierrecaja.objects.filter(aperturacaja=aperturaCajas)
    jsonFinal = []

    for apCaja in aperturaCajas:
        jsonCaja = {}
        fecha = str(apCaja.fecha.day) + '-' + str(apCaja.fecha.month) + '-' + str(apCaja.fecha.year)
        jsonCaja['fecha'] = fecha
        jsonCaja['monto'] = apCaja.monto

        jsonFinal.append(jsonCaja)
    
    return JsonResponse(jsonFinal, safe=False)

def movimientosCajaTotales(request, añoActual, mesActual):
    cajas = Caja.objects.all()
    jsonFinal = []
    monto = 0

    for caja in cajas:
        jsonMontoCaja = {}  
        aperturaCaja = Aperturacaja.objects.filter(
            caja=caja,
            fecha__month=mesActual,
            fecha__year=añoActual
        ).latest('pk')

        monto += aperturaCaja.monto
        jsonMontoCaja['cajaId'] = caja.id
        jsonMontoCaja['caja'] = caja.nombre
        jsonMontoCaja['montoFinalCaja'] = monto
        jsonFinal.append(jsonMontoCaja)
    
    return JsonResponse(jsonFinal, safe=False)
