import pygame
import math
from utils.configs import *

class SteeringOutput:
    """
    Representa la salida de steering con componentes lineales y angulares.
    Atributos:
        linear: tupla (ax, ay) representando la aceleración lineal en x e y
        angular: aceleración angular en radianes
    """
    def __init__(self, linear=(0, 0), angular=0.0):
        self.linear = linear    # Aceleracion lineal en x e y
        self.angular = angular  # Aceleracion angular en radianes

class Kinematic:
    """
    Clase base para entidades con movimiento y colisiones.
    Atributos:
        position: tupla (x, y) representando la posición en píxeles
        orientation: ángulo en radianes representando la orientación
        velocity: tupla (vx, vy) representando la velocidad en píxeles/segundo
        rotation: velocidad angular en radianes/segundo
        map_width, map_height: dimensiones del mapa para limitar el movimiento
        collision_rects: lista de pygame.Rect para detección de colisiones
    """
    def __init__(self, position=(0, 0), orientation=0.0, velocity=(0, 0), rotation=0.0):
        self.position = position        # Posicion (x, y)
        self.orientation = orientation  # Orientacion en radianes
        self.velocity = velocity        # Velocidad de desplazamiento en x e y.
        self.rotation = rotation        # Velocidad de rotacion

        self.size = 48                  # Tamaño lógico para colisiones y límites

    def validate_movement(self, new_x, new_z, collision_rects):
        """
        Valida si la nueva posición (new_x, new_y) colisiona con algún rectángulo de colisión.
        Retorna True si el movimiento es válido (sin colisiones), False si hay colisiónes.
        Usa un rectángulo centrado en (new_x, new_y) con tamaño self.size x self.size.
        """
        if collision_rects is None:
            return True

        # Bounding box del personaje en coordenadas de mapa
        w, h = self.size, self.size
        box_collider = pygame.Rect(
            int(new_x - w // 2),
            int(new_z - h // 2), 
            w, 
            h
        )

        for col_rect in collision_rects:
            if box_collider.colliderect(col_rect):
                return False  # Colisión detectada
        return True  # Movimiento válido

    def updateKinematic(self, steering : SteeringOutput, maxSpeed: float, time : float, collision_rects):
        """
        Actualiza la posición, orientación, velocidad y rotación del objeto
        usando el steering proporcionado, respetando las colisiones y límites del mapa.
        """
        # Actualizar posición y orientación según la entrada de control
        x, z = self.position
        vx, vz = self.velocity

        # Propuesta de nueva posición
        new_x = x + vx * time
        new_z = z + vz * time

        # 1. Intentar movimiento completo
        if self.validate_movement(new_x, new_z, collision_rects):
            self.position = (new_x, new_z)
        else:
            # 2. Intentar solo en X
            if self.validate_movement(new_x, z, collision_rects):
                self.position = (new_x, z)
            # 3. Intentar solo en Y
            elif self.validate_movement(x, new_z, collision_rects):
                self.position = (x, new_z)
            # 4. Si no puede moverse, no cambia posición

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