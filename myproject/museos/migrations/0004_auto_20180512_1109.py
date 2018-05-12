# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180512_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
