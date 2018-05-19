# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0007_auto_20180516_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='color_fondo_css',
            field=models.CharField(max_length=32, default='rgb(242, 245, 254)'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='tam_letra_css',
            field=models.IntegerField(default=11),
        ),
    ]
