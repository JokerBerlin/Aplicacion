# Generated by Django 2.1.1 on 2019-01-23 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190117_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='nrecibo',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='lote',
            name='precioCompra',
            field=models.FloatField(null=True),
        ),
    ]
