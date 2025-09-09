import pygame
from src.states.base_state import BaseState
from src.config import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.parts_library import AVAILABLE_PARTS

class CellEditor(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.ui_buttons = []

    def startup(self, persistent):
        super().startup(persistent)
        self.player = self.persist.get("player")
        if not self.player:
            # This shouldn't happen, but as a fallback
            self.done = True
            self.next_state = "main_menu"
            return

        self.create_ui_buttons()

    def create_ui_buttons(self):
        self.ui_buttons = []
        unlocked_parts = [part for part in AVAILABLE_PARTS if part.unlocked]
        for i, part in enumerate(unlocked_parts):
            # Create a rect for the button
            button_rect = pygame.Rect(50, 50 + i * 60, 300, 50)
            # Create text for the button
            text = f"{part.name} (Cost: {part.cost})"
            self.ui_buttons.append({"rect": button_rect, "part": part, "text": text})

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "gameplay"
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.ui_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.buy_part(button["part"])
                    break

    def buy_part(self, part):
        if self.player.dna_points >= part.cost:
            self.player.dna_points -= part.cost
            self.player.add_part(part)

    def draw(self, surface):
        surface.fill(BLACK)

        # Draw the player cell in the center
        if self.player:
            player_rect = self.player.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            surface.blit(self.player.image, player_rect)

            # Draw DNA points
            dna_text = self.font.render(f"DNA: {self.player.dna_points}", True, WHITE)
            surface.blit(dna_text, (50, 10))

        # Draw UI buttons
        for button in self.ui_buttons:
            pygame.draw.rect(surface, (50, 50, 50), button["rect"])
            pygame.draw.rect(surface, WHITE, button["rect"], 2)
            text_surf = self.font.render(button["text"], True, WHITE)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            surface.blit(text_surf, text_rect)
