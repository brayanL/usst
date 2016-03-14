from django.contrib import admin
from .models import *


admin.site.register(evaluacion_riesgo)
admin.site.register(puesto_trabajo)
admin.site.register(peligros)
admin.site.register(peligro_detalle)
admin.site.register(peligro_evaluacion)
admin.site.register(medida_control)
admin.site.register(plan_accion)


