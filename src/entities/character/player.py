import pygame
from pygame import mixer
from os import path
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
        temp_list = []
        self.is_player2 = is_player2
        self.last_tile_x = (WOLRD_CSV_COLLUNMS) * TILE_SIZE
        
        #sound effects
        pygame.mixer.set_num_channels(800)  # Add two channels for player sounds
        self.gunshot_fx = pygame.mixer.Sound(path.join(SOUNDS_PATH, 'shot2.mp3'))
        self.gunshot_fx.set_volume(0.2)
        self.jump_fx = pygame.mixer.Sound(path.join(SOUNDS_PATH, 'jump.mp3'))
        self.jump_fx.set_volume(0.15)
        self.collect_fx = pygame.mixer.Sound(path.join(SOUNDS_PATH, 'collect.mp3'))
        self.collect_fx.set_volume(0.3)

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
                self.jump_fx.play()
                self.update_action(Character_action.JUMP.value)
                self.jumping = True
                self.gravity = -15   

    def check_collect_item(self, game):
        
        if self.action == Character_action.DEATH.value:
            return
        
        for collectable in game.collectables:
            if self.rect.colliderect(collectable.rect):
                self.collect_fx.play()
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

    def handle_transition(self, game,follow_player):
        
        if self.rect.x > 1130 and self is follow_player:
            game.__init__()
            game.world = game.world3
    
    def update(self, game, follow_player):
        super().update(game, follow_player)
        self.handle_input()
        self.handle_transition(game,follow_player)
        self.check_collect_item(game)
        self.invincibility_track()


        is_on_border = self.rect.left < 0 or self.rect.right > SCREEN_WIDTH
        should_be_dragged_by_scroll = (
            self.hp > 0 and
            is_on_border
        )
        if not should_be_dragged_by_scroll and self is not follow_player:
            self.rect.x += game.screen_scroll
