import pygame
import csv
from os import path

from .background import Background
from .water import Water

from ..character.enemy import Enemy
from ..entities_enum import Character_type

from ...config.settings import *
from ...config.paths import *

class World:
    """World representation class."""

    def __init__(self, game):
        """Initilizates world attributes."""

        self.background = Background()
        self.obstacle_list = list()
        self.water_group = pygame.sprite.Group()
        self.images = []

        self.world_data = list()
        self.process_world_csv()
        self.process_data(game)

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

    def process_data(self, game):
        """Process the data matriz containing information about the wolrd creation of the current level."""

        self.level_length = len(self.world_data[0])

        for i, row in enumerate(self.world_data):
            for j, tile in enumerate(row):
                if tile >= 0:
                    image = game.tiles_image_list[tile]
                    image_rectangle = image.get_rect()
                    image_rectangle.x = j * TILE_SIZE
                    image_rectangle.y = i * TILE_SIZE
                    tile_data = (image, image_rectangle)

                    if tile < 9:
                        self.obstacle_list.append(tile_data)
                    elif tile < 11:
                        water = Water(image, j * TILE_SIZE, i * TILE_SIZE)
                        self.water_group.add(water)
                    elif tile == 16:
                        enemy = Enemy(Character_type.ENEMY.value, j * TILE_SIZE, i * TILE_SIZE)
                        game.enemies.add(enemy)


    def draw(self, screen, game):
        """Draw the world into game screen."""

        self.background.draw(screen, game.screen_scroll)
        self.water_group.draw(screen)
        
        for tile in self.obstacle_list:
            tile[1][0] += game.screen_scroll
            screen.blit(tile[0], tile[1])