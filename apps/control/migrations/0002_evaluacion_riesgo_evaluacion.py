# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion_riesgo',
            name='evaluacion',
            field=models.BooleanField(default=False),
        ),
    ]
