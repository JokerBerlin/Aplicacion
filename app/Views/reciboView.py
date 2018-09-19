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
def BuscarRecibo(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        print(Datos)
        usuario=True
        if usuario==True:
            nombreRecibo = Datos["nombreRecibo"]
            jsonfinal = {}
            jsonfinal["recibos"] = []
            try:
                oRecibos = Recibo.objects.filter(nombre__icontains=nombreRecibo,estado = 1)
                for oRecibo in oRecibos:
                    
                    jsonRecibo = {}
                    jsonRecibo["id"] = oRecibo.id
                    jsonRecibo["nombre"] = oRecibo.nombre

                    jsonfinal["recibos"].append(jsonRecibo)
                    
               	return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
            except Exception as e:
              return HttpResponse(json.dumps({'exito':0}), content_type="application/json")