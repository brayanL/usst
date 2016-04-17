from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Image, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, A5, landscape
from reportlab.platypus import Table
from apps.reportPadre import generar_pdf, estiloTablas
from .models import *


#+['']*(18-len(allPlan))
def reportePrueba(reqyest):
        styles = getSampleStyleSheet()
        story = []

        story.append(Spacer(0, 140))
        allPlan = [(0,
                    p.accion,
                    p.responsable,
                    p.fecha_finalizacion, p.fecha_firma) for p in PlanAccion.objects.all()]

        table = Table([
            ['Plan de Acción'],
                          [' Peligro', 'Accion requerida', 'Responsable', 'Fecha finalización','Comprobacion'
                                                        'Eficacia de la acción   (Firma y Fecha)'],
        ]+allPlan, colWidths=[40, 205, 205, 85, 265], rowHeights=16)
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
            ['Elaborado por:','','','','Firma:'],
            ['Plan de acción realizado por:','','','','Firma:'],
            ['','','','',''],
            ['Fecha proxima de evaluación:']
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

        return generar_pdf('EL TITULOX', story)
