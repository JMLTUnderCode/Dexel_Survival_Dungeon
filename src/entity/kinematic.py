import math
import pygame
from typing import Tuple, List, Optional
from entity.entity_spec import Stats, SpawnedEntityMeta
from configs.package import CONF

# 2. Algoritmos que usan orientación explícita (lista de claves de algoritmo)
ALGORITHM_USE_ROTATION = [
    "PLAYER",
    CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
    CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
    CONF.ALG.ALGORITHM.ALIGN,
    CONF.ALG.ALGORITHM.FACE,
    CONF.ALG.ALGORITHM.PURSUE,
    CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING,
    CONF.ALG.ALGORITHM.VELOCITY_MATCH,
    CONF.ALG.ALGORITHM.PATH_FOLLOWING,
    CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING,
]

class SteeringOutput:
    """
    Descripción
        CLASE: Representa la salida de steering con componentes lineal y angular.

    Atributos
        - linear (tuple[float,float]): vector de aceleración lineal (ax, az).
        - angular (float): aceleración angular en radianes.
    """
    def __init__(self, linear: Tuple[float, float] = (0.0, 0.0), angular: float = 0.0) -> None:
        # 1. Inicializar componentes de salida
        self.linear: Tuple[float, float] = (float(linear[0]), float(linear[1]))
        self.angular: float = float(angular)

class KinematicSteeringOutput:
    """
    Descripción
        CLASE: Representa la salida cinemática (velocidad y rotación).

    Atributos
        - velocity (tuple[float,float]): velocidad objetivo (vx, vz).
        - rotation (float): velocidad angular objetivo en radianes.
    """
    def __init__(self, velocity: Tuple[float, float] = (0.0, 0.0), rotation: float = 0.0) -> None:
        # 1. Inicializar la velocidad y rotación objetivo
        self.velocity: Tuple[float, float] = (float(velocity[0]), float(velocity[1]))
        self.rotation: float = float(rotation)

class Kinematic:
    """
    Descripción
        CLASE: Base para entidades con movimiento y colisiones.

    Atributos
        - position (tuple[float,float]): posición (x, z) en píxeles.
        - orientation (float): orientación en radianes.
        - velocity (tuple[float,float]): velocidad actual (vx, vz).
        - rotation (float): velocidad angular.
        - alive (bool): indicador de vida.
        - max_health (float): salud máxima.
        - health (float): salud actual.
        - spawn_meta (Optional[SpawnedEntityMeta]): metadatos de spawn/invocación.
        - node_location: nodo de navmesh asociado (opcional).
    
    Métodos y Funciones
        - take_damage: aplica daño y marca la entidad muerta si corresponde.
        - is_alive: retorna si la entidad está viva.
        - die: hook por defecto para marcar entidad como muerta.
        - is_a_collision: verifica colisión contra rectángulos del mapa.
        - validate_movement: intenta mover respetando colisiones (total / parcial).
        - update_by_kinematic: aplica movimiento kinemático (velocity, rotation).
        - update_by_dynamic: aplica movimiento basado en aceleraciones (steering).
        - new_orientation: calcula orientación desde un vector de velocidad.
        - get_pos: retorna la posición actual.
        - draw_life_bar: dibuja la barra de vida sobre el sprite.
    
    Propósito
        - Proveer utilidades compartidas por Player y Enemy para actualización física y colisiones.
    """
    def __init__(
        self,
        position: Tuple[float, float] = (0.0, 0.0),
        orientation: float = 0.0,
        velocity: Tuple[float, float] = (0.0, 0.0),
        rotation: float = 0.0,
        statistics: Optional[Stats] = None,
        spawn_meta: Optional[SpawnedEntityMeta] = None,
    ) -> None:
        # 1. Inicializar estado cinemático básico
        self.position: Tuple[float, float] = (float(position[0]), float(position[1]))
        self.orientation: float = float(orientation)
        self.velocity: Tuple[float, float] = (float(velocity[0]), float(velocity[1]))
        self.rotation: float = float(rotation)

        # 2. Inicializar estadísticas (si se proporcionan) o valores por defecto
        self.alive: bool = statistics.alive if statistics else True
        self.max_health: float = statistics.health if statistics else 100.0
        self.health: float = self.max_health
        self.max_mana: float = statistics.mana if statistics and statistics.mana is not None else 100.0
        self.mana: float = self.max_mana
        self.max_armor: float = statistics.armor if statistics and statistics.armor is not None else 0.0
        self.armor: float = self.max_armor
        
        self.mele_dmg: float = statistics.mele_dmg if statistics and statistics.mele_dmg is not None else 20.0
        self.max_mele_dmg: float = 2 * self.mele_dmg
        self.mele_cooldown: float = statistics.mele_cooldown if statistics and statistics.mele_cooldown is not None else 1.2
        self.curr_mele_cooldown: float = 0.0
        
        self.magic_dmg: float = statistics.magic_dmg if statistics and statistics.magic_dmg is not None else 25.0
        self.max_magic_dmg: float = 2 * self.magic_dmg
        self.magic_cooldown: float = statistics.magic_cooldown if statistics and statistics.magic_cooldown is not None else 1.2
        self.curr_magic_cooldown: float = 0.0

        # 3. Metadatos de spawn (si aplica)
        self.spawn_meta: Optional[SpawnedEntityMeta] = spawn_meta

        # 4. Nodo del NavMesh donde se encuentra la entidad (puede permanecer None)
        self.node_location = None

        # 5. Bandera para controlar si el efecto actual ya aplicó daño
        self.effect_damage_applied: bool = False

    def update_cooldowns(self, dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza los contadores de cooldown de habilidades.

        Argumentos
            - dt (float): delta time en segundos.
        """
        if self.curr_mele_cooldown > 0:
            self.curr_mele_cooldown = max(0.0, self.curr_mele_cooldown - dt)
        
        if self.curr_magic_cooldown > 0:
            self.curr_magic_cooldown = max(0.0, self.curr_magic_cooldown - dt)

    def take_damage(self, amount: float) -> float:
        """
        Descripción
            MÉTODO: Aplica `amount` de daño a la entidad y marca vivencia.
        
        Argumentos
            - amount (float): cantidad de daño a aplicar (valor absoluto).
        
        Retorno
            - float: vida restante después de aplicar el daño.
        """
        # 1. No aplicar daño si ya está muerto
        if not self.alive:
            return self.health

        # 2. Reducir la vida y comprobar si alcanza 0
        self.health = max(0.0, self.health - float(amount))
        if self.health <= 0.0:
            self.die()

    def is_alive(self) -> bool:
        """
        Descripción
            FUNCIÓN: Indica si la entidad está viva.
        
        Argumentos
            - Ninguno
        
        Retorno
            - bool: True si la entidad está viva, False en caso contrario.
        """
        return bool(self.alive)

    def die(self) -> None:
        """
        Descripción
            MÉTODO: Hook por defecto al morir; marca la entidad como no viva.
        
        Argumentos
            - Ninguno
        """
        # 1. Marcar entidad como no viva
        self.alive = False

    def is_a_collision(
        self,
        pos: Tuple[float, float],
        collision_rects: Optional[List[pygame.Rect]],
        collider_box: Tuple[int, int],
    ) -> bool:
        """
        Descripción
            FUNCIÓN: Verifica si la posición dada colisiona con alguno de los rectángulos provistos.
        
        Argumentos
            - pos (tuple[float,float]): posición (x, z) a validar.
            - collision_rects (Optional[List[pygame.Rect]]): lista de rectángulos del mapa.
            - collider_box (tuple[int,int]): dimensiones de la caja de colisión (w, h).
        
        Retorno
            - bool: True si hay colisión, False si no.
        """
        # 1. Si no hay rectángulos de colisión, no hay colisión
        if collision_rects is None:
            return False

        # 2. Construir rectángulo centrado en la posición propuesta
        pos_x, pos_z = float(pos[0]), float(pos[1])
        box_collider = pygame.Rect(
            int(pos_x - collider_box[0] // 2),
            int(pos_z - collider_box[1] // 2),
            int(collider_box[0]),
            int(collider_box[1]),
        )

        # 3. Comprobar intersección con cualquiera de los rectángulos
        for col_rect in collision_rects:
            if box_collider.colliderect(col_rect):
                return True
        return False

    def validate_movement(
        self,
        new_pos: Tuple[float, float],
        pos: Tuple[float, float],
        collision_rects: Optional[List[pygame.Rect]],
        collider_box: Tuple[int, int],
    ) -> None:
        """
        Descripción
            MÉTODO: Valida y aplica el movimiento intentando evitar colisiones.
            Intenta movimiento completo, luego solo en X, luego solo en Z.
        
        Argumentos
            - new_pos (tuple[float,float]): posición propuesta (x, z).
            - pos (tuple[float,float]): posición actual (x, z).
            - collision_rects (Optional[List[pygame.Rect]]): rectángulos de colisión del mapa.
            - collider_box (tuple[int,int]): dimensiones del collider.
        """
        # 1. Intentar movimiento completo y aplicar si no colisiona
        new_x, new_z = float(new_pos[0]), float(new_pos[1])
        x, z = float(pos[0]), float(pos[1])
        if not self.is_a_collision((new_x, new_z), collision_rects, collider_box):
            self.position = (new_x, new_z)
            return

        # 2. Intentar mover solo en X
        if not self.is_a_collision((new_x, z), collision_rects, collider_box):
            self.position = (new_x, z)
            return

        # 3. Intentar mover solo en Z
        if not self.is_a_collision((x, new_z), collision_rects, collider_box):
            self.position = (x, new_z)
            return

        # 4. Si no puede moverse, mantener posición actual (no cambiar)

    def update_by_kinematic(
        self,
        steering: KinematicSteeringOutput,
        time: float,
        collision_rects: Optional[List[pygame.Rect]],
        collider_box: Tuple[int, int],
        algorithm: str,
    ) -> None:
        """
        Descripción
            MÉTODO: Actualiza posición y orientación usando salida kinemática (velocity + rotation).
        
        Argumentos
            - steering (KinematicSteeringOutput): salida que contiene velocity y rotation.
            - time (float): delta time en segundos.
            - collision_rects (Optional[List[pygame.Rect]]): rects para validar colisiones.
            - collider_box (tuple[int,int]): dimensiones del collider.
            - algorithm (str): identificador del algoritmo activo (para decidir rotación).
        """
        # 1. Calcular nueva posición a partir de la velocidad
        x, z = float(self.position[0]), float(self.position[1])
        vx, vz = float(steering.velocity[0]), float(steering.velocity[1])

        new_x = x + vx * float(time)
        new_z = z + vz * float(time)

        # 2. Validar movimiento y aplicar la mejor opción permitida
        self.validate_movement((new_x, new_z), (x, z), collision_rects, collider_box)

        # 3. Actualizar orientación: depende si el algoritmo usa rotación explícita
        if algorithm in ALGORITHM_USE_ROTATION:
            self.orientation += float(steering.rotation) * float(time)
        else:
            # 3.1 Si no usa rotación explícita, orientar según la velocidad actual
            self.orientation = self.new_orientation(self.orientation, steering.velocity)

    def update_by_dynamic(
        self,
        steering: SteeringOutput,
        max_speed: float,
        time: float,
        collision_rects: Optional[List[pygame.Rect]],
        collider_box: Tuple[int, int],
        algorithm: str,
    ) -> None:
        """
        Descripción
            MÉTODO: Actualiza posición, orientación, velocidad y rotación usando aceleraciones.
        
        Argumentos
            - steering (SteeringOutput): aceleraciones linear y angular.
            - max_speed (float): velocidad máxima permitida para la entidad.
            - time (float): delta time en segundos.
            - collision_rects (Optional[List[pygame.Rect]]): rectángulos para colisión.
            - collider_box (tuple[int,int]): dimensiones del collider.
            - algorithm (str): identificador del algoritmo activo.
        """
        # 1. Aplicar integración simple para posición
        x, z = float(self.position[0]), float(self.position[1])
        vx, vz = float(self.velocity[0]), float(self.velocity[1])

        new_x = x + vx * float(time)
        new_z = z + vz * float(time)

        # 2. Validar movimiento y aplicar
        self.validate_movement((new_x, new_z), (x, z), collision_rects, collider_box)

        # 3. Actualizar orientación
        if algorithm in ALGORITHM_USE_ROTATION:
            self.orientation += float(self.rotation) * float(time)
        else:
            self.orientation = self.new_orientation(self.orientation, self.velocity)

        # 4. Integrar velocidad y rotación usando steering
        self.velocity = (
            self.velocity[0] + steering.linear[0] * float(time),
            self.velocity[1] + steering.linear[1] * float(time),
        )
        self.rotation += float(steering.angular) * float(time)

        # 5. Limitar la velocidad a max_speed
        speed = math.hypot(self.velocity[0], self.velocity[1])
        if speed > float(max_speed) and speed > 0.0:
            scale = float(max_speed) / speed
            self.velocity = (self.velocity[0] * scale, self.velocity[1] * scale)

    def new_orientation(self, current_orientation: float, velocity: Tuple[float, float]) -> float:
        """
        Descripción
            FUNCIÓN: Calcula la nueva orientación (radianes) basada en el vector de velocity.

        Argumentos
            - current_orientation (float): orientación actual en radianes.
            - velocity (tuple[float,float]): vector de velocidad (vx, vz).

        Retorno
            - float: nueva orientación en radianes.
        """
        # 1. Si no hay velocidad, mantener orientación actual
        if velocity == (0.0, 0.0):
            return current_orientation
        # 2. Calcular ángulo con atan2 (y luego devolver en radianes)
        return math.atan2(float(velocity[1]), float(velocity[0]))

    def get_pos(self) -> Tuple[float, float]:
        """
        Descripción
            FUNCIÓN: Retorna la posición actual de la entidad.

        Argumentos
            - Ninguno

        Retorno
            - tuple[float,float]: (x, z) posición en píxeles.
        """
        return self.position

    def draw_life_bar(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja la barra de vida sobre el sprite en la superficie indicada.

        Argumentos
            - surface (pygame.Surface): superficie de destino.
            - camera_x (float): coordenada X de la cámara.
            - camera_z (float): coordenada Z de la cámara.
        """
        # 1. Calcular coordenadas de pantalla relativas a la cámara
        sx = int(self.position[0] - camera_x)
        sz = int(self.position[1] - camera_z)

        # 2. Dimensiones de la barra y posición sobre el sprite
        bar_w = 74
        bar_h = 14
        bar_x = sx - bar_w // 2
        bar_y = sz - (getattr(self, "current_animation", None).get_size()[1] // 2 if getattr(self, "current_animation", None) else 0) - 12

        # 3. Dibujar fondo, barra de vida y borde
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
        hp_ratio = max(0.0, min(1.0, getattr(self, "health", 0.0) / max(1.0, getattr(self, "max_health", 1.0))))
        fill_w = int(bar_w * hp_ratio)
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_w, bar_h), 1)

    def get_current_effect_center(self) -> Optional[Tuple[float, float]]:
        """
        Descripción
            FUNCIÓN: Calcula la posición central (x, z) del efecto de ataque activo en coordenadas de mundo.
            Reutiliza la lógica visual para asegurar que la hitbox coincida con el sprite.

        Argumentos
            - Ninguno

        Retorno
            - Optional[Tuple[float, float]]: Coordenadas (x, z) del centro del efecto, o None si no hay efecto activo.
        """
        # 1. Validar si hay efecto activo
        if not self.current_effect or self.current_effect.is_finished:
            return None

        # 2. Calcular posición según el tipo de efecto
        cx, cz = self.position[0], self.position[1]

        if self.current_effect_type == "mele":
            # 2.1 Mele: Offset fijo en la dirección de la orientación
            offset_dist = 30.0
            off_x = math.cos(self.orientation) * offset_dist
            off_y = math.sin(self.orientation) * offset_dist
            return (cx + off_x, cz + off_y)

        elif self.current_effect_type == "magic":
            # 2.2 Magic: Interpolación lineal (Lerp) basada en el progreso de la animación
            anim = self.current_effect
            total_duration = anim.frame_count * anim.frame_duration
            elapsed = anim.current_frame * anim.frame_duration + anim.time_acc
            progress = min(1.0, elapsed / total_duration) if total_duration > 0 else 0.0

            start_x, start_z = self.magic_start_pos
            target_x, target_z = self.magic_target_pos
            
            curr_x = start_x + (target_x - start_x) * progress
            curr_z = start_z + (target_z - start_z) * progress
            return (curr_x, curr_z)
        
        elif self.current_effect_type == "healing":
            return (cx, cz)

        elif self.current_effect_type == "invocation":
            return (cx, cz)

        # 2.3 Default: Sobre la entidad
        return (cx, cz)

    def draw_attack_effect(self, surface: pygame.Surface, camera_x: float, camera_z: float, deg: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja el efecto de ataque activo usando la posición calculada centralizada.
        """
        # 1. Obtener posición de mundo del efecto
        world_pos = self.get_current_effect_center()
        
        if world_pos:
            # 2. Convertir a coordenadas de pantalla
            wx, wz = world_pos
            effect_draw_pos = (wx - camera_x, wz - camera_z)
            
            # 3. Obtener frame y rotar
            effect_frame = self.current_effect.get_frame()
            
            if self.current_effect_type == "mele":
                rotated_effect = pygame.transform.rotate(effect_frame, deg + 90.0)
            elif self.current_effect_type == "magic":
                rotated_effect = pygame.transform.rotate(effect_frame, deg - 120.0)
            elif self.current_effect_type == "invocation":
                rotated_effect = pygame.transform.rotate(effect_frame, deg)
            else:
                rotated_effect = pygame.transform.rotate(effect_frame, deg)

            # 4. Dibujar
            effect_rect = rotated_effect.get_rect(center=effect_draw_pos)
            surface.blit(rotated_effect, effect_rect)