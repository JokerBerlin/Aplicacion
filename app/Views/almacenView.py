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
def BuscarAlmacen(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        print(Datos)
        usuario=True
        if usuario==True:
            nombreAlmacen = Datos["nombreAlmacen"]
            jsonfinal = {}
            jsonfinal["almacenes"] = []
            try:
                oAlmacenes = Almacen.objects.filter(nombre__icontains=nombreAlmacen,estado = 1)
                for oAlmacen in oAlmacenes:
                    
                    jsonAlmacen = {}
                    jsonAlmacen["id"] = oAlmacen.id
                    jsonAlmacen["nombre"] = oAlmacen.nombre

                    jsonfinal["almacenes"].append(jsonAlmacen)
                    
               	return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
            except Exception as e:
              return HttpResponse(json.dumps({'exito':0}), content_type="application/json")