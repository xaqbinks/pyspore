import pygame
from src.states.base_state import BaseState
from src.config import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Background

class MainMenu(BaseState):
    def __init__(self):
        super().__init__()
        self.background = Background()

        self.title_font = pygame.font.Font(None, 64)
        self.prompt_font = pygame.font.Font(None, 32)

        self.title_text = self.title_font.render("Project Progenitus", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

        # Diet selection buttons
        self.herbivore_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2, 300, 50)
        self.carnivore_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 70, 300, 50)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.herbivore_button.collidepoint(event.pos):
                self.start_game('herbivore')
            elif self.carnivore_button.collidepoint(event.pos):
                self.start_game('carnivore')

    def start_game(self, diet):
        self.persist['diet'] = diet
        self.done = True
        self.next_state = "gameplay"

    def update(self, dt):
        self.background.update(dt)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.background.draw(surface)
        surface.blit(self.title_text, self.title_rect)

        # Draw buttons
        pygame.draw.rect(surface, (0, 100, 0), self.herbivore_button)
        pygame.draw.rect(surface, WHITE, self.herbivore_button, 2)
        herb_text = self.prompt_font.render("Begin as Herbivore", True, WHITE)
        surface.blit(herb_text, herb_text.get_rect(center=self.herbivore_button.center))

        pygame.draw.rect(surface, (100, 0, 0), self.carnivore_button)
        pygame.draw.rect(surface, WHITE, self.carnivore_button, 2)
        carn_text = self.prompt_font.render("Begin as Carnivore", True, WHITE)
        surface.blit(carn_text, carn_text.get_rect(center=self.carnivore_button.center))
