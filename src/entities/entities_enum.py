import pygame
from enum import Enum
from ..config.settings import *
from ..config.paths import *

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Team(Enum):
    ALLIES = 0
    ENEMY = 1

class Weapon(Enum):
    REGULAR = {"damage": 2, "speed": 10, "bullet_range": 700, "cooldown": 300, 'gun_type': 0}
    RIFLE = {"damage": 6, "speed": 12, "bullet_range": 1200, "cooldown": 450, 'gun_type': 1}
    MINIGUN = {"damage": 2, "speed": 14, "bullet_range": 700, "cooldown": 100, 'gun_type': 2}

class Item_code(Enum):
    RIFLE_CODE = 0
    MINIGUN_CODE = 1
    BUBBLE_CODE = 2
    COIN_CODE = 3
    HEALTH_KIT_CODE = 4

class Collectable_types(Enum):
    WEAPON = 0
    POWER_UP = 1 # please make the healing kit one of those, I know the name sucks but if you make another one of those types it will create clutter. and I am NOT fond of clutter
    COIN = 2

class Collectable_item(Enum):
    RIFLE_ITEM = { "image": "rifle.png", "value": 15, "type": Collectable_types.WEAPON, "item": Weapon.RIFLE, "code": Item_code.RIFLE_CODE }
    MINIGUN_ITEM = { "image": "minigun.png", "value": 100, "type": Collectable_types.WEAPON, "item": Weapon.MINIGUN, "code": Item_code.MINIGUN_CODE }
    BUBBLE_ITEM = { "image": "bubble.png", "type": Collectable_types.POWER_UP, "item": { "value": 10 * 1000 }, "code": Item_code.BUBBLE_CODE}
    COIN_ITEM = { "image": "coin.png", "type": Collectable_types.COIN, "item": {}, "code": Item_code.COIN_CODE}


##### CHARACTER ######
# era pra tá em um arquivo separaldus quem quiser arrumar os imports só fazer :)

class Character_action(Enum):
    IDLE = 0
    RUN = 1
    DEATH = 2
    JUMP = 3

class Images_info():
    def __init__(self, animation_type: int, num_images: int, path: str):
        self.animation_type = animation_type
        self.num_images = num_images
        self.path = path

class Character_images_info(Enum):
    PLAYER_1 = [
        Images_info(Character_action.IDLE.value, 5, IDLE_PATH),
        Images_info(Character_action.RUN.value, 10, RUN_PATH),
        Images_info(Character_action.JUMP.value, 9, JUMP_PATH),
        Images_info(Character_action.DEATH.value, 10, DEATH_PATH)
    ]
    ENEMY = [
        Images_info(Character_action.IDLE.value, 2, ENEMY_IDLE_PATH),
        Images_info(Character_action.RUN.value, 10, ENEMY_RUN_PATH),
        Images_info(Character_action.DEATH.value, 12, ENEMY_DEATH_PATH)
    ]

class Controll():
    def __init__(self, up, down, left, right, shoot):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.shoot = shoot


class Character_type_info():
    def __init__(self, 
            images_info: Character_images_info, direction: Direction, weapon: Weapon, 
            speed: int, hp: int, ai_move_duration: int, team: Team, controll: Controll):
        self.images_info = images_info
        self.direction = direction
        self.weapon = weapon
        self.speed = speed
        self.hp = hp
        self.ai_move_duration = ai_move_duration
        self.team = team
        self.controll = controll

class Character_type(Enum):
    PLAYER_1 = Character_type_info(
        Character_images_info.PLAYER_1, Direction.RIGHT, Weapon.REGULAR.value,
        PLAYER_SPEED, PLAYER_HP, 0, Team.ALLIES, Controll(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_c))
    PLAYER_2 = Character_type_info(
        Character_images_info.PLAYER_1, Direction.RIGHT, Weapon.REGULAR.value,
        PLAYER_SPEED, PLAYER_HP, 0, Team.ALLIES, Controll(pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_n))
    ENEMY = Character_type_info(
        Character_images_info.ENEMY, Direction.LEFT, Weapon.REGULAR.value,
        ENEMY_SPEED, ENEMY_HP, AI_DECISION_COOLDOWN, Team.ENEMY, Controll(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_c))

##### CHARACTER ######