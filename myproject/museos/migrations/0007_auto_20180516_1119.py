# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0006_auto_20180516_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='MuseoLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='usuario_museo',
        ),
        migrations.AddField(
            model_name='museolike',
            name='usuario',
            field=models.ForeignKey(to='museos.Usuario'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='likes',
            field=models.ManyToManyField(to='museos.Museo', blank=True, through='museos.MuseoLike'),
        ),
    ]
