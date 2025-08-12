
import pygame
from os import path
from ...config.paths import *


class Price_hud (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 1050
        self.y = 0
        self.scale = (100,100)
        self.test_font = pygame.font.Font(None, 80)
        
        self.image = path.join(COLLECTABLES_PATH, "coin.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


    def update(self, game):
        self.text_surface = self.test_font.render(str(5 - game.multiplayer_count), False, "#172653") #this first number is the price
        self.image.fill((0, 0, 0, 0))
        
        self.image = path.join(COLLECTABLES_PATH, "coin.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scale)

        W = self.text_surface.get_width()
        H = self.text_surface.get_height()
        self.image.blit(self.text_surface, (self.scale[0]/2 - W/2, self.scale[0]/2 - H/2))
