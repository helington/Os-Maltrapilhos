import pygame
from ..entities_enum import Character_type


class Character_Props:
    def __init__(self, x, y, character: Character_type):
        self.x = x
        self.y = y
        self.__dict__.update(character.__dict__)