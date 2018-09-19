from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *

from ferreteria.urls import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *

@csrf_exempt
def registrarLote(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
        #Dato = json.loads(request.body)
        #Dato = request.POST
        nombreProveedor = Datos['proveedor']
        nombreRecibo= Datos['recibo']

        # if dnis.isdigit() == False :
        #     dni = Cliente.objects.get(nombre=dnis).numerodocumento
        oRecibo= Recibo.objects.get()
        oRecibo.save()
        oProveedor = Proveedor.objects.get(nombre=nombreProveedor)
        oProveedor.save()


        Dato = Datos['productos']
        oPedidoProductos = Dato


        for oPedidoProducto in oPedidoProductos:
            oPedidoproductospresentacions = Pedidoproductospresentacions()
            print(oPedidoProducto[1])
            oPedidoproductospresentacions.valor = oPedidoProducto[2]
            oPedidoproductospresentacions.cantidad = oPedidoProducto[0]
            oPedidoproductospresentacions.pedido = oPedido
            oPedidoproductospresentacions.productopresentacions_id=oPedidoProducto[1]
            oPedidoproductospresentacions.save()
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

        #datos_list = json.loads(datos[0])

        #return render(request, '/pedido/listar.html')
    else:

        return render(request, 'lote/nuevo.html', {})
