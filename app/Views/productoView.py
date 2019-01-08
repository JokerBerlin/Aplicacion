# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from ferreteria.urls import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *
from django.views.generic import DetailView

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.validacionUser import validacionUsuario

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil,
#   y en buscaar producto retorno de imagen.
###########################################################

perfiles_correctos = [1, 3]
@login_required
def ListarProductos(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        return render(request, 'Producto/listar.html')
    else:
        oProductos = Producto.objects.filter(estado = True).order_by('-id')
        precios=[]
        #for oProducto in oProductos:
        for oProducto in oProductos:
            nuevo={}
            try:
                oUltimoP=Producto_almacens.objects.filter(producto_id=oProducto).latest('id')
                print(oUltimoP)
                nuevo['id'] = oProducto.id
                nuevo['cantidad'] = round(oUltimoP.cantidad,2)
            except Exception as e:
                print(e)
                nuevo['id'] = oProducto.id
                nuevo['cantidad'] = 0
            precios.append(nuevo)
        #nuevo={}
        print(precios)

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

        return render(request, 'producto/listar.html', {'precios':precios,"oProductos": productoPagina,"page_range": page_range})

@csrf_exempt
@login_required
def registrarPresentacion(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
        Dato = Datos['presentaciones']
        print(Dato)
        #oPrecios = Datos['precios']
        oPresentaciones = Dato
        producto = Datos['producto']
        for oPresentacion in oPresentaciones:
            oProducto = Producto.objects.get(nombre=producto)
            #oPresentacion = Presentacion.objects.get(id=oPresentacion[1])
            oProductoPresentacions = Productopresentacions()
            oPre = Presentacion.objects.get(nombre=oPresentacion[0])
            oProductoPresentacions.producto_id = oProducto.id
            oProductoPresentacions.presentacion_id = oPre.id
            oProductoPresentacions.valor = round(1/float(oPresentacion[1]),8)
            oProductoPresentacions.unidadprincipal = 0
            oProductoPresentacions.save()
            oProductoPresentacions = Productopresentacions.objects.get(producto_id=oProducto.id,presentacion_id = oPre.id)
            #cont = 1
            oPrecios = Precio.objects.filter(estado=1)
            cont = 2
            for oPrecio in oPrecios:
                oProductoPresentacionsprecios = Productopresentacionsprecios()


                oProductoPresentacionsprecios.valor = oPresentacion[cont]
                oProductoPresentacionsprecios.precio_id = oPrecio.id
                oProductoPresentacionsprecios.productopresentacions_id = oProductoPresentacions.id
                oProductoPresentacionsprecios.save()
                cont = cont + 1



        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

    else:
        oUltimoP=Producto.objects.all().latest('id')
        print(oUltimoP.nombre)
        oPrecios = Precio.objects.filter(estado=True)
        oPresentacions = Presentacion.objects.all()
        oProPre = Productopresentacions.objects.get(producto_id=oUltimoP.id)
        oPresent = Presentacion.objects.get(id=oProPre.presentacion_id)
        print(oProPre.presentacion_id)
        presentaciones=[]
        for oPresentacion in oPresentacions:
            nuevo={}
            if(oPresent.id != oPresentacion.id):
                nuevo['id']=oPresentacion.id
                nuevo['nombre']=oPresentacion.nombre
                presentaciones.append(nuevo)

        print(presentaciones)

        return render(request,'producto/agregarPresentacion.html',{'precios':oPrecios,'producto':oUltimoP,'presentaciones':presentaciones})

@csrf_exempt
def insertarProducto(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)

    return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")

@login_required
def registrarProducto(request):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    if request.method == 'POST':
        Datos = request.POST
        print(Datos)
        form = ProductoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.valor = 1
            form = form.save(commit=False)
            form.save()
            oProducto = form
            oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
            producto_id = str(oProducto.id)
            oProductopresentacions= Productopresentacions(producto_id=oProducto.id, presentacion_id=oPresentacion.id,valor=1,unidadprincipal=True)
            oProductopresentacions.save()
            oProductopresentacions = Productopresentacions.objects.get(producto=oProducto.id, presentacion=oPresentacion.id)

            oPrecios = Precio.objects.filter(estado=True)

            for oPrecio in oPrecios:
                idPrecio = str(oPrecio.id)
                oProductoPresentacionsprecios = Productopresentacionsprecios(
                    valor=Datos[idPrecio],
                    precio=oPrecio,
                    productopresentacions_id=oProductopresentacions.id
                )
                oProductoPresentacionsprecios.save()

            return redirect('/Producto/editar/'+producto_id+'/')
        else:
            return render(request, 'producto/listar.html')

    else:
        form = ProductoForm()
        oPrecios = Precio.objects.filter(estado=True)
        oPresentaciones = Presentacion.objects.filter(estado=True)

    context = {
        'form': form,
        'precios':oPrecios,
        'presentaciones':oPresentaciones
    }

    return render(request, 'producto/registrar.html', context)

@csrf_exempt
def BuscarProducto(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #print Datos
        usuario=True
        #usuario= BuscarUsuario(Datos["idUsuario"])

        if usuario==True:
            nombreProducto = Datos["nombreProducto"]
            oProductos = Producto.objects.filter(nombre__icontains=nombreProducto, estado=True)
            jsonProductos = {}
            jsonProductos["productos"] = []
            for oProducto in oProductos:
                jsonProducto = {}
                jsonProducto["id"] = oProducto.id
                jsonProducto["nombre"] = oProducto.nombre
                jsonProducto["codigo"] = oProducto.codigo
                jsonProducto["valor"] = oProducto.valor

                if oProducto.imagen=="":
                    jsonProducto["imagen"] = "/media/default.jpg"
                else:
                    jsonProducto["imagen"] = oProducto.imagen.url
                print(jsonProducto["imagen"])
                jsonProductos["productos"].append(jsonProducto)

            return HttpResponse(json.dumps(jsonProductos), content_type="application/json")

        if request.is_ajax:
            palabra=request.GET.get('term','')

            doctores=Doctor.objects.filter(name__icontains=palabra)

            results=[]

            for doctor in doctores:
                doctor_json={}
                doctor_json['label']=doctor.name
                doctor_json['value']=doctor.name
                results.append(doctor_json)

            data_json=json.dumps(results)
        else:
            data_json='fail'
        mimetype="application/json"
        return HttpResponse(data_json,mimetype)


@csrf_exempt
def BuscarProductoPresentacionVenta(request):
    if request.method == 'POST':
        presentacion = request.POST['presentacion']
        producto = request.POST['producto']
        precio = request.POST['precioTipo']

        oProducto = Producto.objects.get(nombre=producto)
        oPresentacion = Presentacion.objects.get(nombre=presentacion)
        oPrecio = Precio.objects.get(pk=precio)

        try:
            oProductoPres = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
            oProductoPresPrecio = Productopresentacionsprecios.objects.get(precio=oPrecio, productopresentacions=oProductoPres)
            jsonResultado = {}
            jsonResultado["precio"] = oProductoPresPrecio.valor

        except Exception as e:
            jsonResultado = {}
            jsonResultado["precio"] = ''

    return HttpResponse(json.dumps(jsonResultado), content_type='application/json')


@csrf_exempt
def BuscarProductoPresentacion (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #print Datos
        usuario=True
        #usuario= BuscarUsuario(Datos["idUsuario"])

        if usuario==True:
            nombreProducto = Datos["nombreProducto"]
            oProductos = Producto.objects.filter(nombre__icontains=nombreProducto,estado = True)

            jsonProductos = {}

            jsonProductos["productos"] = []
            jsonProductos["presentacion"]=[]
            jsonProductos["precios"]=[]

            for oProducto in oProductos:
                jsonProducto = {}
                jsonProducto["id"] = oProducto.id
                jsonProducto["nombre"] = oProducto.nombre
                jsonProducto["codigo"] = oProducto.codigo
                jsonProducto["valor"] = oProducto.valor
                print ("------------------")
                print (oProducto.imagen)
                print ("------------------")
                if oProducto.imagen=="":
                    jsonProducto["imagen"] = "/media/default.jpg"
                else:
                    jsonProducto["imagen"] = oProducto.imagen.url
                jsonProductos["productos"].append(jsonProducto)

                oPresentaciones = Productopresentacions.objects.filter(producto=oProducto.id)

                for oPresentacion in oPresentaciones:
                    jsonPresentacion={}
                    jsonPresentacion["id"] = oPresentacion.id
                    jsonPresentacion["nombre"] = oPresentacion.presentacion.nombre
                    jsonPresentacion["valor"] = oPresentacion.valor
                    jsonProductos["presentacion"].append(jsonPresentacion)
                    oPrecios = Productopresentacionsprecios.objects.filter(productopresentacions=oPresentacion.id)
                    for oPrecio in oPrecios:
                        jsonPrecio={}
                        jsonPrecio["id"] = oPrecio.id
                        jsonPrecio["preId"] = oPresentacion.id
                        jsonPrecio["nombre"]=oPrecio.precio.nombre
                        jsonPrecio["valor"]=oPrecio.valor
                        jsonProductos["precios"].append(jsonPrecio)
                print(jsonProductos)


            return HttpResponse(json.dumps(jsonProductos), content_type="application/json")

        if request.is_ajax:
            palabra=request.GET.get('term','')

            doctores=Doctor.objects.filter(name__icontains=palabra)

            results=[]

            for doctor in doctores:
                doctor_json={}
                doctor_json['label']=doctor.name
                doctor_json['value']=doctor.name
                results.append(doctor_json)

            data_json=json.dumps(results)
        else:
            data_json='fail'
        mimetype="application/json"
        return HttpResponse(data_json,mimetype)


@csrf_exempt
def ListarPresentacionesProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print(Datos)
        #print Datos
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idProducto = Datos["idProducto"]
            oProuctoPresentaciones = Productopresentacions.objects.filter(producto= idProducto)
            #print oProuctoPresentaciones
            jsonPresentaciones = {}
            jsonPresentaciones["presentaciones"] = []
            for oProuctoPresentacion in oProuctoPresentaciones:
                jsonPresentacion = {}
                jsonPresentacion["id"] = oProuctoPresentacion.presentacion.id
                jsonPresentacion["nombre"] = oProuctoPresentacion.presentacion.nombre
                jsonPresentacion["codigo"] = oProuctoPresentacion.presentacion.codigo
                jsonPresentacion["valor"] = oProuctoPresentacion.valor
                OProductopresentacionsprecios = Productopresentacionsprecios.objects.filter(productopresentacions = oProuctoPresentacion.presentacion.id)
                jsonPrecios = []
                for OProductopresentacionsprecio in OProductopresentacionsprecios:
                    jsonPrecio = {}
                    jsonPrecio["id"] = OProductopresentacionsprecio.precio.id
                    jsonPrecio["nombrePrecio"] = OProductopresentacionsprecio.precio.nombre
                    jsonPrecio["precio"] = OProductopresentacionsprecio.valor
                    jsonPrecios.append(jsonPrecio)
                jsonPresentacion["valor"] =jsonPrecios
                jsonPresentaciones["presentaciones"].append(jsonPresentacion)
            print(jsonPresentaciones)
            return HttpResponse(json.dumps(jsonPresentaciones), content_type="application/json")

#<QueryDict: {u'imagen': [u''], u'url': [u''], u'1': [u'1'], u'3': [u'1'], u'2': [u'1'], u'nombre': [u'asd'], u'csrfmiddlewaretoken': [u'nsbA68zMnq7Ez6Gi2zEKqQQ45t5yWukYwqC9Tuo3Frl23Q9xajNt8htfhJQzWpP7'], u'codigo': [u''], u'cantidadPrincipal': [u'1']}>
#
#
@csrf_exempt
def CantidadPresentacionesProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idProducto = Datos["idProducto"]
            idPresentacion = Datos["idPresentacion"]
            jsonProducto = {}
            oProucto = Producto.objects.get(id = idProducto)
            oProductopresentacions = Productopresentacions.objects.get(producto = oProucto , presentacion = idPresentacion)
            oProductoalmacens = Producto_almacens.objects.filter(producto=oProucto).latest('pk')
            jsonProducto["cantidad"] = (oProductoalmacens.cantidad)*(oProductopresentacions.valor)
            print(jsonProducto)
            return HttpResponse(json.dumps(jsonProducto), content_type="application/json")

"""
def detalleProducto(request,producto_id):
    if request.method == 'GET':
        idProducto = int(producto_id)
        oProducto = Producto.objects.get(id = idProducto)
        form = ProductoForm(instance= oProducto)
        oProductospresentacions = Productopresentacions.objects.filter(producto = oProducto)
        oProductos = []

        for oProductospresentacion in oProductospresentacions:
            oProdu = {}
            oProdu["nombrePresentacions"] = oProductospresentacion.presentacion.nombre
            oProductos.append(oProdu)
            print(oProductos)
            return render(request, 'producto/detalle.html', {"form": form, "oPresentacion": oProducto.presentacions, "oProductos":oProductos})
    else:
        oPedi = Producto.objects.filter(estado = True)
        return render(request, 'producto/listar.html',{"oProductos": oPedi})
"""
@login_required
def detalleProducto(request,producto_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')

    oProducto = Producto.objects.get(pk=producto_id)
    oAlmacens = Producto_almacens.objects.filter(producto_id = producto_id).latest('id')
    return render(request, 'producto/detalle.html', {'oProducto':oProducto,'oAlmacens':oAlmacens,})

@login_required
def editarProducto(request,producto_id):
    if not validacionUsuario(request.user) in perfiles_correctos:
        return redirect('/error/')
    oProducto = Producto.objects.get(id = producto_id)
    if request.method=='POST':
        form = ProductoForm(request.POST, request.FILES, instance=oProducto)
        if form.is_valid():
            edit_prod=form.save(commit=False)
            form.save_m2m()
            edit_prod.status=True
            edit_prod.save()

            return redirect('/Producto/editar/'+producto_id+'/')
    else:
        forms= ProductoForm(instance=oProducto)
        oProductoPresentacions = Productopresentacions.objects.filter(producto_id=oProducto.id)
        productos = []
        presentaciones = []
        oPresentaciones = Presentacion.objects.all()
        Productopresentaciones = Productopresentacions.objects.filter(producto_id=oProducto.id,unidadprincipal=1).latest("id")
        nombrePresentacionPrincipal = Productopresentaciones.presentacion.nombre

        for oPresentacion in oPresentaciones:
            if oPresentacion.nombre != nombrePresentacionPrincipal:
                nuevoP={}
                nuevoP['id']=oPresentacion.id
                nuevoP['nombre']=oPresentacion.nombre
                presentaciones.append(nuevoP)

        precios = Precio.objects.filter(estado=True)
        for oProductoPresentacion in oProductoPresentacions:
            nuevo = {}
            nuevo['productoId'] = producto_id
            nuevo['presentacionId']=oProductoPresentacion.id
            nuevo['presentacion']=oProductoPresentacion.presentacion.nombre
            nuevo['valor']=int(round(1/oProductoPresentacion.valor,2))
            oProductoPresentacionsprecios = Productopresentacionsprecios.objects.filter(productopresentacions_id=oProductoPresentacion.id)
            cont = 1
            for oProductoPresentacionsprecio in oProductoPresentacionsprecios:
                c = oProductoPresentacionsprecio.valor
                valorPrecio = str(c).replace(",", ".")
                nuevo["precio"+str(cont)+"Id"]= oProductoPresentacionsprecio.id
                nuevo["precio"+str(cont)]= valorPrecio
                cont = cont + 1
            productos.append(nuevo)

        ctx = {'forms':forms, 'oProducto': oProducto,'productos':productos, 'presentaciones':presentaciones,'precios':precios,'productoId':producto_id,}


    return render(request, 'producto/editar.html',ctx)

def eliminar_identificador_producto(request):
    pk = request.POST.get('identificador_id')
    identificador = Producto.objects.get(pk=pk)
    identificador.estado = 0
    identificador.save()
    response = {}
    return JsonResponse(response)


"""
def actualizarProducto(request, producto_id):
    oProducto=Producto.objects.get(id=producto_id)
    if request.method=='POST':
        form= ProductoForm(request.POST, instance=oProducto)
        form.save()

    return

    """
