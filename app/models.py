# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Almacen(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Caja(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Aperturacaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=False)
    monto = models.FloatField()
    activo = models.BooleanField(blank=True,default=True)
    estado = models.BooleanField(blank=True,default=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)

class Anulacionventa(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=False)
    descripcion = models.TextField(blank=True, null=True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)

class Cierrecaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    aperturacaja = models.ForeignKey(Aperturacaja, on_delete=models.CASCADE)  # Field name made lowercase.

class Precio(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=45,unique=True)
    direccion = models.CharField(max_length=45)
    longitud = models.CharField(max_length=25, blank=True, null=True)
    latitud = models.CharField(max_length=25, blank=True, null=True)
    numerodocumento = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)
    precio = models.ForeignKey(Precio, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % self.nombre

class Cobro(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)  # Field name made lowercase.
    recibo = models.ForeignKey('Recibo', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

class Detalletipooperacion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    tipooperacion = models.ForeignKey('Tipooperacion', on_delete=models.CASCADE)  # Field name made lowercase.
    def __str__(self):
        return '%s' % self.nombre

class Empleado(models.Model):
    PERFIL_EMP = (
        (1, 'Administrador'),
        (2,'Pedido'),
        (3,'Almacen'),
        (4,'Ventas'),
        (5,'Repartidor'),
    )
    nombre = models.CharField(max_length=45)
    imei = models.CharField(max_length=45, blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True)#upload_to='%Y/%m/%d',
    perfil = models.IntegerField(blank=True, null=True,default=2, choices=PERFIL_EMP)
    estado = models.BooleanField(blank=True,default=True)
    almacen = models.ForeignKey('Almacen', default=1, on_delete=models.CASCADE)
    caja = models.ForeignKey(Caja,null=True, on_delete=models.PROTECT)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Empleado: %s con usuario: %s' % (self.nombre, self.usuario.username)

class Lote(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    fechavencimiento = models.DateField(auto_now=False, auto_now_add=False,null=True)
    modificado = models.DateTimeField(auto_now=True, blank=True)
    estado = models.BooleanField(blank=True,default=True)
    nrecibo = models.CharField(max_length=45, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)  # Field name made lowercase.
    recibo = models.ForeignKey('Recibo', on_delete=models.CASCADE)  # Field name made lowercase.



class Operacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)  # Field name made lowercase.
    detalletipooperacion = models.ForeignKey(Detalletipooperacion, on_delete=models.CASCADE)  # Field name made lowercase.
    cobro = models.ForeignKey('Cobro', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    estado = models.IntegerField(default=1)
    tipo = models.IntegerField(default=1)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)  # Field name made lowercase.
    cliente = models.ForeignKey('Cliente', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    def __str__(self):
        return 'Pedido hecho por cliente %s' % self.cliente

class Movimiento(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad_producto = models.FloatField(default=0.0)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)

class Presentacion(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    imagen = models.ImageField(upload_to='', blank=True, null=True)#upload_to='%Y/%m/%d',
    url = models.CharField(max_length=100, blank=True, null=True)
    valor = models.FloatField(default=1,blank=True)
    estado = models.BooleanField(blank=True,default=True)
    presentacions = models.ManyToManyField(Presentacion)
    def __str__(self):
        return '%s' % self.nombre

class Productopresentacions(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    valor = models.FloatField(default=1)
    unidadprincipal = models.BooleanField(default=False,blank=True)
    precios = models.ManyToManyField(Precio)
    class Meta:
        managed = False
        db_table = 'app_producto_presentacions'
    def __str__(self):
        return '%s %s' % (self.producto, self.presentacion)

class Producto_almacens(models.Model):
    cantidad = models.FloatField()
    cantidadinicial = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Field name made lowercase.
    precioCompra = models.FloatField(null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # Field name made lowercase.
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)  # Field name made lowercase.

class Producto_categorias(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Field name made lowercase.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Field name made lowercase.

class Pedidoproductospresentacions(models.Model):
    valor                 = models.FloatField(blank=True, null=True)
    cantidad              = models.FloatField(blank=True,default=0)
    pedido                = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Field name made lowercase.
    productopresentacions = models.ForeignKey('Productopresentacions', on_delete=models.PROTECT)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'app_pedido_productos_presentacions'
    def __str__(self):
        return '%s' % self.pedido

class Productopresentacionsprecios(models.Model):
    precio                = models.ForeignKey(Precio, on_delete=models.CASCADE)  # Field name made lowercase.
    productopresentacions = models.ForeignKey('Productopresentacions', on_delete=models.CASCADE)  # Field name made lowercase.
    valor                 = models.FloatField(blank=True,default=0)
    class Meta:
        managed = False
        db_table = 'app_producto_presentacions_precios'

class Proveedor(models.Model):
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    documento = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Recibo(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Serie(models.Model):
    numeroSerie = models.CharField(max_length=3)
    recibo = models.ForeignKey('Recibo', blank=True, null=True, on_delete=models.PROTECT)
    def __str__(self):
        return 'Numero de serie: %s' % self.numeroSerie

class Ruta(models.Model):
    nombre   = models.CharField(max_length=45)
    fecha    = models.DateTimeField(auto_now_add=True, blank=True)
    activo   = models.BooleanField(blank=True,default=True)
    estado   = models.BooleanField(blank=True,default=True)
    clientes = models.ManyToManyField(Cliente)
    repartidor = models.OneToOneField(Empleado, on_delete=models.CASCADE)


class Rutaclientes(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    ruta         = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    cliente      = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    activo       = models.BooleanField(blank=True,default=True)
    estado       = models.BooleanField(blank=True,default=True)

    class Meta:
        managed = False
        db_table = 'app_ruta_clientes'

class Tipooperacion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return '%s' % self.nombre

class Tipoventa(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)


class Venta(models.Model):
    fecha   = models.DateTimeField(auto_now_add=True, blank=True)
    monto   = models.FloatField()
    nrecibo = models.CharField(max_length=45, blank=True, null=True)
    estado  = models.BooleanField(blank=True,default=True)
    pedido  = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    tipoventa = models.ManyToManyField(Tipoventa)


class Visita(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    rutacliente  = models.ForeignKey(Rutaclientes, on_delete=models.CASCADE)
    empleado     = models.ForeignKey('Empleado', on_delete=models.CASCADE)  # Field name made lowercase.
    nivel        = models.IntegerField(blank=True,null=True,default=1)
    activo       = models.BooleanField(blank=True,default=True)
    estado       = models.BooleanField(blank=True,default=True)
    clientes     = models.ManyToManyField(Cliente)

class Error(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    actividad  = models.CharField(max_length=20)

