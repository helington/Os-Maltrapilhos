import pygame
from os import path

from settings import *

class Background:
    
    # Para a proporcao 800x200, 135p é a altura mínima do chao

    # init com variaveis, percorre as imagens na pasta
    def __init__(self):
        self.scroll = 0

        ground_path = path.join(GROUND_PATH, "ground.png")
        self.ground_v0 = pygame.image.load(ground_path).convert_alpha()
        self.ground = pygame.transform.scale(self.ground_v0,(160,80))
        self.ground_width = self.ground.get_width()
        self.ground_heigth = self.ground.get_height()
        self.images = []

        for i in range(1,6):
            current_image_path = path.join(BACKGROUND_PATH, f'plx-{i}.png')
            current_image_v0 = pygame.image.load(current_image_path).convert_alpha()
            current_image = pygame.transform.scale(current_image_v0,(800,800))
            self.images.append(current_image)

        self.image_width = current_image.get_width()

    def draw_bg(self, screen):
        for x in range (5):
            speed = 1
            for i in self.images:
                screen.blit(i,((x*self.image_width) - self.scroll*speed,0))
                speed+=0.2

    def draw_ground(self, screen):
        
        rect = pygame.Rect(550,200,200,100)
        pygame.draw.rect(screen,(133,44,76),rect)
        for x in range(15):
            screen.blit(self.ground, ((x* self.ground_width) - self.scroll *2.5,SCREEN_HEIGHT - self.ground_heigth))

    def draw(self, screen):
        self.draw_bg(screen)
        self.draw_ground(screen)
