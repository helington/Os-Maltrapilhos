

import pygame

from settings import *
from ..entities_enum import Direction, Weapon
from ..bullet import Bullet_props, Bullet

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.LEFT
        image_path = path.join(PLAYER_PATH, "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(630, 600))
        self.speed = 5
        self.hp = 3 # todo verificar
        self.moving_left = False
        self.moving_right = False
        self.jumping = True
        self.has_shot = False
        self.gravity = 0
        self.dy = 0
        self.dx = 0
        self.last_time_shot = 0
        self.weapon = Weapon.REGULAR.value

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_c]:
            self.has_shot = True

        if keys[pygame.K_a]:
            self.moving_left = True
        else:
            self.moving_left = False

        if keys[pygame.K_d]:
            self.moving_right = True
        else:
            self.moving_right = False
        
        if keys[pygame.K_w] and not self.jumping:
            self.jumping = True
            self.gravity = -12       

    def move(self, game, obstacle_list):
        game.screen_scroll = 0
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.dx -= self.speed
            self.direction = Direction.LEFT
        elif self.moving_right:
            self.direction = Direction.RIGHT
            self.dx += self.speed
            
        self.apply_gravity()

        for tile in obstacle_list:

            modifyed_rect_1 = pygame.Rect(self.rect.x + self.dx, self.rect.y, self.width, self.height)
            #check collision in the x direction
            if tile[1].colliderect(modifyed_rect_1):
                self.dx = 0
            
            modifyed_rect_2 = pygame.Rect(self.rect.x, self.rect.y + self.dy, self.width, self.height)
            #check for collision in the y direction
            if tile[1].colliderect(modifyed_rect_2):
                
                #check if below the ground, i.e. jumping
                if self.gravity < 0:
                    self.gravity = 0
                    self.dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.gravity >= 0:
                    self.gravity = 0
                    self.jumping = False
                    self.dy = tile[1].top - self.rect.bottom

        self.rect.x += self.dx
        self.rect.y += self.dy

        should_scroll = ( 
            self.rect.right > SCREEN_WIDTH - SCROLLING_THRESHOLD and self.direction == Direction.RIGHT or 
            self.rect.left < SCROLLING_THRESHOLD and self.direction == Direction.LEFT
        )
        if should_scroll:
            self.rect.x -= self.dx
            game.screen_scroll = -self.dx

    def shoot(self, game):
        time_last_shot = pygame.time.get_ticks() - self.last_time_shot
        cooldown_passed = time_last_shot > self.weapon["cooldown"]
        previous_shot = self.has_shot
        self.has_shot = False
        if previous_shot and cooldown_passed:
            self.last_time_shot = pygame.time.get_ticks()
            bullet_dx = DISTANCE_FROM_PLAYER if self.direction == Direction.RIGHT else -DISTANCE_FROM_PLAYER
            props = Bullet_props(self.weapon, self.rect.centerx + bullet_dx, self.rect.centery, self.direction)
            bullet = Bullet(props)
            game.bullets.add(bullet)

    def apply_gravity(self):
        self.gravity += 0.75
        if self.gravity > 10:
            self.gravity
        self.dy = self.gravity
        # self.rect.bottom = min(FLOOR_Y, self.rect.bottom)

    def handle_direction(self):
        sprite = pygame.image.load(path.join(PLAYER_PATH, "player.png")).convert_alpha()
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(sprite, True, False)
            self.image = pygame.transform.scale(self.image, (64, 64))
        else:
            self.image = pygame.transform.scale(sprite, (64, 64))

    def check_hurt(self, game):
        for bullet in game.bullets:
            if self.rect.colliderect(bullet.rect):
                game.bullets.remove(bullet)
                self.hp -= 1
                if self.hp <= 0:
                    game.john.remove(self)

    def update(self, game):
        # self.handle_input()
        handle_direction = self.handle_direction()
        self.check_hurt(game)
        # self.move(game, game.world.obstacle_list)
        # self.shoot(game)

