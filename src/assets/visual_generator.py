import pygame
import noise
import numpy as np
from src.config import WHITE

def generate_blob_points(size, complexity, seed):
    """
    Generates a list of points for a blob shape using Perlin noise.

    :param size: The average radius of the blob.
    :param complexity: How detailed/jagged the blob shape is. Higher is more complex.
    :param seed: A random seed for the noise generator.
    :return: A list of (x, y) tuples representing the blob's vertices.
    """
    points = []
    num_points = 100 # More points make a smoother curve

    for i in range(num_points):
        angle = (i / num_points) * 2 * np.pi

        # Use Perlin noise to vary the radius
        noise_val = noise.pnoise1(seed + i * complexity, octaves=4, persistence=0.5, lacunarity=2.0)
        radius = size + (noise_val * size * 0.4) # vary radius by up to 40%

        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        points.append((x, y))

    return points

def generate_blob_surface(size, complexity, seed, color=WHITE):
    """
    Generates a pygame.Surface with a procedurally generated blob drawn on it.

    :param size: The average radius of the blob.
    :param complexity: The complexity of the blob's shape.
    :param seed: A random seed for the noise generator.
    :param color: The color of the blob.
    :return: A tuple of (pygame.Surface, pygame.mask.Mask)
    """
    points = generate_blob_points(size, complexity, seed)

    # Find the bounding box of the points to size the surface
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    width = int(max_x - min_x) + 4 # Add padding
    height = int(max_y - min_y) + 4

    # Create a surface that fits the blob
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Translate points to be relative to the surface's top-left corner
    translated_points = [(p[0] - min_x + 2, p[1] - min_y + 2) for p in points]

    # Draw the blob
    pygame.draw.polygon(surface, color, translated_points)

    # Create a mask for pixel-perfect collision
    mask = pygame.mask.from_surface(surface)

    return surface, mask
