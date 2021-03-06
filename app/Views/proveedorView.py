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


@csrf_exempt
def BuscarProveedor(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        print(Datos)
        usuario=True
        if usuario==True:
            nombreProveedor = Datos["nombreProveedor"]
            jsonfinal = {}
            jsonfinal["proveedores"] = []
            try:
                oProveedores = Proveedor.objects.filter(nombre__icontains=nombreProveedor,estado = 1)|Proveedor.objects.filter(documento__icontains=nombreProveedor,estado = 1)
                for oProveedor in oProveedores:
                    
                    jsonProveedor = {}
                    jsonProveedor["id"] = oProveedor.id
                    jsonProveedor["nombre"] = oProveedor.nombre
                    jsonProveedor["direccion"] = oProveedor.direccion
                    jsonProveedor["documento"] = oProveedor.documento
                    jsonfinal["proveedores"].append(jsonProveedor)
                    
               	return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
            except Exception as e:
              return HttpResponse(json.dumps({'exito':1}), content_type="application/json")