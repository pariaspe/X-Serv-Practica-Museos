# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_auto_20180512_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='accesibilidad',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='barrio',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='museo',
            name='direccion',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='distrito',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='museo',
            name='telefono',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='museo',
            name='url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
    ]
