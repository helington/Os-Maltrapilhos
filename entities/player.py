import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image_path = path.join(PLAYER_PATH, "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (y, y))
        self.rect = self.image.get_rect(midbottom=(x, 625))
        self.speed = 2
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.gravity = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.moving_left = True
        else:
            self.moving_left = False

        if keys[pygame.K_d]:
            self.moving_right = True
        else:
            self.moving_right = False
        
        if keys[pygame.K_w] and self.rect.bottom >= 625 and not self.jumping:
            self.jumping = True
            self.gravity = -11

    def move(self):
        if self.moving_left:
            self.rect.x -= self.speed
        elif self.moving_right:
            self.rect.x += self.speed

        if self.rect.bottom >= 625:
            self.jumping = False

    def apply_gravity(self):
        self.gravity += 0.75
        self.rect.y += self.gravity
        self.rect.bottom = min(625, self.rect.bottom)

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.move()