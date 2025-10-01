import math

class SteeringOutput:
    def __init__(self, linear=(0, 0), angular=0.0):
        self.linear = linear    # Aceleracion lineal en x e y
        self.angular = angular  # Aceleracion angular en radianes

class Kinematic:
    def __init__(self, position=(0, 0), orientation=0.0, velocity=(0, 0), rotation=0.0, map_width=800, map_height=600):
        self.position = position        # Posicion (x, y)
        self.orientation = orientation  # Orientacion en radianes
        self.velocity = velocity        # Velocidad de desplazamiento en x e y.
        self.rotation = rotation        # Velocidad de rotacion
       
        self.map_width = map_width      # Ancho del mapa para límites
        self.map_height = map_height    # Alto del mapa para límites
        self.size = 48                  # Tamaño lógico para colisiones y límites
        
        # Ajustar límites para centrar el área jugable: sumar offset a ambos lados
        offset_x = self.size // 2
        offset_z = offset_x
        self.min_x = offset_x + self.size // 2
        self.max_x = self.map_width - offset_x - self.size // 2
        self.min_z = offset_z + self.size // 2
        self.max_z = self.map_height - offset_z - self.size // 2

    def updateKinematic(self, steering : SteeringOutput, maxSpeed: float, time : float):
        # Actualizar posición y orientación según la entrada de control
        x, z = self.position
        x = max(self.min_x, min(x + self.velocity[0] * time, self.max_x))
        z = max(self.min_z, min(z + self.velocity[1] * time, self.max_z))
        self.position = (x, z)

        self.orientation += self.rotation * time

        # Actualizar velocidad y rotación
        self.velocity = (
            self.velocity[0] + steering.linear[0] * time,
            self.velocity[1] + steering.linear[1] * time
        )
        self.rotation += steering.angular * time

        # Limitar la velocidad a la máxima permitida
        speed = math.hypot(self.velocity[0], self.velocity[1])
        if speed > maxSpeed:
            # Normalizar la velocidad y escalar a maxSpeed
            scale = maxSpeed / speed
            self.velocity = (self.velocity[0] * scale, self.velocity[1] * scale)