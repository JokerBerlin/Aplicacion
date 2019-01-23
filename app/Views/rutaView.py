# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,  HttpResponseServerError
from ferreteria import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from datetime import datetime,date
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.rutaForm import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from app.validacionUser import validacionUsuario
###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################

perfiles_correctos = [1, 5]
@csrf_exempt
def rutaUsuario(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print (Datos)
        usuario=True
       # usuario= BuscarUsuario(Datos["idUsuario"])

        if usuario==True:
            idEmpleado = Datos["idEmpleado"]
            #try:
            oEmpleado = Empleado.objects.get(id=idEmpleado)
            oVisitas = Visita.objects.filter(estado = True, empleado = oEmpleado, nivel=oEmpleado.perfil)
            jsonfinal = {}
            jsonfinal["rutas"] = []
            for oVisita in oVisitas:
                rutasJson = {}
                rutasJson["x"]= oVisita.rutacliente.cliente.latitud
                rutasJson["y"]= oVisita.rutacliente.cliente.longitud
                rutasJson["activo"] = oVisita.activo
                rutasJson["idCliente"] = oVisita.rutacliente.cliente.id
                rutasJson["nombreCliente"] = oVisita.rutacliente.cliente.nombre
                rutasJson["idVisita"]= oVisita.id
                rutasJson["idPedido"]= 4
                jsonfinal["rutas"].append(rutasJson)
            return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
"""
def nuevaRuta(request):
    if request.method == 'POST':
        Datos = request.POST
        form = RutaForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('/Ruta/listar/')

    else:
        form = RutaForm()
        return render(request, 'Ruta/nuevo.html', {'form': form})

def listarRutas(request):
        oRuta=Ruta.objects.all()
        return render(request, 'ruta/listar.html', {'oRutas':oRuta})

"""
@login_required
@csrf_exempt
def detalleRuta(request,ruta_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'GET':
        idRuta = int(ruta_id)
        print(idRuta)
        oRuta = Ruta.objects.get(id=idRuta)
        print(oRuta)
        oRutaCliente = Rutaclientes.objects.filter(ruta=oRuta)
        coordenadas = []
        print(oRutaCliente)
        for rutaCliente in oRutaCliente:

            coord = {}
            coord['cliente'] = rutaCliente.cliente.nombre
            coord['lat'] = rutaCliente.cliente.latitud
            coord['lng'] = rutaCliente.cliente.longitud
            coordenadas.append(coord)

        print(coordenadas)

        listaCoordenadas = json.dumps(coordenadas)

        context = {
            "oRutaCliente": oRutaCliente,
            "oRuta": oRuta,
            "coordenadas": listaCoordenadas
        }

        return render(request, 'ruta/detalle.html', context)

@csrf_exempt
@login_required
def registrarRuta(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # print(Datos)
        nombreRuta = Datos['oRutas'][0][0]
        oRuta = Ruta.objects.create(nombre=nombreRuta)
        for oRutas in Datos['oRutas']:
            print(oRutas)
            nombreCliente = oRutas[1]
            oCliente = Cliente.objects.get(nombre=nombreCliente)
            oRutaCliente = Rutaclientes(ruta=oRuta, cliente=oCliente)
            oRutaCliente.save()

        return HttpResponse(json.dumps({'exito':1, 'idRuta':oRuta.id}), content_type="application/json")
    else:
        return render(request, 'ruta/nuevo.html', {})

@login_required
def editarRuta(request,ruta_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oRuta = Ruta.objects.get(id = ruta_id)
    if request.method=='POST':
        form =RutaForm(request.POST, instance=oRuta)
        if form.is_valid():
            edit_prod=form.save(commit=False)
            form.save_m2m()
            edit_prod.status=True
            edit_prod.save()

            return redirect('/Ruta/listar/')
    else:
        form= RutaForm(instance=oRuta)
        ctx = {'form':form, 'oCliente': oRuta.clientes, 'oRuta':oRuta}
    return render(request, 'Ruta/editar.html',ctx)

@login_required
def listarRutas(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        return render(request, 'Ruta/listar.html')
    else:
        oRuta = Ruta.objects.filter(estado = True).order_by('-id')
        paginator = Paginator(oRuta,10)

        page = request.GET.get('page')
        try:
            rutaPagina = paginator.page(page)
        except PageNotAnInteger:
            rutaPagina = paginator.page(1)
        except EmptyPage:
            rutaPagina = paginator.page(paginator.num_pages)

        index = rutaPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return render(request, 'ruta/listar.html', {"oRutas": rutaPagina,"page_range": page_range})