import pygame
import random
import math
from os import path
from ...config.paths import BOSS_DEATH_PATH, BOSS_MOUTH_PATH, BOSS_ATTACK_PATH
from ...config.settings import TILE_SIZE, BOSS_MAX_HP
from ..entities_enum import Character_action, Team
from .boss_bullet import BossBullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        # Basic informations
        self.images = list()
        self.hurted = 0
        self.open = 0
        self.hurting_time = pygame.time.get_ticks()
        self.hurting_time_cooldown = 300

        # Sprites base do boss
        image_closed_raw_path = path.join(BOSS_MOUTH_PATH, "closed.png")
        image_open_raw_path = path.join(BOSS_MOUTH_PATH, "open.png")
        image_closed_raw = pygame.image.load(image_closed_raw_path).convert_alpha()
        image_open_raw = pygame.image.load(image_open_raw_path).convert_alpha()

        # Sprites da bala (3 frames)
        bullet0_raw = pygame.image.load(path.join(BOSS_ATTACK_PATH, "0.png")).convert_alpha()
        bullet1_raw = pygame.image.load(path.join(BOSS_ATTACK_PATH, "1.png")).convert_alpha()
        bullet2_raw = pygame.image.load(path.join(BOSS_ATTACK_PATH, "2.png")).convert_alpha()

        # Tamanho do boss e da bala
        self._size = (TILE_SIZE * 4, TILE_SIZE * 5)

        self.images = list()

        image_closed = pygame.transform.scale(image_closed_raw, self._size)
        image_closed_hurted = self.get_hurted_boss_image(image_closed)
        images_closed = [image_closed, image_closed_hurted]

        image_open = pygame.transform.scale(image_open_raw, self._size)
        image_open_hurted = self.get_hurted_boss_image(image_open)
        images_open = [image_open, image_open_hurted]

        self.images = [images_closed, images_open]

        bullet_size = (TILE_SIZE, TILE_SIZE)
        self.bullet_frames = [
            pygame.transform.scale(bullet0_raw, bullet_size),
            pygame.transform.scale(bullet1_raw, bullet_size),
            pygame.transform.scale(bullet2_raw, bullet_size),
        ]

        # Sprite atual do boss
        self.image = self.images[self.open][self.hurted]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)

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

        # Ataque
        self.attack_cooldown = 60
        self.attack_timer = random.randint(20, self.attack_cooldown)
        self.bullet_group = bullet_group

        # Propriedades do projétil
        self.bullet_speed = 7.0
        self.bullet_damage = 2
        self.bullet_knockback = 8
        self.bullet_frame_duration = 4  # velocidade da animação da bala

        # Boca aberta ao atacar
        self.mouth_open_duration = 18  # ticks que a boca fica aberta após atacar
        self.mouth_open_timer = 0

        # Contato
        self.contact_damage = 2
        self.contact_knockback = 8
        self.touch_cooldown_ms = 500
        self._last_touch = {}

    # --------- Boca (mantendo a função que já existia) ---------
    def open_mouth(self, duration: int | None = None):
        """Abre a boca, trocando para boss_open.png e inicia um timer opcional."""
        self.open = 1
        self.mouth_open_timer = duration if duration is not None else self.mouth_open_duration

    def close_mouth(self):
        """Fecha a boca, voltando para boss_closed.png."""
        self.open = 0
        self.mouth_open_timer = 0

    def load_death_animation_list(self):
        for i in range(6):
            image_path = path.join(BOSS_DEATH_PATH, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE * 4, TILE_SIZE * 5))
            self.images_destruction.append(image)

    def _pick_new_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        self.vel.from_polar((1, math.degrees(angle)))
        self.change_dir_timer = random.randint(45, 150)

    def _rotate_velocity(self, delta_angle_rad):
        angle = math.atan2(self.vel.y, self.vel.x) + delta_angle_rad
        self.vel.x = math.cos(angle)
        self.vel.y = math.sin(angle)

    def _keep_inside_bounds(self, bounds: pygame.Rect):
        bounced = False
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
            self.pos.update(self.rect.topleft)
            self._rotate_velocity(random.uniform(-math.pi / 6, math.pi / 6))

    def get_hurted_boss_image(self, image):
        hurt_image = image.copy().convert_alpha()

        red_tint = pygame.Surface(hurt_image.get_size(), pygame.SRCALPHA)
        red_tint.fill((50, 0, 0, 0))  # 100 = intensidade da transparência

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

    def _try_attack(self, game):
        if self.attack_timer > 0:
            self.attack_timer -= 1
            return

        target = getattr(game, "follow_player", None)
        if not target or not hasattr(target, "rect"):
            return

        origin = pygame.math.Vector2(self.rect.center)
        target_pos = pygame.math.Vector2(target.rect.center)
        direction = target_pos - origin
        if direction.length_squared() == 0:
            direction = pygame.math.Vector2(1, 0)

        vel = direction.normalize() * self.bullet_speed

        # Abre a boca no momento do disparo
        self.open_mouth()

        # Cria bala animada (passa a lista de frames)
        bullet = BossBullet(
            origin,
            vel,
            self.bullet_frames,
            damage=self.bullet_damage,
            knockback=self.bullet_knockback,
            frame_duration=self.bullet_frame_duration
        )
        self.bullet_group.add(bullet)

        # Reinicia cooldown
        self.attack_timer = self.attack_cooldown

    def touch_damage_players(self, game):
        now = pygame.time.get_ticks()
        players = getattr(game, "players", [])
        for player in players:
            if not hasattr(player, "rect"):
                continue
            if hasattr(player, "hp") and player.hp <= 0:
                continue
            if not self.rect.colliderect(player.rect):
                continue
            last = self._last_touch.get(id(player), 0)
            if now - last < self.touch_cooldown_ms:
                continue
            if hasattr(player, "take_damage") and callable(player.take_damage):
                player.take_damage(self.contact_damage)
            elif hasattr(player, "hp"):
                player.hp = max(0, player.hp - self.contact_damage)
            if hasattr(player, "vel"):
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                vec = pygame.math.Vector2(dx, dy)
                if vec.length_squared() == 0:
                    vec = pygame.math.Vector2(1, -0.5)
                vec = vec.normalize() * self.contact_knockback
                player.vel.x += vec.x
                player.vel.y += vec.y
            self._last_touch[id(player)] = now

    def update(self, game):
        surface = pygame.display.get_surface()
        if not surface:
            return
        bounds = surface.get_rect()

        # Movimento contínuo
        if self.alive:
            self.pos += self.vel * self.speed
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self._keep_inside_bounds(bounds)

        # Mudar direção às vezes
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

            # Tentar atacar
            self._try_attack(game)

            # Dano por contato
            self.touch_damage_players(game)

            # Timer da boca aberta
            if self.mouth_open_timer > 0:
                self.mouth_open_timer -= 1
                # Garante que a imagem esteja aberta durante o timer
                if self.image not in self.images[1]:
                    self.open = 1
            else:
                # Fecha a boca quando o timer acaba
                if self.image not in self.images[0]:
                    self.open = 0

            self.image = self.images[self.open][self.hurted]
            
