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

from app.validacionUser import validacionUsuario

perfiles_correctos = [1, 3]

@login_required
def nuevoLote(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
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
        oProveedor.documento = Datos['documento']
        oProveedor.save()
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")


@csrf_exempt
@login_required
def registrarLote(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
            Datos = json.loads(request.body)
            print(Datos)
        #Dato = json.loads(request.body)
        #Dato = request.POST
            nombreProveedor = Datos['oProveedor']
            if nombreProveedor.isdigit() == False :
                nombreProveedor = Proveedor.objects.get(nombre=nombreProveedor).documento

            oProveedor = Proveedor.objects.get(documento=nombreProveedor)
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
        if not validacionUsuario(request.user) in perfiles_correctos:
            return redirect('/error/')
        oRecibos = Recibo.objects.filter(estado=True)
        oAlmacens = Almacen.objects.filter(estado=True)
        context ={
            'recibos':oRecibos,
            'almacens': oAlmacens,
        }
        return render(request, 'lote/nuevo.html', context)

@login_required
def listarLote(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'lote/listar.html')
    else:
        oLotes = Lote.objects.filter(estado=True).order_by('-id')
        for oLote in oLotes:
            oProductoAlmacens = Producto_almacens.objects.filter(lote_id=oLote.id)
            for ope in oProductoAlmacens:
                oNuevo={}
                oNuevo['id']=oLote.id
                oNuevo['producto']=ope.producto.nombre
                oProductos.append(oNuevo)

        paginator = Paginator(oLotes,10)

        page = request.GET.get('page')
        try:
            lotePagina = paginator.page(page)
        except PageNotAnInteger:
            lotePagina = paginator.page(1)
        except EmptyPage:
            lotePagina = paginator.page(paginator.num_pages)

        index = lotePagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return render(request, 'lote/listar.html', {"oLotes": lotePagina,"oProductos":oProductos,"page_range": page_range})
        #return render(request, 'venta/prueba.html', {})

@login_required
def detalleLote(request, lote_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'GET':
        oLote = Lote.objects.get(id=lote_id)
        oProductoAlmacens = Producto_almacens.objects.filter(lote_id=oLote.id)
        oProductos = []
        for oProductoAlmacen in oProductoAlmacens:
            oProducto = {}
            oProducto["imagen"] = oProductoAlmacen.producto.imagen
            oProducto["nombre"] = oProductoAlmacen.producto.nombre
            oProducto["cantidad"] = oProductoAlmacen.cantidad
            oProducto["cantidadInicial"] = oProductoAlmacen.cantidadinicial
            oProducto["almacen"] = oProductoAlmacen.almacen.nombre
            oProductos.append(oProducto)
        return render(request, 'lote/detalle.html', {"oProveedor": oLote.proveedor,"oProductos":oProductos})
