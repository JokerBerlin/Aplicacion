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

from datetime import datetime as dt
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
        cantidadProducto = prodAlmacens.latest('pk').cantidad
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
        jsonProductosSalidas['cantidadActualProducto'] = cantidadProducto
        # print(jsonProductosSalidas)

        jsonfinal.append(jsonProductosSalidas)

    return HttpResponse(json.dumps(jsonfinal), content_type="application/json")


# Servicio para la cantidad de productos en almacen
# Sujeto a la datatableCantidadProducto en la vista reporte almacen
def cantidadProductoAlmacen(request):
    productos = Producto.objects.all()
    jsonfinal = []
    for producto in productos:
        jsonProductoCantidad = {}
        
        prodAlmacen = Producto_almacens.objects.filter(producto=producto).latest('pk')
        
        jsonProductoCantidad['producto'] = producto.nombre
        jsonProductoCantidad['cantidadProducto'] = prodAlmacen.cantidad
        
        jsonfinal.append(jsonProductoCantidad)
        
    return HttpResponse(json.dumps(jsonfinal), content_type="application/json")


def tiempoPedidoAlmacen(request):
    pedidos = Pedido.objects.all()
    jsonfinal = []
    hoy = dt.now()

    for pedido in pedidos:
        jsonTiempoPedido = {}
        
        if pedido.estado == 1 or pedido.estado == 2:
            delta = hoy - pedido.fecha
            
            jsonTiempoPedido['pedidoId'] = pedido.pk
            jsonTiempoPedido['cliente'] = pedido.cliente.nombre
            jsonTiempoPedido['fechaPedido'] = str(pedido.fecha)
            jsonTiempoPedido['delta'] = str(delta.days)

            jsonfinal.append(jsonTiempoPedido)
    
    return HttpResponse(json.dumps(jsonfinal), content_type="application/json")

        
