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
            nombreProveedor = Datos['oProveedor']
            oProveedor = Proveedor.objects.get(nombre=nombreProveedor)
            nombreRecibo= Datos['oRecibo']
            oRecibo= Recibo.objects.get(nombre=nombreRecibo)

            oLote= Lote(proveedor_id=oProveedor.id, recibo_id= oRecibo.id)
            oLote.save()

            oProductoAlmacens= Datos['oProductoAlmacen']
            for oProductoAlmacen in oProductoAlmacens:
                print(oProductoAlmacen)
                cantidad= oProductoAlmacen[0]

                nombreAlmacen= oProductoAlmacen[1]
                oAlmacen= Almacen.objects.get(nombre=nombreAlmacen)

                nombreProducto=oProductoAlmacen[2]
                oProducto= Producto.objects.get(nombre= nombreProducto)

                oProducto_alma = Producto_almacens(cantidad=cantidad, cantidadinicial= cantidad, almacen_id=oAlmacen.id, lote_id= oLote.id, producto_id= oProducto.id)
                
               # oProducto_almacens=Producto_almacens()
               # oProducto_almacens.cantidad=oProductoAlmacen[0]
               # oProducto_almacens.cantidadinicial= oProductoAlmacen[0]
               # oProducto_almacens.almacen_id= oProductoAlmacen[1]
               # oProducto_almacens.lote_id= oLote
               # oProducto_almacens.producto_id= oProductoAlmacen[2]

                oProducto_alma.save()

            return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

        #datos_list = json.loads(datos[0])

        #return render(request, '/pedido/listar.html')
    else:

        return render(request, 'lote/nuevo.html', {})
