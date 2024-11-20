import random
import itertools
from Carta import Carta

class Mazo:
    def __init__(self):
        self.cartas = self.crear_mazo()

    def crear_mazo(self):
        colores_luminosos = ['Rojo', 'Verde', 'Azul', 'Amarillo']
        valores_luminosos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Draw Two', 'Flip', 'Reverse', 'Skip']
        valores_wild_luminosos = ['Wild', 'Wild Draw Four']

        colores_oscuros = ['Rosado', 'Naranja', 'Morado', 'Turquesa']
        valores_oscuros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Draw Five', 'Flip', 'Reverse', 'Skip Everyone']
        valores_wild_oscuros = ['Wild', 'Wild Draw Color']

        mazo = []

        # Crear cartas luminosas con colores
        for color_lum, valor_lum in itertools.product(colores_luminosos, valores_luminosos):
            for color_osc, valor_osc in itertools.product(colores_oscuros, valores_oscuros):
                mazo.append(Carta(color_lum, color_osc, valor_lum, valor_osc))

        # Crear cartas Wild luminosas
        for valor_wild_lum in valores_wild_luminosos:
            for valor_wild_osc in valores_wild_oscuros:
                mazo.append(Carta(None, None, valor_wild_lum, valor_wild_osc))  # Sin colores para cartas Wild

        # Barajar el mazo
        random.shuffle(mazo)
        return mazo

    def sacar_carta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            print("El mazo está vacío.")
            return None
