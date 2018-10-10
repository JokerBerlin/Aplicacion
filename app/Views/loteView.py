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

def nuevoLote(request):
    oRecibos = Recibo.objects.filter(estado=True)
    oAlmacens = Almacen.objects.filter(estado=True)
    context ={
        'recibos':oRecibos,
        'almacens': oAlmacens,
    }
    return render(request, 'lote/nuevo.html', context)

@csrf_exempt
def registrarProveedor(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        oProveedor = Proveedor()
        oProveedor.nombre = Datos['nombre']
        oProveedor.direccion = Datos['direccion']
        oProveedor.numerodocumento = Datos['documento']
        oProveedor.save()
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")


@csrf_exempt
def registrarLote(request):
    if request.method == 'POST':
            Datos = json.loads(request.body)
            print(Datos)
        #Dato = json.loads(request.body)
        #Dato = request.POST
            nombreProveedor = Datos['oProveedor']
            oProveedor = Proveedor.objects.get(nombre=nombreProveedor)
            print(oProveedor.nombre)
            nombreRecibo= Datos['oRecibo']
            oRecibo= Recibo.objects.get(nombre=nombreRecibo)
            print(oRecibo.nombre)
            oLote= Lote(proveedor_id=oProveedor.id, recibo_id= oRecibo.id)
            oLote.save()

            oProductoAlmacens= Datos['oProductoAlmacen']
            for oProductoAlmacen in oProductoAlmacens:
                print(oProductoAlmacen)
                cantidad= float(oProductoAlmacen[0])

                nombreAlmacen= oProductoAlmacen[1]
                oAlmacen= Almacen.objects.get(nombre=nombreAlmacen)
                nombreProducto=oProductoAlmacen[2]
                oProducto= Producto.objects.get(nombre= nombreProducto)
                oAlmacenese = Producto_almacens.objects.filter(producto_id=oProducto.id).exists()
                print(oAlmacenese)
                if oAlmacenese == True:
                    oUltimoP=Producto_almacens.objects.filter(producto_id=oProducto).latest('id')
                    cantidadIni = float(oUltimoP.cantidad)

                    cantidadNueva = cantidadIni + cantidad
                    oProducto_alma = Producto_almacens(cantidad=cantidadNueva, cantidadinicial= cantidadIni, almacen_id=oAlmacen.id, lote_id= oLote.id, producto_id= oProducto.id)
                    oProducto_alma.save()
                else:
                    #oUltimoP=Producto_almacens.objects.filter(producto_id=oProducto).latest('id')
                    oProducto_alma = Producto_almacens(cantidad=cantidad, cantidadinicial= 0, almacen_id=oAlmacen.id, lote_id= oLote.id, producto_id= oProducto.id)
                    oProducto_alma.save()


            return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

        #datos_list = json.loads(datos[0])

        #return render(request, '/pedido/listar.html')
    else:
        oRecibos = Recibo.objects.filter(estado=True)
        oAlmacens = Almacen.objects.filter(estado=True)
        context ={
            'recibos':oRecibos,
            'almacens': oAlmacens,
        }
        return render(request, 'lote/nuevo.html', context)
