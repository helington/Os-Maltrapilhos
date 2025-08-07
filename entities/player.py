import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image_path = path.join(PLAYER_PATH, "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(230, 600))
        self.speed = 5
        self.moving_left = False
        self.moving_right = False
        self.jumping = True
        self.gravity = 0
        self.dy = 0
        self.dx = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.moving_left = True
        else:
            self.moving_left = False

        if keys[pygame.K_d]:
            self.moving_right = True
        else:
            self.moving_right = False
        
        if keys[pygame.K_w] and not self.jumping:
            print("jump")
            self.jumping = True
            self.gravity = -12

    def move(self, game, obstacle_list):
        game.screen_scroll = 0
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.dx -= self.speed
        elif self.moving_right:
            self.dx += self.speed
            
        self.apply_gravity()

        for tile in obstacle_list:

            modifyed_rect_1 = pygame.Rect(self.rect.x + self.dx, self.rect.y, self.width, self.height)
            #check collision in the x direction
            if tile[1].colliderect(modifyed_rect_1):
                self.dx = 0
            
            modifyed_rect_2 = pygame.Rect(self.rect.x, self.rect.y + self.dy, self.width, self.height)
            #check for collision in the y direction
            if tile[1].colliderect(modifyed_rect_2):
                
                #check if below the ground, i.e. jumping
                if self.gravity < 0:
                    self.gravity = 0
                    self.dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.gravity >= 0:
                    self.gravity = 0
                    self.jumping = False
                    self.dy = tile[1].top - self.rect.bottom

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right > SCREEN_WIDTH - SCROLLING_THRESHOLD or self.rect.left < SCROLLING_THRESHOLD:
            self.rect.x -= self.dx
            game.screen_scroll = -self.dx

    def apply_gravity(self):
        self.gravity += 0.75
        if self.gravity > 10:
            self.gravity
        self.dy = self.gravity
        # self.rect.bottom = min(FLOOR_Y, self.rect.bottom)

    def update(self, game):
        self.handle_input()
        self.move(game, game.world.obstacle_list)
