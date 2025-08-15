import pygame
from pygame import mixer
from os import path

from ..world import World
from .character import Character
from ...config.settings import *
from ...config.paths import *
from ..entities_enum import Character_action, Character_type, Collectable_types, Item_code, Collectable_item, Item_code
from .bubble import Bubble
from ..collectable.collectable import Collectable, Collectable_Props

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
        self.last_time_buy = 0
        self.joystick = None
        
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

    def add_joystick(self, joystick):
        self.joystick = joystick

    def handle_input(self):
        self.moving_right = False
        self.moving_left = False

        keys = pygame.key.get_pressed()
        
        if self.action != Character_action.DEATH.value:

            # Controller movement
            if self.joystick is not None:
                joystick_x = self.joystick.get_axis(0)

                DEAD_ZONE = 0.2

                if abs(joystick_x) < DEAD_ZONE:
                    joystick_x = 0

                if  self.joystick.get_button(2):
                    self.has_shot = True

                if joystick_x < 0:
                    self.update_action(Character_action.RUN.value)
                    self.moving_left = True

                if joystick_x > 0:
                    self.update_action(Character_action.RUN.value)
                    self.moving_right = True
                
                if self.joystick.get_button(0) and not self.jumping:
                    self.jump_fx.play()
                    self.update_action(Character_action.JUMP.value)
                    self.jumping = True 
                    self.gravity = -15

            # Keyboard movement
            else:
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
        for collectable in game.world.collectables:
            if self.rect.colliderect(collectable.rect):
                self.collect_fx.play()
                game.world.collectables.remove(collectable)
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
                if collectable.code == Item_code.HEALTH_KIT_CODE:
                    self.hp += 1
    
    def invincibility_track(self):
        if self.invincible == True:
            if pygame.time.get_ticks() >= self.expiration_date_bubble: 
                self.invincible = False

    def handle_transition(self, game, follow_player):    
        if self.rect.x > 1130 and self is follow_player:
            game.load_next_level()

    def purchase(self, game):
        keys = pygame.key.get_pressed()

        can_buy = False
        if self.joystick is not None:
            if self.joystick.get_button(1):
                can_buy = True
        else:
            if keys[self.controll.buy]:
                can_buy = True
        
        if can_buy and self.coins >= 5 - game.multiplayer_count:
            curr_time = pygame.time.get_ticks()
            buy_cooldown_passed = (curr_time - self.last_time_buy) > 300
            self.last_time_buy = curr_time
            if buy_cooldown_passed:
                self.coins -= 5 - game.multiplayer_count
                health_kit_props = Collectable_Props(self.rect.centerx, self.rect.centery - 128, Collectable_item.HEALTH_KIT_ITEM) # 128 is an arbitrary amount by which the medikit spawns above the player!
                game.world.collectables.add(Collectable(health_kit_props))

    def update(self, game, follow_player):
        super().update(game, follow_player)
        self.handle_input()
        self.handle_transition(game,follow_player)
        self.check_collect_item(game)
        self.invincibility_track()
        self.purchase(game)

        is_on_border = self.rect.left < 0 or self.rect.right > SCREEN_WIDTH
        should_be_dragged_by_scroll = (
            self.hp > 0 and
            is_on_border
        )
        if not should_be_dragged_by_scroll and self is not follow_player:
            self.rect.x += game.world.screen_scroll