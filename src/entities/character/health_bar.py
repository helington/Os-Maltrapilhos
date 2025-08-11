import pygame
from os import path

from ...config.paths import HEALTH_PATH
from ...config.paths import *

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.load_images()
        self.image = self.images[6]
        self.rect = self.image.get_rect()

    def update_heart(self, game):
        player_list = list(game.player)
        if len(player_list) > 0:
            health = player_list[0].hp
        else:
            health = 0
        self.image = self.images[health]
    
    def load_images(self):
        images_list = []
        for i in range(9):
            image_path = path.join(HEALTH_PATH, f'heart{i}.png')
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (100, 50))
            images_list.append(image)

        self.images = images_list

    def update(self, game):
        #super().update()
        self.update_heart(game)