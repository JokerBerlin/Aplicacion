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

from app.validacionUser import validacionUsuario

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################

perfiles_correctos = [1, 2, 3]
@csrf_exempt
# Pedido/registrar/
@login_required
def insertarPedido(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
        #Dato = json.loads(request.body)
        #Dato = request.POST
        dnis = Datos['cliente']
        print(dnis)
        try:
            oCliente = Cliente.objects.get(numerodocumento=dnis)
        except Exception as e:
            oCliente = ''
            print('none')
        #   oCliente = Cliente.objects.get(numerodocumento=dnis)
        fechaHoy=date.today()
        usuario = request.user
        empleado = Empleado.objects.get(usuario=usuario)
        if oCliente == '':
            oPedido = Pedido(fecha=fechaHoy,estado=1,empleado=empleado)
        else:
            oPedido = Pedido(fecha=fechaHoy,estado=1,empleado=empleado,cliente_id=oCliente.id)

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

    else:

        return render(request, 'pedido/nuevo.html', {})

@login_required
def registrarPedido(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')

    oPresentaciones = Presentacion.objects.filter(estado=True)
    oPrecios = Precio.objects.filter(estado=True)

    context = {
        'presentaciones': oPresentaciones,
        'precios': oPrecios
    }

    return render(request, 'pedido/nuevo.html', context)

@login_required
def ListarPedidos(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.all().order_by('-id')
        for oPedido in oPedidos:
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oPedido.id)
            print(pedidoproductospresentacions)
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oPedido.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        paginator = Paginator(oPedidos,10)

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
@login_required
def ListarEstadoPedidos(request,estado_id):
    if validacionUsuario(request.user) in [1, 2]:
        if estado_id != '1':
            return redirect('/error/')
    if validacionUsuario(request.user) in [1, 3, 4]:
        if estado_id != '2':
            return redirect('/error/')
    if validacionUsuario(request.user) in [1, 4]:
        if estado_id == '3':
            return redirect('/error/')

    oProductos=[]
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado=estado_id).order_by('-id')
        for oPedido in oPedidos:
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=oPedido.id)
            print(pedidoproductospresentacions)
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oPedido.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        paginator = Paginator(oPedidos,10)

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
        estadoPedido = int(estado_id)
        if estadoPedido==1:
            return render(request, 'pedido/almacen.html', {"oPedidos": pedidoPagina,"oProductos":oProductos,"page_range": page_range})
        if estadoPedido==2:
            return render(request, 'pedido/ventaPendiente.html', {"oPedidos": pedidoPagina,"oProductos":oProductos,"page_range": page_range})
        else:
            return render(request, 'pedido/listar.html', {"oPedidos": pedidoPagina,"oProductos":oProductos,"page_range": page_range})

@login_required
def ResumenPedidos(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = 2)

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
        print(oProductos)
        paginator = Paginator(oProductos,10)

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

@login_required
def DetallePedido(request,pedido_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
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
        return render(request, 'pedido/detalle.html', {"oCliente": oPedido.cliente, "oProductos": oProductos,"idPedido":idPedido})
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        return render(request, 'pedido/listar.html',{"oPedidos": oPedidos})

@csrf_exempt
def InstarPedido(request):
    if request.method=='POST':
        Datos = json.loads(request.body)
        print(Datos)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idEmpleado = Datos["idEmpleado"]
            oEmpleado = Empleado.objects.get(id=idEmpleado)
            idCliente = Datos["idCliente"]
            oCliente = Cliente.objects.get(id= idCliente)
            tipoPedido = Datos['tipoPedido']

            oPedido = Pedido()
            oPedido.empleado = oEmpleado
            oPedido.cliente = oCliente
            oPedido.tipo = tipoPedido
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
        print(Datos)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            fecha = datetime.today()
            print(fecha)
            idEmpleado = Datos["idEmpleado"]
            jsonPedidos = {}
            jsonPedidos["pedidos"] = []
            TotalPedidos = 0

            #oPedidos = Pedido.objects.filter(estado = True,fecha = fecha, empleado = idEmpleado)
            oPedidos = Pedido.objects.filter(estado = 2, empleado = idEmpleado, fecha__month=fecha.month, fecha__year=fecha.year)
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


                TotalPedidos = TotalPedidos + TotalPedido
                jsonPedido["TotalPedido"] = TotalPedido

                jsonPedidos["pedidos"].append(jsonPedido)
                # print(jsonPedidos)
            jsonPedidos["TotalPedidos"] = TotalPedidos
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

@login_required
def editarPedido(request,pedido_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    #oProductopresentacions= Productopresentacions.objects.filter(producto_in=oPedidoproductospresentacions.productopresentacions.producto.id)
    if request.method == 'POST':
        # form = PedidoproductospresentacionsForm(instance=oPedidoproductospresentacions)
        # form2=Productopresentacions()
        # if form.is_valid():
        #     edit_ped=form.save(commit=False)
        #     edit_pre=form2.save(commit=False)
        #     form.save_m2m()
        #     form2.save_m2m()
        #     edit_ped.status=True
        #     edit_pre.status=True
        #     edit_ped.save()
        #     edit_pre.save()

        return redirect('/Pedido/listar/')


    else:
        oPedido = Pedido.objects.get(id=pedido_id)
        try:
            cliente = oPedido.cliente.nombre

        except Exception as e:
            cliente = ''
        empleado = oPedido.empleado.nombre
        print(empleado)
        fecha = oPedido.fecha
        oPedidoproductospresentacions= Pedidoproductospresentacions.objects.filter(pedido=pedido_id)
        print(oPedidoproductospresentacions)
        cantidadPedido = []
        cont = 0
        totalMonto = 0;
        for oPedido in oPedidoproductospresentacions:
            oNuevo = {}
            oNuevo['id']=oPedido.id
            c = int(round(oPedido.cantidad))
            oNuevo['cantidad']=str(c).replace(",", ".")
            oAlmacens = Producto_almacens.objects.filter(producto_id = oPedido.productopresentacions.producto.id).latest('id')
            oNuevo['cantidadTotal'] = oAlmacens.cantidad
            oNuevo['contador']=cont
            oNuevo['valor']="{0:.2f}".format(round(float(oPedido.valor),8))
            subt = round(float(oPedido.cantidad)*float(oPedido.valor),8)
            totalMonto = totalMonto + subt
            oNuevo['total']="{0:.2f}".format(round(subt,2))
            cantidadPedido.append(oNuevo)
            cont = cont + 1
        totalMonto = "{0:.2f}".format(round(totalMonto,2))
        #form = PedidoproductospresentacionsForm(instance=oPedidoproductospresentacions)
        #form2= ProductopresentacionsForm(instance=oProductopresentacions)
        return render(request, 'pedido/editar.html', {'cliente': cliente,'pedidoId':pedido_id,'fecha':fecha, 'empleado': empleado, 'pedidos':oPedidoproductospresentacions,'cantidadPedido':cantidadPedido,'totalMonto':totalMonto,})

@csrf_exempt
@login_required
def pedidoVenta(request,pedido_id):
    if not validacionUsuario(request.user) in [1, 2, 3, 4]:
        return redirect('/error/')
    #oProductopresentacions= Productopresentacions.objects.filter(producto_in=oPedidoproductospresentacions.productopresentacions.producto.id)
    if request.method == 'POST':

        Datos = json.loads(request.body)
        cliente = Datos['cliente']
        tipoRecibo = Datos['tipoRecibo']
        numeroRecibo = Datos['numeroRecibo']
        total = Datos['total']
        oPedido = Pedido.objects.get(id=pedido_id)
        oVenta = Venta()
        oVenta.monto = total
        oVenta.nrecibo = numeroRecibo
        oVenta.estado = True
        try:
            oCliente = Cliente.objects.get(nombre=cliente)
            oVenta.cliente_id = oCliente.id
        except Exception as e:
            oCliente = ''

        oVenta.pedido_id = oPedido.id
        oVenta.save()
        oPedido.estado = 3
        oPedido.save()
        oCobro = Cobro()
        oCobro.estado=True
        oCobro.monto=total
        oCobro.recibo_id=tipoRecibo
        oCobro.venta_id=oVenta.id
        oCobro.save()

        usuario = request.user
        empleado = Empleado.objects.get(usuario=usuario)

        oOperacion = Operacion(
            monto = oCobro.monto,
            estado = True,
            caja_id = empleado.caja.id,
            cobro = oCobro ,
            detalletipooperacion_id=1
        )

        oOperacion.save()

        # oAperturaCaja = Aperturacaja.objects.filter(caja_id=empleado.caja.id).latest('pk')
        # monto = float(oAperturaCaja.monto) + float(oOperacion.monto)
        # # oAperturaCajaNuevo = Aperturacaja(
        #     monto=monto,
        #     activo=1,
        #     estado=1,
        #     caja_id=empleado.caja.id
        # )
        # oAperturaCajaNuevo.save()
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

    else:
        #oUltimoP=Producto_almacens.objects.filter(producto_id=oProductoPresentacions.producto_id).latest('id')

        oSerie = Serie.objects.filter(recibo_id=2).latest('id')

        print("#####serie####")
        print(oSerie.numeroSerie)

        oPedido = Pedido.objects.get(id=pedido_id)
        oRecibos = Recibo.objects.filter(estado=True)
        try:
            cliente = oPedido.cliente.nombre
        except Exception as e:
            cliente = ''
        empleado = oPedido.empleado.nombre
        fecha = oPedido.fecha
        oPedidoproductospresentacions= Pedidoproductospresentacions.objects.filter(pedido=pedido_id)
        cantidadPedido = []
        cont = 0
        for oPedido in oPedidoproductospresentacions:
            oNuevo = {}
            oNuevo['id']=oPedido.id
            c = oPedido.cantidad
            oNuevo['cantidad']=str(c).replace(",", ".")
            oNuevo['contador']=cont
            oNuevo['valor']=float(oPedido.valor)
            oNuevo['total']="{0:.2f}".format(float(oPedido.cantidad)*float(oPedido.valor))
            cantidadPedido.append(oNuevo)
            cont = cont + 1

        try:
            oVenta = Venta.objects.latest('id')
            listacf = oVenta.nrecibo.split("-")
        except Exception as e:
            listacf = oSerie.numeroSerie + '-0000001'
        #else:
        #    pass
        #print(listacf)
        if oSerie.numeroSerie == listacf[0]:
            print("hola mundo")
            valorNumeroBoleta = int(listacf[1]) + 1
            print(valorNumeroBoleta)
            listacf[1]=valorNumeroBoleta
            print(listacf)
            cantidadDigitos = len(str(valorNumeroBoleta))
            cadena = ''

            c = 7
            c = c - cantidadDigitos
            cadena = ''
            while c>=1:
                cadena = cadena + '0'
                c = c-1
            cadena = cadena + str(valorNumeroBoleta)
            listacf[1]=cadena
            cadenaNueva = "-".join(listacf)
            print(cadenaNueva)

        else:
            listacf[0]=oSerie.numeroSerie
            listacf[1]='0000001'
            cadenaNueva = "-".join(listacf)

        return render(request, 'venta/mostrarPedido.html', {'nroRecibo':cadenaNueva,'cliente': cliente,'pedidoId':pedido_id,'fecha':fecha, 'empleado': empleado, 'pedidos':oPedidoproductospresentacions,'cantidadPedido':cantidadPedido,'oRecibos':oRecibos})


@csrf_exempt
def modificarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
        dato = Datos['productos']
        idPedido = Datos['pedido']
        print(idPedido)
        for oPedidoProducto in dato:

            id=int(oPedidoProducto[0])
            oPedidoproductospresentacions = Pedidoproductospresentacions.objects.get(id=id)
            #cantidad = (oPedidoProducto[1])
            oPedidoproductospresentacions.cantidad = oPedidoProducto[1]
            oPedidoproductospresentacions.save()
            #oPedidoproductospresentacions = Pedidoproductospresentacions.objects.get(id=id)

            oProductoPresentacions = Productopresentacions.objects.get(id=oPedidoproductospresentacions.productopresentacions_id)
            oUltimoP=Producto_almacens.objects.filter(producto_id=oProductoPresentacions.producto_id).latest('id')
            dato = float(oPedidoProducto[1]) * oProductoPresentacions.valor
            cantidadPedido = oUltimoP.cantidad - dato
            oProducto_alma = Producto_almacens(cantidad=cantidadPedido, cantidadinicial= oUltimoP.cantidad, almacen_id=oUltimoP.almacen_id, lote_id= oUltimoP.lote_id, producto_id= oUltimoP.producto_id)
            oProducto_alma.save()
        oPedido = Pedido.objects.get(id=idPedido)
        oPedido.estado = 2
        oPedido.save()
    return HttpResponse(json.dumps({'exito':1}), content_type="application/json")


def eliminar_identificador_pedido(request):
    pk = request.POST.get('identificador_id')
    identificador = Pedido.objects.get(pk=pk)
    identificador.estado = 0
    identificador.save()
    response = {}
    return JsonResponse(response)

@login_required
def FiltrarPedido(request):
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
        print(dni.isdigit())
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
        pedido = Pedido.objects.filter(id__in=[s.pedido_id for s in pedidoproductopresentacion]).order_by("-id")
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


        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(cliente_id=cliente.id).order_by('-id')
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
            venta = Pedido.objects.filter(id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos = []
            venta = Pedido.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
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
            venta = Pedido.objects.filter(id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
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
            venta = Pedido.objects.filter(id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(fecha__lte=fecha2).order_by('-id')
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
        oVenta = Pedido.objects.all().order_by('-id')
        for o in oVenta:
            #pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=o.id)
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
        oVentas = oVenta
    paginator = Paginator(oVentas,10)

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

@login_required
def EstadoPedido(request,estado_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProductos=[]
    oVentas=[]
    estadoPedido=int(estado_id)
    if "producto_busca" in request.COOKIES:
        producto = request.COOKIES["producto_busca"]
        print(request.COOKIES["producto_busca"])
    else:
        producto = ''

    if "cliente_busca" in request.COOKIES:
        dni = request.COOKIES["cliente_busca"]

        if dni.isdigit() == False :
            dni = Cliente.objects.get(nombre=dni).numerodocumento
        print(dni.isdigit())
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
        pedido = Pedido.objects.filter(estado=estadoPedido,id__in=[s.pedido_id for s in pedidoproductopresentacion]).order_by("-id")
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


        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(estado=estadoPedido,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Pedido.objects.filter(estado=estadoPedido,cliente_id=cliente.id).order_by('-id')
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
            venta = Pedido.objects.filter(estado=estadoPedido,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos = []
            venta = Pedido.objects.filter(estado=estadoPedido,fecha__range=[fecha1,fecha2]).order_by('-id')
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
            venta = Pedido.objects.filter(estado=estadoPedido,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(estado=estadoPedido,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
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
            venta = Pedido.objects.filter(estado=estadoPedido,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            venta = Pedido.objects.filter(estado=estadoPedido,fecha__lte=fecha2).order_by('-id')
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
        oVenta = Pedido.objects.filter(estado = estadoPedido).order_by('-id')
        for o in oVenta:
            #pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id=o.id)
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
        oVentas = oVenta
    paginator = Paginator(oVentas,10)

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


    print(estadoPedido)
    if estadoPedido==1:
        return render(request, 'pedido/almacen.html', {"oPedidos": ventaPagina,"oProductos":oProductos,"page_range": page_range,"tags":tags,})
    elif estadoPedido==2:
        return render(request, 'pedido/ventaPendiente.html', {"oPedidos": ventaPagina,"oProductos":oProductos,"page_range": page_range,"tags":tags,})
    else:
        return render(request, 'pedido/nuevo.html')


@csrf_exempt
def ventaPedido(request):
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
