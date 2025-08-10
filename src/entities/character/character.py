import pygame
from os import path

from ...config.settings import *
from ..entities_enum import Direction, Character_action, Images_info, Team, Weapon
from ..bullet import Bullet_props, Bullet
from .character_props import Character_Props

class Character(pygame.sprite.Sprite):    
    def __init__(self, props: Character_Props, x, y):
        super().__init__()
        self.__dict__.update(props.__dict__)
        self.update_time = pygame.time.get_ticks()
        self.action = Character_action.IDLE.value
        
        # render sprites
        self.index = 0
        temp_list = []
        self.load_animation_list(self.images_info.value)
        self.image = self.animation_list[self.index]
        self.rect = self.image[0].get_rect(midbottom=(x, y))

        # movement
        self.moving_left = False
        self.moving_right = False
        self.jumping = True
        self.has_shot = False
        self.gravity = 0
        self.dy = 0
        self.dx = 0
        self.last_time_shot = 0
        self.ammo = float('inf')
        
        self.ai_update_time = pygame.time.get_ticks()

        self.width = self.image[0].get_width()
        self.height = self.image[0].get_height()

    def load_animation_list(self, list: list[Images_info]):
        self.animation_list = {}
        for image_info in list:
            temp_list = []
            for i in range(image_info.num_images):
                image_path = path.join(image_info.path, f"{i}.png")
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (64, 64))
                temp_list.append(image)
                self.animation_list[image_info.animation_type] = temp_list

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

    def update_action(self, new_action):
        """ Update self.action based on action and reset the index if the new action is replaced """

        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, game, world):
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.update_action(Character_action.RUN.value)
            self.dx -= self.speed
            self.direction = Direction.LEFT
        elif self.moving_right:
            self.update_action(Character_action.RUN.value)
            self.direction = Direction.RIGHT
            self.dx += self.speed
        
        if self.dx ==0 and self.dy == 0:
            self.update_action(Character_action.IDLE.value)
            
        self.apply_gravity()

        for tile in world.obstacle_list:

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

        # Check for player going to world limit
        if self.team == Team.ALLIES:
            if self.rect.left + self.dx < 0 or self.rect.right + self.dx > SCREEN_WIDTH:
                self.dx = 0
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if it's time to scrolling the world
        if self.team == Team.ALLIES:
            game.screen_scroll = 0
            should_scroll = (
                (self.rect.right > SCREEN_WIDTH - SCROLLING_THRESHOLD and self.direction == Direction.RIGHT and
                world.background.scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or 
                self.rect.left < SCROLLING_THRESHOLD and self.direction == Direction.LEFT and
                world.background.scroll > abs(self.dx)
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
            self.handle_ammo()
            
            self.last_time_shot = pygame.time.get_ticks()
            bullet_dx = DISTANCE_FROM_PLAYER if self.direction == Direction.RIGHT else -DISTANCE_FROM_PLAYER
            props = Bullet_props(self.weapon, self.rect.centerx + bullet_dx, self.rect.centery, self.direction, self.team)
            bullet = Bullet(props)
            game.bullets.add(bullet)

    def handle_ammo(self):
        self.ammo -= 1
        if self.ammo < 1:
            self.weapon = Weapon.REGULAR.value
            self.ammo = float('inf')


    def apply_gravity(self):
        self.gravity += 0.75
        if self.gravity > 10:
            self.gravity
        self.dy = self.gravity

    def check_hurt(self, game):
        for bullet in game.bullets:
            is_hit = (
                self.rect.colliderect(bullet.rect) and
                bullet.team != self.team
            )
            if is_hit:
                game.bullets.remove(bullet)
                self.hp -= bullet.damage
                if self.hp <= 0:
                    self.action = Character_action.DEATH.value
                    self.moving_left = False
                    self.moving_right = False
                    self.index = 0
                    self.update_time = pygame.time.get_ticks()

    def update(self, game):
        self.check_hurt(game)
        self.shoot(game)
        self.update_animation()
        if self.action != Character_action.DEATH.value:
            self.move(game, game.world)
            