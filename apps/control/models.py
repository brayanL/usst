from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class puesto_trabajo(models.Model):
    nombre = models.CharField(max_length=30)

class peligros(models.Model):
    nombre = models.CharField(max_length=30)

class evaluacion_riesgo(models.Model):
    localizacion = models.CharField(max_length=50)
    puestos = models.IntegerField()
    trabajadores = models.IntegerField()
    fecha_eval = models.DateField(auto_now=True)
    fecha_ul_eval = models.DateField()
    puesto = models.ForeignKey(puesto_trabajo)
    usuario = models.ForeignKey(User)

class peligro_detalle(models.Model):
    nombre = models.CharField(max_length=100)
    peligro = models.ForeignKey(peligros)

class peligro_evaluacion(models.Model):
    evaluacion = models.ForeignKey(evaluacion_riesgo)
    peligro_det = models.ForeignKey(peligro_detalle)
    TIPOS_PROB = (
        ('B', 'Baja'),
        ('M', 'Mediana'),
        ('A', 'Alta')
    )
    probabilidad = models.CharField(choices=TIPOS_PROB, max_length=1)
    TIPOS_CONSEC = (
        ('LD', 'Ligeramente Dañino'),
        ('D', 'Dañino'),
        ('ED', 'Extremandamente Dañino')
    )
    consecuencias = models.CharField(choices=TIPOS_CONSEC, max_length=2)
    estimacion = models.CharField(max_length=2)

class medida_control(models.Model):
    usuario = models.ForeignKey(User)
    peligro_eval = models.ForeignKey(peligro_evaluacion)
    medida_control = models.CharField(max_length=100)
    procedimiento = models.CharField(max_length=100)
    informacion = models.CharField(max_length=100)
    formacion = models.CharField(max_length=100)
    riesgo_controlado = models.BooleanField()

class plan_accion(models.Model):
    usuario = models.ForeignKey(User)
    peligro_eval = models.ForeignKey(peligro_evaluacion)
    accion = models.CharField(max_length=100)
    responsable = models.CharField(max_length=50)
    finalizacion = models.DateField()