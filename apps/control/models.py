from django.db import models
from django.contrib.auth.models import User


class FactorRiesgo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        db_table = 'factor_riesgo'

    def __str__(self):
        return "%s" % (self.nombre)


class PeligroDetalle(models.Model):
    nombre = models.CharField(max_length=100)
    factor_r = models.ForeignKey(FactorRiesgo)

    class Meta:
        db_table = 'peligro_detalle'

    def __str__(self):
        return "%s,%s" % (self.nombre, self.factor_r)


class EvaluacionRiesgo(models.Model):
    localizacion = models.CharField(max_length=200)
    puesto = models.CharField(max_length=200)
    trabajadores = models.IntegerField()
    fecha_eval = models.DateField()
    fecha_ul_eval = models.DateField(null=True)
    usuario = models.ForeignKey(User)
    evaluacion = models.BooleanField()

    class Meta:
        db_table = 'evaluacion_riesgo'

    def __str__(self):
        return "%s,%s" % (self.pk, self.localizacion)

'''
Una evaluacion de riesgo no puede tener dos peligros iguales, por tal razon
evaluacion y peligro_det seran una llave compuesta
'''
class PeligroEvaluacion(models.Model):
    evaluacion = models.ForeignKey(EvaluacionRiesgo)
    peligro_det = models.ForeignKey(PeligroDetalle)
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
    realizo_medida = models.BooleanField(default=False)
    realizo_plan = models.BooleanField(default=False)

    class Meta:
        db_table = 'peligro_evaluacion'
        unique_together = ('evaluacion', 'peligro_det')



class MedidaControl(models.Model):
    usuario = models.ForeignKey(User)
    peligro_eval = models.ForeignKey(PeligroEvaluacion)
    medida_control = models.CharField(max_length=100, null=True)
    procedimiento = models.CharField(max_length=100, null=True)
    informacion = models.CharField(max_length=100, null=True)
    formacion = models.CharField(max_length=100, null=True)
    riesgo_controlado = models.NullBooleanField(null=True)

    class Meta:
        db_table = 'medida_control'

class PlanAccion(models.Model):
    usuario = models.ForeignKey(User)
    peligro_eval = models.ForeignKey(PeligroEvaluacion)
    accion = models.CharField(max_length=100, null=True)
    responsable = models.CharField(max_length=50, null=True)
    fecha_finalizacion = models.DateField(null=True)
    fecha_firma = models.DateField(null=True)
    realizado_por = models.CharField(max_length=100, null=True)
    next_evaluacion = models.DateField(null=True)

    class Meta:
        db_table = 'plan_accion'
