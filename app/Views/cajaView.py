
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
            return redirect('caja/apertura.html')

    else:
        form = AperturaCajaForm()
        oCajas = Caja.objects.filter(estado=1)
        detalleTipoOperaciones = Detalletipooperacion.objects.all() 

        context = {
            'form': form,
            'cajas': oCajas,
            'detalleOperaciones': detalleTipoOperaciones
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
