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
