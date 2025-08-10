# this is the bubble effect, it probably shouldn't be in character, but it has no obvious home so...

import pygame
from os import path
from ..entities_enum import Direction
from ...config.paths import *

class Bubble(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.image = path.join(PLAYER_PATH, "bubble.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.player = player
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))

    def update(self, game):
        #self.x = self.player.x
        #self.y = self.player.y
        self.rect.center = self.player.rect.center

        if self.player.invincible == False:
            self.kill()

