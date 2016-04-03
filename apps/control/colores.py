'''
    Clase para poder establecer los colores para:
    1. Probabilidad
    2. Consecuencia
    3. Estimacion de Riesgo
'''
class colores:
    def colores_tabla(self):
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

