import pygame

class AttackWave:
    def __init__(self, x, z, color=(50, 120, 255), max_radius=54, duration=25):
        # Posición inicial de la onda (centro)
        self.x = x
        self.z = z
        self.color = color           # Color de la onda (RGB)
        self.max_radius = max_radius # Radio máximo que alcanzará la onda
        self.duration = duration     # Duración total de la onda en frames
        self.frame = 0               # Frame actual (cuenta cuántos frames ha estado activa)
        self.alive = True            # Estado de vida: True si la onda sigue activa, False si debe eliminarse

        self._applied = False        # Marca si el daño ya fue aplicado

    @property
    def applied(self) -> bool:
        return self._applied

    def mark_applied(self) -> None:
        self._applied = True

    def update(self):
        # Avanza un frame la animación de la onda
        self.frame += 1
        # Si se supera la duración, la onda muere
        if self.frame >= self.duration:
            self.alive = False

    def draw(self, surface, camera_x, camera_z):
        # No dibujar si la onda ya está muerta
        if not self.alive:
            return
        # Calcular posición en pantalla ajustada por la cámara
        sx = self.x - camera_x
        sz = self.z - camera_z
        
        # El radio crece linealmente con el tiempo
        radius = int(1 + (self.max_radius - 1) * (self.frame / self.duration))
        
        # El alpha (transparencia) disminuye linealmente para desvanecer la onda
        alpha = max(0, 255 - int(255 * (self.frame / self.duration)))
        
        # Crear una superficie temporal con canal alpha para dibujar la onda
        circ_surf = pygame.Surface((self.max_radius*2+2, self.max_radius*2+2), pygame.SRCALPHA)
        
        # Dibujar el círculo de la onda con el color y alpha calculados
        pygame.draw.circle(circ_surf, (*self.color, alpha), (self.max_radius+1, self.max_radius+1), radius, 2)
        
        # Blittear la onda en la posición correcta de la pantalla
        surface.blit(circ_surf, (sx - self.max_radius - 1, sz - self.max_radius - 1))