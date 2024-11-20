from collections import Counter
from Jugador import Jugador

class JugadorSintetico(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)

    def elegir_carta(self, carta_actual, estado_actual):
        # Filtrar cartas compatibles por color, valor o si son Wild
        compatibles = [
            carta for carta in self.cartas
            if carta.color == carta_actual.color or carta.valor == carta_actual.valor or carta.valor in ["Wild", "Wild Draw Four"]
        ]

        if not compatibles:
            # Si no hay cartas compatibles, devuelve None (no puede jugar)
            return None

        # Priorizar cartas Wild si están disponibles
        wild_cards = [carta for carta in compatibles if carta.valor in ["Wild", "Wild Draw Four"]]
        if wild_cards:
            return wild_cards[0]  # Jugar la primera Wild disponible

        # Luego, buscar cartas de acción especiales (Draw Two, Reverse, Skip)
        especiales = [carta for carta in compatibles if carta.es_accion]
        if especiales:
            return especiales[0]  # Jugar la primera carta especial disponible

        # Por último, jugar la primera carta compatible numérica
        return compatibles[0]

    def elegir_color_wild(self, estado_juego):
        # Colores posibles según el estado del juego
        colores_posibles = {
            "luminoso": ['Rojo', 'Verde', 'Azul', 'Amarillo'],
            "oscuro": ['Rosado', 'Naranja', 'Morado', 'Turquesa']
        }

        # Obtener los colores compatibles con el estado actual
        esquema_colores = colores_posibles.get(estado_juego, colores_posibles["luminoso"])

        # Contar los colores de las cartas en mano, excluyendo Wild y ajustando al esquema actual
        colores = [carta.color for carta in self.cartas if carta.color in esquema_colores]

        if colores:
            # Contar la frecuencia de los colores en la mano
            contador_colores = Counter(colores)
            # Elegir el color más frecuente
            color_mas_frecuente = contador_colores.most_common(1)[0][0]
            return color_mas_frecuente
        else:
            # Si no hay colores en mano, elegir el primer color del esquema como predeterminado
            return esquema_colores[0]


    def jugar_turno(self, carta_actual, estado_actual, mazo):
        print(f"\nTurno del jugador sintético: {self.nombre}")
        print(f"Cartas en mano: {', '.join(str(carta) for carta in self.cartas)}")
        print(f"Carta en la pila de descarte: {carta_actual}")

        # Intentar jugar una carta
        carta_elegida = self.elegir_carta(carta_actual, estado_actual)

        if carta_elegida:
            # Si la carta es Wild, se selecciona un color una vez
            if carta_elegida.valor in ["Wild", "Wild Draw Four", "Wild Draw Color"]:
                color_elegido = self.elegir_color_wild(estado_actual)  # Selección de color
                carta_elegida.color = color_elegido  # Asignar el color a la carta Wild
                print(f"{self.nombre} juega una carta Wild. El color del juego ahora es: {color_elegido}")
                
            # Eliminar la carta elegida de la mano
            self.cartas.remove(carta_elegida)
            return carta_elegida
        else:
            # Si no tiene carta para jugar, roba una carta
            nueva_carta = mazo.sacar_carta()
            if nueva_carta:
                self.agregar_carta(nueva_carta)
                print(f"{self.nombre} no tiene cartas para jugar. Roba una carta: {nueva_carta}")
            return None

