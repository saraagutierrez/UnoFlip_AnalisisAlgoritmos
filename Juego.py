from JugadorSintetico import JugadorSintetico
from Mazo import Mazo
from Jugador import Jugador
import random

class UnoFlip:
    colores_luminosos = ['Rojo', 'Verde', 'Azul', 'Amarillo']
    colores_oscuros = ['Rosado', 'Naranja', 'Morado', 'Turquesa']

    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.pila_descartes = []
        self.estado_actual = "luminoso"  # El estado inicial del juego
        print(f"Estado inicial: {self.estado_actual}")
        self.turno_actual = 0
        self.mazo = Mazo()
        self.primera_carta = True  # Indicador para la primera carta
        self.iniciar_juego()

    def asignar_color_por_estado(self, estado):
        if estado == 'luminoso':
            return self.colores_luminosos
        else:
            return self.colores_oscuros
        
    @staticmethod
    def es_jugada_valida(carta_jugada, carta_actual, estado_actual):
        return (
            carta_jugada.color == carta_actual.color or
            carta_jugada.valor == carta_actual.valor or
            carta_jugada.valor in ['Wild', 'Wild Draw'] or
            carta_jugada.valor == 'Flip'
        )

    def iniciar_juego(self):
        # Iniciar todas las cartas con el estado 'luminoso' inicialmente
        for carta in self.mazo.cartas:
            carta.lado = "luminoso"  # Asegurar que todas las cartas empiecen luminosas
            # Asignamos un color aleatorio para cada carta
            carta.color = random.choice(self.colores_luminosos)  # Asigna un color aleatorio luminoso

        # Repartir 7 cartas a cada jugador
        for _ in range(7):
            for jugador in self.jugadores:
                jugador.agregar_carta(self.mazo.sacar_carta())

        # Sacar la primera carta para la pila de descarte
        carta_inicial = self.mazo.sacar_carta()
        while carta_inicial and carta_inicial.valor in ['Wild', 'Wild Draw Four', 'Reverse', 'Skip', 'Flip']:
            # Si la carta inicial es especial, descartarla y sacar otra
            print(f"Se descarta una carta especial: {carta_inicial}")
            carta_inicial = self.mazo.sacar_carta()

        # Asegurarse de que la carta inicial sea válida
        if carta_inicial:
            carta_inicial.lado = "luminoso"
            # Asignamos el color adecuado según el estado luminoso
            carta_inicial.color = random.choice(self.colores_luminosos)  # Asigna un color aleatorio luminoso
            self.pila_descartes.append(carta_inicial)
            print(f"Carta inicial: {carta_inicial}")

        self.ajustar_cartas()  # Ajustar cartas al estado actual

    def ajustar_cartas(self):
        # Ajustar todas las cartas en manos de los jugadores según el estado
        for jugador in self.jugadores:
            for carta in jugador.cartas:
                carta.lado = self.estado_actual
                # Asignar un color aleatorio luminoso a cada carta de la mano del jugador
                colores = self.asignar_color_por_estado(self.estado_actual)
                carta.color = random.choice(colores)  # Asigna un color aleatorio de los disponibles

        # Ajustar las cartas en la pila de descartes
        for carta in self.pila_descartes:
            carta.lado = self.estado_actual
            colores = self.asignar_color_por_estado(self.estado_actual)
            carta.color = random.choice(colores)  # Asigna un color aleatorio de los disponibles

    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]
        carta_actual = self.pila_descartes[-1]

        if isinstance(jugador, JugadorSintetico):
            carta_jugada = jugador.jugar_turno(carta_actual, self.estado_actual, self.mazo)
        else:
            carta_jugada = self.manejar_turno_humano(jugador, carta_actual)

        if carta_jugada:
            if self.primera_carta and carta_jugada.valor not in ['Wild', 'Wild Draw Four', 'Reverse', 'Skip', 'Flip']:
                self.pila_descartes.append(carta_jugada)
                print(f"{jugador.nombre} juega: {carta_jugada}")
                self.procesar_carta_especial(carta_jugada, jugador)
                self.primera_carta = False  # Después de jugar la primera carta, ya no es necesario validar más
            elif not self.primera_carta and self.es_jugada_valida(carta_jugada, carta_actual, self.estado_actual):
                self.pila_descartes.append(carta_jugada)
                print(f"\n{jugador.nombre} juega: {carta_jugada}")
                self.procesar_carta_especial(carta_jugada, jugador)
                if len(jugador.cartas) == 1:
                    print(f"¡UNO! {jugador.nombre} tiene solo una carta.")
            else:
                print(f"{jugador.nombre} no puede jugar {carta_jugada}.")
                jugador.agregar_carta(carta_jugada)

        if not jugador.cartas:
            print(f"{jugador.nombre} ha ganado el juego!")
            return True
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        return False

    def manejar_turno_humano(self, jugador, carta_actual):
        print(f"\nTurno de {jugador.nombre}. Carta actual: {carta_actual}")
        for i, carta in enumerate(jugador.cartas):
            print(f"{i}: {carta}")
        
        while True:
            try:
                opcion = int(input("\nSelecciona una carta (-1 para robar): "))
                if opcion == -1:
                    # Si el jugador elige robar, se le reparte una carta
                    carta_robada = self.mazo.sacar_carta()
                    if carta_robada:
                        carta_robada.estado = self.estado_actual
                        jugador.agregar_carta(carta_robada)
                        print(f"Robaste: {carta_robada}")
                    return None
                elif 0 <= opcion < len(jugador.cartas):
                    carta_jugada = jugador.jugar_carta(opcion)
                    if self.es_jugada_valida(carta_jugada, carta_actual, self.estado_actual):
                        return carta_jugada
                    else:
                        print(f"Error: La carta {carta_jugada} no es válida. Intenta de nuevo.")
                else:
                    print("Opción inválida. Intenta de nuevo.")
            except ValueError:
                print("Opción inválida. Intenta de nuevo.")


    def procesar_carta_especial(self, carta_jugada, jugador_actual):
        if carta_jugada.valor == "Flip":
            # Cambiar el estado del juego
            self.estado_actual = 'oscuro' if self.estado_actual == 'luminoso' else 'luminoso'
            print(f"El estado del juego cambia a: {self.estado_actual}")

            # Ajustar el estado de todas las cartas
            self.ajustar_cartas()

        elif carta_jugada.valor == "Skip":
            print(f"El siguiente jugador es saltado.")
            # Salta al siguiente jugador
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Reverse":
            print(f"Cambio de sentido.")
            # Invierte el orden de turnos
            self.jugadores.reverse()
            self.turno_actual = len(self.jugadores) - self.turno_actual - 1

        elif carta_jugada.valor == "Draw Two":
            print(f"El siguiente jugador debe robar 2 cartas.")
            # El siguiente jugador roba dos cartas
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            for _ in range(2):
                siguiente_jugador.agregar_carta(self.mazo.sacar_carta())
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Draw Five":
            print(f"El siguiente jugador debe robar 5 cartas.")
            # El siguiente jugador roba cinco cartas
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            for _ in range(5):
                siguiente_jugador.agregar_carta(self.mazo.sacar_carta())
            self.turno_actual = (self.turno_actual + 5) % len(self.jugadores)

        elif carta_jugada.valor == "Wild":
            # Cambiar color
            nuevo_color = input("Elige un nuevo color: ")
            carta_jugada.color = nuevo_color

        elif carta_jugada.valor == "Wild Draw Four":
            # Cambiar color y el siguiente jugador roba 4 cartas
            nuevo_color = input("Elige un nuevo color: ")
            carta_jugada.color = nuevo_color
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            for _ in range(4):
                siguiente_jugador.agregar_carta(self.mazo.sacar_carta())

        elif carta_jugada.valor == "Wild Draw Color":
            # Cambiar color y el siguiente jugador roba cartas hasta que salga una carta del color elegido
            nuevo_color = input("Elige un nuevo color: ")
            carta_jugada.color = nuevo_color
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            print(f"El siguiente jugador debe robar cartas hasta que salga una carta de color {nuevo_color}.")
            
            # Robar cartas hasta que salga una carta del color seleccionado
            carta_robo = None
            while carta_robo is None or carta_robo.color != nuevo_color:
                carta_robo = self.mazo.sacar_carta()
                if carta_robo:
                    siguiente_jugador.agregar_carta(carta_robo)
                    print(f"{siguiente_jugador.nombre} roba una carta: {carta_robo}")
            
            # El turno del jugador actual es el que sigue después del robo
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Skip Everyone":
            # Salta a todos los jugadores y le vuelve a tocar al mismo jugador
            print(f"Todos los jugadores son saltados. {self.jugadores[self.turno_actual].nombre} vuelve a jugar.")
            
            # El turno vuelve al mismo jugador que jugó la carta
            self.turno_actual = self.turno_actual  # No cambia el turno, es el mismo jugador quien repite el turno
    def fin_del_juego(self):
        for jugador in self.jugadores:
            if not jugador.cartas:
                print(f"{jugador.nombre} ha ganado el juego!")
                return True
        return False