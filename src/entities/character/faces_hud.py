
import pygame
from os import path
from ...config.paths import *


class Faces_hud (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.image = path.join(ICON_PATH, "icons1.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self, game):
        player_n = game.multiplayer_count
        self.image = path.join(ICON_PATH, f"icons{player_n}.png")
        self.image = pygame.image.load(self.image).convert_alpha()

