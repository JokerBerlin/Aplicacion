# Generated by Django 2.1.1 on 2019-01-30 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20190130_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoventa',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
