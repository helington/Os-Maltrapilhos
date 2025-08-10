import pygame

from .character import Character
from ...config.settings import *
from ...config.paths import *
from ..entities_enum import Direction, Weapon, Character_action, Character_type

class Player(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)
        self.direction = Direction.RIGHT
        
        # specific animation handle to player
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0 
        temp_list = []


    def handle_input(self):
        self.moving_right = False
        self.moving_left = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_c]:
            self.has_shot = True

        if keys[pygame.K_a]:
            self.action = Character_action.RUN.value
            self.moving_left = True

        if keys[pygame.K_d]:
            self.action = Character_action.RUN.value
            self.moving_right = True
         
        if keys[pygame.K_w] and not self.jumping:
            self.action = Character_action.JUMP.value
            self.jumping = True
            self.gravity = -12       

    def update_animation(self):
        
        animation_cooldown = 150 if self.action != Character_action.JUMP.value else 50 # Shrink cooldown if it is jumping

        #update image depending on current frame
        self.image = self.animation_list[self.action][self.index]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index >= len(self.animation_list):
                self.index = 0
        
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (64, 64))
        else:
            self.image = pygame.transform.scale(self.image, (64, 64))

    def check_collect_item(self, game):
        for collectable in game.collectables:
            if self.rect.colliderect(collectable.rect):
                game.collectables.remove(collectable)
                self
                if self.hp <= 0:
                    self.action = Character_action.DEATH.value
                    self.index = 0
                    self.update_time = pygame.time.get_ticks()


        

    def update(self, game):
        super().update(game)
        if self.action == Character_action.DEATH.value:
            # todo death animations??
            self.kill()
        self.handle_input()
        self.update_animation()
