import pygame
import time
import math
import random
from src.entities.entity import Entity
from src.assets.visual_generator import generate_blob_surface
from src.config import GREEN

class Player(Entity):
    def __init__(self, x, y, diet='herbivore'):
        size = 30
        self.original_base_image, _ = generate_blob_surface(
            size=size,
            complexity=0.1,
            seed=time.time(),
            color=GREEN
        )
        self.base_image = self.original_base_image.copy()
        super().__init__(x, y, self.base_image.copy())

        # Movement stats
        self.diet = diet
        self.angle = 0
        self.base_speed = 200
        self.base_turning_speed = 150 # degrees per second

        self.dna_points = 0
        self.parts = []
        self.recalculate_stats()

    def add_part(self, part):
        self.parts.append(part)
        self.recalculate_stats()
        self.redraw_image()

    def recalculate_stats(self):
        """Calculates stats based on base values and parts."""
        self.speed = self.base_speed
        self.turning_speed = self.base_turning_speed
        self.defense = 0
        self.diet_bonus = 0

        for part in self.parts:
            self.speed += part.stat_bonuses.get("speed", 0)
            self.defense += part.stat_bonuses.get("defense", 0)
            self.turning_speed += part.stat_bonuses.get("turning_speed", 0)

            if self.diet == 'herbivore':
                self.diet_bonus += part.stat_bonuses.get("herbivore_bonus", 0)
            elif self.diet == 'carnivore':
                self.diet_bonus += part.stat_bonuses.get("carnivore_bonus", 0)

    def redraw_image(self):
        """Redraws the main image with parts attached."""
        self.base_image = self.original_base_image.copy()
        for i, part in enumerate(self.parts):
            # Improved attachment logic with some randomness
            angle = (i / max(1, len(self.parts))) * 360 + random.uniform(-10, 10)
            radius = 25 + random.uniform(-3, 3)
            offset = pygame.math.Vector2(radius, 0).rotate(angle)
            part_rect = part.image.get_rect(center=self.base_image.get_rect().center + offset)
            self.base_image.blit(part.image, part_rect)

        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def handle_input(self, dt):
        """Handles user input and updates player velocity and angle."""
        keys = pygame.key.get_pressed()
        rotation_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            rotation_dir += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            rotation_dir -= 1

        thrust = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            thrust = 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            thrust = -0.5

        # Rotate
        self.angle += rotation_dir * self.turning_speed * dt
        self.angle %= 360

        # Apply thrust
        self.vel = pygame.math.Vector2(1, 0).rotate(self.angle) * thrust * self.speed

    def update(self, dt, player): # player arg is unused
        self.handle_input(dt)

        # Update position
        self.pos += self.vel * dt

        # Update visuals
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
