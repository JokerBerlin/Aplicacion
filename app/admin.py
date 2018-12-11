# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Producto)
admin.site.register(Empleado)
admin.site.register(Almacen)
admin.site.register(Caja)
admin.site.register(Precio)
admin.site.register(Presentacion)
admin.site.register(Serie)
admin.site.register(Tipooperacion)
admin.site.register(Detalletipooperacion)
admin.site.register(Recibo)