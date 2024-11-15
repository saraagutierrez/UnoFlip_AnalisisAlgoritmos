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

    def jugar_turno(self, carta_actual, estado_actual, mazo):
        print(f"\nTurno del jugador sintético: {self.nombre}")
        print(f"Cartas en mano: {', '.join(str(carta) for carta in self.cartas)}")
        print(f"Carta en la pila de descarte: {carta_actual}")
        
        # Intentar jugar una carta
        carta_elegida = self.elegir_carta(carta_actual, estado_actual)
        if carta_elegida:
            self.cartas.remove(carta_elegida)  # Remover la carta elegida de la mano
            print(f"{self.nombre} juega: {carta_elegida}")
            return carta_elegida
        else:
            # Robar una carta si no tiene jugada posible
            nueva_carta = mazo.sacar_carta()
            if nueva_carta:
                self.agregar_carta(nueva_carta)
                print(f"{self.nombre} no tiene cartas para jugar. Roba una carta: {nueva_carta}")
            return None
