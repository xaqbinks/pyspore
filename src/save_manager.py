import json
import pygame
from src.entities.player import Player
from src.entities.ai_cell import AICell, MateCell, PreyCell
from src.entities.plant_food import PlantFood
from src.entities.environment import Meteorite, PartPickup
from src.parts_library import AVAILABLE_PARTS

class GameStateEncoder(json.JSONEncoder):
    """A custom JSON encoder to handle special game objects."""
    def default(self, obj):
        if isinstance(obj, pygame.math.Vector2):
            return {"__type__": "Vector2", "x": obj.x, "y": obj.y}
        # This encoder is now mainly for nested objects, not top-level entities.
        return super().default(obj)

def _entity_to_dict(entity):
    """Converts a game entity to a serializable dictionary."""
    entity_dict = {
        "__type__": entity.__class__.__name__,
        "pos": entity.pos
    }
    if isinstance(entity, Player):
        entity_dict["dna_points"] = entity.dna_points
        entity_dict["diet"] = entity.diet
        entity_dict["parts"] = [p.name for p in entity.parts]
    elif isinstance(entity, PartPickup):
        entity_dict["part_name"] = entity.part.name

    return entity_dict

def save_game(gameplay_state, slot="savegame.json"):
    """Saves the entire game state to a JSON file."""

    master_state = {
        "unlocked_parts": [part.name for part in AVAILABLE_PARTS if part.unlocked],
        "entities": []
    }

    # Serialize all sprites into dictionaries
    for sprite in gameplay_state.all_sprites:
        master_state["entities"].append(_entity_to_dict(sprite))

    try:
        with open(slot, 'w') as f:
            json.dump(master_state, f, cls=GameStateEncoder, indent=4)
        print(f"Game saved successfully to {slot}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def game_state_decoder(obj):
    """A custom JSON decoder for game state objects."""
    if "__type__" in obj:
        if obj["__type__"] == "Vector2":
            return pygame.math.Vector2(obj["x"], obj["y"])
    return obj

def load_game(slot="savegame.json"):
    """Loads a game state from a JSON file."""
    try:
        with open(slot, 'r') as f:
            master_state = json.load(f, object_hook=game_state_decoder)
        print(f"Game loaded successfully from {slot}")
        return master_state
    except FileNotFoundError:
        print(f"No save file found at {slot}")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None
