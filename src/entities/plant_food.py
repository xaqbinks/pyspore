import pygame
import time
from src.entities.entity import Entity
from src.assets.visual_generator import generate_blob_surface
from src.config import WHITE

class PlantFood(Entity):
    def __init__(self, x, y):
        size = 10
        image, _ = generate_blob_surface(
            size=size,
            complexity=0.3,
            seed=time.time() + x + y, # Use position to vary seed
            color=WHITE
        )
        super().__init__(x, y, image)
