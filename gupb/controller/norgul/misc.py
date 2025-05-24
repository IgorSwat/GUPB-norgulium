from gupb.model import coordinates


# -----------------------------------
# Helper functions - distance metrics
# -----------------------------------

# Manhattan distance metric
def manhattan_dist(coord1: coordinates.Coords, coord2: coordinates.Coords) -> int:
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

# Maximum (chebyshev) metric
def max_dist(coord1: coordinates.Coords, coord2: coordinates.Coords) -> int:
    return max(abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1]))