import pygame
import csv
from os import path

from settings import *

class Background:
    """Background representation class."""

    def __init__(self):
        """Initializates background attributes"""

        self.scroll = 0
        
        self.images = list()
        self.get_parellel_images()
    
    def get_parellel_images(self):
        """Get all parellel images and put them into images list."""
        
        for i in range(5):
            current_image_path = path.join(BACKGROUND_PATH, f'plx-{i + 1}.png')
            current_image = pygame.image.load(current_image_path).convert_alpha()
            current_image = pygame.transform.scale(current_image,(SCREEN_WIDTH, SCREEN_HEIGHT))
            self.images.append(current_image)

    def draw(self, screen, game_screen_scroll):

        """Draw background applying the scrolling."""
        self.scroll -= game_screen_scroll

        for x in range (10):
            speed = 0.5
            for i in self.images:
                screen.blit(i,((x*SCREEN_WIDTH) - self.scroll*speed,0))
                speed+=0.1

class Water(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class World:
    """World representation class."""

    def __init__(self, tiles_image_list):
        """Initilizates world attributes."""

        self.background = Background()
        self.obstacle_list = list()
        self.water_group = pygame.sprite.Group()
        self.images = []

        self.world_data = list()
        self.process_world_csv()
        self.process_data(tiles_image_list)

    def process_world_csv(self):
        """Process the csv data containing information about the world creation of the current level."""

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
        """Process the data matriz containing information about the wolrd creation of the current level."""

        self.level_length = len(self.world_data[0])

        for i, row in enumerate(self.world_data):
            for j, tile in enumerate(row):
                if tile >= 0:
                    image = tiles_image_list[tile]
                    image_rectangle = image.get_rect()
                    image_rectangle.x = j * TILE_SIZE
                    image_rectangle.y = i * TILE_SIZE
                    tile_data = (image, image_rectangle)

                    if tile < 9:
                        self.obstacle_list.append(tile_data)
                    elif tile < 11:
                        water = Water(image, i * TILE_SIZE, j * TILE_SIZE)
                        self.water_group.add(water)


    def draw(self, screen, game):
        """Draw the world into game screen."""

        self.background.draw(screen, game.screen_scroll)
        
        for tile in self.obstacle_list:
            tile[1][0] += game.screen_scroll
            screen.blit(tile[0], tile[1])