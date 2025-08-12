import pygame 
from os import path
from ...config.paths import GRAPHICS_PATH
from ...config.settings import TILE_SIZE

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load sprites
        self.image_closed = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_closed.png")).convert_alpha()
        self.image_open = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_open.png")).convert_alpha()
        self.image = self.image_closed
        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 9, TILE_SIZE * 10))

        # Rect for position
        self.rect = self.image.get_rect(topleft=(x, y))

        # Moviment
        self.speed = 2
        self.directions = ["right", "down", "left", "up"]
        self.current_dir = 0
        self.distance_moved = 0
        self.move_limit = 150

        # Attack
        self.attack_cooldown = 60
        self.attack_timer = 0
        # self.bullet_group = bullet_group
        # self.bullet_image = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_attack.png")).convert_alpha()

    # def update(self):
    #     # Movimento em losango
    #     direction = self.directions[self.current_dir]
    #     if direction == "right": self.rect.x += self.speed
    #     elif direction == "down":
    #         self.rect