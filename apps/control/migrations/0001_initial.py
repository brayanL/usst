# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='evaluacion_riesgo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('localizacion', models.CharField(max_length=100)),
                ('trabajadores', models.IntegerField()),
                ('fecha_eval', models.DateField()),
                ('fecha_ul_eval', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='factor_riesgo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='medida_control',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('medida_control', models.CharField(max_length=100)),
                ('procedimiento', models.CharField(max_length=100)),
                ('informacion', models.CharField(max_length=100)),
                ('formacion', models.CharField(max_length=100)),
                ('riesgo_controlado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='peligro_detalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=100)),
                ('peligro', models.ForeignKey(to='control.factor_riesgo')),
            ],
        ),
        migrations.CreateModel(
            name='peligro_evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('probabilidad', models.CharField(max_length=1, choices=[('B', 'Baja'), ('M', 'Mediana'), ('A', 'Alta')])),
                ('consecuencias', models.CharField(max_length=2, choices=[('LD', 'Ligeramente Dañino'), ('D', 'Dañino'), ('ED', 'Extremandamente Dañino')])),
                ('estimacion', models.CharField(max_length=2)),
                ('evaluacion', models.ForeignKey(to='control.evaluacion_riesgo')),
                ('peligro_det', models.ForeignKey(to='control.peligro_detalle')),
            ],
        ),
        migrations.CreateModel(
            name='plan_accion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('accion', models.CharField(max_length=100)),
                ('responsable', models.CharField(max_length=50)),
                ('finalizacion', models.DateField()),
                ('peligro_eval', models.ForeignKey(to='control.peligro_evaluacion')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='puesto_trabajo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='medida_control',
            name='peligro_eval',
            field=models.ForeignKey(to='control.peligro_evaluacion'),
        ),
        migrations.AddField(
            model_name='medida_control',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluacion_riesgo',
            name='puesto',
            field=models.ForeignKey(to='control.puesto_trabajo'),
        ),
        migrations.AddField(
            model_name='evaluacion_riesgo',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
