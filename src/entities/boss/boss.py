import pygame
import random
import math
from os import path
from ...config.paths import GRAPHICS_PATH
from ...config.settings import TILE_SIZE


class BossBullet(pygame.sprite.Sprite):
    def __init__(self, pos_center: pygame.math.Vector2, velocity: pygame.math.Vector2, image: pygame.Surface, damage=2, knockback=8):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(int(pos_center.x), int(pos_center.y)))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(velocity)
        self.damage = damage
        self.knockback = knockback

        # 🔹 Define como projétil inimigo para não quebrar check_hurt()
        self.team = "enemy"

    def update(self, game):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Colisão com players
        if hasattr(game, "players"):
            hits = pygame.sprite.spritecollide(self, game.players, False)
            if hits:
                knock_dir = pygame.math.Vector2(self.vel)
                if knock_dir.length_squared() > 0:
                    knock_dir = knock_dir.normalize()

                for player in hits:
                    if hasattr(player, "take_damage") and callable(player.take_damage):
                        player.take_damage(self.damage)
                    elif hasattr(player, "hp"):
                        player.hp = max(0, player.hp - self.damage)

                    # Knockback
                    delta = knock_dir * self.knockback
                    if hasattr(player, "vel"):
                        player.vel.x += delta.x
                        player.vel.y += delta.y

                self.kill()
                return

        # Remove se sair da tela
        surface = pygame.display.get_surface()
        if surface and not surface.get_rect().colliderect(self.rect):
            self.kill()

        # Elimina se sair da tela
        surface = pygame.display.get_surface()
        if not surface:
            return
        bounds = surface.get_rect()
        if not bounds.colliderect(self.rect):
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        # Sprites base
        self.image_closed_raw = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_closed.png")).convert_alpha()
        self.image_open_raw = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_open.png")).convert_alpha()

        # Tamanhos padronizados
        self._size = (TILE_SIZE * 4, TILE_SIZE * 5)
        self.image_closed = pygame.transform.scale(self.image_closed_raw, self._size)
        self.image_open = pygame.transform.scale(self.image_open_raw, self._size)

        # Sprite atual (fechado por padrão)
        self.image = self.image_closed

        # Rect e posição em float
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)  # posição contínua

        # Movimento
        self.speed = 2.5
        self.vel = pygame.math.Vector2(0, 0)
        self.change_dir_timer = 0
        self._pick_new_direction()

        # Ataque
        self.attack_cooldown = 60  # frames entre disparos
        self.attack_timer = random.randint(20, self.attack_cooldown)  # variação inicial
        self.bullet_group = bullet_group

        bullet_img_raw = pygame.image.load(path.join(GRAPHICS_PATH, "boss", "boss_attack.png")).convert_alpha()
        # Escala do projétil; ajuste se quiser maior/menor
        self.bullet_image = pygame.transform.scale(bullet_img_raw, (TILE_SIZE, TILE_SIZE))
        self.bullet_speed = 7.0
        self.bullet_damage = 2
        self.bullet_knockback = 8  # ajuste conforme desejar

        # Boca aberta por alguns frames após disparar
        self.open_frames_left = 0
        self.open_duration = 8  # quantos frames a boca fica aberta após o tiro

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

    def _try_attack(self, game):
        # Regride o timer
        if self.attack_timer > 0:
            self.attack_timer -= 1
            return

        # Precisa de um alvo válido
        target = getattr(game, "follow_player", None)
        if not target or not hasattr(target, "rect"):
            return

        origin = pygame.math.Vector2(self.rect.center)
        target_pos = pygame.math.Vector2(target.rect.center)
        direction = target_pos - origin
        if direction.length_squared() == 0:
            # Evita divisão por zero
            direction = pygame.math.Vector2(1, 0)

        vel = direction.normalize() * self.bullet_speed

        # Cria e adiciona o projétil
        bullet = BossBullet(origin, vel, self.bullet_image, damage=self.bullet_damage, knockback=self.bullet_knockback)
        self.bullet_group.add(bullet)

        # Troca sprite para boca aberta por alguns frames
        self.image = self.image_open
        self.open_frames_left = self.open_duration

        # Reinicia cooldown
        self.attack_timer = self.attack_cooldown

    def update(self, game):
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

        # Lógica de ataque
        self._try_attack(game)

        # Volta para sprite de boca fechada quando acabar a janela de ataque
        if self.open_frames_left > 0:
            self.open_frames_left -= 1
            if self.open_frames_left == 0:
                self.image = self.image_closed