
import random
import pygame

from ..entities_enum import Character_action, Direction, Character_type
from .character import Character

class Enemy(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)
        self.world_x = x
        self.world_y = y

    def ai_behavior(self, game_screen_scroll):
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
    
    def update(self, game):
        self.rect.x += game.screen_scroll

        if self.action == Character_action.DEATH.value:
            self.update_animation()
            if self.index == len(self.animation_list[self.action]) - 1:
                game.enemies.remove(self)
            return

        super().update(game)

        self.ai_behavior(game.screen_scroll)
        self.update_animation()
