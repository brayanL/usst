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
            name='EvaluacionRiesgo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('localizacion', models.CharField(max_length=200)),
                ('puesto', models.CharField(max_length=200)),
                ('trabajadores', models.IntegerField()),
                ('fecha_eval', models.DateField()),
                ('fecha_ul_eval', models.DateField(null=True)),
                ('evaluacion', models.BooleanField()),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'evaluacion_riesgo',
            },
        ),
        migrations.CreateModel(
            name='FactorRiesgo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'factor_riesgo',
            },
        ),
        migrations.CreateModel(
            name='MedidaControl',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('medida_control', models.CharField(null=True, max_length=100)),
                ('procedimiento', models.CharField(null=True, max_length=100)),
                ('informacion', models.CharField(null=True, max_length=100)),
                ('formacion', models.CharField(null=True, max_length=100)),
                ('riesgo_controlado', models.NullBooleanField()),
            ],
            options={
                'db_table': 'medida_control',
            },
        ),
        migrations.CreateModel(
            name='PeligroDetalle',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('factor_r', models.ForeignKey(to='control.FactorRiesgo')),
            ],
            options={
                'db_table': 'peligro_detalle',
            },
        ),
        migrations.CreateModel(
            name='PeligroEvaluacion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('probabilidad', models.CharField(choices=[('B', 'Baja'), ('M', 'Mediana'), ('A', 'Alta')], max_length=1)),
                ('consecuencias', models.CharField(choices=[('LD', 'Ligeramente Dañino'), ('D', 'Dañino'), ('ED', 'Extremandamente Dañino')], max_length=2)),
                ('estimacion', models.CharField(max_length=2)),
                ('priorizacion', models.CharField(max_length=3)),
                ('orden', models.IntegerField()),
                ('realizo_medida', models.BooleanField(default=False)),
                ('realizo_plan', models.BooleanField(default=False)),
                ('evaluacion', models.ForeignKey(to='control.EvaluacionRiesgo')),
                ('peligro_det', models.ForeignKey(to='control.PeligroDetalle')),
            ],
            options={
                'db_table': 'peligro_evaluacion',
            },
        ),
        migrations.CreateModel(
            name='PlanAccion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(null=True, max_length=100)),
                ('responsable', models.CharField(null=True, max_length=50)),
                ('fecha_finalizacion', models.DateField(null=True)),
                ('fecha_firma', models.DateField(null=True)),
                ('realizado_por', models.CharField(null=True, max_length=100)),
                ('next_evaluacion', models.DateField(null=True)),
                ('peligro_eval', models.ForeignKey(to='control.PeligroEvaluacion')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'plan_accion',
            },
        ),
        migrations.AddField(
            model_name='medidacontrol',
            name='peligro_eval',
            field=models.ForeignKey(to='control.PeligroEvaluacion'),
        ),
        migrations.AddField(
            model_name='medidacontrol',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='peligroevaluacion',
            unique_together=set([('evaluacion', 'peligro_det')]),
        ),
    ]
