import pygame
import random
from src.entities.entity import Entity

class Meteorite(Entity):
    def __init__(self):
        # Create a simple grey square for the meteorite
        image = pygame.Surface((30, 30))
        image.fill((100, 100, 100))

        # Spawn at a random position off-screen at the top
        x = random.randint(0, 1280)
        y = -50

        super().__init__(x, y, image)

        # Set a random downward velocity
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(2, 5))
        self.vel.normalize_ip()
        self.speed = 250
        self.vel *= self.speed

    def update(self, dt, player): # Player argument is unused but required by the sprite group
        super().update(dt)
        # Remove meteorite if it goes off the bottom of the screen
        if self.rect.top > 720:
            self.kill()

class PartPickup(Entity):
    def __init__(self, x, y, part):
        # Create a simple flashing representation
        self.part = part
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0)) # Yellow square

        super().__init__(x, y, self.image)
        self.vel = pygame.math.Vector2(0, 0) # It's stationary

    def update(self, dt, player):
        pass # Does not move on its own
