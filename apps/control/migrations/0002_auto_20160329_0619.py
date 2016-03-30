# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='peligro_evaluacion',
            unique_together=set([('evaluacion', 'peligro_det')]),
        ),
    ]
