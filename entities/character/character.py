

import random
import pygame

from settings import *
from ..entities_enum import Direction, Weapon
from ..bullet import Bullet_props, Bullet

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.LEFT
        self.animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0 #  0: idle, 1: run, 2: death
        temp_list = []
        for i in range(2):
            image_path = path.join(ENEMY_IDLE_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(10):
            image_path = path.join(ENEMY_RUN_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(12):
            image_path = path.join(ENEMY_DEATH_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.index]
        self.rect = self.image[0].get_rect(midbottom=(630, 600))
        self.speed = 5
        self.hp = 6 # todo verificar
        self.moving_left = False
        self.moving_right = False
        self.jumping = True
        self.has_shot = False
        self.gravity = 0
        self.dy = 0
        self.dx = 0
        self.last_time_shot = 0
        self.ai_update_time = pygame.time.get_ticks()
        self.ai_move_duration = 500  # Change direction every 1000 milliseconds
        self.weapon = Weapon.REGULAR.value

        self.width = self.image[0].get_width()
        self.height = self.image[0].get_height()

    def update_animation(self):
        
        animation_cooldown = 150
        #update image depending on current frame
        current_animation = self.animation_list[self.action]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index >= len(current_animation):
                self.index = 0
        
        self.image = current_animation[self.index]
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (64, 64))
        else:
            self.image = pygame.transform.scale(self.image, (64, 64))
    
    
    def ai_behavior(self):
        # Change movement every ai_move_duration milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - self.ai_update_time > self.ai_move_duration:
            self.ai_update_time = current_time
            # Random movement choice
            choice = random.randint(0, 2)
            if choice == 0:
                self.moving_left = True
                self.moving_right = False
            elif choice == 1:
                self.moving_right = True
                self.moving_left = False
            else:
                self.moving_left = False
                self.moving_right = False      

    def move(self, game, obstacle_list):
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.action = 1  # Running
            self.dx -= self.speed
            self.direction = Direction.LEFT
        elif self.moving_right:
            self.action = 1  # Running
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

    def check_hurt(self, game):
        for bullet in game.bullets:
            if self.rect.colliderect(bullet.rect):
                game.bullets.remove(bullet)
                self.hp -= bullet.damage
                if self.hp <= 0:
                    self.action = 2  # Death
                    game.john.remove(self)

    def update(self, game):
        # self.handle_input()
        self.ai_behavior()
        self.check_hurt(game)
        self.update_animation()
        self.move(game, game.world.obstacle_list)
        # self.shoot(game)

