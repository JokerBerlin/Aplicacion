# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-11-14 11:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedidoproductospresentacions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(blank=True, null=True)),
                ('cantidad', models.FloatField(blank=True, default=0)),
            ],
            options={
                'db_table': 'app_pedido_productos_presentacions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Productopresentacions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(default=1)),
                ('unidadprincipal', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'app_producto_presentacions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Productopresentacionsprecios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(blank=True, default=0)),
            ],
            options={
                'db_table': 'app_producto_presentacions_precios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rutaclientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificacion', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'app_ruta_clientes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aperturacaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cierrecaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.FloatField()),
                ('estado', models.BooleanField(default=True)),
                ('aperturacaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Aperturacaja')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, unique=True)),
                ('direccion', models.CharField(max_length=45)),
                ('longitud', models.CharField(blank=True, max_length=25, null=True)),
                ('latitud', models.CharField(blank=True, max_length=25, null=True)),
                ('numerodocumento', models.CharField(blank=True, max_length=11, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.FloatField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detalletipooperacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('imei', models.CharField(blank=True, max_length=45, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('perfil', models.IntegerField(blank=True, default=1, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('actividad', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cantidad_producto', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.FloatField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Caja')),
                ('cobro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cobro')),
                ('detalletipooperacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Detalletipooperacion')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('codigo', models.CharField(blank=True, max_length=45, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('codigo', models.CharField(blank=True, max_length=45, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('valor', models.FloatField(blank=True, default=1)),
                ('estado', models.BooleanField(default=True)),
                ('presentacions', models.ManyToManyField(to='app.Presentacion')),
            ],
        ),
        migrations.CreateModel(
            name='Producto_almacens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('cantidadinicial', models.FloatField()),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Almacen')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Lote')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Producto_categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Categoria')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('direccion', models.CharField(max_length=45)),
                ('documento', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('estado', models.BooleanField(default=True)),
                ('clientes', models.ManyToManyField(to='app.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Tipooperacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.FloatField()),
                ('nrecibo', models.CharField(blank=True, max_length=45, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificacion', models.DateTimeField(auto_now=True)),
                ('nivel', models.IntegerField(blank=True, default=1, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('estado', models.BooleanField(default=True)),
                ('clientes', models.ManyToManyField(to='app.Cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Empleado')),
                ('rutacliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Rutaclientes')),
            ],
        ),
        migrations.AddField(
            model_name='movimiento',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pedido'),
        ),
        migrations.AddField(
            model_name='lote',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Proveedor'),
        ),
        migrations.AddField(
            model_name='lote',
            name='recibo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Recibo'),
        ),
        migrations.AddField(
            model_name='detalletipooperacion',
            name='tipooperacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Tipooperacion'),
        ),
        migrations.AddField(
            model_name='cobro',
            name='recibo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Recibo'),
        ),
        migrations.AddField(
            model_name='cobro',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Venta'),
        ),
        migrations.AddField(
            model_name='aperturacaja',
            name='caja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Caja'),
        ),
    ]
