import pygame
from src.assets.visual_generator import generate_blob_surface

class CellPart:
    def __init__(self, name, cost, stat_bonuses, image):
        """
        Represents a part that can be attached to a cell.

        :param name: The name of the part.
        :param cost: The DNA cost of the part.
        :param stat_bonuses: A dictionary of stat changes, e.g., {"speed": 50}.
        :param image: The pygame.Surface for the part's visual.
        """
        self.name = name
        self.cost = cost
        self.stat_bonuses = stat_bonuses
        self.image = image
        self.rect = self.image.get_rect()

# We can define a function to create a simple shape for a part
def create_part_image(width, height, color):
    """Creates a simple rectangular surface for a part."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)
    return surface
