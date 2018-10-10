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
def insertarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
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
        print(oPedidoProductos)
        for oPedidoProducto in oPedidoProductos:
            print(oPedidoProducto[1])
            oProducto = Producto.objects.get(codigo=oPedidoProducto[1])
            print(oProducto.id)
            print(oPedidoProducto[3])
            oPresentacion = Presentacion.objects.get(nombre=oPedidoProducto[3])
            print(oPresentacion.id)
            oProductoPresentacions = Productopresentacions.objects.get(producto_id=oProducto.id,presentacion_id=oPresentacion.id)
            print(oProductoPresentacions.id)
            oPedidoproductospresentacions = Pedidoproductospresentacions()
            oPedidoproductospresentacions.valor = oPedidoProducto[4]
            oPedidoproductospresentacions.cantidad = oPedidoProducto[0]
            oPedidoproductospresentacions.pedido = oPedido
            oPedidoproductospresentacions.productopresentacions_id=oProductoPresentacions.id
            oPedidoproductospresentacions.save()
        return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")

        #datos_list = json.loads(datos[0])

        #return render(request, '/pedido/listar.html')
    else:

        return render(request, 'pedido/nuevo.html', {})
        return render(request, 'venta/prueba.html', {})


def registrarPedido(request):
    # if request.method == 'POST':
        # oPedido = Pedido.objects.get(pk=request.POST['pedido'])
        # oPedidoproductospresentacion = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
        # monto = 0.0
        # for item in oPedidoproductospresentacion:
        #     producto = item.productopresentacions.producto
        #     producto.cantidad -= item.cantidad
        #     monto += item.valor
        #
        # oVenta = Venta()
        # oVenta = monto
        # oVenta.nrecibo = request.POST['nrecibo']
        # oVenta.estado = True
        # oVenta.pedido_id = request.POST['pedido']
        # oVenta.cliente_id = oPedido.cliente_id

    oPresentaciones = Presentacion.objects.filter(estado=True)
    oPrecios = Precio.objects.filter(estado=True)

    context = {
        'presentaciones': oPresentaciones,
        'precios': oPrecios
    }

    return render(request, 'pedido/nuevo.html', context)


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

def FiltrarPedido(request):
    oProductos=[]
    oVentas=[]
    if "producto_busca" in request.COOKIES:
        producto = request.COOKIES["producto_busca"]
        print(request.COOKIES["producto_busca"])
    else:
        producto = ''

    if "cliente_busca" in request.COOKIES:
        dni = request.COOKIES["cliente_busca"]
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
        pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion]).order_by("-id")
        venta = pedido
        productonombre = Producto.objects.get(id=producto).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)

        oVentas = pedido
    if dni != '':
        objetotag={}
        objetotag['dni']=dni
        tags.append(objetotag)
        if dni.isdigit() == False :
            dni = Cliente.objects.get(nombre=dni).numerodocumento

        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
            for oVenta in venta:
                #pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oVenta.id)
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
            venta = Pedido.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos = []
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')
            for oVenta in venta:
                #pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oVenta.id)
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
            venta = Pedido.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
            for oVenta in venta:
                #pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oVenta.id)
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
            venta = Pedido.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')
            for oVenta in venta:
                #pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oVenta.id)
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
            oVentas = venta

    if producto=='' and dni=='' and fecha_inicio=='' and fecha_fin=='':
        oVenta = Pedido.objects.filter(estado = True).order_by('-id')
        for o in oVenta:
            #pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=o.id)
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

    return render(request, 'pedido/listar.html', {"oPedidos": ventaPagina,"oProductos":oProductos,"page_range": page_range,"tags":tags,})

@csrf_exempt
def pedidoVenta(request):
    if request.method == 'POST':
        dato = json.loads(request.body)
        pk = dato['cmbPedido']
        
        pedido = Pedido.objects.get(pk = pk)
        jsonPedidos = {}
        jsonPedidos.pk = pedido.pk
        jsonPedidos.fecha = pedido.fecha
        jsonPedidos.estado = pedido.estado
        jsonPedidos.empleado = pedido.empleado
        jsonPedidos.cliente = pedido.cliente

    return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")