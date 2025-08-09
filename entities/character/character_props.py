from os import path
import pygame
from settings import PLAYER_PATH
from ..entities_enum import Direction, Character_type, Weapon


class Character_Props:
    def __init__(self, x, y, character: Character_type):
        self.x = x
        self.y = y
        self.__dict__.update(character.__dict__)