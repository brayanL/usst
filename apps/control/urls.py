from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^eval_riesgo/$', new_eval_riesgo, name='new_eval_riesgo'),
    url(r'^carga_friesgos/$', carga_friesgos, name='carga_friesgos'),
    url(r'^carga_peligros/$', carga_peligros, name='carga_peligros'),

    url(r'^list_evaluaciones/$', list_eval_riesgo, name="evaluciones"),
    url(r'^list_evaluaciones/edit/(?P<pk>\d+)/$', view_edit_peligros_er, name="edit_er"),

    url(r'^carga_colores/$', carga_colores, name="carga_colores"),

    url(r'^total_eval_pendientes/$', total_eval_pendientes, name="teval_pendientes"),

    url(r'^eval_pendientes/$', eval_pendientes, name="eval_pendientes"),

    url(r'^medida_control/(?P<pk>\d+)/$', new_medida_control, name="new_medida_control"),

    url(r'^peligros_mc/$', peligros_medida_control, name="peligros_mc")
]

