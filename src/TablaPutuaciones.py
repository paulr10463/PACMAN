import json
class TablaPuntuaciones:
    def __init__(self):
        self.puntuaciones = []
        self.cargarPuntuaciones()

    def cargarPuntuaciones(self):
        try:
            with open('res/puntuaciones.json') as json_file:
                self.puntuaciones = json.load(json_file)
        except:
            self.puntuaciones = []
    
    def guardarPuntuaciones(self):
        with open('res/puntuaciones.json', 'w') as outfile:
            json.dump(self.puntuaciones, outfile)

    def agregarPuntuacion(self, nombre, puntuacion):
        self.puntuaciones.append({"nombre": nombre, "puntuacion": puntuacion})
        self.puntuaciones=sorted(self.puntuaciones, key=lambda k: k['puntuacion'], reverse=True)
        self.puntuaciones = self.puntuaciones[:5]
        self.guardarPuntuaciones()