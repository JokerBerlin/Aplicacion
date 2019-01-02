# Generated by Django 2.1.1 on 2019-01-02 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_anulacionventa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='almacen',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='aperturacaja',
            name='activo',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='aperturacaja',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='cierrecaja',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='cobro',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='detalletipooperacion',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='precio',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='activo',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='tipooperacion',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='visita',
            name='activo',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='visita',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
