from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^eval_riesgo/$', new_eval_riesgo, name='new_eval_riesgo'),
    url(r'^carga_friesgos/$', carga_friesgos, name='carga_friesgos'),
    url(r'^carga_peligros/$', carga_peligros, name='carga_peligros'),

    url(r'^list_evaluaciones/(?P<op>\w)/$', list_eval_riesgo, name="list_evaluciones"),
    url(r'^list_evaluaciones/det/(?P<pk>\d+)/$', det_eval_riesgo, name="det_eval_riesgo"),

    url(r'^carga_colores/$', carga_colores, name="carga_colores"),

    url(r'^total_eval_pendientes/$', total_eval_pendientes, name="teval_pendientes"),

    url(r'^eval_pendientes/$', eval_pendientes, name="eval_pendientes"),

    url(r'^medida_control/(?P<pk>\d+)/$', new_medida_control, name="new_medida_control"),

    url(r'^peligros_mc/$', peligros_medida_control, name="peligros_mc"),

    url(r'^total_medidas_pendientes/$', total_medidas_pendientes, name="tmed_pendientes"),

    url(r'^medidas_pendientes/$', medidas_pendientes, name="medidas_pendientes"),

    url(r'^nuevo_plan_accion/(?P<pk>\d+)/$', new_plan_accion, name="new_plan_accion"),

    url(r'^peligros_pa/$', peligros_plan_accion, name="peligros_pa"),

    # Para Peligros
    url(r'^peligros/$', peligros, name="peligros"),
    url(r'^peligros/nuevo/$', new_peligro, name="new_peligro"),
    url(r'^peligros/edit/(?P<pk>\d+)/$', edit_peligro, name="edit_peligro"),

    #Usuarios
    url(r'^perfil_usuario/$', perfil_usuario, name="perfil_usuario"),
    url(r'^perfil/modal/$', load_modal, name="mpassword"),
    url(r'^perfil/change_password/$', change_password, name="cpassword"),

]

