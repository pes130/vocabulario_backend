class TerminoResultado:
    def __init__(self, termino, aciertos, fallos):
        self.termino = termino
        self.aciertos = aciertos
        self.fallos = fallos
    
    def json(self):
        return {
            'termino': self.termino,
            'aciertos': self.aciertos, 
            'fallos': self.fallos,
            'total': round(self.aciertos / (self.aciertos + self.fallos) * 100, 3)
        }
