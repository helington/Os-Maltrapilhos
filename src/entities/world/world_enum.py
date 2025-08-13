from enum import Enum

class TILES_TYPE(Enum):
    FLOOR_GRASS = 0
    FLOOR_DIRT = 4
    WATER_SURFACE = 9
    WATER_DEEP = 10
    PLAYER = 15
    ENEMY = 16
    GATE = 20
    ELSE = -1