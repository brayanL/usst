# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_evaluacion_riesgo_evaluacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion_riesgo',
            name='localizacion',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='evaluacion_riesgo',
            name='puesto',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='puesto_trabajo',
        ),
    ]
