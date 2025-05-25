# ------------------------------------
# Norgul hyperparameters - exploration
# ------------------------------------

EXPLORATION_MAX_TIME_DIFF = 50
EXPLORATION_TIME_FACTOR = 1.3
EXPLORATION_DISTANCE_FACTOR = 0.5


# ----------------------------------------
# Norgul hyperparameters - item collection
# ----------------------------------------

WEAPON_VALUES = {
    "bow": 0.8,
    "bow_unloaded": 0.8,
    "bow_loaded": 0.8,
    "knife": 1.0,
    "sword": 2.5,
    "axe": 5.0,
    "amulet": 0.0,
    "scroll": 0.0
}

POTION_VALUE = 2.0

COLLECTION_BASE_FACTOR = 1000.0
COLLECTION_DISTANCE_FACTOR = 0.9
COLLECTION_ENEMY_FACTOR = 0.5