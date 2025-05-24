from gupb.controller.norgul.arena_knowledge import ArenaKnowledge
from gupb.controller.norgul.misc import manhattan_dist

from gupb.model import arenas
from gupb.model import characters
from gupb.model import coordinates
from gupb.model import tiles


# -------------------
# Norgul memory class
# -------------------

# An abstraction for champion's memory
class Memory:
    
    def __init__(self):
        # Player state memory
        self.pos = None
        self.dir = None
        self.weapon = "knife"

        # Arena state memory
        self.arena = ArenaKnowledge()

        # Other things
        # ...
    
    # -------------
    # Static update
    # -------------

    def reset(self) -> None:
        self.current_pos = None
        self.current_dir = None
        self.current_weapon = "knife"

        self.arena.clear()
    
    # --------------
    # Dynamic update
    # --------------

    def update(self, knowledge: characters.ChampionKnowledge) -> None:
        self.pos = knowledge.position
        self.dir = knowledge.visible_tiles[self.pos].character.facing
        self.weapon = knowledge.visible_tiles[self.pos].character.weapon.name

        self.arena.update(knowledge)