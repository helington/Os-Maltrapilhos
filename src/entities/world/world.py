import pygame
import csv
from os import path

from .background import Background
from .water import Water
from ..boss.boss import Boss

from ..character.enemy import Enemy
from ..collectable import Collectable, Collectable_item, Collectable_Props
from ..entities_enum import Character_type

from ...config.settings import *
from ...config.paths import *
from .world_enum import TILES_TYPE

class World:
    def __init__(self, level=0):
        self.background = Background(level)
        self.obstacle_list = list()
        self.water_group = pygame.sprite.Group()
        self.images = []
        self.level = level
        self.enemies = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.tiles_image_list = list()
        self.screen_scroll = 0
        
        self.world_data = list()
        self.process_world_csv()
        self.get_tiles_images()
        self.process_data()

        self.bullets = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()
        if level == 2:
            self.boss.add(Boss(0, 0, self.bullets))

    def get_tiles_images(self):
        for i in range(TILE_TYPES):
            current_image_path = path.join(TILES_PATH, f"{i}.png")
            current_image = pygame.image.load(current_image_path)
            if i == TILES_TYPE.PLAYER:
                pass
            elif i == TILES_TYPE.ENEMY:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE * 2, TILE_SIZE * 2))
            else:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE, TILE_SIZE))
            self.tiles_image_list.append(current_image)

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

    def process_data(self):
        """Process the data matriz containing information about the wolrd creation of the current level."""

        self.level_length = len(self.world_data[0])

        for i, row in enumerate(self.world_data):
            for j, tile in enumerate(row):
                if tile >= TILES_TYPE.FLOOR_GRASS.value:
                    image = self.tiles_image_list[tile]
                    image_rectangle = image.get_rect()
                    image_rectangle.x = j * TILE_SIZE
                    image_rectangle.y = i * TILE_SIZE
                    tile_data = (image, image_rectangle)

                    if tile in [TILES_TYPE.FLOOR_GRASS.value, TILES_TYPE.FLOOR_DIRT.value, TILES_TYPE.FLOOR_BOSS_LEVEL.value, TILES_TYPE.BOSS_LAB_FLOOER.value]:
                        self.obstacle_list.append(tile_data)
                    elif tile in [TILES_TYPE.WATER_DEEP.value, TILES_TYPE.WATER_SURFACE.value]:
                        water = Water(image, j * TILE_SIZE, i * TILE_SIZE)
                        self.water_group.add(water)
                    elif tile == TILES_TYPE.RIFLE.value:
                        rifle = Collectable_Props(j * TILE_SIZE, i * TILE_SIZE, Collectable_item.RIFLE_ITEM)
                        self.collectables.add(Collectable(rifle))
                    elif tile == TILES_TYPE.MINIGUN.value:
                        minigun = Collectable_Props(j * TILE_SIZE, i * TILE_SIZE, Collectable_item.MINIGUN_ITEM)
                        self.collectables.add(Collectable(minigun))
                    elif tile == TILES_TYPE.COIN.value:
                        coin = Collectable_Props(j * TILE_SIZE, i * TILE_SIZE, Collectable_item.COIN_ITEM)
                        self.collectables.add(Collectable(coin))
                    elif tile == TILES_TYPE.ENEMY.value:
                        enemy = Enemy(Character_type.ENEMY.value, j * TILE_SIZE, i * TILE_SIZE)
                        self.enemies.add(enemy)

    
    def is_ground(self, x, y):
        point_rect = pygame.Rect(x, y, 1, 1)

        for tile in self.obstacle_list:
            if point_rect.colliderect(tile[1]):
                return True
            
        return False

    def draw(self, screen):
        """Draw the world into game screen."""

        self.background.draw(screen, self.screen_scroll)
        self.water_group.draw(screen)
        
        for tile in self.obstacle_list:
            tile[1][0] += self.screen_scroll
            screen.blit(tile[0], tile[1])