# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peligroevaluacion',
            name='realizo_medida',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='peligroevaluacion',
            name='realizo_plan',
            field=models.NullBooleanField(),
        ),
    ]
