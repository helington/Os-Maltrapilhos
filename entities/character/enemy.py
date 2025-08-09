
import random
import pygame

from ..entities_enum import Character_action, Direction, Character_type
from .character import Character

class Enemy(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)

    def ai_behavior(self):
        # Change movement every ai_move_duration milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - self.ai_update_time > (self.ai_move_duration / 2):
            self.has_shot = True

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

    def update_animation(self):
        
        animation_cooldown = 150
        #update image depending on current frame
        current_animation = self.animation_list[self.action]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index >= len(current_animation):
                if self.action == Character_action.DEATH.value:  # If death animation, stay on last frame
                    self.index = len(current_animation) - 1
                else:
                    self.index = 0
        
        self.image = current_animation[self.index]
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (64, 64))
        else:
            self.image = pygame.transform.scale(self.image, (64, 64))
    
    def update(self, game):
        if self.action == Character_action.DEATH.value:
            self.update_animation()
            if self.index == len(self.animation_list[self.action]) - 1:
                game.enemies.remove(self)
            return

        super().update(game)
        self.ai_behavior()
        self.update_animation()