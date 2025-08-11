import pygame
from os import path

from ...config.paths import HEALTH_PATH
from ...config.paths import *
from ...entities.character.player import Player

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player2: bool, player: Player):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player
        self.is_player2 = is_player2
        self.load_images()
        self.image = self.images[6]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update_heart(self):
        if self.player.alive:
            health = self.player.hp
            health = min(8, health)
            health = max(0, health)
        else:
            health = 0
        self.image = self.images[health]
    
    def load_images(self):
        images_list = []
        for i in range(9):
            image_path = path.join(HEALTH_PATH, f'heart{i}.png')
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (150, 50))
            images_list.append(image)

        self.images = images_list

    def update(self, game):
        #super().update()
        self.update_heart()