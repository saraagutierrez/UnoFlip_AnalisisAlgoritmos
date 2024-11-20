import random

class Carta:
    def __init__(self, colorLuminoso, colorOscuro, valorLuminoso, valorOscuro, lado="luminoso"):
        # Si el valor es 'Wild', no asignamos color
        if valorLuminoso == "Wild" or valorOscuro == "Wild":
            self.colorLuminoso = None
            self.colorOscuro = None
            self.valorLuminoso = valorLuminoso 
            self.valorOscuro = valorOscuro     # No tiene valor oscuro
        else:
            self.colorLuminoso = colorLuminoso
            self.colorOscuro = colorOscuro
            self.valorLuminoso = valorLuminoso
            self.valorOscuro = valorOscuro
        
        self.lado = lado  # "luminoso" o "oscuro"
        # Atributo color que se calcula dependiendo del lado
        self.color = self.colorLuminoso if self.lado == "luminoso" else self.colorOscuro
        self.valor = self.valorLuminoso if self.lado == "luminoso" else self.valorOscuro
        self.es_accion = self.valor in ["Skip", "Reverse", "Draw Two", "Wild", "Wild Draw Four", "Flip"]


    def voltear(self):
        self.lado = "oscuro" if self.lado == "luminoso" else "luminoso"
        # Actualizar el color cuando se voltea
        self.color = self.colorLuminoso if self.lado == "luminoso" else self.colorOscuro

    def __str__(self):
        if self.valorLuminoso == "Wild" or self.valorOscuro == "Wild":
            return f"Wild (Sin color) ({self.lado})"
        if self.lado == "luminoso":
            return f"{self.colorLuminoso} {self.valorLuminoso} ({self.lado})"
        else:
            return f"{self.colorOscuro} {self.valorOscuro} ({self.lado})"
