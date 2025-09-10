import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK

from src.state_machine import StateMachine
from src.states.main_menu import MainMenu
from src.states.gameplay import Gameplay
from src.states.cell_editor import CellEditor
from src.states.win_screen import WinScreen
from src.states.pause_menu import PauseMenu
from src.states.diet_selection_menu import DietSelectionMenu

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.state_machine = StateMachine()
        states = {
            "main_menu": MainMenu(),
            "diet_selection_menu": DietSelectionMenu(),
            "gameplay": Gameplay(),
            "cell_editor": CellEditor(),
            "win_screen": WinScreen(),
            "pause_menu": PauseMenu(),
        }
        self.state_machine.setup_states(states, "main_menu")

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state_machine.get_event(event)

    def update(self):
        self.state_machine.update(self.dt)
        if self.state_machine.quit:
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.state_machine.draw(self.screen)
        pygame.display.flip()
