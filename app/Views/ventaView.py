# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from datetime import datetime,date

from django.forms.models import model_to_dict
##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core import serializers
from django.db.models import Sum

###reporteVentas
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from django.db.models import Q

import io
from django.http import FileResponse

from app.validacionUser import validacionUsuario

perfiles_correctos = [1, 4]

@login_required
def ListarVentas(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
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
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=3)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range": page_range})


@csrf_exempt
def filtrarVentas(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #Datos = request.POST
        producto = Datos["producto"]
        print(producto)
        dni = Datos["cliente"]
        fecha_inicio = Datos["desde"]
        fecha_fin = Datos["hasta"]
        oProductos=[]
        oVentas=[]
        tags=[]
        oDatosVenta = {}
        oDatosVenta["oProductos"]=[]
        oDatosVenta["oVenta"]=[]
        if producto != '':
            objetotag={}
            objetotag['producto']=producto
            tags.append(objetotag)
            producto = Producto.objects.get(nombre=producto).id
            presentacion = Productopresentacions.objects.filter(producto=producto)
            pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
            pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion])
            #venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id")
            venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id").values('id','fecha','monto','nrecibo','pedido','cliente')
            for instance in venta:
                instance['fecha'] = instance['fecha'].strftime('%d de %B del %Y %H:%M:%S')
                instance['cliente']=Cliente.objects.get(id=instance['cliente']).nombre

            #ase = list(dict((m.id, m.fecha) for m in venta))
            #print('------*-----------')
            #print(ase)
            #print('------*-----------')
            productonombre = Producto.objects.get(id=producto).nombre
            print('------')
            print(list(venta))
            print('------')
            for v in venta:
                oNuevo={}
                oNuevo['id']=v['id']
                oNuevo['producto']=productonombre
                oDatosVenta["oProductos"].append(oNuevo)
                oProductos.append(oNuevo)
            oVentas = venta
            print(venta)
            #print(model_to_dict(venta))
            #ventass = serializers.serialize('json',venta)
            # ventado = list(ventass)
            # for i in ventado:
            #     print(i)
            oDatosVenta["oVenta"] = list(venta)

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
                        oDatosVenta["oProductos"].append(oNuevo)
                        oProductos.append(oNuevo)
            oVentas = venta
            ventass = serializers.serialize('json',venta)
            oDatosVenta["oVenta"] = ventass
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
        #ventas = {}
        #print(oProductos)
        #ventas["oVentas"] = oVentas
        #ventas["oProductos"] = oProductos
        #ventas["page_range"] = []
        #ventas["tags"] = []
        #ventas["oVentas"].append(oVentas)
        #ventas["oProductos"].append(oProductos)
        #ventas["page_range"].append(page_range)
        #ventas["tags"].append(tags)
        print(oDatosVenta["oProductos"])
        #print(ventass)
        return HttpResponse(json.dumps(oDatosVenta), content_type='application/json')
        #return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range":page_range,"tags":tags,})

@csrf_exempt
def guardar_cookies(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        response = HttpResponse()
        if "nombreProductos" in Datos:
            producto=Datos["nombreProductos"]
            response.set_cookie("producto_busca",producto)
        if "nombreClientes" in Datos:
            cliente=Datos["nombreClientes"]
            response.set_cookie("cliente_busca",cliente)
        if "fechaInicio" in Datos:
            fecha_inicio=Datos["fechaInicio"]
            response.set_cookie("fecha_inicio",fecha_inicio)
        if "fechaFin" in Datos:
            print(Datos["fechaFin"])
            fecha_fin=Datos["fechaFin"]
            response.set_cookie("fecha_fin",fecha_fin)
        return response


@csrf_exempt
def eliminar_cookies(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        response = HttpResponse()
        if "nombreProductos" in Datos:
            response.delete_cookie("producto_busca")
        if "nombreClientes" in Datos:
            response.delete_cookie("cliente_busca")
        if "fechaInicio" in Datos:
            response.delete_cookie("fecha_inicio")
        if "fechaFin" in Datos:
            response.delete_cookie("fecha_fin")
        return response

@login_required
def FiltrarVenta(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProductos=[]
    oVentas=[]
    if "producto_busca" in request.COOKIES:
        producto = request.COOKIES["producto_busca"]
        print(request.COOKIES["producto_busca"])
    else:
        producto = ''

    if "cliente_busca" in request.COOKIES:
        dni = request.COOKIES["cliente_busca"]
        if dni.isdigit() == False :
            dni = Cliente.objects.get(nombre=dni).numerodocumento
        print(request.COOKIES["cliente_busca"])
    else:
        dni = ''

    if "fecha_inicio" in request.COOKIES:
        fecha_inicio = request.COOKIES["fecha_inicio"]
        print(request.COOKIES["fecha_inicio"])
    else:
        fecha_inicio = ''
    if "fecha_fin" in request.COOKIES:
        fecha_fin = request.COOKIES["fecha_fin"]
        print(request.COOKIES["fecha_fin"])
    else:
        fecha_fin = ''

    tags=[]
    #

    if producto != '':
        objetotag={}
        objetotag['producto']=producto
        tags.append(objetotag)
        producto = Producto.objects.get(nombre=producto).id
        presentacion = Productopresentacions.objects.filter(producto=producto)
        pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
        pedido = Pedido.objects.filter(estado=3,id__in=[s.pedido_id for s in pedidoproductopresentacion])
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

        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=3,id=oVenta.pedido_id)
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
                pedido = Pedido.objects.filter(estado=3,id=oVenta.pedido_id)
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
                pedido = Pedido.objects.filter(estado=3,id=oVenta.pedido_id)
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
                pedido = Pedido.objects.filter(estado=3,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
            oVentas = venta

    if producto=='' and dni=='' and fecha_inicio=='' and fecha_fin=='':
        oVenta = Venta.objects.filter(estado = True).order_by('-id')
        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=3)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
        oVentas = oVenta
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


def eliminar_identificador_venta(request):
    pk = request.POST.get('identificador_id')
    print(pk)
    identificador = Venta.objects.get(pk=pk)
    oPedido = identificador.pedido
    oPedido.estado = 0
    oPedido.save()
    print(oPedido)
    identificador.estado = 0
    identificador.save()

    oPedProdPres = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
    for oPedProdPre in oPedProdPres:
        cantidad = oPedProdPre.cantidad
        oProdPresentacions = oPedProdPre.productopresentacions
        oProducto = oProdPresentacions.producto
        # almacen
        oAlmacen = 1
        fraccion = oProdPresentacions.valor
        prodAlmacen = Producto_almacens.objects.filter(producto=oProducto, almacen_id=oAlmacen).latest('pk')
        cantidadAntesAnulacion = prodAlmacen.cantidad
        cantidadDespuesAnulacion = float(cantidadAntesAnulacion) + float(cantidad) * float(fraccion)
        prodAlmacenNuevo = Producto_almacens(
            cantidad=cantidadDespuesAnulacion,
            cantidadinicial=cantidadAntesAnulacion,
            almacen=prodAlmacen.almacen,
            lote=prodAlmacen.lote,
            producto=prodAlmacen.producto
        )
        prodAlmacenNuevo.save()

    response = {}
    return JsonResponse(response)

@login_required
def ventaNuevo(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oPresentaciones = Presentacion.objects.filter(estado=True)
    oPrecios = Precio.objects.filter(estado=True)
    oPedidos = Pedido.objects.filter(estado=2)
    oRecibos = Recibo.objects.filter(estado=True)
    oCajas = Caja.objects.filter(estado=True)

    context = {
        'presentaciones': oPresentaciones,
        'precios': oPrecios,
        'pedidos': oPedidos,
        'recibos': oRecibos,
        'cajas': oCajas
    }

    return render(request, 'venta/nuevo.html', context)

@csrf_exempt
#Caso en el que se crea una venta sin pasar antes por pedidos y almacen
@login_required
def insertarVenta(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        datos = json.loads(request.body)
        print(datos)
        dni_cliente = datos['cliente']
        nroRecibo = datos['nrecibo']
        tipoRecibo = datos['tipoRecibo']
        cajaId = datos['cajaId']

        #Se genera el pedido con un estado 3
        #Se hace el descuento de producto en producto_almacen
        oCliente = Cliente.objects.get(numerodocumento=dni_cliente)
        usuario = request.user
        print(usuario)
        usuario = request.user
        empleado = Empleado.objects.get(usuario=usuario)
        oPedido = Pedido(estado=3, empleado=empleado, cliente=oCliente)
        oPedido.save()
        oVenta = Venta(pedido=oPedido, cliente=oCliente, nrecibo=nroRecibo)
        monto_venta = 0.00

        productos = datos['productos']
        print(productos)
        for producto in productos:
            monto_venta += round(float(producto[0]) * float(producto[4]), 2)
            oProducto = Producto.objects.get(codigo=producto[1])
            oPresentacion = Presentacion.objects.get(nombre=producto[3])
            oProductoPresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
            oPedidoproductospresentacions = Pedidoproductospresentacions(
                valor = producto[4],
                cantidad = producto[0],
                pedido = oPedido,
                productopresentacions = oProductoPresentacions
            )
            oPedidoproductospresentacions.save()

            oUltimoP = Producto_almacens.objects.filter(producto = oProducto).latest('id')
            cantidad_dscto_almacen = float(producto[0]) * oProductoPresentacions.valor
            cantidad_sobrante_almacen = oUltimoP.cantidad - cantidad_dscto_almacen

            nuevoCantidadProductoAlmacen = Producto_almacens(
                cantidad=cantidad_sobrante_almacen,
                cantidadinicial=oUltimoP.cantidad,
                almacen_id=oUltimoP.almacen_id,
                lote_id=oUltimoP.lote_id,
                producto_id=oUltimoP.producto_id
            )
            nuevoCantidadProductoAlmacen.save()

        oVenta.monto = monto_venta
        oVenta.save()

        oCobro = Cobro(
            monto=monto_venta,
            estado=True,
            recibo_id=tipoRecibo,
            venta=oVenta
        )
        oCobro.save()

        oOperacion = Operacion(
            monto=oCobro.monto,
            estado=True,
            caja_id=cajaId,
            cobro=oCobro,
            detalletipooperacion_id=1
        )
        oOperacion.save()

        oAperturaCaja = Aperturacaja.objects.filter(caja_id=cajaId).latest('pk')
        monto = oAperturaCaja.monto + oOperacion.monto
        oAperturaCajaNuevo = Aperturacaja(
            monto=monto,
            activo=1,
            estado=1,
            caja_id=cajaId
        )
        oAperturaCajaNuevo.save()
        return HttpResponse(json.dumps({'exito': 1, "idPedido": oPedido.id}), content_type="application/json")

    else:
        return render(request, 'venta/nuevo')


@login_required
def anularVenta(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'venta/anular.html')
    else:
        oVenta = Venta.objects.filter(estado = True).order_by('-id')
        paginator = Paginator(oVenta, 5)

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
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=3)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        context = {
            "oVenta": ventaPagina,
            "oProductos":oProductos,
            "page_range": page_range
        }

        return render(request, 'venta/anular.html', context)

    context = {}
    return render(request, 'venta/anular.html', context)


def eliminar_identificador_venta(request):
    Datos = request.POST
    pk = Datos['identificador_id']
    identificador = Venta.objects.get(pk=pk)
    anulacionVenta = Anulacionventa(
        descripcion=Datos['descripcion'],
        venta=identificador,
        usuario=request.user
    )

    oPedido = identificador.pedido
    oPedido.estado = 0
    oPedido.save()
    identificador.estado = 0
    identificador.save()
    oCobro = Cobro.objects.get(venta=identificador)
    oCobro.estado=False
    oCobro.save()

    oPedProdPres = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
    for oPedProdPre in oPedProdPres:
        cantidad = oPedProdPre.cantidad
        oProdPresentacions = oPedProdPre.productopresentacions
        oProducto = oProdPresentacions.producto
        # almacen
        oAlmacen = 1
        fraccion = oProdPresentacions.valor
        prodAlmacen = Producto_almacens.objects.filter(producto=oProducto, almacen_id=oAlmacen).latest('pk')
        cantidadAntesAnulacion = prodAlmacen.cantidad
        cantidadDespuesAnulacion = float(cantidadAntesAnulacion) + float(cantidad) * float(fraccion)

        loteReversion = Lote(proveedor_id=1, recibo_id=1)
        loteReversion.save()

        prodAlmacenNuevo = Producto_almacens(
            cantidad=cantidadDespuesAnulacion,
            cantidadinicial=cantidadAntesAnulacion,
            almacen=prodAlmacen.almacen,
            lote=loteReversion,
            producto=prodAlmacen.producto
        )
        prodAlmacenNuevo.save()

    response = {}
    return JsonResponse(response)

@login_required
def DetalleVenta(request,venta_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'GET':
        oVenta = Venta.objects.get(id=venta_id)
        oPedido = Pedido.objects.get(id = oVenta.pedido_id)
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

@login_required
def reporteVentas(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oEmpleados = Empleado.objects.filter(Q(perfil=1) | Q(perfil=4))
    context = {
        "empleados": oEmpleados
        }
    return render(request, 'reporte/ventas.html', context)

def imprimir(request,venta_id):
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename=Venta-report.pdf'
    print(venta_id)
    oPedidoproducto = Pedidoproductospresentacions.objects.filter(pedido_id=venta_id)
    print(oPedidoproducto)

    productos = []
    for oPedido in oPedidoproducto:
        nuevo = {}
        nuevo['nombreProducto'] = oPedido.productopresentacions.producto.nombre
        nuevo['nombrePresentacion'] = oPedido.productopresentacions.presentacion.nombre
        nuevo['cantidad'] = oPedido.cantidad
        nuevo['precioUnitario'] = oPedido.valor
        nuevo['subtotal'] = float(oPedido.valor)*float(oPedido.cantidad)
        productos.append(nuevo)
    print(productos)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    fecha = datetime.today()
    hoy = fecha.strftime("%d/%m/%Y")
    #header
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30,750,'Venta')
    c.setFont('Helvetica', 22)
    c.drawString(30,735,'Reporte')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(480,750,hoy)
    c.line(460,747,560,747)

    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10
    nombreProducto = Paragraph('''Producto''',styleBH)
    nombrePresentacion = Paragraph('''Presentacion''',styleBH)
    cantidad = Paragraph('''Cantidad''',styleBH)
    precioUnitario = Paragraph('''Precio Unitario''',styleBH)
    subtotal = Paragraph('''Sub total''',styleBH)

    data = []

    data.append([nombreProducto,nombrePresentacion,cantidad,precioUnitario,subtotal])

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 650
    for producto in productos:
        this_producto = [producto['nombreProducto'],producto['nombrePresentacion'],producto['cantidad'],producto['precioUnitario'],producto['subtotal']]
        data.append(this_producto)
        high = high - 18

    width, height = A4
    table = Table(data, colWidths=[1.9 * cm, 9.5 * cm,1.9 * cm,1.9 * cm,1.9 * cm,1.9 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('BOX',(0,0),(-1,-1),0.25,colors.black),
    ]))

    table.wrapOn(c,width,height)
    table.drawOn(c,30,high)
    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def todosEmpleadosVentas(request, mesActual, añoActual):
    empleados = Empleado.objects.filter(Q(perfil=1) | Q(perfil=4))
    jsonFinal = []
    # mesActual = datetime.now().month
    # añoActual = datetime.now().year

    for empleado in empleados:
        jsonEmpleadoVenta = {}
        jsonEmpleadoVenta['empleadoId'] = empleado.id
        jsonEmpleadoVenta['empleadoNombre'] = empleado.nombre
        montoFinal = 0.0

        pedidos = Pedido.objects.filter(empleado=empleado, estado=3, fecha__month=mesActual, fecha__year=añoActual) | Pedido.objects.filter(empleado=empleado, estado=4, fecha__month=mesActual, fecha__year=añoActual)
        if pedidos:
            for pedido in pedidos:
                montoVentasEmpleado = Venta.objects.filter(pedido=pedido, estado=True).aggregate(Sum('monto'))['monto__sum']
                print(montoVentasEmpleado)
                if montoVentasEmpleado:
                    montoFinal += montoVentasEmpleado
                else:
                    montoFinal = 0.0

            jsonEmpleadoVenta['montoVenta'] = montoFinal
        else:
            jsonEmpleadoVenta['montoVenta'] = 0.0

        jsonFinal.append(jsonEmpleadoVenta)

    return JsonResponse(jsonFinal, safe=False)

def empleadoVentas(request, empleado_id, mesActual, añoActual):
    jsonFinal = []

    empleado = Empleado.objects.get(id=empleado_id)

    if empleado:
        pedidos = Pedido.objects.filter(empleado=empleado, estado=3, fecha__month=mesActual, fecha__year=añoActual) | Pedido.objects.filter(empleado=empleado, estado=4, fecha__month=mesActual, fecha__year=añoActual)
        if pedidos:
            for pedido in pedidos:
                montoVentaEmpleado = Venta.objects.filter(pedido=pedido, estado=True).aggregate(Sum('monto'))['monto__sum']
                jsonEmpleadoVenta = {}
                jsonEmpleadoVenta['fecha'] = pedido.fecha
                jsonEmpleadoVenta['monto'] = montoVentaEmpleado
                jsonFinal.append(jsonEmpleadoVenta)
        else:
            jsonEmpleadoVenta = {}
            jsonEmpleadoVenta['fecha'] = 'no existen registros'
            jsonEmpleadoVenta['monto'] = 0.0
            jsonFinal.append(jsonEmpleadoVenta)
    else:
        jsonEmpleadoVenta = {}
        jsonFinal.append(jsonEmpleadoVenta)

    return JsonResponse(jsonFinal, safe=False)

@login_required
def reporteVentasAnuladas(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oEmpleados = Empleado.objects.filter(Q(perfil=1) | Q(perfil=4))
    context = {
        "empleados": oEmpleados
        }

    return render(request, 'reporte/ventasAnuladas.html', context)


def ventasAnuladasReporte(request, empleado_id, mesActual, añoActual):
    jsonFinal = []

    empleado = Empleado.objects.get(id=empleado_id)
    anulaciones = Anulacionventa.objects.filter(fecha__month=mesActual, fecha__year=añoActual, usuario=empleado.usuario)

    for anulacion in anulaciones:
        jsonEmpleadoVentaAnulada = {}
        jsonEmpleadoVentaAnulada['fechaAnulacion'] = anulacion.fecha
        jsonEmpleadoVentaAnulada['fechaVenta'] = anulacion.venta.fecha
        jsonEmpleadoVentaAnulada['descripcion'] = anulacion.descripcion
        jsonEmpleadoVentaAnulada['monto'] = anulacion.venta.monto
        jsonFinal.append(jsonEmpleadoVentaAnulada)

    return JsonResponse(jsonFinal, safe=False)

def todoMontoVentasAnuladas(request, mesActual, añoActual):
    jsonFinal = []

    empleados = Empleado.objects.filter(Q(perfil=1) | Q(perfil=4))

    for empleado in empleados:
        jsonEmpleadoVentaAnulada = {}
        jsonEmpleadoVentaAnulada['empleadoId'] = empleado.id
        jsonEmpleadoVentaAnulada['empleadoNombre'] = empleado.nombre
        montoFinal = 0.0

        ventaAnuladas = Anulacionventa.objects.filter(fecha__year=añoActual, fecha__month=mesActual, usuario=empleado.usuario)
        if ventaAnuladas:
            for ventaAnulada in ventaAnuladas:
                montoVentaAnulada = ventaAnulada.venta.monto
                montoFinal += montoVentaAnulada
            jsonEmpleadoVentaAnulada['monto'] = montoFinal

        else:
            jsonEmpleadoVentaAnulada['monto'] = '0.0'

        jsonFinal.append(jsonEmpleadoVentaAnulada)

    return JsonResponse(jsonFinal, safe=False)
