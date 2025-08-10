import pygame

from .character import Character
from ...config.settings import *
from ...config.paths import *
from ..entities_enum import Direction, Weapon, Character_action, Character_type

class Player(Character):
    def __init__(self, character_info: Character_type, x, y):
        super().__init__(character_info, x, y)
        self.direction = Direction.RIGHT
        
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0 
        temp_list = []

        # animation
        self.animation_list = []
        for i in range(5):
            image_path = path.join(IDLE_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(10):
            image_path = path.join(RUN_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(9):
            image_path = path.join(JUMP_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(10):
            image_path = path.join(DEATH_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        
        # /animation

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect(midbottom=(x, y))
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
        self.weapon = Weapon.REGULAR.value

        self.width = self.image.get_width()
        self.height = self.image.get_height()

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

    def update(self, game):
        super().update(game)
        if self.action == Character_action.DEATH.value:
            # todo death animations??
            self.kill()
        self.handle_input()
        self.update_animation()
