from gupb.controller.norgul.memory import Memory
from gupb.controller.norgul.navigation import Navigator

from gupb.model import arenas
from gupb.model import characters
from gupb.model import coordinates

import numpy as np

from math import sqrt
from itertools import product


# --------------------
# Norgul's brain class
# --------------------

class Brain:

    def __init__(self, memory: Memory):
        # Memory connection
        self.memory = memory

        # Brain components
        self.navigator = Navigator(self.memory.arena)

        # Hyperparameters
        # TODO: move into separate config file
        self.radius = 4
        self.mist_vec_weight = 50
        self.enemy_vec_weight = 5
    

    # TODO: replace with better code
    def pick_target(norgul):
        if not norgul.memory.arena.any_mist:
            if norgul.memory.arena[norgul.memory.pos].type == "forest":
                return norgul.memory.pos
            
            target_sq = norgul.memory.arena.nearest_forest(norgul.memory.pos)
            if target_sq is not None:
                return target_sq

        # Calculate current important zone around our character
        character_zone = [norgul.memory.pos + diff for diff in product(range(-norgul.radius, norgul.radius + 1),
                                                                       range(-norgul.radius, norgul.radius + 1))]
        character_zone = [sq for sq in character_zone if 0 <= sq[0] < norgul.memory.arena.height and 0 <= sq[1] < norgul.memory.arena.width]
        
        # Target vector
        target_vec = np.array([0.0, 0.0])

        # Mist center calculation
        mist_mean = np.array([0.0, 0.0])
        mist_count = 0

        for sq in character_zone:
            if norgul.memory.arena[sq].effects and ("mist",) in norgul.memory.arena[sq].effects:
                mist_mean = mist_mean + sq
                mist_count += 1
            if norgul.memory.arena[sq].character is not None and sq != norgul.memory.pos:
                vec = np.array(norgul.memory.pos) - sq
                target_vec = target_vec + (vec * norgul.enemy_vec_weight)
        
        # Calculate mist center and add mist vector
        if mist_count > 0:
            mist_mean = mist_mean / mist_count
            vec = np.array(norgul.memory.pos) - mist_mean
            target_vec = target_vec + (vec * norgul.mist_vec_weight)
        
        
        if target_vec[0] == 0 and target_vec[1] == 0:
            return norgul.memory.pos
        
        # Normalize target vector
        target_vec = target_vec * (1 / sqrt(target_vec[0] ** 2 + target_vec[1] ** 2))

        target_sq = norgul.memory.pos
        for i in range(1, 10):
            some_sq = np.array(norgul.memory.pos) + target_vec * i
            some_sq = coordinates.Coords(int(some_sq[0]), int(some_sq[1]))
            if not (0 <= some_sq[0] < norgul.memory.arena.width) or not (0 <= some_sq[1] < norgul.memory.arena.height):
                continue
            if abs(some_sq[0] - norgul.memory.pos[0]) <= norgul.radius and abs(some_sq[1] - norgul.memory.pos[1]) <= norgul.radius:
                target_sq = some_sq
        
        return target_sq

    # TODO: replace with better code
    def move_to_target(norgul, target, fast=False):
        """If Fast -> do not waste moves to turn"""

        next_sq = norgul.navigator.find_path(norgul.memory.pos, target)

        if norgul.memory.pos != next_sq:
            if next_sq != norgul.memory.pos + norgul.memory.dir.value:
                if next_sq == norgul.memory.pos + norgul.memory.dir.turn_right().value:
                    return characters.Action.TURN_RIGHT if not fast else characters.Action.STEP_RIGHT
                elif next_sq == norgul.memory.pos + norgul.memory.dir.turn_left().value:
                    return characters.Action.TURN_LEFT if not fast else characters.Action.STEP_LEFT
                else:
                    return characters.Action.TURN_LEFT if not fast else characters.Action.STEP_BACKWARD
            elif norgul.memory.arena[next_sq].character is not None:
                return characters.Action.ATTACK
            else:
                return characters.Action.STEP_FORWARD

        
        elif norgul.memory.arena[norgul.memory.pos + norgul.memory.dir.value].character is not None:
            if norgul.memory.arena[norgul.memory.pos + norgul.memory.dir.value].type == "forest":
                return None
            return characters.Action.ATTACK