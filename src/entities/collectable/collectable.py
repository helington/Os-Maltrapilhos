import math
import pygame
from os import path
from ...config.paths import COLLECTABLES_PATH
from .collectable_props import Collectable_Props

class Collectable(pygame.sprite.Sprite):
    def __init__(self, props: Collectable_Props):
        super().__init__()
        self.__dict__.update(props.__dict__)
        
        image_path = path.join(COLLECTABLES_PATH, self.image)
        image = pygame.image.load(image_path).convert_alpha()
        scale = (64, 64) if self.image != "coin.png" else (40, 40)
        image = pygame.transform.scale(image, scale)
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction_handler = 0

    def move(self):
        oscilation_slowness = 100
        self.direction_handler = (self.direction_handler + 1) % oscilation_slowness
        amplitude = 18  
        offset = int(amplitude * math.sin(2 * math.pi * self.direction_handler / (oscilation_slowness)))
        self.rect.y = self.y + offset

    def update(self, game):
        self.rect.x += game.screen_scroll
        self.move()
