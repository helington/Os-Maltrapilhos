import pygame
from os import path

from settings import *

class Background:
    
    # Para a proporcao 800x200, 135p é a altura mínima do chao

    # init com variaveis, percorre as imagens na pasta
    def __init__(self):
        self.scroll = 0

        ground_path = path.join(GROUND_PATH, "ground.png")
        self.ground = pygame.image.load(ground_path).convert_alpha()
        self.ground_width = self.ground.get_width()
        self.ground_heigth = self.ground.get_height()
        self.images = []

        for i in range(1,6):
            current_image_path = path.join(BACKGROUND_PATH, f'plx-{i}.png')
            current_image = pygame.image.load(current_image_path).convert_alpha()
            self.images.append(current_image)

        self.image_width = current_image.get_width()

    def draw_bg(self, screen):
        for x in range (5):
            speed = 1
            for i in self.images:
                screen.blit(i,((x*self.image_width) - self.scroll*speed,0))
                speed+=0.2

    def draw_ground(self, screen):
        for x in range(15):
            screen.blit(self.ground, ((x* self.ground_width) - self.scroll *2.5,SCREEN_HEIGHT - self.ground_heigth))

    def draw(self, screen):
        self.draw_bg(screen)
        self.draw_ground(screen)