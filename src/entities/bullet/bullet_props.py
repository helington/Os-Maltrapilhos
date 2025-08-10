from os import path
import pygame

from ...config.paths import MINIGAN_PATH, REGULAR_PATH, RIFLE_PATH
from ..entities_enum import Weapon, Direction, Team

class Bullet_props():
    def __init__(self, weapon: Weapon, x: int, y: int, direction: Direction, team: Team):
        self.x = x
        self.y = y
        self.direction = direction
        self.team = team
        # Atualiza atributos vindo de Weapon (por ex: speed, range)
        self.__dict__.update(weapon)

        # Propriedades de animação
        self.animation_fps = 12  # quadros por segundo (ajuste se quiser)

    @classmethod
    def get_frames(cls, direction: Direction, gun_type: int):
        """
        Retorna lista de 7 frames dimensionados e com flip para LEFT.
        Usa cache para não recarregar toda chamada.
        """
        # cache estático
        if not hasattr(cls, "_cache"):
            cls._cache = [
                {"LEFT": [], "RIGHT": []} for i in range(3)
            ]
            bullets_types_paths = [REGULAR_PATH, RIFLE_PATH, MINIGAN_PATH]
            for i in range(3):
                # Rifles has 5 frames instead 7
                frames = 5 if i == 1 else 7
                for j in range(frames):
                    filename = f"{j}.png"
                    fullpath = path.join(bullets_types_paths[i], filename)
                    img = pygame.image.load(fullpath).convert_alpha()

                    # Riffles bullets should be longer
                    if i == 1:
                        img_size = (20 + 8 * j, 20)
                    else:
                        img_size =  (20, 20)
                    
                    img = pygame.transform.scale(img, img_size)
                    cls._cache[i]["RIGHT"].append(img)
                    # gera espelhado
                    flipped = pygame.transform.flip(img, True, False)
                    cls._cache[i]["LEFT"].append(flipped)

        key_2 = "LEFT" if direction == Direction.LEFT else "RIGHT"
        return cls._cache[gun_type][key_2]