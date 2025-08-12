import pygame
import csv
from os import path

from .background import Background
from .water import Water

from ..character.enemy import Enemy
from ..entities_enum import Character_type

from ...config.settings import *
from ...config.paths import *
from .world_enum import TILES_TYPE

class World:
    """World representation class."""

    def __init__(self, game,level=0):
        """Initilizates world attributes."""

        self.background = Background()
        self.obstacle_list = list()
        self.water_group = pygame.sprite.Group()
        self.images = []
        self.level = level
        self.initialize_by_level(game)
        
        self.world_data = list()
        self.process_world_csv()
        self.process_data(game)

    def initialize_by_level(self, game):
        if self.level == 0:
            self.enemies = game.enemies
        if self.level == 1:
            self.enemies = game.enemies2
        if self.level == 2:
            self.enemies = game.enemies3

    def process_world_csv(self):
        """Process the csv data containing information about the world creation of the current level."""

        for i in range(WOLRD_CSV_ROWS):
            row = [-1] * WOLRD_CSV_COLLUNMS
            self.world_data.append(row)

        level_path = path.join(LEVELS_PATH, f"level{self.level}_data.csv")
        with open(level_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(reader):
                for j, tile in enumerate(row):
                    self.world_data[i][j] = int(tile)

    def process_data(self, game):
        """Process the data matriz containing information about the wolrd creation of the current level."""

        self.level_length = len(self.world_data[0])

        for i, row in enumerate(self.world_data):
            for j, tile in enumerate(row):
                if tile >= TILES_TYPE.FLOOR_GRASS.value: # = 0
                    image = game.tiles_image_list[tile]
                    image_rectangle = image.get_rect()
                    image_rectangle.x = j * TILE_SIZE
                    image_rectangle.y = i * TILE_SIZE
                    tile_data = (image, image_rectangle)

                    if tile in [TILES_TYPE.FLOOR_GRASS.value, TILES_TYPE.FLOOR_DIRT.value]:
                        self.obstacle_list.append(tile_data)
                    elif tile in [TILES_TYPE.WATER_DEEP.value, TILES_TYPE.WATER_SURFACE.value]:
                        water = Water(image, j * TILE_SIZE, i * TILE_SIZE)
                        self.water_group.add(water)
                    elif tile == TILES_TYPE.ENEMY.value:
                        enemy = Enemy(Character_type.ENEMY.value, j * TILE_SIZE, i * TILE_SIZE)
                        self.enemies.add(enemy)
        

    def restart_level(self, game):
        """Restart the current level by reloading the world data and resetting entities."""

        self.obstacle_list.clear()
        self.water_group.empty()
        game.enemies.empty()
        game.effects.empty()

        # Reset player positions
        for player in game.players:
            player.rect.x = 230
            player.rect.y = 400
        
        self.__init__(game)
        self.process_world_csv()
        self.process_data(game)

    
    def is_ground(self, x, y):
        point_rect = pygame.Rect(x, y, 1, 1)

        for tile in self.obstacle_list:
            if point_rect.colliderect(tile[1]):
                return True
            
        return False

    def draw(self, screen, game):
        """Draw the world into game screen."""

        self.background.draw(screen, game.screen_scroll)
        self.water_group.draw(screen)
        
        for tile in self.obstacle_list:
            tile[1][0] += game.screen_scroll
            screen.blit(tile[0], tile[1])