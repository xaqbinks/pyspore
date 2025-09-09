import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
