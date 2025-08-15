import math
import pygame
from os import path
from ...config.paths import COLLECTABLES_PATH
from .collectable_props import Collectable_Props
from ..entities_enum import Item_code

class Collectable(pygame.sprite.Sprite):
    def __init__(self, props: Collectable_Props):
        super().__init__()
        self.__dict__.update(props.__dict__)
        
        self.load_image()
        image_path = path.join(COLLECTABLES_PATH, self.image)
        image = pygame.image.load(image_path).convert_alpha()

        if self.image == "health_kit.png":
            scale = (60, 50)
        elif self.image == "coin.png":
            scale = (40, 40)
        else:
            scale = (64, 64)
        
        image = pygame.transform.scale(image, scale)
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction_handler = 0


    def load_image(self):
        if self.code == Item_code.COIN_CODE: self.image = "coin.png"
        if self.code == Item_code.BUBBLE_CODE: self.image = "bubble.png"
        if self.code == Item_code.MINIGUN_CODE: self.image = "minigun.png"
        if self.code == Item_code.RIFLE_CODE: self.image = "rifle.png"
        if self.code == Item_code.HEALTH_KIT_CODE: self.image = "health_kit.png"

    def move(self, ):
        oscilation_slowness = 100
        self.direction_handler = (self.direction_handler + 1) % oscilation_slowness
        amplitude = 18  
        offset = int(amplitude * math.sin(2 * math.pi * self.direction_handler / (oscilation_slowness)))
        self.rect.y = self.y + offset

    def update(self, game):
        self.rect.x += game.world.screen_scroll
        self.move()

