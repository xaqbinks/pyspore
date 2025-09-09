import pygame
import time
import random
from src.entities.entity import Entity
from src.assets.visual_generator import generate_blob_surface
from src.config import RED, WHITE

class AICell(Entity):
    def __init__(self, x, y):
        size = 50 # Larger than the player
        image, _ = generate_blob_surface(
            size=size,
            complexity=0.2,
            seed=time.time() + x + y,
            color=RED
        )
        super().__init__(x, y, image)
        self.speed = 100
        self.detection_radius = 300
        self.state = 'wander'

        # Wander behavior
        self.wander_timer = 0
        self.wander_interval = 2.0 # Change direction every 2 seconds
        self.pick_new_direction()

    def pick_new_direction(self):
        """Picks a random direction vector."""
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.vel.length() > 0:
            self.vel.normalize_ip()
            self.vel *= self.speed
        self.wander_timer = 0

    def update(self, dt, player):
        distance_to_player = self.pos.distance_to(player.pos)

        if distance_to_player < self.detection_radius:
            self.state = 'hunt'
        else:
            self.state = 'wander'

        if self.state == 'hunt':
            # Move towards the player
            direction = (player.pos - self.pos).normalize()
            self.vel = direction * self.speed
        elif self.state == 'wander':
            # Standard wander behavior
            self.wander_timer += dt
            if self.wander_timer > self.wander_interval:
                self.pick_new_direction()

        self.pos += self.vel * dt
        self.rect.center = self.pos

class MateCell(Entity):
    def __init__(self, x, y):
        size = 35
        image, _ = generate_blob_surface(
            size=size,
            complexity=0.1,
            seed=time.time() + x + y,
            color=(100, 100, 255) # Light blue
        )
        super().__init__(x, y, image)
        # Mate cells are stationary
        self.vel = pygame.math.Vector2(0, 0)

class PreyCell(AICell):
    def __init__(self, x, y):
        # Use AICell's __init__ but override some parameters
        super().__init__(x, y)

        size = 15 # Smaller than player
        self.image, _ = generate_blob_surface(
            size=size,
            complexity=0.4,
            seed=time.time() + x + y,
            color=(0, 255, 100) # Light green
        )
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 75
        self.pick_new_direction() # Get a new speed

    def update(self, dt, player):
        # Prey just wanders, it doesn't hunt. It ignores the player argument.
        self.wander_timer += dt
        if self.wander_timer > self.wander_interval:
            self.pick_new_direction()

        self.pos += self.vel * dt
        self.rect.center = self.pos
