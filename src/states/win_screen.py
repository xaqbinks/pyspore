import pygame
from src.states.base_state import BaseState
from src.config import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class WinScreen(BaseState):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.Font(None, 72)
        self.prompt_font = pygame.font.Font(None, 36)

        self.title_text = self.title_font.render("You Evolved!", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))

        self.prompt_text = self.prompt_font.render("Press ESC to return to the Main Menu", True, WHITE)
        self.prompt_rect = self.prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "main_menu"

    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.title_text, self.title_rect)
        surface.blit(self.prompt_text, self.prompt_rect)
