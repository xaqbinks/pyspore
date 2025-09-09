import pygame
import random
from src.states.base_state import BaseState
from src.config import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN
from src.entities.player import Player
from src.entities.plant_food import PlantFood
from src.entities.ai_cell import AICell, MateCell, PreyCell
from src.entities.environment import Meteorite, PartPickup
from src.environment import Background
from src.parts_library import AVAILABLE_PARTS
from src.assets.audio_generator import generate_sound

class Gameplay(BaseState):
    def __init__(self):
        super().__init__()
        self.background = Background()

    def startup(self, persistent):
        super().startup(persistent)
        self.diet = self.persist.get('diet', 'herbivore')

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.plant_food_group = pygame.sprite.Group()
        self.prey_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.mate_group = pygame.sprite.Group()
        self.meteorite_group = pygame.sprite.Group()
        self.part_pickup_group = pygame.sprite.Group()

        # Player
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, diet=self.diet)
        self.all_sprites.add(self.player)

        # Populate world
        self.populate_world()

        # Timers
        self.meteor_spawn_timer = 0
        self.meteor_spawn_interval = 10 # seconds

        # UI
        self.growth_bar_max_width = 200
        self.growth_bar_height = 20
        self.growth_bar_rect = pygame.Rect(10, 10, 0, self.growth_bar_height)

        # Pre-generate sounds
        self.sounds = {
            'eat_plant': generate_sound('sine', 600, 0.1, 0.4),
            'eat_prey': generate_sound('sawtooth', 300, 0.15, 0.5),
            'damage': generate_sound('noise', 200, 0.2, 0.6),
            'unlock': generate_sound('square', 880, 0.3, 0.5)
        }

    def populate_world(self):
        for _ in range(20):
            food = PlantFood(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.all_sprites.add(food)
            self.plant_food_group.add(food)
        for _ in range(10):
            prey = PreyCell(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.all_sprites.add(prey)
            self.prey_group.add(prey)
        for _ in range(5):
            enemy = AICell(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.all_sprites.add(enemy)
            self.enemy_group.add(enemy)
        mate = MateCell(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.all_sprites.add(mate)
        self.mate_group.add(mate)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "main_menu"

    def update(self, dt):
        self.background.update(dt)
        self.all_sprites.update(dt, self.player)

        # Spawn meteorites
        self.meteor_spawn_timer += dt
        if self.meteor_spawn_timer > self.meteor_spawn_interval:
            self.meteor_spawn_timer = 0
            meteorite = Meteorite()
            self.all_sprites.add(meteorite)
            self.meteorite_group.add(meteorite)

        self.handle_collisions()

        # Update UI and check win condition
        self.update_ui()

    def handle_collisions(self):
        # Diet-based eating
        if self.player.diet == 'herbivore':
            eaten_food = pygame.sprite.spritecollide(self.player, self.plant_food_group, True, pygame.sprite.collide_mask)
            if eaten_food:
                self.sounds['eat_plant'].play()
                base_dna = len(eaten_food) * 5
                self.player.dna_points += base_dna + self.player.diet_bonus
        elif self.player.diet == 'carnivore':
            eaten_prey = pygame.sprite.spritecollide(self.player, self.prey_group, True, pygame.sprite.collide_mask)
            if eaten_prey:
                self.sounds['eat_prey'].play()
                base_dna = len(eaten_prey) * 10
                self.player.dna_points += base_dna + self.player.diet_bonus

        # Enemy collision
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False, pygame.sprite.collide_mask):
            self.sounds['damage'].play()
            penalty = max(1, 50 - self.player.defense)
            self.player.dna_points = max(0, self.player.dna_points - penalty)

        # Mate collision
        if pygame.sprite.spritecollide(self.player, self.mate_group, False, pygame.sprite.collide_mask):
            self.persist["player"] = self.player
            self.done = True
            self.next_state = "cell_editor"

        # Meteorite collision
        meteor_collided = pygame.sprite.spritecollide(self.player, self.meteorite_group, True, pygame.sprite.collide_mask)
        if meteor_collided:
            self.sounds['damage'].play() # Re-use damage sound for impact
            self.spawn_part_pickup(meteor_collided[0].rect.center)

        # Part pickup collision
        pickup_collided = pygame.sprite.spritecollide(self.player, self.part_pickup_group, True, pygame.sprite.collide_mask)
        if pickup_collided:
            self.sounds['unlock'].play()
            for pickup in pickup_collided:
                pickup.part.unlocked = True

    def spawn_part_pickup(self, pos):
        locked_parts = [p for p in AVAILABLE_PARTS if not p.unlocked]
        if locked_parts:
            part_to_unlock = random.choice(locked_parts)
            pickup = PartPickup(pos[0], pos[1], part_to_unlock)
            self.all_sprites.add(pickup)
            self.part_pickup_group.add(pickup)

    def update_ui(self):
        dna_target = 200
        growth_percentage = min(self.player.dna_points / dna_target, 1.0)
        self.growth_bar_rect.width = self.growth_bar_max_width * growth_percentage
        if self.player.dna_points >= dna_target:
            self.done = True
            self.next_state = "win_screen"

    def draw(self, surface):
        surface.fill(BLACK)
        self.background.draw(surface)
        self.all_sprites.draw(surface)

        # Draw UI
        pygame.draw.rect(surface, WHITE, (10, 10, self.growth_bar_max_width, self.growth_bar_height), 2)
        pygame.draw.rect(surface, GREEN, self.growth_bar_rect)
