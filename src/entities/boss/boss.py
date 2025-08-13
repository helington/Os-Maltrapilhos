import pygame
import random
import math
from os import path
from ...config.paths import GRAPHICS_PATH
from ...config.settings import TILE_SIZE, BOSS_MAX_HP
from ..entities_enum import Character_action, Team

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        # Sprites
        self.image_closed = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_closed.png")).convert_alpha()
        self.image_open = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_open.png")).convert_alpha()
        self.images = list()
        self.images.append(pygame.transform.scale(self.image_closed, (TILE_SIZE * 4, TILE_SIZE * 5)))
        self.images.append(self.get_hurted_boss_image(self.images[0]))
        self.hurted = 0
        self.hurting_time = pygame.time.get_ticks()
        self.hurting_time_cooldown = 300
        self.image = self.images[self.hurted]

        # Rect e posição em float
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)  # posição contínua

        # Movimento
        self.speed = 2.5
        self.vel = pygame.math.Vector2(0, 0)
        self.change_dir_timer = 0
        self._pick_new_direction()

        self.images_destruction = list()
        self.load_death_animation_list()
        self.index = 0
        self.update_time = pygame.time.get_ticks()

        self.team = Team.ENEMY
        self.alive = True

        self.hp = BOSS_MAX_HP

        # Ataque (placeholder)
        self.attack_cooldown = 60
        self.attack_timer = 0
        self.bullet_group = bullet_group
        self.bullet_image = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_attack.png")).convert_alpha()

    def load_death_animation_list(self):
        for i in range(6):
            image_path = path.join(GRAPHICS_PATH, "boss", "destruction", f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE * 4, TILE_SIZE * 5))
            self.images_destruction.append(image)

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

    def get_hurted_boss_image(self, image):
        # Faz uma cópia da imagem original para não alterar o original
        hurt_image = image.copy().convert_alpha()

        # Cria uma superfície vermelha com transparência
        red_tint = pygame.Surface(hurt_image.get_size(), pygame.SRCALPHA)
        red_tint.fill((50, 0, 0, 0))  # 100 = intensidade da transparência

        # Aplica o vermelho em cima da imagem
        hurt_image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return hurt_image

    def check_hurt(self, game):
        for bullet in game.bullets:
            is_hit = (
                self.rect.colliderect(bullet.rect) and
                bullet.team != self.team
            )
            if is_hit:
                self.hurted = 1
                self.hurting_time = pygame.time.get_ticks()
                game.bullets.remove(bullet)
                self.hp -= bullet.damage

                if self.hp <= 0:
                    self.alive = False

    def death_animation(self, game):
        animation_cooldown = 250
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.index += 1
            self.update_time = pygame.time.get_ticks()
            if self.index >= len(self.images_destruction):
                self.kill()
                game.win = True
            else:
                self.image = self.images_destruction[self.index]

    def draw_boss_health_bar(self, screen, x, y, width, height):
        ratio = self.hp / BOSS_MAX_HP
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, width * ratio, height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)

    def update(self, game, *_):
        # Bounds reais da janela (mais seguro que constantes)
        surface = pygame.display.get_surface()
        if not surface:  # fallback defensivo
            return
        bounds = surface.get_rect()

        # Movimento contínuo
        if self.alive:
            self.pos += self.vel * self.speed
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Limites da tela + rebate
        self._keep_inside_bounds(bounds)

        # Troca de direção aleatória
        self.change_dir_timer -= 1
        if self.change_dir_timer <= 0:
            self._pick_new_direction()

        if not self.alive:
            self.death_animation(game)
        else:
            if self.hurted:
                if pygame.time.get_ticks() - self.hurting_time > self.hurting_time_cooldown:
                    self.hurted = 0

            self.check_hurt(game)
            self.image = self.images[self.hurted]

        # (Opcional) lógica de ataque aqui usando self.attack_timer / cooldown