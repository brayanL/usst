from django.shortcuts import render
from django.http import HttpResponse
import json
from .forms import *

from .models import factor_riesgo

# Create your views here.
def new_eval_riesgo(request):
    form = EvalRiesgoForm()
    return render(request, "new_eval_riesgo.html", {"collapse_er": "in", "active_n": "active", "form": form})

def carga_friesgos(request):
    if request.method == "GET" and request.is_ajax():
        friesgo = list(factor_riesgo.objects.values('id', 'nombre'))
        #print(friesgo)
        return HttpResponse(json.dumps(friesgo), content_type='application/json')

def carga_peligros(request):
    if request.method == "GET" and request.is_ajax():
        peligroR = request.GET['id1']
        print(peligroR)
        fpeligro = list(peligro_detalle.objects.filter(peligro=factor_riesgo.objects.get(pk=peligroR)).values('id', 'nombre'))
        print(fpeligro)
        return HttpResponse(json.dumps(fpeligro), content_type='application/json')
