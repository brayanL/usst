from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Image, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, A5, landscape
from reportlab.platypus import Table, PageBreak
from apps.reportPadre import generar_pdf, estiloTablas
from .models import *
from django.http import HttpResponse, HttpResponseNotFound
from .colores import *


#+['']*(18-len(allPlan))
def reporteEvaluacionRiesgo(request, pk_evaluacion):
    er = EvaluacionRiesgo.objects.get(pk=pk_evaluacion)
    peligros_eval = PeligroEvaluacion.objects.filter(evaluacion=er)
    story = []
    list_peligros_eval_for_table = [(pe.orden, pe.peligro_det.factor_r.nombre, pe.peligro_det.nombre,
                      pe.probabilidad, pe.consecuencias, pe.estimacion, pe.priorizacion)for pe in peligros_eval]

    inicial = ' '
    periodica = ' '
    if er.evaluacion:
        inicial = '*'
    else:
        periodica = '*'

    estilo_table = TableStyle([
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(3,2)),
        ('SPAN',(4,1),(6,1)),
        ('SPAN',(4,2),(6,2)),
        ('SPAN',(0,3),(3,3)),
        ('SPAN',(0,4),(3,4)),

        ('SPAN',(4,3),(6,3)),
        ('SPAN',(4,4),(6,4)),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    estilo_table=colores().poner_colores(peligros_eval, estilo_table)

    table = Table([
        ['Evaluación General de Riesgos'],
        ['Localización %s'%er.localizacion,'','','','Evaluación','',''],
        ['','','','','Inicial [ %s ]            Periodica [ %s ]'%(inicial, periodica), '',''],
        ['Puestos de Trabajo: %s'%er.puesto,'','','','Fecha Evaluación: %s'%er.fecha_eval,'',''],
        ['N° Trabajadores: %s'%er.trabajadores,'','','','Fecha Ultima Evaluación: %s'%er.fecha_ul_eval,'',''],
        ['N°','Factor Riesgo','Peligro Identificado','Probabilidad','Consecuencia','Estimazión Riesgo','Priorización']
    ]+list_peligros_eval_for_table
        , colWidths=[40, 140, 200, 90, 90, 110, 110, 110]
        , rowHeights=16, style = estilo_table)
    table.setStyle([

    ])
    story.append(table)
    return reporteMedidaControl(story,  peligros_eval)


def reporteMedidaControl(story, list_peligros_eval):
    styles = getSampleStyleSheet()
    list_med_control_priori = []
    print('lista peligros eval: ', list_peligros_eval)
    for pe in list_peligros_eval:
        print('peligro individual: ', pe)
        if int(pe.priorizacion) == 1 or int(pe.priorizacion) == 2 or int(pe.priorizacion) == 3:
            print('Agregar a lista los q tienen priorizacion entre 1 y 3, si hay reporte')
            list_med_control_priori.append(pe.rmedida_control.get(peligro_eval=pe.id))
        else:
            print('Prioridad entre 4 y 5, no hay reporte')
    print('Fin for')
    print(list_med_control_priori.__len__())
    if list_med_control_priori.__len__()>0:
        story.append(PageBreak())

        story.append(Spacer(0, 140))
        list_med_control_for_table = [(mc.peligro_eval.orden, mc.peligro_eval.peligro_det.nombre, mc.medida_control,
                          mc.procedimiento, mc.informacion, mc.formacion, '*' if mc.riesgo_controlado else '',
                          '*' if not mc.riesgo_controlado else '') for mc in list_med_control_priori]

        table = Table([
                          ['Peligro N°', 'Peligro','Medida Control',
                           'Procedimiento Trabajo','Información','Formación',
                           '¿Riesgo Controlado?'],
                          ['', '','','','','','Si','No']
        ]+list_med_control_for_table, colWidths=[50, 145, 130, 181, 100, 100, 47, 47], rowHeights=16)
        table.setStyle([
            ('SPAN',(0,0),(0,1)),
            ('SPAN',(1,0),(1,1)),
            ('SPAN',(2,0),(2,1)),
            ('SPAN',(3,0),(3,1)),
            ('SPAN',(4,0),(4,1)),
            ('SPAN',(5,0),(5,1)),
            ('SPAN',(6,0),(7,0)),
            #('SPAN',(0,1),(-1,1)),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            #('FONTSIZE', (56, 1), (0, 1), 12),
            ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
            #('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
            #('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            #('GRID', (0, 3), (-1, 3), 1, colors.black),
            #('BACKGROUND', (1, 1), (1, -1), colors.dodgerblue)
        ])
        story.append(table)
        return reportePlanAccion(story, list_med_control_priori)
    else:
        story.append(Paragraph("No hay reporte de medida de control", styles['Normal']))
        return generar_pdf('EL TITULOX', story)


def reportePlanAccion(story, list_med_control):
    styles = getSampleStyleSheet()
    list_plan_accion = []
    for mc in list_med_control:
        if not mc.riesgo_controlado:
            print('Agregar los q no tienen riesgo controlado, Si hay reporte')
            list_plan_accion.append(mc.peligro_eval.rplan_accion.get(peligro_eval=mc.peligro_eval.id))
        else:
            print('Si hay riesgo controlado, No hay reporte')
    print('Fin for 2222')
    print(list_plan_accion.__len__())
    if list_plan_accion.__len__()>0:
        story.append(PageBreak())
        story.append(Spacer(0, 140))
        list_plan_for_table = [(p.peligro_eval.orden,
                    p.accion,
                    p.responsable,
                    p.fecha_finalizacion, p.fecha_firma) for p in list_plan_accion]

        table = Table([
            ['Plan de Acción'],
                          [' Peligro', 'Accion requerida', 'Responsable', 'Fecha finalización','Comprobacion'
                                                        'Eficacia de la acción   (Firma y Fecha)'],
        ]+list_plan_for_table, colWidths=[40, 205, 205, 85, 265], rowHeights=16)
        table.setStyle([
            ('SPAN',(0,0),(-1,0)),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            #('FONTSIZE', (56, 1), (0, 1), 12),
            ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
            #('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
            #('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            #('GRID', (0, 3), (-1, 3), 1, colors.black),
            #('BACKGROUND', (1, 1), (1, -1), colors.dodgerblue)
        ])
        story.append(table)

        table_footer= Table([
            ['Elaborado por: %s'%list_plan_accion.__getitem__(0).usuario.first_name+' '+
                list_plan_accion.__getitem__(0).usuario.last_name,'','','','Firma:'],
            ['Plan de acción realizado por: %s'%list_plan_accion.__getitem__(0).realizado_por,'','','','Firma:'],
            ['','','','',''],
            ['Fecha proxima de evaluación: %s'%list_plan_accion.__getitem__(0).next_evaluacion]
        ],colWidths=[95,160,120,160,265])
        table_footer.setStyle([
            ('SPAN',(0,0),(3,0)),
            ('SPAN',(0,1),(3,1)),
            ('SPAN',(0,3),(4,3)),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            #('FONTSIZE', (56, 1), (0, 1), 12),
            ('FONT', (0, 0), (-1, -1), 'Times-Bold'),
            #('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
            #('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            #('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            #('GRID', (0, 3), (-1, 3), 1, colors.black),
            #('BACKGROUND', (1, 1), (1, -1), colors.dodgerblue)
        ])
        story.append(table_footer)
    else:
        story.append(Paragraph("No hay reporte de Plan de acion", styles['Normal']))
    return generar_pdf('EL TITULOX', story)

