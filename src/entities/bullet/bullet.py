import pygame

from ..entities_enum import Direction
from .bullet_props import Bullet_props

class Bullet(pygame.sprite.Sprite):
    def __init__(self, props: Bullet_props):
        super().__init__()
        self.direction = props.direction
        self.gun_type = props.gun_type

        # 1) carregar frames e inicializar animação
        self.frames = Bullet_props.get_frames(self.direction, self.gun_type)
        self.current_frame = 0
        self.animation_fps = props.animation_fps
        self.frame_duration = 1000 // self.animation_fps  # ms por frame
        self.last_frame_time = pygame.time.get_ticks()

        # 2) configurar imagem inicial e rect
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(props.x, props.y))

        # 3) propagar demais atributos (speed, bullet_range, team…)
        self.__dict__.update(props.__dict__)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_time >= self.frame_duration:
            self.last_frame_time = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center)

    def move(self, game):
        dx = self.speed if self.direction == Direction.RIGHT else -self.speed
        self.bullet_range -= abs(dx)
        self.rect.x += dx

        if self.bullet_range <= 0:
            self.kill()
            return

        # colisões com mapa
        for tile in game.world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
                return

    def update(self, game):
        self.move(game)
        self.animate()


