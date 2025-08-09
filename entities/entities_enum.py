from enum import Enum

class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class Weapon(Enum):
    REGULAR = {"damage": 2, "speed": 10, "bullet_range": 900, "cooldown": 300}
    RIFLE = {"damage": 6, "speed": 12, "bullet_range": 1200, "cooldown": 450}
    MINIGUN = {"damage": 2, "speed": 14, "bullet_range": 900, "cooldown": 100}
