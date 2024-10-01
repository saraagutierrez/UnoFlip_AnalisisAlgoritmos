import random
from Carta import Carta

class Mazo:
    def __init__(self):
        self.cartas = self.crear_mazo()  # Inicializa el mazo

    def crear_mazo(self):
        colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
        valores_luminosos = ['Wild', 'Wild Draw Two', 'Draw One', 'Flip', 'Reverse', 'Skip']
        valores_oscuros = ['Wild', 'Wild Draw Color', 'Draw Five', 'Flip', 'Reverse', 'Skip Everyone']

        mazo = []

        # Crear cartas luminosas
        for color in colores:
            for valor in valores_luminosos:
                mazo.append(Carta(color, valor, es_accion=True, lado="luminoso"))
        
        # Crear cartas oscuras
        for color in colores:
            for valor in valores_oscuros:
                mazo.append(Carta(color, valor, es_accion=True, lado="oscuro"))

        return mazo

    def sacar_carta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            return None  # En caso de que el mazo esté vacío
