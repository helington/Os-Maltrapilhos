import pygame
from os import path
from entities.entities_enum import Direction
from settings import BULLET_PATH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, damage: int, bullet_range: int, direction: int):
        super().__init__()
        self.direction = direction
        image_path = path.join(BULLET_PATH, "bullet.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.range = int
        self.last_move_time = 0

    def render_image(self):
        image_path = path.join(BULLET_PATH, "bullet.png")
        image = pygame.image.load(image_path).convert_alpha()
        sprite = pygame.transform.scale(self.image, (20, 20))
        if self.direction == Direction.LEFT:
            return pygame.transform.flip(sprite, True, False)
        return sprite

    def move(self):
        dx = self.speed
        self.range -= 1
        self.x += dx
        if self.x > self.range:
            self.x = 0
        self.draw(pygame.display.get_surface())
