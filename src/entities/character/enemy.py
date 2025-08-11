
import random
import pygame

from ..entities_enum import Character_action, Direction, Character_type, Collectable_item, Item_code
from .character import Character

from ..collectable.collectable import Collectable, Collectable_Props

class Enemy(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)
        self.world_x = x
        self.world_y = y
        self.vision = pygame.Rect(0, 0, 150, 20)

    def update_moving(self, left, right):
        self.moving_left = left
        self.moving_right = right

    def check_danger(self, world):
        direction_to_consider = 1 if self.direction == Direction.RIGHT else -1

        test_x = self.rect.x + (self.width / 2) + (self.width / 2) * direction_to_consider
        test_y = self.rect.bottom + 1

        if not world.is_ground(test_x, test_y):
            return True
        else:
            return False

    def ai_behavior(self, players, world):
        # Change movement every ai_move_duration milliseconds
        current_time = pygame.time.get_ticks()

        some_target_in_vision = False

        for player in players:
            # if player is in enemy field of view
            if player.alive and not some_target_in_vision:
                if self.vision.colliderect(player):
                    self.update_action(Character_action.IDLE.value)
                    some_target_in_vision = True
                else:
                    direction_vision = -75 if self.direction == Direction.LEFT else 75
                    self.vision.center = (self.rect.centerx + direction_vision, self.rect.centery)
            
        if some_target_in_vision:
            self.has_shot = True
        else:
            self.has_shot = False

        # if enemy is in a danger place
        if self.check_danger(world):
            if self.direction == Direction.RIGHT:
                self.update_moving(True, False)
            else:
                self.update_moving(False, True)

        elif current_time - self.ai_update_time > self.ai_move_duration:
            self.ai_update_time = current_time
            # Random movement choice
            choice = random.randint(0, 2)
            if choice == 0:
                self.update_moving(True, False)
            elif choice == 1:
                self.update_moving(False, True)
            else:
                self.update_moving(False, False)
    
    def update(self, game, follow_player):
        self.game = game # i believe this is needed for dropping loot
        self.rect.x += game.screen_scroll

        if self.action == Character_action.DEATH.value:
            self.update_animation()
            if self.index == len(self.animation_list[self.action]) - 1:
                self.drop_loot()
                game.enemies.remove(self)
            return

        super().update(game, follow_player)

        self.ai_behavior(game.players.sprites(), game.world)
        self.update_animation()

    def drop_loot(self):
        # this function is full of magic numbers, here is how it works, 80% something drops, 50% its health kit, 50% its bubble
        # this function can also be simplified in the future
        drop_options = [Item_code.BUBBLE_CODE, Item_code.HEALTH_KIT_CODE, Item_code.COIN_CODE]
        drop_weights = [0.25, 0.25, 0.50]
        drop_choice = random.choices(drop_options, drop_weights, k=1)[0]
        if drop_choice == Item_code.BUBBLE_CODE:
            bubble_props = Collectable_Props(self.rect.centerx, self.rect.centery - 20, Collectable_item.BUBBLE_ITEM)
            self.game.collectables.add(Collectable(bubble_props))
        elif drop_choice == Item_code.COIN_CODE:
            coin_props = Collectable_Props(self.rect.centerx, self.rect.centery - 20, Collectable_item.COIN_ITEM)
            self.game.collectables.add(Collectable(coin_props))
                