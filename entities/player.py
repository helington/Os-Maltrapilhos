import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image_path = path.join(PLAYER_PATH, "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(230, 600))
        self.speed = 5
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
        
        if keys[pygame.K_w] and self.rect.bottom >= FLOOR_Y and not self.jumping:
            self.jumping = True
            self.gravity = -11

    def move(self, game):
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.dx -= self.speed
        elif self.moving_right:
            self.dx += self.speed

        if self.rect.bottom >= FLOOR_Y:
            self.jumping = False

        print(self.rect.x)
        self.rect.x += self.dx
        print(self.rect.x)
        self.rect.y += self.dy

        if self.rect.right > SCREEN_WIDTH - SCROLLING_THRESHOLD or self.rect.left < SCROLLING_THRESHOLD:
            self.rect.x -= self.dx
            game.screen_scroll = -self.dx

    def apply_gravity(self):
        self.gravity += 0.75
        self.rect.y += self.gravity
        self.rect.bottom = min(FLOOR_Y, self.rect.bottom)

    def update(self, game):
        self.handle_input()
        self.apply_gravity()
        self.move(game)