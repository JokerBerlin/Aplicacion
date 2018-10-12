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
###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción: 
#   servicio de busqueda de usuario para la app movil
###########################################################

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
                rutasJson["x"]= oVisita.rutacliente.cliente.longitud
                rutasJson["y"]= oVisita.rutacliente.cliente.latitud
                rutasJson["activo"]= oVisita.activo
                rutasJson["idCliente"]= oVisita.rutacliente.cliente.id
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
def listarRutas(request):
    if request.method == 'POST':
        return render(request, 'Ruta/listar.html')
    else:
        oRuta= Ruta.objects.filter(estado = True)
        return render(request, 'ruta/listar.html', {"oRutas": oRuta})

def detalleRuta(request,ruta_id):
    if request.method == 'GET':
        idRuta = int(ruta_id)
        oRuta= Ruta.objects.get(id=idRuta)
        return render(request, 'ruta/detalle.html', {"oRuta":oRuta})

@csrf_exempt
def registrarRuta(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #print(Datos)

        for oRutas in Datos['oRutas']:
            print(oRutas)
            nombreCliente= oRutas[1]
            oCliente= Cliente.objects.filter(nombre=nombreCliente)

            nombreRuta=oRutas[0]
            oRuta=Ruta.objects.create(nombre=nombreRuta)
            for oClientes in oCliente:
                oRuta.clientes.add(oClientes)
                oRuta.save()

        return HttpResponse(json.dumps({'exito':1, 'idRuta':oRuta.id}), content_type="application/json")
    else:

        return render(request, 'ruta/nuevo.html', {})

def editarRuta(request,ruta_id):
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


def listarRutas(request):
    if request.method == 'POST':
        return render(request, 'Ruta/listar.html')
    else:
        oRuta= Ruta.objects.filter(estado = True)
        return render(request, 'ruta/listar.html', {"oRutas": oRuta})
