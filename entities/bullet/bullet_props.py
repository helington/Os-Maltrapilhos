from os import path
import pygame

from settings import BULLET_PATH
from ..entities_enum import Weapon, Direction, Team

class Bullet_props():
    def __init__(self, weapon: Weapon,  x: int, y: int, direction: Direction, team: Team):
        self.x = x
        self.y = y
        self.direction = direction
        self.team = team
        self.__dict__.update(weapon)

    @classmethod
    def get_image(cls, direction):
        image_path = path.join(BULLET_PATH, "bullet.png")
        image = pygame.image.load(image_path).convert_alpha()
        sprite = pygame.transform.scale(image, (20, 20))
        if direction == Direction.LEFT:
            return pygame.transform.flip(sprite, True, False)
        return sprite
        