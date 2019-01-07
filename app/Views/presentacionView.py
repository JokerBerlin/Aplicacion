# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *

from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *
from app.validacionUser import validacionUsuario

perfiles_correctos = [1, 3]

def registrarPresentacionProducto(request):
    if request.method == 'POST':
        Datos = request.POST
        idProducto = str(Datos['idProducto'])
        oProducto = Producto.objects.get(id=idProducto)
        oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacion']))
        oProducto.presentacions.add(oPresentacion)
        oProductopresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
        oProductopresentacions.valor = int(Datos['cantPresentacion'])
        oProductopresentacions.unidadprincipal = False
        oProductopresentacions.save()
        oPrecios = Precio.objects.filter(estado=1)
        for oPrecio in oPrecios:
            oProductoPresentacionsprecios = Productopresentacionsprecios()
            oProductoPresentacionsprecios.precio = oPrecio
            oProductoPresentacionsprecios.producto_presentacions = oProductopresentacions
            idPrecio = str(oPrecio.id)
            #print idPrecio
            oProductoPresentacionsprecios.valor = Datos[idPrecio]
            oProductoPresentacionsprecios.save()
        return HttpResponseRedirect('/Presentacion/Listar/'+Datos['idProducto']+'/')

def eliminarPresentacionProducto(request, presentacion_id,producto_id):
    #oPresentacion = Presentacion.objects.get(id=presentacion_id)
    #oProducto = Producto.objects.get(id=producto_id)
    #oProducto.presentacions.remove(oPresentacion)
    try:
        oProductopresentacion = Productopresentacions.objects.get(id=presentacion_id)
        # oProductoPresentacionPrecios = Productopresentacionsprecios.objects.filter(productopresentacions_id=oProductopresentacion.id)
        # for oProductoPresentacionPrecio in oProductoPresentacionPrecios:
        #     oPresentacionPrecios = Productopresentacionsprecios.objects.get(id=oProductoPresentacionPrecio.id)
        #     oPresentacionPrecios.delete()
        oProductopresentacion.delete()

    except Exception as e:
        print('No se puede eliminar el producto')
        return HttpResponseRedirect('/Producto/editar/'+producto_id+'/')

    return HttpResponseRedirect('/Producto/editar/'+producto_id+'/')

@login_required
def presentacion_detalle(request,producto_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProducto = Producto.objects.get(id=producto_id)
    oPrecios = Precio.objects.filter(estado=True)
    oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'presentacion/listar.html', {'producto':oProducto,'precios':oPrecios,'presentaciones':oPresentaciones})

def getPresentaciones(request):
    if request.method == 'GET':
        try:
            jsonfinal = {}
            jsonfinal["presentaciones"] = []
            oPresentacion = Presentacion.objects.filter(estado = True).order_by('nombre')
            for presentacion in oPresentacion:
                presentacionjson = {}
                presentacionjson["id"] = presentacion.id
                presentacionjson["nombre"] = presentacion.nombre
                jsonfinal['presentaciones'].append(presentacionjson)
            return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

@csrf_exempt
def editarPresentacion(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)

        cantidad = round(1/float(Datos['valorPrecio']),8)
        print(cantidad)
        oProductoPresentacion = Productopresentacions.objects.get(id=Datos['productoPresentacionId'])
        oProductoPresentacion.valor = cantidad
        oProductoPresentacion.save()

        oPrecios = Precio.objects.filter(estado=True)
        cont = 1
        for precio in oPrecios:
            idPrecio = "precio"+str(cont)+"Id"
            oProductoPresentacionPrecio = Productopresentacionsprecios.objects.get(id=Datos[idPrecio])
            valorPrecio = "precio"+str(cont)+"";
            oProductoPresentacionPrecio.valor = float(Datos[valorPrecio])
            oProductoPresentacionPrecio.save()
            cont = cont + 1

        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
