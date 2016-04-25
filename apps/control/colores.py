"""
    Clase para poder establecer los colores para:
    1. Probabilidad
    2. Consecuencia
    3. Estimacion de Riesgo
"""
import json;

class colores:
    def colores_tabla(self):
        data = {"colores":
            [{"probabilidad":
                [
                    {"abr": "B", "nombre": "Baja", "color": "#ffbb99"},
                    {"abr": "M", "nombre": "Media", "color": "#ffff00"},
                    {"abr": "A", "nombre": "Alta", "color": "#ff3300"}]
            },
                {"consecuencia":
                    [
                        {"abr": "LD", "nombre": "Ligeramente Dañino", "color": "#ffbb99"},
                        {"abr": "D", "nombre": "Dañino", "color": "#ffff00"},
                        {"abr": "ED", "nombre": "Extremadamente Dañino", "color": "#ff3300"}
                    ]},
                {"estimacion":
                    [
                        {"abr": "T", "nombre": "Trivial", "color": "#ffff99"},
                        {"abr": "TO", "nombre": "Tolerable", "color": "#ffff00"},
                        {"abr": "M", "nombre": "Moderado", "color": "#ff6666"},
                        {"abr": "I", "nombre": "Importante", "color": "#c2c2d6"},
                        {"abr": "IN", "nombre": "Intolerable", "color": "#ff0000"}
                    ]}
            ]
        }
        return data

    def colores_tabla_matrices(self):
        probabilidad = [[[] for i in range(3)] for i in range(3)]
        consecuencia = [[[] for i in range(3)] for i in range(3)]
        estimacion = [[[] for i in range(3)] for i in range(5)]

        # Asignar los colores a probabilidad

        probabilidad[0][0]= 'B'
        probabilidad[0][1]= 'Baja'
        probabilidad[0][2]= '#ffbb99'

        probabilidad[1][0]= 'M'
        probabilidad[1][1]= 'Media'
        probabilidad[1][2]= '#ffff00'

        probabilidad[2][0]= 'A'
        probabilidad[2][1]= 'Alta'
        probabilidad[2][2]= '#ff3300'

        # Asignar los colores a consecuencia
        consecuencia[0][0]= 'LD'
        consecuencia[0][1]= 'Ligeramente Dañino'
        consecuencia[0][2]= '#ffbb99'

        consecuencia[1][0]= 'D'
        consecuencia[1][1]= 'Dañino'
        consecuencia[1][2]= '#ffff00'

        consecuencia[2][0]= 'ED'
        consecuencia[2][1]= 'Extremadamente Dañino'
        consecuencia[2][2]= '#ff3300'

        # Asignar los colores a estimacion

        estimacion[0][0]= 'T'
        estimacion[0][1]= 'Trivial'
        estimacion[0][2]= '#ffff99'

        estimacion[1][0]= 'TO'
        estimacion[1][1]= 'Tolerable'
        estimacion[1][2]= '#ffff00'

        estimacion[2][0]= 'M'
        estimacion[2][1]= 'Moderado'
        estimacion[2][2]= '#ff6666'

        estimacion[3][0]= 'I'
        estimacion[3][1]= 'Importante'
        estimacion[3][2]= '#c2c2d6'

        estimacion[4][0]= 'IN'
        estimacion[4][1]= 'Intolerable'
        estimacion[4][2]= '#ff0000'

        return probabilidad, consecuencia, estimacion


    def poner_colores(self, peligros_eval, estilo_table):
        color_probabilidad, color_consecuencia, color_estimacion = colores().colores_tabla_matrices()
        indice_colum_stimacion = 6
        indice_colum_probabilidad = 6
        indice_colum_consecuencia = 6
        for pe in peligros_eval:
            print(pe.estimacion)
            if pe.estimacion == 'T':
                estilo_table.add('BACKGROUND', (5, indice_colum_stimacion), (5, indice_colum_stimacion),
                                 color_estimacion[0][2])
            if pe.estimacion == 'TO':
                estilo_table.add('BACKGROUND', (5, indice_colum_stimacion), (5, indice_colum_stimacion),
                                 color_estimacion[1][2])
            if pe.estimacion == 'M':
                estilo_table.add('BACKGROUND', (5, indice_colum_stimacion), (5, indice_colum_stimacion),
                                 color_estimacion[2][2])
            if pe.estimacion == 'I':
                estilo_table.add('BACKGROUND', (5, indice_colum_stimacion), (5, indice_colum_stimacion),
                                 color_estimacion[3][2])
            if pe.estimacion == 'IN':
                estilo_table.add('BACKGROUND', (5, indice_colum_stimacion), (5, indice_colum_stimacion),
                                 color_estimacion[4][2])


            if pe.probabilidad == 'B':
                estilo_table.add('BACKGROUND', (3, indice_colum_probabilidad), (3, indice_colum_probabilidad),
                                 color_probabilidad[0][2])
            if pe.probabilidad == 'M':
                estilo_table.add('BACKGROUND', (3, indice_colum_probabilidad), (3, indice_colum_probabilidad),
                                 color_probabilidad[1][2])
            if pe.probabilidad == 'A':
                estilo_table.add('BACKGROUND', (3, indice_colum_probabilidad), (3, indice_colum_probabilidad),
                                 color_probabilidad[2][2])


            if pe.consecuencias == 'LD':
                estilo_table.add('BACKGROUND', (4, indice_colum_consecuencia), (4, indice_colum_consecuencia),
                                 color_consecuencia[0][2])
            if pe.consecuencias == 'D':
                estilo_table.add('BACKGROUND', (4, indice_colum_consecuencia), (4, indice_colum_consecuencia),
                                 color_consecuencia[1][2])
            if pe.consecuencias == 'ED':
                estilo_table.add('BACKGROUND', (4, indice_colum_consecuencia), (4, indice_colum_consecuencia),
                                 color_consecuencia[2][2])
            print('index_col_est',indice_colum_probabilidad)
            indice_colum_stimacion = indice_colum_stimacion+1
            indice_colum_probabilidad=indice_colum_probabilidad+1
            indice_colum_consecuencia = indice_colum_consecuencia+1
        return estilo_table


