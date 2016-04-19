from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, TableStyle, Image, Spacer, Paragraph, BaseDocTemplate, PageTemplate
from reportlab.lib import colors
from reportlab.platypus import Table, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_LEFT
from reportlab.lib.pagesizes import A4, letter, A5, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import time

fechaSistema = time.strftime("%d/%m/%y")

def __encabezado_A4_Horizontal(canvas, doc):
    listPosLogo = [90,70]
    ####
    canvas.saveState()
    canvas.drawImage("apps/inicio/static/sb-admin/image/logoUtmach.jpg", 105, 515, 85, 65)
    canvas.setFont('Helvetica-Bold', 13)
    canvas.drawString(280, 550, "UNIVERSIDAD TECNICA DE MACHALA")

    canvas.setFont('Helvetica-Bold', 13)
    canvas.drawString(250, 530, "UNIDAD DE SEGURIDAD Y SALUD DEL TRABAJO")

    canvas.setFont('Times-Roman', 12)
    canvas.drawString(230, 495, "SISTEMA DE GESTION DE SEGURIDAD Y SALUD EN EL TRABAJO")

    canvas.setFont('Times-Roman', 12)
    canvas.drawString(160, 480, "MATRIZ DE INDENTIFICACION DE PELIGROS, EVALUCACION DE RIESGOS Y CONTROL")



    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(705, 550, "VERSION: 00")

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(675, 540, "CÓDIGO")

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(705, 530, "UTMACH-USST")

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(675, 520, "FECHA:")

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(705, 510, "%s"%fechaSistema)


    canvas.restoreState()



def generar_pdf(titulo, elementsFilaPage):
    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()
    doc = BaseDocTemplate(buff, pagesize=landscape(A4), title=titulo)
    doc.addPageTemplates([
            PageTemplate(id='cabecera', frames=Frame(inch/3, inch/3, 800, 560, id='normal', showBoundary=0),
                         onPage=__encabezado_A4_Horizontal),
        ]
        )
    story = []
    styles = getSampleStyleSheet()

    story.append(Spacer(0, 150))
    for i in elementsFilaPage:
         story.append(i)

    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response


def estiloTablas(t):
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))