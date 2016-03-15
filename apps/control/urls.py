from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^eval_riesgo/$', new_eval_riesgo, name='new_eval_riesgo'),
]

