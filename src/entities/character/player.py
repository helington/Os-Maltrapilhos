import pygame

from .character import Character
from ...config.settings import *
from ...config.paths import *
from ..entities_enum import Direction, Weapon, Character_action, Character_type, Collectable_types

class Player(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)

        # specific animation handle to player
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0 
        self.alive = True
        temp_list = []


    def handle_input(self):
        self.moving_right = False
        self.moving_left = False

        keys = pygame.key.get_pressed()
        
        if self.action != Character_action.DEATH.value:
            if keys[pygame.K_c]:
                self.has_shot = True

            if keys[pygame.K_a]:
                self.update_action(Character_action.RUN.value)
                self.moving_left = True

            if keys[pygame.K_d]:
                self.update_action(Character_action.RUN.value)
                self.moving_right = True
            
            if keys[pygame.K_w] and not self.jumping:
                self.update_action(Character_action.JUMP.value)
                self.jumping = True
                self.gravity = -12       

    def check_collect_item(self, game):
        for collectable in game.collectables:
            if self.rect.colliderect(collectable.rect):
                game.collectables.remove(collectable)
                if collectable.type == Collectable_types.WEAPON:
                    self.weapon = collectable.item.value
                    self.ammo = collectable.value
        
    def update(self, game):
        super().update(game)
        if self.action == Character_action.DEATH.value:
            # todo death animations??
            self.alive = False
        self.handle_input()
        self.check_collect_item(game)
