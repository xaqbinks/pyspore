import pygame
import noise
import numpy as np
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Background:
    def __init__(self, num_layers=3):
        self.layers = []
        self.scroll_speeds = []

        for i in range(num_layers):
            # Make closer layers faster and more opaque
            speed = (i + 1) * 0.25
            alpha = 50 + i * 25
            color = (50 + i * 20, 80 + i * 30, 50 + i * 20) # Greenish hues

            self.scroll_speeds.append(speed)
            layer_surface = self.create_noise_layer(SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2, color, alpha, seed=i)
            self.layers.append({
                "surface": layer_surface,
                "x_pos": 0
            })

    def create_noise_layer(self, width, height, color, alpha, seed):
        """Creates a surface with a Perlin noise pattern."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for x in range(width):
            for y in range(height):
                # Use noise to vary the alpha value
                val = noise.pnoise2(x * 0.01 + seed, y * 0.01 + seed, octaves=2)

                # Map noise from [-1, 1] to [0, alpha]
                pixel_alpha = int((val + 1) / 2 * alpha)

                if pixel_alpha > 10: # Threshold to make it sparse
                    surface.set_at((x, y), (*color, pixel_alpha))

        return surface

    def update(self, dt):
        """Scrolls the layers."""
        for i, layer in enumerate(self.layers):
            layer["x_pos"] -= self.scroll_speeds[i]
            # Reset position to create an infinite loop
            if layer["x_pos"] <= -SCREEN_WIDTH:
                layer["x_pos"] = 0

    def draw(self, screen):
        """Draws all layers to the screen."""
        for layer in self.layers:
            screen.blit(layer["surface"], (layer["x_pos"], 0))
            screen.blit(layer["surface"], (layer["x_pos"] + SCREEN_WIDTH, 0)) # Draw a second time for seamless scrolling
