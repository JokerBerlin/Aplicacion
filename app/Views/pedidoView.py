# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.cierrecajaForm import *
from app.fomularios.pedidoForm import *
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from datetime import datetime,date

#funcion sum
from django.db.models import Sum

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################
@csrf_exempt
def registrarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #Dato = json.loads(request.body)
        #Dato = request.POST
        dnis = Datos['cliente']

        # if dnis.isdigit() == False :
        #     dni = Cliente.objects.get(nombre=dnis).numerodocumento

        oCliente = Cliente.objects.get(numerodocumento=dnis)
        fechaHoy=date.today()
        empleado = 1
        oPedido = Pedido(fecha=fechaHoy,estado=True,empleado_id=empleado,cliente_id=oCliente.id)
        oPedido.save()

        #Datos = request.POST.getlist('datos')
        Dato = Datos['productos']
        oPedidoProductos = Dato
        #oPedidoProductos = json.dumps(Datos)

        for oPedidoProducto in oPedidoProductos:
            oPedidoproductospresentacions = Pedidoproductospresentacions()
            print(oPedidoProducto[1])
            oPedidoproductospresentacions.valor = oPedidoProducto[2]
            oPedidoproductospresentacions.cantidad = oPedidoProducto[0]
            oPedidoproductospresentacions.pedido = oPedido
            oPedidoproductospresentacions.productopresentacions_id=oPedidoProducto[1]
            oPedidoproductospresentacions.save()
        return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")

        #datos_list = json.loads(datos[0])

        #return render(request, '/pedido/listar.html')
    else:

        return render(request, 'pedido/nuevo.html', {})
        #return render(request, 'venta/prueba.html', {})
        #
def ListarPedidos(request):
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = True).order_by('-id')
        for oPedido in oPedidos:
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oPedido.id)
            print(pedidoproductospresentacions)
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oPedido.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        paginator = Paginator(oPedidos,2)

        page = request.GET.get('page')
        try:
            pedidoPagina = paginator.page(page)
        except PageNotAnInteger:
            pedidoPagina = paginator.page(1)
        except EmptyPage:
            pedidoPagina = paginator.page(paginator.num_pages)

        index = pedidoPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return render(request, 'pedido/listar.html', {"oPedidos": pedidoPagina,"oProductos":oProductos,"page_range": page_range})
        #return render(request, 'venta/prueba.html', {})

def ResumenPedidos(request):
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = True)

        oProductos = []

        oPedidopropre = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in oPedidos]).values('productopresentacions_id').annotate(Sum('cantidad'))
        for o in oPedidopropre:
            id = o['productopresentacions_id']
            oProductopresentacions = Productopresentacions.objects.get(id=id)
            oProducto = {}
            oProducto["nombreProducto"] = oProductopresentacions.producto.nombre
            oProducto["nombrePresentacion"] = oProductopresentacions.presentacion.nombre
            oProducto["cantidad"] = o['cantidad__sum']
            oProductos.append(oProducto)

        paginator = Paginator(oProductos,3)

        page = request.GET.get('page')
        try:
            productoPagina = paginator.page(page)
        except PageNotAnInteger:
            productoPagina = paginator.page(1)
        except EmptyPage:
            productoPagina = paginator.page(paginator.num_pages)

        index = productoPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return render(request, 'pedido/resumen.html', {"oProductos": productoPagina,"page_range":page_range})

@csrf_exempt
def DetallePedidoMovil(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idPedido = Datos["idPedido"]
            oPedido = Pedido.objects.get(id = idPedido)
            jsonPedidos = {}
            jsonPedidos["productos"] = []
            oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
            for oPedidoproductospresentacion in oPedidoproductospresentacions:
                oProducto = {}
                oProducto["nombreProducto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                oProducto["nombrePresentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                oProducto["cantidad"] = oPedidoproductospresentacion.cantidad
                jsonPedidos["productos"].append(oProducto)
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

def DetallePedido(request,pedido_id):
    if request.method == 'GET':
        idPedido = int(pedido_id)
        oPedido = Pedido.objects.get(id = idPedido)
        oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
        oProductos = []
        for oPedidoproductospresentacion in oPedidoproductospresentacions:
            oProducto = {}
            oProducto["nombreProducto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
            oProducto["nombrePresentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
            oProducto["cantidad"] = oPedidoproductospresentacion.cantidad
            oProductos.append(oProducto)
            print(oProductos)
        return render(request, 'pedido/detalle.html', {"oCliente": oPedido.cliente, "oProductos": oProductos})
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        return render(request, 'pedido/listar.html',{"oPedidos": oPedidos})

@csrf_exempt
def InstarPedido(request):
    if request.method=='POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idEmpleado = Datos["idEmpleado"]
            oEmpleado = Empleado.objects.get(id= idEmpleado)
            idCliente = Datos["idCliente"]
            oCliente = Cliente.objects.get(id= idCliente)

            oPedido = Pedido()
            oPedido.empleado = oEmpleado
            oPedido.cliente = oCliente
            oPedido.save()
            oPedidoProductos = Datos["oPedidoProductos"]
            for oPedidoProducto in oPedidoProductos:
                oPedidoproductospresentacions = Pedidoproductospresentacions()
                oPedidoproductospresentacions.valor = oPedidoProducto["valor"]
                oPedidoproductospresentacions.cantidad = oPedidoProducto["cantidad"]
                oPedidoproductospresentacions.pedido = oPedido
                oProductopresentacions = Productopresentacions.objects.get(id = oPedidoProducto["idPresentacion"])
                oPedidoproductospresentacions.productopresentacions = oProductopresentacions
                oPedidoproductospresentacions.save()
            return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")


@csrf_exempt
def ListarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            fecha = Datos["fecha"]
            idEmpleado = Datos["idEmpleado"]
            jsonPedidos = {}
            jsonPedidos["pedidos"] = []
            TotalPedidos = 0

            #oPedidos = Pedido.objects.filter(estado = True,fecha = fecha, empleado = idEmpleado)
            oPedidos = Pedido.objects.filter(estado = True, empleado = idEmpleado)
            for oPedido in oPedidos:
                jsonPedido = {}
                jsonPedido["idPedido"] = oPedido.id
                jsonPedido["fecha"] = str(oPedido.fecha)
                jsonPedido["cliente"] = oPedido.cliente.nombre
                jsonPedido["productos"] = []
                oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
                TotalPedido = 0
                for oPedidoproductospresentacion in oPedidoproductospresentacions:
                    jsonPedidoProductoPresentacion = {}
                    jsonPedidoProductoPresentacion["cantidad"] = oPedidoproductospresentacion.cantidad
                    jsonPedidoProductoPresentacion["valor"] = oPedidoproductospresentacion.valor
                    jsonPedidoProductoPresentacion["presentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                    jsonPedidoProductoPresentacion["producto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                    TotalPedido = TotalPedido + (jsonPedidoProductoPresentacion["cantidad"]*jsonPedidoProductoPresentacion["valor"])
                    jsonPedido["productos"].append(jsonPedidoProductoPresentacion)


                TotalPedidos = TotalPedidos +TotalPedido
                jsonPedido["TotalPedido"] = TotalPedido

                jsonPedidos["pedidos"].append(jsonPedido)
            jsonPedidos["TotalPedidos"] = TotalPedidos
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

def editarPedido(request,pedido_id):
        oPedidoproductospresentacions= Pedidoproductospresentacions.objects.get(pedido=pedido_id)
        oProductopresentacions= Productopresentacions.objects.get(producto=oPedidoproductospresentacions.productopresentacions.producto.id)
        if request.method == 'POST':
                form = PedidoproductospresentacionsForm(instance=oPedidoproductospresentacions)
                form2=Productopresentacions()
                if form.is_valid():
                    edit_ped=form.save(commit=False)
                    edit_pre=form2.save(commit=False)
                    form.save_m2m()
                    form2.save_m2m()
                    edit_ped.status=True
                    edit_pre.status=True
                    edit_ped.save()
                    edit_pre.save()

                return redirect('/Pedido/listar/')


        else:
         form = PedidoproductospresentacionsForm(instance=oPedidoproductospresentacions)
         form2= ProductopresentacionsForm(instance=oProductopresentacions)
        return render(request, 'Pedido/editar.html', {'form': form, 'form2': form2})


def eliminar_identificador_pedido(request):
    pk = request.POST.get('identificador_id')
    identificador = Pedido.objects.get(pk=pk)
    identificador.estado = 0
    identificador.save()
    response = {}
    return JsonResponse(response)
