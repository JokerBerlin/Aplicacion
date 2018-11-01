# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def BuscarAlmacen(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        print(Datos)
        usuario=True
        if usuario==True:
            nombreAlmacen = Datos["nombreAlmacen"]
            jsonfinal = {}
            jsonfinal["almacenes"] = []
            try:
                oAlmacenes = Almacen.objects.filter(nombre__icontains=nombreAlmacen,estado = 1)
                for oAlmacen in oAlmacenes:
                    
                    jsonAlmacen = {}
                    jsonAlmacen["id"] = oAlmacen.id
                    jsonAlmacen["nombre"] = oAlmacen.nombre

                    jsonfinal["almacenes"].append(jsonAlmacen)
                    
               	return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
            except Exception as e:
              return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

def reporteAlmacen(request):
    context = {}
    return render(request, 'reporte/almacen.html', context)


# Servicio para el ranking de productos mas vendidos
# Sujeto a un datatable dentro de la vista de reporte almacen
def salidaProductoAlmacen(request):
    productos = Producto.objects.all()
    jsonfinal = []
    for producto in productos:
        prodAlmacens = Producto_almacens.objects.filter(producto=producto)
        jsonProductosSalidas = {}
        cantidadProductosSalida = 0
        for prodAlmacen in prodAlmacens:
            cantSalida = prodAlmacen.cantidad - prodAlmacen.cantidadinicial
            if cantSalida < 0:
                cantidadProductosSalida += 0
            else:
                cantidadProductosSalida += cantSalida
        
        jsonProductosSalidas['producto'] = producto.nombre
        jsonProductosSalidas['cantidadSalidas'] = cantidadProductosSalida
        # print(jsonProductosSalidas)

        jsonfinal.append(jsonProductosSalidas)
        print('fin for %s' % jsonfinal)
    print('final %s' % jsonfinal)
    
    return HttpResponse(json.dumps(jsonfinal), content_type="application/json")


# Servicio para la cantidad de productos en almacen
# Sujeto a la datatableCantidadProducto en la vista reporte almacen
def cantidadProductoAlmacen(request):
    productos = Producto.objects.all()
    jsonfinal = []
    for producto in productos:
        jsonProductoCantidad = {}
        try:
            prodAlmacen = Producto_almacens.objects.filter(producto=producto).latest('pk')
            jsonProductoCantidad['producto'] = producto.nombre
            jsonProductoCantidad['cantidadProducto'] = prodAlmacen.cantidad
        except:
            jsonProductoCantidad['producto'] = producto.nombre
            jsonProductoCantidad['cantidadProducto'] = 0.0
            
        jsonfinal.append(jsonProductoCantidad)
            
    return HttpResponse(json.dumps(jsonfinal), content_type="applicacion/json")