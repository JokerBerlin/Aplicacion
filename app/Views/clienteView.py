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
from app.fomularios.clienteForm import *

from app.validacionUser import validacionUsuario

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from geopy.distance import distance, lonlat

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################

perfiles_correctos = [1, 4]

# Funcion para calcular distancia dados la latitud y longitud
def calcularDistancia(lat1, lng1, lat2, lng2):
    coords_1 = lonlat(lng1, lat1)
    coords_2 = lonlat(lng2, lat2)

    return distance(coords_1, coords2).km * 1000

# es necesario pasar el dato de corrdenadas para poder calcular la distancia y devolver verdad o falso
@csrf_exempt
def buscarCliente(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print("DATOS", Datos)
        usuario=True
        if usuario==True:
            nombreCliente = Datos["nombreCliente"]
            jsonfinal = {}
            jsonfinal["clientes"] = []
            try:
                oClientes = Cliente.objects.filter(nombre__icontains=nombreCliente,estado = 1)|Cliente.objects.filter(numerodocumento__icontains=nombreCliente,estado = 1)
                for oCliente in oClientes:
                    jsonCliente = {}
                    jsonCliente["id"] = oCliente.id
                    jsonCliente["direccion"] = oCliente.direccion
                    jsonCliente["nombre"] = oCliente.nombre
                    jsonCliente["numerodocumento"] = oCliente.numerodocumento
                    jsonCliente["longitud"] = oCliente.longitud
                    jsonCliente["latitud"] = oCliente.latitud
                    jsonCliente["precioId"] = oCliente.precio_id
                    jsonfinal["clientes"].append(jsonCliente)
                print("JSONFINAL", jsonfinal)
                return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

@login_required
def detalleCliente(request,cliente_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oCliente = Cliente.objects.get(id=cliente_id,estado=True)
    oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'cliente/detalle.html', {'oCliente':oCliente})

def estadoCliente(request):
    pk = request.POST.get('identificador_id')
    id = Cliente.objects.get(id=pk).update(estado=0)

    response = {}
    return JsonResponse(response)

@csrf_exempt
def detalleClienteWS(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idCliente = Datos["idCliente"]
            #try:
            oCliente = Cliente.objects.get(id=idCliente,estado = 1)
            jsonCliente = {}
            jsonCliente["id"] = oCliente.id
            jsonCliente["direccion"] = oCliente.direccion
            jsonCliente["nombre"] = oCliente.nombre
            jsonCliente["numerodocumento"] = oCliente.numerodocumento
            jsonCliente["latitud"] = oCliente.latitud
            jsonCliente["longitud"] = oCliente.longitud
            ############### Calcular ##################
            jsonCliente["LimiteCredito"] = 1200
            jsonCliente["MontoCredito"] = 980.50
            jsonCliente["Pedidos"] = []
            oPedidos = Pedido.objects.filter(cliente=oCliente,estado = True)
            for oPedido in oPedidos:
                jsonPedido = {}
                jsonPedido["fecha"] = oPedido.fecha
                jsonPedido["monto"] = "S/. 251.00"
                jsonCliente["Pedidos"].append(jsonPedido)

            return HttpResponse(json.dumps(jsonCliente), content_type="application/json")
            #except Exception as e:
        #    return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

@login_required
def editarCliente(request,cliente_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oCliente = Cliente.objects.get(id = cliente_id)
    if request.method == 'POST':
        Datos = request.POST
        form = ClienteForm(request.POST or None, instance=oCliente)
        if form.is_valid():
            form = form.save()
            return redirect('/Cliente/listar/')

        else:
            return render(request, '/Cliente/error.html')
    else:
        if not validacionUsuario(request.user) in perfiles_correctos:
            return redirect('/error/')
        form = ClienteForm(request.POST or None, instance=oCliente)
        print(form)
        return render(request, 'cliente/editar.html', {'form': form, 'oCliente':oCliente})

@csrf_exempt
def registrarCliente(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        oCliente = Cliente()
        oCliente.nombre = Datos['nombre']
        oCliente.direccion = Datos['direccion']
        oCliente.longitud = Datos['longitud']
        oCliente.latitud = Datos['latitud']
        oCliente.numerodocumento = Datos['documento']
        oCliente.precio_id = Datos['precio']
        oCliente.save()
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

@login_required
def nuevoCliente(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        Datos = request.POST
        cliente = Cliente(
            nombre=Datos['nombre'],
            direccion=Datos['direccion'],
            numerodocumento=Datos['numerodocumento'],
            precio_id=Datos['id_precio'],
            latitud=Datos['latitud'],
            longitud=Datos['longitud']
            )
        if cliente:
            cliente.save()
            return redirect('/Cliente/listar/')

        else:
            return render(request, 'cliente/error.html')
    else:
        if not validacionUsuario(request.user) in perfiles_correctos:
            return redirect('/error/')
        precios = Precio.objects.all()
        return render(request, 'cliente/nuevo.html', {'precios': precios})

@login_required
def listarCliente(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'GET':
        if not validacionUsuario(request.user) in perfiles_correctos:
            return redirect('/error/')
        oClientes = Cliente.objects.filter(estado=True).order_by('-id')
        paginator = Paginator(oClientes,10)

        page = request.GET.get('page')
        try:
            client = paginator.page(page)
        except PageNotAnInteger:
            client = paginator.page(1)
        except EmptyPage    :
            client = paginator.page(paginator.num_pages)

        index = client.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]



        try:
            return render(request, 'cliente/listar.html',{'oClientes':client,'page_range':page_range})
        except Exception as e:
                return render(request, 'cliente/error.html')
    else:
        return render(request, 'cliente/nuevo.html', {})

def eliminar_identificador_cliente(request):
    pk = request.POST.get('identificador_id')
    identificador = Cliente.objects.get(pk=pk)
    identificador.estado = 0
    identificador.save()
    response = {}
    return JsonResponse(response)
