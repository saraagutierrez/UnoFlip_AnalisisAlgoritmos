class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cartas = []

    def agregar_carta(self, carta):
        self.cartas.append(carta)

    def jugar_carta(self, indice):
        return self.cartas.pop(indice)  # Eliminar y devolver la carta jugada

    def __str__(self):
        return f"{self.nombre} ({len(self.cartas)} cartas)"