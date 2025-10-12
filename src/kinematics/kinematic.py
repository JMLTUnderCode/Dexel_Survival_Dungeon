import pygame
import math
from typing import Tuple
import utils.configs as configs

ALGORITHM_USE_ROTATION = [
    "PLAYER", 
    configs.ALGORITHM.WANDER_KINEMATIC,
    configs.ALGORITHM.ALIGN, 
    configs.ALGORITHM.FACE, 
    configs.ALGORITHM.LOOK_WHERE_YOURE_GOING, 
    #configs.ALGORITHM.VELOCITY_MATCH,
]

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

class KinematicSteeringOutput:
    """
    Representa la salida de steering cinemático con componentes de velocidad y rotación.
    Atributos:
        velocity: tupla (vx, vz) representando la velocidad en x, z
        rotation: velocidad angular en radianes
    """
    def __init__(self, velocity=(0, 0), rotation=0.0):
        self.velocity = velocity  # Velocidad en x, z
        self.rotation = rotation  # Velocidad angular en radianes

class Kinematic:
    """
    Clase base para entidades con movimiento y colisiones.
    Atributos:
        position: tupla (x, y) representando la posición en píxeles
        orientation: ángulo en radianes representando la orientación
        velocity: tupla (vx, vy) representando la velocidad en píxeles/segundo
        rotation: velocidad angular en radianes/segundo
    """
    def __init__(self, position=(0, 0), orientation=0.0, velocity=(0, 0), rotation=0.0):
        self.position = position        # Posicion (x, y)
        self.orientation = orientation  # Orientacion en radianes
        self.velocity = velocity        # Velocidad de desplazamiento en x e y.
        self.rotation = rotation        # Velocidad de rotacion

    def is_a_collision(
        self, 
        pos: tuple[float, float],
        collision_rects: list[pygame.Rect], 
        collider_box: tuple[int, int]
    ) -> bool:
        """
        Verifica si la posición actual colisiona con algún rectángulo de colisión.
        Retorna True si hay colisión, False si no.
        Usa un rectángulo centrado en la posición actual con dimensiones de collider_box.
        """
        if collision_rects is None:
            return False  # Sin colisiones si no hay rectángulos
        
        pos_x, pos_z = pos
        # Bounding box del personaje en coordenadas de mapa
        box_collider = pygame.Rect(
            int(pos_x - collider_box[0] // 2),
            int(pos_z - collider_box[1] // 2),
            collider_box[0],
            collider_box[1]
        )

        for col_rect in collision_rects:
            if box_collider.colliderect(col_rect):
                return True  # Colisión detectada
        return False  # Sin colisiones

    def validate_movement(
        self, 
        new_pos: tuple[float, float], 
        pos: tuple[float, float],
        collision_rects: list[pygame.Rect], 
        collider_box: tuple[int, int]
    ) -> None:
        """
        Valida el movimiento del objeto en función de las colisiones.
        Intenta mover a new_pos; si colisiona, intenta solo en X o solo en Z.
        """
        new_x, new_z = new_pos
        x, z = pos
        # 1. Intentar movimiento completo
        if not self.is_a_collision(new_pos, collision_rects, collider_box):
            self.position = new_pos
        else:
            # 2. Intentar solo en X
            if not self.is_a_collision((new_x, z), collision_rects, collider_box):
                self.position = (new_x, z)
            # 3. Intentar solo en Y
            elif not self.is_a_collision((x, new_z), collision_rects, collider_box):
                self.position = (x, new_z)
            # 4. Si no puede moverse, no cambia posición

    def update_by_kinematic(
        self, 
        steering: KinematicSteeringOutput, 
        time: float, 
        collision_rects: list[pygame.Rect], 
        collider_box: tuple[int, int], 
        algorithm: str
    ) -> None:
        """
        Actualiza la posición y orientación del objeto usando el steering proporcionado.
        No considera aceleración, solo mueve según velocity y rotation. Respeta las colisiones.
        """
        # Actualizar posición y orientación según la entrada de control
        x, z = self.position
        vx, vz = steering.velocity

        # Propuesta de nueva posición
        new_x = x + vx * time
        new_z = z + vz * time

        # Validar movimiento con colisiones
        self.validate_movement((new_x, new_z), self.position, collision_rects, collider_box)
        
         # Actualizar orientación
        if algorithm in ALGORITHM_USE_ROTATION:
            self.orientation += steering.rotation * time
        else:
            self.orientation = self.newOrientation(self.orientation, steering.velocity)
            

    def update_by_dynamic(
        self, 
        steering: SteeringOutput, 
        maxSpeed: float, 
        time: float, 
        collision_rects: list[pygame.Rect], 
        collider_box: tuple[int, int],
        algorithm: str
    ) -> None:
        """
        Actualiza la posición, orientación, velocidad y rotación del objeto
        usando el steering proporcionado, respetando las colisiones.
        """
        # Actualizar posición
        x, z = self.position
        vx, vz = self.velocity

        # Propuesta de nueva posición
        new_x = x + vx * time
        new_z = z + vz * time

        # Validar movimiento con colisiones
        self.validate_movement((new_x, new_z), self.position, collision_rects, collider_box)
        
        # Actualizar orientación
        if algorithm in ALGORITHM_USE_ROTATION:
            self.orientation += self.rotation * time
        else:
            self.orientation = self.newOrientation(self.orientation, self.velocity)

        # Actualizar velocidad
        self.velocity = (
            self.velocity[0] + steering.linear[0] * time,
            self.velocity[1] + steering.linear[1] * time
        )
        # Actualizar rotación
        self.rotation += steering.angular * time

        # Limitar la velocidad a la máxima permitida
        speed = math.hypot(self.velocity[0], self.velocity[1])
        if speed > maxSpeed:
            # Normalizar la velocidad y escalar a maxSpeed
            scale = maxSpeed / speed
            self.velocity = (self.velocity[0] * scale, self.velocity[1] * scale)

    def newOrientation(self, current_orientation: float, velocity: Tuple[float, float]) -> float:
        """
        Calcula y devuelve la nueva orientación (ángulo en radianes) a partir de la dirección del vector velocity.

        - Si velocity == (0,0): devuelve current_orientation (sin cambios).
        - Se usa math.atan2(vy, vx) para obtener el ángulo en radianes en el rango [-pi, pi].
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])