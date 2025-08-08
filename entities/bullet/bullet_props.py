from ..entities_enum import Weapon
from ..entities_enum import Direction

class Bullet_props():
    def __init__(self, weapon: Weapon,  x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.__dict__.update(weapon)