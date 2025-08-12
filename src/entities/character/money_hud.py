
import pygame
from os import path
from ...config.paths import *

# WARNING
# This code looks very redundant, however, when I try to remove anything. it breaks a lot
# so please don't

class Money_hud (pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()

        self.player = player
        
        self.x = x
        self.y = y

        self.test_font = pygame.font.Font(None, 50)
        
        self.image = path.join(COLLECTABLES_PATH, "coin.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


    def update(self, game):
        self.text_surface = self.test_font.render(str(self.player.coins), False, "Black")
        self.image.fill((0, 0, 0, 0))  

        self.image = path.join(COLLECTABLES_PATH, "coin.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))

        W = self.text_surface.get_width()
        H = self.text_surface.get_height()
        self.image.blit(self.text_surface, (50/2 - W/2, 50/2 - H/2))

        