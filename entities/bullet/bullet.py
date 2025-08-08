import pygame
from os import path
from entities.entities_enum import Direction
from settings import BULLET_PATH
from .bullet_props import Bullet_props

class Bullet(pygame.sprite.Sprite):
    def __init__(self, props: Bullet_props):
        super().__init__()
        self.direction = props.direction
        
        image_path = path.join(BULLET_PATH, "bullet.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=(props.x, props.y))
        self.speed = props.speed
        self.damage = props.damage
        self.bullet_range = props.bullet_range
        self.last_move_time = 0

    def render_image(self):
        image_path = path.join(BULLET_PATH, "bullet.png")
        image = pygame.image.load(image_path).convert_alpha()
        sprite = pygame.transform.scale(self.image, (20, 20))
        if self.direction == Direction.LEFT:
            return pygame.transform.flip(sprite, True, False)
        return sprite

    def check_collision(self, game):
        for tile in game.world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # todo collision with characters

    def move(self, game):
        dx = self.speed if self.direction == Direction.RIGHT else -self.speed
        self.bullet_range -= 18
        self.rect.x += dx
        if self.bullet_range <= 0:
            self.kill()
        self.check_collision(game)

    def update(self, game):
        self.move(game)
