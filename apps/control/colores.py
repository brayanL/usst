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
        #probabilidad = [['M'], ['Media'], ['#ffff99']]
