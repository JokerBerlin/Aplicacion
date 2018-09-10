# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from datetime import datetime,date

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def nuevoVenta(request):
    if request.method == 'GET':
        Datos = request.POST
        return render(request, 'venta/nuevo.html', {})
        nombre = Datos()
def ListarVentas(request):
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'venta/listar.html')
    else:
        oVenta = Venta.objects.filter(estado = True).order_by('-id')
        paginator = Paginator(oVenta,2)

        page = request.GET.get('page')
        try:
            ventaPagina = paginator.page(page)
        except PageNotAnInteger:
            ventaPagina = paginator.page(1)
        except EmptyPage:
            ventaPagina = paginator.page(paginator.num_pages)

        index = ventaPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range": page_range})

def filtrarVentas(request):
    if request.method == 'POST':
        Datos = request.POST
        producto = Datos["producto_buscado"]
        print(producto)
        dni = Datos["cliente_buscado"]
        fecha_inicio = Datos["desde"]
        fecha_fin = Datos["hasta"]
        oProductos=[]
        oVentas=[]
        tags=[]

        if producto != '':
            objetotag={}
            objetotag['producto']=producto
            tags.append(objetotag)
            producto = Producto.objects.get(nombre=producto).id
            presentacion = Productopresentacions.objects.filter(producto=producto)
            pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
            pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion])
            venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id")
            productonombre = Producto.objects.get(id=producto).nombre
            for v in venta:
                oNuevo={}
                oNuevo['id']=v.id
                oNuevo['producto']=productonombre
                oProductos.append(oNuevo)
            oVentas = venta
        if dni != '':
            objetotag={}
            objetotag['dni']=dni
            tags.append(objetotag)
            if dni.isdigit() == False :
                dni = Cliente.objects.get(nombre=dni).numerodocumento

            if producto != '':
                cliente = Cliente.objects.get(numerodocumento=dni)
                venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

            else:
                oProductos=[]
                cliente = Cliente.objects.get(numerodocumento=dni)
                venta = Venta.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
                for oVenta in venta:
                    pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                    pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                    for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                        oNuevo={}
                        oNuevo['id']=oVenta.id
                        oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                        oProductos.append(oNuevo)
            oVentas = venta
        if fecha_inicio!='' and fecha_fin!='':
            objetotag={}
            objetotag['fecha_inicio']=fecha_inicio
            objetotag['fecha_fin']=fecha_fin
            tags.append(objetotag);
            fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
            fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
            if producto !='' or dni!='':
                venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
            else:
                oProductos = []
                venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')
                for oVenta in venta:
                    pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                    pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                    for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                        oNuevo={}
                        oNuevo['id']=oVenta.id
                        oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                        oProductos.append(oNuevo)
            oVentas = venta
        elif fecha_inicio!='':
            objetotag={}
            objetotag['fecha_inicio']=fecha_inicio
            tags.append(objetotag);
            fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
            fecha2=date.today()
            if producto !='' or dni!='':
                venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
            else:
                oProductos=[]
                venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
                for oVenta in venta:
                    pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                    pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                    for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                        oNuevo={}
                        oNuevo['id']=oVenta.id
                        oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                        oProductos.append(oNuevo)
            oVentas = venta
        elif fecha_fin!='':
            objetotag={}
            objetotag['fecha_fin']=fecha_fin
            tags.append(objetotag);
            fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
            if producto !='' or dni!='':
                venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
            else:
                oProductos=[]
                venta = Venta.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')[:50]
                for oVenta in venta:
                    pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                    pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                    for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                        oNuevo={}
                        oNuevo['id']=oVenta.id
                        oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                        oProductos.append(oNuevo)
                oVentas = venta

        paginator = Paginator(oVentas,2)

        page = request.GET.get('page')
        try:
            ventaPagina = paginator.page(page)
        except PageNotAnInteger:
            ventaPagina = paginator.page(1)
        except EmptyPage:
            ventaPagina = paginator.page(paginator.num_pages)

        index = ventaPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range":page_range,"tags":tags,})


def Fentas(request, producto_buscado='',cliente='',inicio='',fin=''):
    oProductos=[]
    oVentas=[]
    producto = producto_buscado
    dni = cliente
    fecha_inicio = inicio
    fecha_fin = fin

    tags=[]

    if producto != '':
        objetotag={}
        objetotag['producto']=producto
        tags.append(objetotag)
        producto = Producto.objects.get(nombre=producto).id
        presentacion = Productopresentacions.objects.filter(producto=producto)
        pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
        pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion])
        venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id")
        productonombre = Producto.objects.get(id=producto).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)
        oVentas = venta
    if dni != '':
        objetotag={}
        objetotag['dni']=dni
        tags.append(objetotag)
        if dni.isdigit() == False :
            dni = Cliente.objects.get(nombre=dni).numerodocumento

        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    if fecha_inicio!='' and fecha_fin!='':
        objetotag={}
        objetotag['fecha_inicio']=fecha_inicio
        objetotag['fecha_fin']=fecha_fin
        tags.append(objetotag);
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' or dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos = []
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_inicio!='':
        objetotag={}
        objetotag['fecha_inicio']=fecha_inicio
        tags.append(objetotag);
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=date.today()
        if producto !='' or dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_fin!='':
        objetotag={}
        objetotag['fecha_fin']=fecha_fin
        tags.append(objetotag);
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' or dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            venta = Venta.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
            oVentas = venta

    paginator = Paginator(oVentas,2)

    page = request.GET.get('page')
    try:
        ventaPagina = paginator.page(page)
    except PageNotAnInteger:
        ventaPagina = paginator.page(1)
    except EmptyPage:
        ventaPagina = paginator.page(paginator.num_pages)

    index = ventaPagina.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range":page_range,"tags":tags,})

"""
@csrf_exempt
def ListarVenta(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            fecha = Datos["fecha"]
            idEmpleado = Datos["idEmpleado"]
            jsonPedidos = {}
            jsonPedidos["pedidos"] = []
            ToProductosalPedidos = 0

            #oPedidos = Pedido.objects.filter(estado = True,fecha = fecha, empleado = idEmpleado)
            oPedidos = Pedido.objects.filter(estado = True, empleado = idEmpleado)
            for oPedido in oPedidos:
                jsonPedido = {}
                jsonPedido["idPedido"] = oPedido.id
                jsonPedido["fecha"] = str(oPedido.fecha)
                jsonPedido["cliente"] = oPedido.cliente.nombre
                jsonPedido["productos"] = []
                oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
                ToProductosalPedido = 0
                for oPedidoproductospresentacion in oPedidoproductospresentacions:
                    jsonPedidoProductoPresentacion = {}
                    jsonPedidoProductoPresentacion["cantidad"] = oPedidoproductospresentacion.cantidad
                    jsonPedidoProductoPresentacion["valor"] = oPedidoproductospresentacion.valor
                    jsonPedidoProductoPresentacion["presentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                    jsonPedidoProductoPresentacion["producto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                    ToProductosalPedido = ToProductosalPedido + (jsonPedidoProductoPresentacion["cantidad"]*jsonPedidoProductoPresentacion["valor"])
                    jsonPedido["productos"].append(jsonPedidoProductoPresentacion)


                ToProductosalPedidos = ToProductosalPedidos +ToProductosalPedido
                jsonPedido["ToProductosalPedido"] = ToProductosalPedido

                jsonPedidos["pedidos"].append(jsonPedido)
            jsonPedidos["ToProductosalPedidos"] = ToProductosalPedidos
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

"""
