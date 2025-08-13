import pygame
import random
import math
from os import path
from ...config.paths import GRAPHICS_PATH
from ...config.settings import TILE_SIZE

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        # Sprites
        self.image_closed = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_closed.png")).convert_alpha()
        self.image_open = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_open.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_closed, (TILE_SIZE * 6, TILE_SIZE * 7))

        # Rect e posição em float
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)  # posição contínua

        # Movimento
        self.speed = 2.5
        self.vel = pygame.math.Vector2(0, 0)
        self.change_dir_timer = 0
        self._pick_new_direction()

        # Ataque (placeholder)
        self.attack_cooldown = 60
        self.attack_timer = 0
        self.bullet_group = bullet_group
        self.bullet_image = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_attack.png")).convert_alpha()

    def _pick_new_direction(self):
        # Garante direção não-nula
        angle = random.uniform(0, 2 * math.pi)
        self.vel.from_polar((1, math.degrees(angle)))  # unit vector
        self.change_dir_timer = random.randint(45, 150)

    def _rotate_velocity(self, delta_angle_rad):
        # Rotaciona vetor de velocidade mantendo módulo 1
        angle = math.atan2(self.vel.y, self.vel.x) + delta_angle_rad
        self.vel.x = math.cos(angle)
        self.vel.y = math.sin(angle)

    def _keep_inside_bounds(self, bounds: pygame.Rect):
        bounced = False

        # Usa rect atualizado para checar limites
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.vel.x = abs(self.vel.x)
            bounced = True
        elif self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.vel.x = -abs(self.vel.x)
            bounced = True

        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.vel.y = abs(self.vel.y)
            bounced = True
        elif self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.vel.y = -abs(self.vel.y)
            bounced = True

        if bounced:
            # Atualiza pos float a partir do rect clamped
            self.pos.update(self.rect.topleft)
            # Pequena variação para evitar ficar “colado” na borda
            self._rotate_velocity(random.uniform(-math.pi / 6, math.pi / 6))

    def update(self, *_):
        # Bounds reais da janela (mais seguro que constantes)
        surface = pygame.display.get_surface()
        if not surface:  # fallback defensivo
            return
        bounds = surface.get_rect()

        # Movimento contínuo
        self.pos += self.vel * self.speed
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Limites da tela + rebate
        self._keep_inside_bounds(bounds)

        # Troca de direção aleatória
        self.change_dir_timer -= 1
        if self.change_dir_timer <= 0:
            self._pick_new_direction()

        # (Opcional) lógica de ataque aqui usando self.attack_timer / cooldown