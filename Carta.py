class Carta:
    def __init__(self, color, valor, es_accion=False, lado="luminoso"):
        self.color = color
        self.valor = valor
        self.es_accion = es_accion
        self.lado = lado  # Lado de la carta ("luminoso" o "oscuro")

    def voltear(self):
        self.lado = "oscuro" if self.lado == "luminoso" else "luminoso"

    def __str__(self):
        return f"{self.color} {self.valor} ({self.lado})"
