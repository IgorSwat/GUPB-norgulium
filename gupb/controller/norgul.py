import heapq
import random

from math import inf

from gupb import controller
from gupb.model import arenas
from gupb.model import characters
from gupb.model import coordinates
from gupb.model import tiles

POSSIBLE_ACTIONS = [
    characters.Action.TURN_LEFT,
    characters.Action.TURN_RIGHT,
    characters.Action.STEP_FORWARD,
    characters.Action.ATTACK,
]


class NorgulController(controller.Controller):
    def __init__(self, first_name: str = "Norgul"):
        self.first_name: str = first_name

        # Global arena state
        # - Used to build connection graph and find path to given square
        self.arena_width = 0
        self.arena_height = 0
        self.arena : dict[coordinates.Coords, tiles.TileDescription] = {}


    def __eq__(self, other: object) -> bool:
        if isinstance(other, NorgulController):
            return self.first_name == other.first_name
        return False


    def __hash__(self) -> int:
        return hash(self.first_name)


    def decide(self, knowledge: characters.ChampionKnowledge) -> characters.Action:
        return random.choice(POSSIBLE_ACTIONS)


    def praise(self, score: int) -> None:
        pass


    def reset(self, game_no: int, arena_description: arenas.ArenaDescription) -> None:
        arena_path = "resources/arenas/" + arena_description.name + ".gupb"
        self._load_arena_state(arena_path)


    def _load_arena_state(self, arena_path: str) -> None:
        ''' Loads and saves given arena state'''

        with open(arena_path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                for j, tile in enumerate(line):
                    if str.isspace(tile):
                        continue

                    coords = coordinates.Coords(i, j)
                    tile_type = arenas.TILE_ENCODING[tile] if not str.isalpha(tile) else tiles.Land
                    tile_name = tile_type.__name__.lower()
                    weapon_name = arenas.WEAPON_ENCODING[tile].__name__.lower() if str.isalpha(tile) else None

                    self.arena[coords] = tiles.TileDescription(tile_name, weapon_name, None, None, None)

                    self.arena_width = j + 1
                
                self.arena_height = i + 1
    

    def _find_path(self, sq_from: coordinates.Coords, sq_to: coordinates.Coords) -> coordinates.Coords:
        '''
            Performs Djikstra algorithm to find the best (defined by connection weights) path from sq_from to sq_to.

            Returns next square on the quickest path from sq_from to sq_to.
            Alternatively, if sq_to is unreachable, returns next square on the quickest path to square that is closest to sq_to.
        '''

        if sq_from == sq_to:
            return sq_to

        # Initialize distances to each square
        distances = {coord: inf for coord in self.arena}
        distances[sq_from]

        # Priority queue representation
        # - First value is a distance to given square
        heap = []
        heapq.heappush(heap, (0, sq_from))

        # Save previously searched squares to reconstruct the best path
        previous = {coord: None for coord in self.arena}
        closest_alternative = None
        closest_dist = inf

        while heap:
            dist, sq = heapq.heappop(heap)

            if sq == sq_to:
                break

            for neighbor in self._connections(sq):
                cost = self._connection_cost(sq, neighbor)

                new_dist = dist + cost
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = sq
                    heapq.heappush(heap, (new_dist, neighbor))
            
            # Update closest alternative path
            # - Manhattan metric
            metric_value = abs(sq[0] - sq_to[0]) + abs(sq[1] - sq_to[1])
            if metric_value < closest_dist:
                closest_alternative = sq
                closest_dist = metric_value

        
        # Reconstruct the path
        current_sq = sq_to

        # No path from sq_from to sq_to
        # - In this case we want to return a path to square which is as close to sq_to as possible
        if previous[current_sq] is None:
            current_sq = closest_alternative
        
        while previous[current_sq] != sq_from:
            current_sq = previous[current_sq]
        
        return current_sq
    

    def _connection_cost(self, sq_from: coordinates.Coords, sq_to: coordinates.Coords) -> float:
        ''' Calculates and returns heuristic cost of moving from square sq_from to square sq_to.
        
            In other words, it returns a weight of an edge between sq_from and sq_to or 
            infinity if sq_from and sq_to are not directly connected.
        '''

        if sq_from == sq_to:
            return 0.0
        
        # Squares not connected
        if abs(sq_from[0] - sq_to[0]) + abs(sq_from[1] - sq_to[1]) != 1:
            return inf
        
        # Stone or sea on target square
        if self.arena[sq_to].type in ["sea", "wall"]:
            return inf

        # Some other character blocking the pass
        if self.arena[sq_to].character is not None:
            return inf
        
        cost = 1.0

        # Penalize walking through mist or fire
        if self.arena[sq_to].effects and "mist" in self.arena[sq_to].effects:
            cost += 5
        if self.arena[sq_to].effects and "fire" in self.arena[sq_to].effects:
            cost += 10

        return cost
    

    def _connections(self, sq_from: coordinates.Coords) -> list[coordinates.Coords]:
        ''' Returns all adjacent squares (which can be accessed in one move from sq_from)'''

        squares = [(sq_from[0] - 1, sq_from[1]),
                   (sq_from[0], sq_from[1] + 1),
                   (sq_from[0] + 1, sq_from[1]),
                   (sq_from[0], sq_from[1] - 1)]

        return [sq for sq in squares if 0 <= sq[0] < self.arena_height and 0 <= sq[1] < self.arena_width]


    @property
    def name(self) -> str:
        return f'{self.first_name}'

    @property
    def preferred_tabard(self) -> characters.Tabard:
        return characters.Tabard.NORGUL


POTENTIAL_CONTROLLERS = [
    NorgulController("Norgul"),
]