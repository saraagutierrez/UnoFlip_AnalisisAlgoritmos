from Jugador import Jugador
from JugadorSintetico import JugadorSintetico
from Juego import UnoFlip

def obtener_jugadores():
    while True:
        try:
            num_jugadores = int(input("Ingrese el número de jugadores (mínimo 2, máximo 10): "))
            if 2 <= num_jugadores <= 10:
                break
            else:
                print("El número de jugadores debe estar entre 2 y 10.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

    jugadores = []
    for i in range(num_jugadores):
        while True:
            nombre = input(f"Ingrese el nombre del jugador {i + 1}: ").strip()
            if nombre:
                if nombre not in [j.nombre for j in jugadores]:
                    break
                else:
                    print(f"El nombre '{nombre}' ya está en uso. Elija otro.")
            else:
                print("El nombre no puede estar vacío.")
        
        while True:
            tipo = input(f"¿{nombre} es un jugador humano (H) o sintético (S)? ").upper()
            if tipo in ["H", "S"]:
                break
            print("Por favor, ingrese 'H' para humano o 'S' para sintético.")

        if tipo == "H":
            jugadores.append(Jugador(nombre))
        else:
            jugadores.append(JugadorSintetico(nombre))

    return jugadores

def main():
    print("¡Bienvenido a Uno Flip!")
    jugadores = obtener_jugadores()
    juego = UnoFlip(jugadores)

    print("\n¡El juego comienza!")
    while not juego.fin_del_juego():
        juego.jugar_turno()

    print("\n¡Gracias por jugar! Fin del juego.")

if __name__ == "__main__":
    main()
