from django.db import models
from django.contrib.auth.models import User


class factor_riesgo(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.nombre)


class peligro_detalle(models.Model):
    nombre = models.CharField(max_length=100)
    factor_r = models.ForeignKey(factor_riesgo)

    def __str__(self):
        return "%s,%s" % (self.nombre, self.factor_r)


class evaluacion_riesgo(models.Model):
    localizacion = models.CharField(max_length=200)
    puesto = models.CharField(max_length=200)
    trabajadores = models.IntegerField()
    fecha_eval = models.DateField()
    fecha_ul_eval = models.DateField(null=True)
    usuario = models.ForeignKey(User)
    evaluacion = models.BooleanField()

'''
Una evaluacion de riesgo no puede tener dos peligros iguales, por tal razon
evaluacion y peligro_det seran una llave compuesta
'''
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
    priorizacion = models.CharField(max_length=3)  # Para indicar el nivel de riesgo
    orden = models.IntegerField()  # Para llevar un orden seguimiento

    class Meta:
        unique_together = ('evaluacion', 'peligro_det')


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
    fecha_finalizacion = models.DateField()
    fecha_firma = models.DateField()
    realizado_por = models.CharField(max_length=100)
    next_evaluacion = models.DateField()
