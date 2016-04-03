import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .forms import *
from .models import factor_riesgo, evaluacion_riesgo, peligro_evaluacion
from .colores import *

# Create your views here.
'''
    1. Hacer con formularios normales a Evaluacion de Riesgo
    2. Hacer el Guardado con Ajax en caso de problema la pagina no se recargue
        y los datos queden en la tabla y en los inputs
'''

@login_required
def new_eval_riesgo(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                mfer = EvalRiesgoForm(request.POST)
                if request.POST["fecha_ul_eval"] == "":
                    del mfer.fields["fecha_ul_eval"]
                if mfer.is_valid():
                    #Para anular el guardado del ModelForm
                    er = mfer.save(commit=False)
                    er.usuario = User.objects.get(pk=request.user.id)

                    #Para asignar un valor a los radio button dependiendo de la opcion seleccionada
                    #Inicial = True, Periodica = False
                    if request.POST["rd_teval"] == "inicial":
                        er.evaluacion = True
                    else:
                        er.evaluacion = False
                    er.save()
                    eval_r = evaluacion_riesgo.objects.get(pk=(evaluacion_riesgo.objects.all().aggregate(Max('id'))).get('id__max'))

                    #Para Guardar los peligros
                    num_filas = int(request.POST["num_filas"])
                    for n in range(num_filas):
                        peli = peligro_detalle.objects.get(pk=int(request.POST[('peli'+str(n+1))]))  # peligro identificado
                        pro = request.POST[('pro'+str(n+1))]  # Probabilidad
                        con = request.POST[('con'+str(n+1))]  # Consecuencia
                        eri = request.POST[('er'+str(n+1))]  # Estimacion de Riesgo
                        prio = request.POST[('prio'+str(n+1))]  # Estimacion de Riesgo
                        peligro_evaluacion.objects.create(evaluacion=eval_r, peligro_det=peli,
                                                          probabilidad=pro, consecuencias=con,
                                                          estimacion=eri, priorizacion=prio, orden=(n+1))

                    messages.info(request, "Se ha guardado con éxito el nuevo registro.")
                    return redirect("/eval_riesgo/")
                else:
                    messages.info(request, "Ingrese Datos Correctos.")
        except Exception as error:
            transaction.rollback()
            messages.error(request, "Error en la transaccion: " + str(error))
            print("Error: ", str(error))
            #return redirect('/eval_riesgo/')
            #return render(request.POST, "new_eval_riesgo.html")
    form = EvalRiesgoForm()
    return render(request, "new_eval_riesgo.html", {"collapse_er": "in", "active_n": "active", "form": form})


def list_eval_riesgo(request):
    evaluaciones = evaluacion_riesgo.objects.all()
    return render(request, "list_eval_riesgo.html", {"evaluaciones": evaluaciones})

'''
    Para listar los peligros asociados a una evaluacion de riesgo especifica
'''
def view_edit_er(request, pk):
    peligros_eval = peligro_evaluacion.objects.filter(evaluacion=pk)  # Para obtener todos los peligros asociados a una evaluacion
    er = evaluacion_riesgo.objects.get(pk=pk)  # Para mostrar datos de la Evaluacion de Riesgos
    c = colores()
    prob, con, est = c.colores_tabla()
    return render(request, "list_peligros_eval.html", {"peligros": peligros_eval, "id_er": pk, "er": er,
                                                       "prob": prob, "con": con, "est": est})


def carga_friesgos(request):
    if request.method == "GET" and request.is_ajax():
        friesgo = list(factor_riesgo.objects.values('id', 'nombre'))
        #print(friesgo)
        return HttpResponse(json.dumps(friesgo), content_type='application/json')


def carga_peligros(request):
    if request.method == "GET" and request.is_ajax():
        factor_r = request.GET['id1']
        peligros = list(peligro_detalle.objects.filter(factor_r=factor_riesgo.objects.get(pk=factor_r)).values('id', 'nombre'))
        return HttpResponse(json.dumps(peligros), content_type='application/json')
