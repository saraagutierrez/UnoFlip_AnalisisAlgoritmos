from collections import Counter
from Jugador import Jugador

class JugadorSintetico(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)

    def elegir_carta(self, carta_actual, estado_actual):
        # Filtrar cartas compatibles
        compatibles = [
            carta for carta in self.cartas
            if carta.color == carta_actual.color or carta.valor == carta_actual.valor or carta.valor == "Wild"
        ]
        
        # Priorizar cartas especiales
        especiales = [carta for carta in compatibles if carta.es_accion]

        # Seleccionar la carta a jugar
        if especiales:
            return especiales[0]  # Priorizar la primera carta especial disponible
        elif compatibles:
            return compatibles[0]  # Jugar la primera carta compatible
        else:
            return None  # No hay carta para jugar

    def elegir_color_wild(self):
        # Contar cuántas veces aparece cada color en las cartas del jugador
        colores = [carta.color for carta in self.cartas if carta.color != 'Wild']
        if colores:
            contador_colores = Counter(colores)
            # Seleccionar el color más frecuente
            color_mas_frecuente = contador_colores.most_common(1)[0][0]
            return color_mas_frecuente
        else:
            # Si no hay cartas de color (todos son Wild), elige uno al azar
            return 'Rojo'  # Elegir un color predeterminado en caso de que no haya colores normales

    def jugar_turno(self, carta_actual, estado_actual, mazo):
        print(f"\nTurno del jugador sintético: {self.nombre}")
        print(f"Cartas en mano: {', '.join(str(carta) for carta in self.cartas)}")
        print(f"Carta en la pila de descarte: {carta_actual}")

        # Intentar jugar una carta
        carta_elegida = self.elegir_carta(carta_actual, estado_actual)

        if carta_elegida:
            # Si la carta es Wild, elige un color automáticamente basado en las cartas del jugador
            if carta_elegida.valor in ["Wild", "Wild Draw Color", "Wild Draw Two"]:
                print(f"{self.nombre} juega una carta Wild. Seleccionando un color...")
                color_elegido = self.elegir_color_wild()
                carta_actual.color = color_elegido
                print(f"El color del juego ahora es: {color_elegido}")
                
            self.cartas.remove(carta_elegida)  # Remover la carta elegida de la mano
            return carta_elegida
        else:
            # Robar una carta si no tiene jugada posible
            nueva_carta = mazo.sacar_carta()
            if nueva_carta:
                self.agregar_carta(nueva_carta)
                print(f"{self.nombre} no tiene cartas para jugar. Roba una carta: {nueva_carta}")
            return None
