from enum import Enum

class TILES_TYPE(Enum):
    FLOOR_GRASS = 0
    FLOOR_DIRT = 4
    BOSS_LAB_FLOOR = 3
    BOSS_LAB_PLATFORM = 8
    WATER_SURFACE = 9
    WATER_DEEP = 10
    PLAYER = 15
    ENEMY = 16
    GATE = 20
    RIFLE = 17
    MINIGUN = 2
    COIN = 5
    ELSE = -1