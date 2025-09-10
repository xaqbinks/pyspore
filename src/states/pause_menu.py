import pygame
from src.states.base_state import BaseState
from src.config import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.save_manager import save_game

class PauseMenu(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 48)
        self.gameplay_state = None

        # Button setup
        self.resume_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 200, 300, 50)
        self.save_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 300, 300, 50)
        self.main_menu_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 400, 300, 50)

        self.buttons = {
            "Resume": self.resume_button,
            "Save Game": self.save_button,
            "Main Menu": self.main_menu_button
        }

    def startup(self, persistent):
        super().startup(persistent)
        self.gameplay_state = self.persist.get('gameplay_state')

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "gameplay"
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.resume_button.collidepoint(event.pos):
                self.done = True
                self.next_state = "gameplay"
            elif self.save_button.collidepoint(event.pos):
                if self.gameplay_state:
                    save_game(self.gameplay_state)
            elif self.main_menu_button.collidepoint(event.pos):
                self.done = True
                self.next_state = "main_menu"

    def draw(self, surface):
        # Draw a semi-transparent overlay on top of the game
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Draw buttons
        for text, rect in self.buttons.items():
            pygame.draw.rect(surface, (50, 50, 50), rect)
            pygame.draw.rect(surface, WHITE, rect, 2)
            text_surf = self.font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)
