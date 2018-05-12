# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='n_id',
            field=models.IntegerField(unique=True, default=0),
            preserve_default=False,
        ),
    ]
