import pygame 
from settings import *


#### ta como old, para não perder esse código, implementação secundaria dele em enemy.py em character
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image_path = path.join(ENEMY_PATH, "enemy.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1
        self.direction = 1
        self.health = 40
        self.alive = True
        self.flip = False
        self.animation_list = []
        self.move_counter = 0


    def move(self):
        """Moves the enemy left or right."""
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed *= -1  # Reverse direction if at screen edge
            

    def ai(self, game):
        """Simple AI to control enemy movement."""
        if self.alive and game.player:
            if self.direction == 1:
                ai_moving_right = True
            else:  
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left, ai_moving_right)
            self.move_conuter += 32

            if self.move_counter >= 160:
                self.direction *= -1
                self.move_counter *= -1

            
    
    def update(self, game):
        """Updates the enemy's position."""
        self.ai
        self.move()
        
