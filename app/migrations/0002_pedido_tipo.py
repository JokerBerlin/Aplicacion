# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-11-30 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='tipo',
            field=models.BooleanField(default=False),
        ),
    ]
