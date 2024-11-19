import random
from Carta import Carta

class Mazo:
    def __init__(self):
        self.cartas = self.crear_mazo()

    def crear_mazo(self):
        # Colores y valores definidos para las cartas luminosas y oscuras
        colores_luminosos = ['Rojo', 'Verde', 'Azul', 'Amarillo']
        valores_luminosos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Wild', 'Wild Draw Four', 'Draw Two', 'Flip', 'Reverse', 'Skip']

        colores_oscuros = ['Rosado', 'Naranja', 'Morado', 'Turquesa']
        valores_oscuros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Wild', 'Wild Draw Color', 'Draw Five', 'Flip', 'Reverse', 'Skip Everyone']

        mazo = []

        # Crear cartas luminosas
        for color in colores_luminosos:
            for valor in valores_luminosos:
                mazo.append(Carta(color, valor, es_accion=True, lado="luminoso"))

        # Crear cartas oscuras
        for color in colores_oscuros:
            for valor in valores_oscuros:
                mazo.append(Carta(color, valor, es_accion=True, lado="oscuro"))

        return mazo

    def sacar_carta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            print("El mazo está vacío.")
            return None