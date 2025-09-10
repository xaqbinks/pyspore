import pygame
import os
from src.states.base_state import BaseState
from src.config import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Background
from src.save_manager import load_game

class MainMenu(BaseState):
    def __init__(self):
        super().__init__()
        self.background = Background()

        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 32)

        self.title_text = self.title_font.render("Project Progenitus", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

        # New Game / Load Game buttons
        self.new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2, 300, 50)
        self.load_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 70, 300, 50)

        self.save_exists = os.path.exists("savegame.json")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.new_game_button.collidepoint(event.pos):
                self.done = True
                self.next_state = "diet_selection_menu"
            elif self.load_game_button.collidepoint(event.pos) and self.save_exists:
                self.load_saved_game()

    def load_saved_game(self):
        loaded_data = load_game()
        if loaded_data:
            self.persist['load_game_data'] = loaded_data
            self.done = True
            self.next_state = "gameplay"

    def update(self, dt):
        self.background.update(dt)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.background.draw(surface)
        surface.blit(self.title_text, self.title_rect)

        # Draw New Game button
        pygame.draw.rect(surface, (0, 100, 0), self.new_game_button)
        pygame.draw.rect(surface, WHITE, self.new_game_button, 2)
        new_game_text = self.button_font.render("New Game", True, WHITE)
        surface.blit(new_game_text, new_game_text.get_rect(center=self.new_game_button.center))

        # Draw Load Game button
        load_color = (0, 0, 100) if self.save_exists else (30, 30, 30)
        pygame.draw.rect(surface, load_color, self.load_game_button)
        pygame.draw.rect(surface, WHITE, self.load_game_button, 2)
        load_game_text = self.button_font.render("Load Game", True, WHITE)
        surface.blit(load_game_text, load_game_text.get_rect(center=self.load_game_button.center))
