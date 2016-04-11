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

                        if prio == "1" or prio == "2" or prio == "3":
                            pe_ev = PeligroEvaluacion.objects.create(evaluacion=eval_r, peligro_det=peli,
                                                              probabilidad=pro, consecuencias=con,
                                                              estimacion=eri, priorizacion=prio, orden=(n+1), realizo_medida=False)
                            # Si priorizacion esta en el rango del 1-3 pasar peligros a medidas de control
                            MedidaControl.objects.create(usuario=usuario, peligro_eval=pe_ev)
                        else:
                            pe_ev = PeligroEvaluacion.objects.create(evaluacion=eval_r, peligro_det=peli,
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
    return render(request, "evaluaciones/new_eval_riesgo.html", {"collapse_er": "in", "active_n": "active", "form": form})


# todo -> con el simbolo - en order by los registros son ordenados de manera descendente
def list_eval_riesgo(request, op):
    if request.method == "GET":
        if op == "t":
            evaluaciones = EvaluacionRiesgo.objects.all().order_by('-id')
            print(evaluaciones)
            return render(request, "evaluaciones/list_eval_riesgo.html", {"evaluaciones": evaluaciones, "selec": "T"})
        if op == "m":
            evaluaciones = []
            ev = PeligroEvaluacion.objects.filter(realizo_medida=True).values('evaluacion').distinct()
            list_ev = [e['evaluacion'] for e in ev]
            for e in list_ev:
                evaluaciones.append(EvaluacionRiesgo.objects.get(pk=e))
            return render(request, "evaluaciones/list_eval_riesgo.html", {"evaluaciones": evaluaciones, "selec": "M"})
        if op == "p":
            evaluaciones = []
            ev = PeligroEvaluacion.objects.filter(realizo_plan=True).values('evaluacion').distinct()
            list_ev = [e['evaluacion'] for e in ev]
            for e in list_ev:
                evaluaciones.append(EvaluacionRiesgo.objects.get(pk=e))
            return render(request, "evaluaciones/list_eval_riesgo.html", {"evaluaciones": evaluaciones, "selec": "P"})

'''
    Para listar los peligros asociados a una evaluacion de riesgo especifica
'''
def view_edit_peligros_er(request, pk):
    peligros_eval = PeligroEvaluacion.objects.filter(evaluacion=pk)  # Para obtener todos los peligros asociados a una evaluacion
    er = EvaluacionRiesgo.objects.get(pk=pk)  # Para mostrar datos de la Evaluacion de Riesgos

    return render(request, "evaluaciones/list_peligros_eval.html", {"peligros": peligros_eval, "id_er": pk, "er": er})


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
def total_eval_pendientes(request):
    if request.method == "GET" and request.is_ajax():
        eval_r = PeligroEvaluacion.objects.filter(realizo_medida=False).values('evaluacion').distinct().count()
        return HttpResponse(json.dumps(eval_r), content_type='application/json')

def eval_pendientes(request):
    #id de evaluaciones pendientes
    # Obtengo todos los peligros de una evaluacion especifica
    #peligros = EvaluacionRiesgo.objects.get(pk=id_ev).peligroevaluacion_set.all()
    evaluacion = []
    ev_id = PeligroEvaluacion.objects.filter(realizo_medida=False).values('evaluacion').distinct()

    list_ev = [ev['evaluacion'] for ev in ev_id]

    for eva in list_ev:
        evaluacion.append(EvaluacionRiesgo.objects.get(pk=eva))

    #ev_pen = PeligroEvaluacion.objects.filter(realizo_medida=False).distinct()
    return render(request, "evaluaciones/list_eval_pendientes.html", {"evaluaciones": evaluacion})


def new_medida_control(request, pk):
    if request.method == "POST":
        try:
            with transaction.atomic():
                num = int(request.POST['num_filas'])
                usuario = User.objects.get(pk=request.user.id)
                for i in range(num):
                    pe = request.POST['id_pe'+str(i)]
                    pe = PeligroEvaluacion.objects.get(pk=pe)
                    mc = request.POST['mc'+str(i)]
                    proc = request.POST['proc'+str(i)]
                    inf = request.POST['inf'+str(i)]
                    forma = request.POST['forma'+str(i)]
                    rc = request.POST['rc'+str(i)]
                    if rc == "S":
                        rc = True
                    else:
                        rc = False

                    # Actualiza Medida de Control para un peligro en especifico
                    MedidaControl.objects.filter(peligro_eval=pe).update(
                        usuario=usuario, medida_control=mc, procedimiento=proc, informacion=inf,
                        formacion=forma, riesgo_controlado=rc)

                    # Actualiza el estado del peligro en PeligroEvaluacion
                    PeligroEvaluacion.objects.filter(pk=pe.id).update(realizo_medida=True)

                    # Si el riesgo no es controlado pasa a la Plan de Accion
                    if rc is not True:
                        PlanAccion.objects.create(usuario=usuario, peligro_eval=pe)
                        PeligroEvaluacion.objects.filter(pk=pe.id).update(realizo_plan=False)

                messages.info(request, "Se ha guardado con éxito el nuevo registro.")
                return redirect("/eval_pendientes/")
        except Exception as error:
            transaction.rollback()
            messages.error(request, "Error en la transaccion: " + str(error))
            print("Error: ", str(error))
    er = EvaluacionRiesgo.objects.get(pk=pk)
    return render(request, "medidas/new_medida_control.html", {"er": er})


# todo - Para cargar los peligros que no se han realizado medidas de control para una evaluacion de riesgo especifica
def peligros_medida_control(request):
    if request.method == "GET" and request.is_ajax():
        id_er = request.GET['id_er']
        peligros = list(PeligroEvaluacion.objects.filter(realizo_medida=False, evaluacion=id_er).values(
            'id','orden', 'peligro_det__nombre', 'peligro_det__factor_r__nombre'))
        return HttpResponse(json.dumps(peligros), content_type='application/json')


# todo - Determinar cuantas evaluaciones tienen planes de accion por realizar
def total_medidas_pendientes(request):
    if request.method == "GET" and request.is_ajax():
        eval_r = PeligroEvaluacion.objects.filter(realizo_plan=False).values('evaluacion').distinct().count()
        return HttpResponse(json.dumps(eval_r), content_type='application/json')


# todo - para poder listar las evaluaciones de riesgo que tienen planes de accion por realizar
def medidas_pendientes(request):
    evaluacion = []
    ev_id = PeligroEvaluacion.objects.filter(realizo_plan=False).values('evaluacion').distinct()

    list_ev = [ev['evaluacion'] for ev in ev_id]

    for eva in list_ev:
        evaluacion.append(EvaluacionRiesgo.objects.get(pk=eva))
    return render(request, "medidas/list_medida_control.html", {"evaluaciones": evaluacion})


def new_plan_accion(request, pk):
    er = EvaluacionRiesgo.objects.get(pk=pk)
    return render(request, "medidas/new_plan_accion.html", {"er": er})


def peligros_plan_accion(request):
    if request.method == "GET" and request.is_ajax():
        id_er = request.GET['id_er']
        peligros = list(PeligroEvaluacion.objects.filter(realizo_plan=False, evaluacion=id_er).values(
            'id','orden', 'peligro_det__nombre', 'peligro_det__factor_r__nombre'))
        return HttpResponse(json.dumps(peligros), content_type='application/json')