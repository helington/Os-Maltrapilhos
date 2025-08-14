import pygame

from ..entities_enum import Character_action, Team

class BossBullet(pygame.sprite.Sprite):
    def __init__(
        self,
        pos_center: pygame.math.Vector2,
        velocity: pygame.math.Vector2,
        frames: list[pygame.Surface],
        damage=2,
        knockback=8,
        frame_duration=4  # frames por quadro de animação da bala
    ):
        super().__init__()
        # Animação
        self.frames = frames
        self.frame_duration = frame_duration
        self.frame_index = 0
        self.frame_timer = self.frame_duration

        # Sprite inicial
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(int(pos_center.x), int(pos_center.y)))

        # Movimento e combate
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(velocity)
        self.damage = damage
        self.knockback = knockback
        self.team = Team.ENEMY

    def _animate(self):
        self.frame_timer -= 1
        if self.frame_timer <= 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_timer = self.frame_duration
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=center)

    def update(self, game):
        self.pos += self.vel
        self._animate()
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        surface = pygame.display.get_surface()
        if not surface:
            return
        if not surface.get_rect().colliderect(self.rect):
            self.kill()