import pygame

from .character import Character
from ...config.settings import *
from ...config.paths import *
from ..entities_enum import Character_action, Character_type, Collectable_types, Item_code
from .bubble import Bubble

class Player(Character):
    def __init__(self, character_info: Character_type, x, y, is_player2: bool):
        super().__init__(character_info, x, y)

        # specific animation handle to player
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0 
        self.coins = 0
        self.alive = True
        temp_list = []
        self.is_player2 = is_player2

        self.invincible = False 
        self.expiration_date_bubble = 0 #this is the time the last bubble was obtained in, in miliseconds

    def handle_input(self):
        self.moving_right = False
        self.moving_left = False

        keys = pygame.key.get_pressed()
        
        if self.action != Character_action.DEATH.value:
            if keys[self.controll.shoot]:
                self.has_shot = True

            if keys[self.controll.left]:
                self.update_action(Character_action.RUN.value)
                self.moving_left = True

            if keys[self.controll.right]:
                self.update_action(Character_action.RUN.value)
                self.moving_right = True
            
            if keys[self.controll.up] and not self.jumping:
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
                if collectable.code == Item_code.BUBBLE_CODE:
                    self.invincible = True
                    self.expiration_date_bubble = pygame.time.get_ticks() + collectable.item['value']
                    my_bubble = Bubble(self)
                    game.effects.add(my_bubble)
                if collectable.code == Item_code.COIN_CODE:
                    self.coins += 1
    
    def invincibility_track(self):
        if self.invincible == True:
            if pygame.time.get_ticks() >= self.expiration_date_bubble: 
                self.invincible = False

    def update(self, game):
        super().update(game)
        if self.action == Character_action.DEATH.value:
            self.alive = False
        self.handle_input()
        self.check_collect_item(game)
        self.invincibility_track()

        if self.controll.up != pygame.K_w:
            self.rect.x += game.screen_scroll
