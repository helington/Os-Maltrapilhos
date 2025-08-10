from os import path
import pygame

from ...config.paths import BULLET_PATH
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
    def get_frames(cls, direction: Direction):
        """
        Retorna lista de 7 frames dimensionados e com flip para LEFT.
        Usa cache para não recarregar toda chamada.
        """
        # cache estático
        if not hasattr(cls, "_cache"):
            cls._cache = {"RIGHT": [], "LEFT": []}
            for i in range(7):
                filename = f"bullet_{i}.png"
                fullpath = path.join(BULLET_PATH, filename)
                img = pygame.image.load(fullpath).convert_alpha()
                img = pygame.transform.scale(img, (20, 20))
                cls._cache["RIGHT"].append(img)
                # gera espelhado
                flipped = pygame.transform.flip(img, True, False)
                cls._cache["LEFT"].append(flipped)

        key = "LEFT" if direction == Direction.LEFT else "RIGHT"
        return cls._cache[key]