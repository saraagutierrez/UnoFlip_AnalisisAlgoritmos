from JugadorSintetico import JugadorSintetico
from Mazo import Mazo
from Jugador import Jugador
import random

class UnoFlip:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.mazo = Mazo()
        self.pila_descartes = []
        self.estado_actual = "luminoso"  # Estado inicial
        self.turno_actual = 0
        self.iniciar_juego()

    def iniciar_juego(self):
        for _ in range(7):
            for jugador in self.jugadores:
                jugador.agregar_carta(self.mazo.sacar_carta())
        
        # Sacar la primera carta para la pila de descarte
        carta_inicial = self.mazo.sacar_carta()
        while carta_inicial and carta_inicial.valorLuminoso in ['Wild', 'Wild Draw Four', 'Draw Two', 'Reverse', 'Skip', 'Flip']:
            # Si la carta inicial es especial, descartarla y sacar otra
            print(f"Se descarta una carta especial: {carta_inicial}")
            carta_inicial = self.mazo.sacar_carta()

        # Asegurarse de que la carta inicial sea válida
        if carta_inicial:
            carta_inicial.lado = "luminoso"  # Iniciar en el lado luminoso
            print(f"Carta inicial: {carta_inicial}")
            self.pila_descartes.append(carta_inicial)

    @staticmethod
    def es_jugada_valida(carta_jugada, carta_actual, estado_actual):
        if carta_jugada.valorLuminoso in ['Wild', 'Wild Draw'] or carta_jugada.valorOscuro in ['Wild', 'Wild Draw']:
            # Las cartas Wild siempre son válidas, independientemente del color
            return True

        if estado_actual == "luminoso":
            return (
                carta_jugada.colorLuminoso == carta_actual.colorLuminoso or
                carta_jugada.valorLuminoso == carta_actual.valorLuminoso or
                carta_jugada.valorLuminoso == 'Flip'
            )
        else:  # estado_actual == "oscuro"
            return (
                carta_jugada.colorOscuro == carta_actual.colorOscuro or
                carta_jugada.valorOscuro == carta_actual.valorOscuro or
                carta_jugada.valorOscuro == 'Flip'
            )

    def ajustar_cartas(self):
        # Ajustar las cartas en manos de los jugadores
        for jugador in self.jugadores:
            for carta in jugador.cartas:
                carta.lado = self.estado_actual  # Cambiar el lado según el estado actual

        # Ajustar las cartas en la pila de descartes
        for carta in self.pila_descartes:
            carta.lado = self.estado_actual  # Cambiar el lado según el estado actual

    def manejar_color_wild(self, jugador):
        # Pedir al jugador que elija un color
        colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
        print(f"Elige un color: {', '.join(colores)}")
        color_elegido = input("Introduce el color: ")
        while color_elegido not in colores:
            print("Color inválido. Intenta de nuevo.")
            color_elegido = input("Introduce el color: ")
        
        return color_elegido


    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]

        carta_actual = self.pila_descartes[-1]  # La carta actual es la última en la pila de descartes

        # Determinar si es un jugador sintético o humano
        if isinstance(jugador, JugadorSintetico):
            carta_jugada = jugador.jugar_turno(carta_actual, self.estado_actual, self.mazo)
            if carta_jugada is None:
                # Si no puede jugar, pasar el turno al siguiente jugador
                self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        else:
            carta_jugada = self.manejar_turno_humano(jugador, carta_actual)

        # Procesar la carta jugada
        if carta_jugada:
            if self.es_jugada_valida(carta_jugada, carta_actual, self.estado_actual):
                # La carta es válida; añadirla a la pila de descartes
                self.pila_descartes.append(carta_jugada)
                print(f"\n{jugador.nombre} juega: {carta_jugada}")

                # Procesar efectos de cartas especiales
                self.procesar_carta_especial(carta_jugada, jugador)
                self.ajustar_cartas()

                # Verificar si el jugador está en estado de UNO
                if len(jugador.cartas) == 1:
                    print(f"¡UNO! {jugador.nombre} tiene solo una carta.")
            else:
                # La carta no es válida, el jugador debe devolverla a su mano
                print(f"{jugador.nombre} no puede jugar {carta_jugada}.")
                jugador.agregar_carta(carta_jugada)
        else:
            # Salta al siguiente jugador
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        # Verificar si el jugador ha ganado
        if not jugador.cartas:
            print(f"{jugador.nombre} ha ganado el juego!")
            return True

        return False
    
    def manejar_turno_humano(self, jugador, carta_actual):
        print(f"\nTurno de {jugador.nombre}. Carta actual: {carta_actual}")

        # Mostrar las cartas del jugador según el estado actual del juego (luminoso u oscuro)
        for i, carta in enumerate(jugador.cartas):
            print(f"{i}: {carta}")

        while True:
            try:
                # Solicitar al jugador seleccionar una carta o robar
                opcion = int(input("\nSelecciona una carta (-1 para robar): "))

                if opcion == -1:
                    # Si el jugador elige robar, se le reparte una carta
                    carta_robada = self.mazo.sacar_carta()
                    if carta_robada:
                        carta_robada.lado = self.estado_actual  # Establecer el lado correcto de la carta robada
                        print(f"Robaste: {carta_robada}")
                        jugador.agregar_carta(carta_robada)
                        # Pasar el turno al siguiente jugador
                        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
                    return None  # No se jugó ninguna carta

                elif 0 <= opcion < len(jugador.cartas):
                    # Verificar si la carta seleccionada es válida
                    carta_jugada = jugador.jugar_carta(opcion)
                    if self.es_jugada_valida(carta_jugada, carta_actual, self.estado_actual):
                        # Si la carta es válida, devolverla
                        return carta_jugada
                    else:
                        print(f"Error: La carta {carta_jugada} no es válida. Intenta de nuevo.")
                else:
                    print("Opción inválida. Intenta de nuevo.")
            except ValueError:
                print("Opción inválida. Intenta de nuevo.")

    def procesar_carta_especial(self, carta_jugada, jugador_actual):
        if carta_jugada.valor == "Flip":
            if carta_jugada.valorLuminoso == "Flip":
                # Cambiar el estado del juego (luminoso/oscuro)
                self.estado_actual = "oscuro" if self.estado_actual == "luminoso" else "luminoso"
                for c in self.pila_descartes + self.mazo.cartas:
                    c.voltear()
                print(f"El estado del juego ahora es: {self.estado_actual}")
            else:
                # Cambio de estado normal (oscuro a luminoso o viceversa)
                self.estado_actual = "luminoso" if self.estado_actual == "oscuro" else "oscuro"
                for c in self.pila_descartes + self.mazo.cartas:
                    c.voltear()
                print(f"El estado del juego ahora es: {self.estado_actual}")
        
        elif carta_jugada.valor == "Skip Everyone":
            print(f"Todos los jugadores son saltados, se repite el turno.")
            # Salta al siguiente jugador
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Skip":
            print(f"El siguiente jugador es saltado.")
            # Salta al siguiente jugador
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Reverse":
            print(f"Cambio de sentido.")
            # Invierte el orden de los jugadores
            self.jugadores.reverse()
            self.turno_actual = len(self.jugadores) - self.turno_actual - 1

        elif carta_jugada.valor == "Draw Two":
            print(f"El siguiente jugador debe robar 2 cartas.")
            
            # El siguiente jugador roba dos cartas
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            for _ in range(2):
                carta_robada = self.mazo.sacar_carta()
                if carta_robada:
                    siguiente_jugador.agregar_carta(carta_robada)
            
            # El siguiente jugador pierde su turno
            print(f"{siguiente_jugador.nombre} pierde su turno.")
            
            # Ahora avanzamos al siguiente jugador, que será el que realmente sigue después de que el jugador pierda su turno
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)

        elif carta_jugada.valor == "Wild Draw Four":
            print(f"El siguiente jugador debe robar 4 cartas y pierde su turno.")
            
            siguiente_jugador = self.jugadores[(self.turno_actual + 1) % len(self.jugadores)]
            for _ in range(4):
                carta_robada = self.mazo.sacar_carta()
                if carta_robada:
                    siguiente_jugador.agregar_carta(carta_robada)
            
            print(f"{siguiente_jugador.nombre} pierde su turno.")
            
            self.turno_actual = (self.turno_actual + 2) % len(self.jugadores)
        
        elif carta_jugada.valor in ['Wild', 'Wild Draw']:
            jugador = (self.turno_actual)
            color_elegido = self.manejar_color_wild(jugador)
            carta_jugada.colorLuminoso = color_elegido  # Establecer el color elegido en la carta
            self.pila_descartes.append(carta_jugada)
            print(f"{jugador.nombre} ha elegido el color: {color_elegido}")
            # Pasar el turno al siguiente jugador
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

        else:
            # Pasar el turno al siguiente jugador
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        


    def fin_del_juego(self):
        for jugador in self.jugadores:
            if not jugador.cartas:
                print(f"{jugador.nombre} ha ganado el juego!")
                return True
        return False