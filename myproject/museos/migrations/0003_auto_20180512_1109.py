# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0002_museo_n_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='contraseña',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.AddField(
            model_name='usuario',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='pagina',
            field=models.CharField(max_length=64, default='Pagina de usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usuario_museo',
            field=models.ManyToManyField(to='museos.Museo', blank=True),
        ),
    ]
