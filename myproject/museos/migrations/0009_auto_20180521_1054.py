# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0008_auto_20180519_1926'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='museolike',
            unique_together=set([('museo', 'usuario')]),
        ),
    ]
