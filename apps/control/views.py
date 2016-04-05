import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .forms import *
from .models import FactorRiesgo, EvaluacionRiesgo, PeligroEvaluacion
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
                    # Para anular el guardado del ModelForm
                    er = mfer.save(commit=False)
                    usuario = User.objects.get(pk=request.user.id)
                    er.usuario = usuario

                    #Para asignar un valor a los radio button dependiendo de la opcion seleccionada
                    #Inicial = True, Periodica = False
                    if request.POST["rd_teval"] == "inicial":
                        er.evaluacion = True
                    else:
                        er.evaluacion = False
                    er.save()
                    eval_r = EvaluacionRiesgo.objects.get(pk=(EvaluacionRiesgo.objects.all().aggregate(Max('id'))).get('id__max'))

                    #Para Guardar los peligros
                    num_filas = int(request.POST["num_filas"])
                    for n in range(num_filas):
                        peli = PeligroDetalle.objects.get(pk=int(request.POST[('peli'+str(n+1))]))  # peligro identificado
                        pro = request.POST[('pro'+str(n+1))]  # Probabilidad
                        con = request.POST[('con'+str(n+1))]  # Consecuencia
                        eri = request.POST[('er'+str(n+1))]  # Estimacion de Riesgo
                        prio = request.POST[('prio'+str(n+1))]  # Estimacion de Riesgo
                        pe_ev = PeligroEvaluacion.objects.create(evaluacion=eval_r, peligro_det=peli,
                                                          probabilidad=pro, consecuencias=con,
                                                          estimacion=eri, priorizacion=prio, orden=(n+1))

                        # Si priorizacion esta en el rango del 1-3 pasar peligros a medidas de control
                        if prio == "1" or prio == "2" or prio == "3":
                            MedidaControl.objects.create(usuario=usuario, peligro_eval=pe_ev)

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
    evaluaciones = EvaluacionRiesgo.objects.all()
    return render(request, "list_eval_riesgo.html", {"evaluaciones": evaluaciones})

'''
    Para listar los peligros asociados a una evaluacion de riesgo especifica
'''
def view_edit_peligros_er(request, pk):
    peligros_eval = PeligroEvaluacion.objects.filter(evaluacion=pk)  # Para obtener todos los peligros asociados a una evaluacion
    er = EvaluacionRiesgo.objects.get(pk=pk)  # Para mostrar datos de la Evaluacion de Riesgos

    return render(request, "list_peligros_eval.html", {"peligros": peligros_eval, "id_er": pk, "er": er})


#Para obtener los colores
def carga_colores(request):
    if request.method == "GET" and request.is_ajax():
        c = colores()
        data = c.colores_tabla()
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

def carga_friesgos(request):
    if request.method == "GET" and request.is_ajax():
        friesgo = list(FactorRiesgo.objects.values('id', 'nombre'))
        return HttpResponse(json.dumps(friesgo), content_type='application/json')


def carga_peligros(request):
    if request.method == "GET" and request.is_ajax():
        factor_r = request.GET['id1']
        peligros = list(PeligroDetalle.objects.filter(factor_r=FactorRiesgo.objects.get(pk=factor_r)).values('id', 'nombre'))
        return HttpResponse(json.dumps(peligros), content_type='application/json')


# Determinar cuantas evaluaciones tienen medidas de control por realizar
def eval_pendientes(request):
    if request.method == "GET" and request.is_ajax():
        eval_r = PeligroEvaluacion.objects.filter(realizo_medida=False).values('evaluacion').distinct().count()
        return HttpResponse(json.dumps(eval_r), content_type='application/json')
