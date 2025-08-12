
import pygame
from os import path
from ...config.paths import *


class Price_hud (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        
        self.x = 1050
        self.y = 0

        self.test_font = pygame.font.Font(None, 150)
        
        self.image = path.join(ICON_PATH, "price.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


    def update(self, game):
        self.text_surface = self.test_font.render(str(5 - game.multiplayer_count), False, "Black") #this first number is the price
        self.image.fill((0, 0, 0, 0))  

        self.image = path.join(COLLECTABLES_PATH, "coin.png")
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150))

        W = self.text_surface.get_width()
        H = self.text_surface.get_height()
        self.image.blit(self.text_surface, (150/2 - W/2, 150/2 - H/2))
