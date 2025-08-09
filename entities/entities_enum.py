from enum import Enum
from settings import *

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Weapon(Enum):
    REGULAR = {"damage": 2, "speed": 10, "bullet_range": 900, "cooldown": 300, 'gun_type': 0}
    RIFLE = {"damage": 6, "speed": 12, "bullet_range": 1200, "cooldown": 450, 'gun_type': 1}
    MINIGUN = {"damage": 2, "speed": 14, "bullet_range": 900, "cooldown": 100, 'gun_type': 2}

class Collectables(Enum):
    RIFLE_ITEM = {"image": "rifle_item.png", "value": 1}


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

class Character_type_info():
    def __init__(self, 
            images_info: Character_images_info, direction: Direction, 
            weapon: Weapon, speed: int, hp: int, ai_move_duration: int):
        self.images_info = images_info
        self.direction = direction
        self.weapon = weapon
        self.speed = speed
        self.hp = hp
        self.ai_move_duration = ai_move_duration

class Character_type(Enum):
    PLAYER_1 = Character_type_info(
        Character_images_info.PLAYER_1, Direction.RIGHT, Weapon.REGULAR.value,
        PLAYER_SPEED, PLAYER_HP, 0)
    ENEMY = Character_type_info(
        Character_images_info.ENEMY, Direction.LEFT, Weapon.REGULAR.value,
        ENEMY_SPEED, ENEMY_HP, AI_DECISION_COOLDOWN)

##### CHARACTER ######