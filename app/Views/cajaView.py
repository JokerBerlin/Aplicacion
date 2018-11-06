
from django.shortcuts import render, render_to_response,redirect
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
