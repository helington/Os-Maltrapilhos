import pygame
import csv
from os import path

from settings import *

class Background:
    
    # Para a proporcao 800x200, 135p é a altura mínima do chao

    # init com variaveis, percorre as imagens na pasta
    def __init__(self):
        self.scroll = 0
        self.obstacle_list = list()

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
        self.world_data = list()

    def process_world_csv(self):
        for i in range(WOLRD_CSV_ROWS):
            row = [-1] * WOLRD_CSV_COLLUNMS
            self.world_data.append(row)

        level0_path = path.join(LEVELS_PATH, "level0_data.csv")
        with open(level0_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(reader):
                for j, tile in enumerate(row):
                    self.world_data[i][j] = int(tile)

    def process_data(self, tiles_image_list):
        for i, row in enumerate(self.world_data):
            for j, tile in enumerate(row):
                if tile >= 0:
                    image = tiles_image_list[tile]
                    image_rectangle = image.get_rect()
                    image_rectangle.x = j * TILE_SIZE
                    image_rectangle.y = i * TILE_SIZE
                    tile_data = (image, image_rectangle)

                    self.obstacle_list.append(tile_data)

    def draw_bg(self, screen):
        for x in range (10):
            speed = 1
            for i in self.images:
                screen.blit(i,((x*self.image_width) - self.scroll*speed,0))
                speed+=0.2

    def draw(self, screen, tiles_image_list):
        self.process_world_csv()
        self.process_data(tiles_image_list)
        self.draw_bg(screen)
        
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])