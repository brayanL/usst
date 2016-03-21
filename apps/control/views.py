import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages

from .forms import *
from .models import factor_riesgo, evaluacion_riesgo, peligro_evaluacion

# Create your views here.
def new_eval_riesgo(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                mfer = EvalRiesgoForm(request.POST)
                if mfer.is_valid():
                    er =mfer.save(commit=False)
                    er.usuario = request.user
                    er.save()
                    messages.info(request, "Se ha guardado con éxito el nuevo registro.")
                    return redirect("/eval_riesgo/")
                else:
                    messages.info(request, "Error al Guardar.")
                #num_filas = request.POST['num_filas']

        except Exception as error:
            print(error)
            transaction.rollback()
            messages.error(request, ("Comuniquese con Soporte técnico. "+ str(error)))
            return redirect('/eval_riesgo/')

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
