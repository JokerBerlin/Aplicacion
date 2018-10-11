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

def FiltrarVenta(request):
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

    if producto=='' and dni=='' and fecha_inicio=='' and fecha_fin=='':
        oVenta = Venta.objects.filter(estado = True).order_by('-id')
        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
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
    identificador = Venta.objects.get(pk=pk)
    identificador.estado = 0
    identificador.save()
    response = {}
    return JsonResponse(response)

def listarPedidosVenta(request):
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'venta/pedido-listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = 2).order_by('-id')
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

        return render(request, 'venta/pedido-listar.html', {"oPedidos": pedidoPagina,"oProductos":oProductos,"page_range": page_range})
        

def ventaNuevo(request):    	
    oPresentaciones = Presentacion.objects.filter(estado=True)	
    oPrecios = Precio.objects.filter(estado=True)	
    oPedidos = Pedido.objects.filter(estado=2)	
    
    context = {	
        'presentaciones': oPresentaciones,	
        'precios': oPrecios,	
        'pedidos': oPedidos	
    }	
    
    return render(request, 'venta/nuevo.html', context)

@csrf_exempt
#Caso en el que se crea una venta sin pasar antes por pedidos y almacen
def insertarVenta(request):
    if request.method == 'POST':
        datos = json.loads(request.body)

        dni_cliente = datos['cliente']

        #Se genera el pedido con un estado 3
        #Se necesita hacer el descuento en almacen
        oCliente = Cliente.objects.get(numerodocumento=dni_cliente)
        empleado = 1
        oPedido = Pedido(estado=3, empleado_id=empleado, cliente=oCliente)
        oPedido.save()
        oVenta = Venta(pedido=oPedido, cliente=oCliente)
        monto_venta = 0.00

        productos = datos['productos']
        print(productos)
        for producto in productos:
            monto_venta += round(float(producto[0]) * float(producto[4]), 2)
            oProducto = Producto.objects.get(codigo=producto[1])
            print(oProducto.nombre)
            oPresentacion = Presentacion.objects.get(nombre=producto[3])
            print(oPresentacion.nombre)
            oProductoPresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
            oPedidoproductospresentacions = Pedidoproductospresentacions(
                valor = producto[4],
                cantidad = producto[0],
                pedido = oPedido,
                productopresentacions = oProductoPresentacions
            )
            oPedidoproductospresentacions.save()
        
        oVenta.monto = monto_venta
        oVenta.save()

        return HttpResponse(json.dumps({'exito': 1, "idPedido": oPedido.id}), content_type="application/json")

    else:
        return render(request, 'venta/nuevo')


    return datos