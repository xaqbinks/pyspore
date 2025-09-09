from src.entities.cell_part import CellPart, create_part_image
from src.config import WHITE

# Add an 'unlocked' flag to each part's dictionary representation
def create_part(name, cost, bonuses, image, unlocked=False):
    part = CellPart(name, cost, bonuses, image)
    part.unlocked = unlocked
    return part

# A library of all available parts in the game
AVAILABLE_PARTS = [
    create_part(
        name="Flagellum",
        cost=25,
        bonuses={"speed": 40},
        image=create_part_image(30, 8, (200, 200, 200)),
        unlocked=True
    ),
    create_part(
        name="Cilia",
        cost=15,
        bonuses={"turning_speed": 100},
        image=create_part_image(5, 10, (200, 200, 200)),
        unlocked=True
    ),
    create_part(
        name="Jets",
        cost=75,
        bonuses={"speed": 100},
        image=create_part_image(20, 10, (255, 165, 0)) # Orange
    ),
    create_part(
        name="Spike",
        cost=40,
        bonuses={"defense": 10},
        image=create_part_image(15, 15, (255, 0, 0))
    ),
    create_part(
        name="Proboscis",
        cost=30,
        bonuses={"herbivore_bonus": 5},
        image=create_part_image(20, 5, (0, 200, 50)) # Greenish
    ),
    create_part(
        name="Jaw",
        cost=30,
        bonuses={"carnivore_bonus": 8},
        image=create_part_image(15, 10, (200, 50, 50))
    )
]
