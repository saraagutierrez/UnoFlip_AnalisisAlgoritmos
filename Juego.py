from random import shuffle
from Mazo import Mazo
from Jugador import Jugador

class UnoFlip:
    def __init__(self, nombres_jugadores):
        self.jugadores = [Jugador(nombre) for nombre in nombres_jugadores]
        self.pila_descartes = []  # Inicialmente vacía
        self.estado_actual = "luminoso"  # Estado inicial del juego
        self.turno_actual = 0  # Para llevar el seguimiento del turno
        self.mazo = Mazo()  # Crear el mazo
        self.iniciar_juego()

    def iniciar_juego(self):
        shuffle(self.mazo.cartas)  # Mezclar el mazo

        # Repartir 7 cartas a cada jugador
        for _ in range(7):
            for jugador in self.jugadores:
                carta = self.mazo.sacar_carta()
                if carta:  # Asegurarse de que hay cartas disponibles
                    jugador.agregar_carta(carta)

        # Colocar la primera carta en la pila de descarte
        carta_inicial = self.mazo.sacar_carta()
        if carta_inicial:  # Asegurarse de que hay una carta inicial
            self.pila_descartes.append(carta_inicial)
            print(f"Carta inicial: {carta_inicial}")

    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]
        print(f"\nTurno del jugador: {jugador}")
        print(f"Cartas en mano: {', '.join(str(carta) for carta in jugador.cartas)}")
        print(f"Carta en la pila de descarte: {self.pila_descartes[-1]}")

        if jugador.cartas:
            carta_jugada = jugador.jugar_carta(0)  # Juega la primera carta
            print(f"{jugador.nombre} juega: {carta_jugada}")

            # Cambiar el estado del juego si se juega una carta de tipo Flip
            if carta_jugada.valor == 'Flip':
                carta_jugada.voltear()  # Voltear la carta
                self.estado_actual = 'oscuro' if self.estado_actual == 'luminoso' else 'luminoso'
                print(f"El estado del juego cambia a: {self.estado_actual}")

            self.pila_descartes.append(carta_jugada)
            print("-------------------------------------------")  # Línea separadora
        else:
            print(f"{jugador.nombre} no tiene cartas para jugar.")

        # Comprobar si el jugador ha ganado
        if not jugador.cartas:  # Si el jugador no tiene cartas
            print(f"{jugador.nombre} ha ganado el juego!")
            return True  # Retornar True para indicar que hay un ganador

        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        return False  # Retornar False si no hay un ganador

    def fin_del_juego(self):
        # Comprobar si algún jugador ha ganado
        for jugador in self.jugadores:
            if not jugador.cartas:
                print(f"{jugador.nombre} ha ganado el juego!")
                return True  # Retornar True si hay un ganador
        return False  # Retornar False si no hay ganadores

# Función para obtener nombres de jugadores con validación
def obtener_nombres_jugadores():
    while True:
        try:
            num_jugadores = int(input("Ingrese el número de jugadores (mínimo 2, máximo 10): "))
            if 2 <= num_jugadores <= 10:
                break
            else:
                print("El número de jugadores debe estar entre 2 y 10.")
        except ValueError:
            print("Por favor ingrese un número válido.")

    nombres_jugadores = []
    for i in range(num_jugadores):
        nombre = input(f"Ingrese el nombre del jugador {i + 1}: ")
        nombres_jugadores.append(nombre)

    return nombres_jugadores

# Inicializar el juego
if __name__ == "__main__":
    nombres_jugadores = obtener_nombres_jugadores()
    juego = UnoFlip(nombres_jugadores)

    # Lógica para jugar turnos hasta que se cumpla alguna condición de fin del juego
    while not juego.fin_del_juego():
        if juego.jugar_turno():
            break  # Salir del bucle si hay un ganador