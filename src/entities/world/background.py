import pygame

from ...config.settings import *
from ...config.paths import *

class Background:
    """Background representation class."""

    def __init__(self):
        """Initializates background attributes"""

        self.scroll = 0
        
        self.images = list()
        self.get_parellel_images()
    
    def get_parellel_images(self):
        """Get all parellel images and put them into images list."""
        
        for i in range(5):
            current_image_path = path.join(BACKGROUND_PATH, f'plx-{i + 1}.png')
            current_image = pygame.image.load(current_image_path).convert_alpha()
            current_image = pygame.transform.scale(current_image,(SCREEN_WIDTH, SCREEN_HEIGHT))
            self.images.append(current_image)

    def draw(self, screen, game_screen_scroll):

        """Draw background applying the scrolling."""
        self.scroll -= game_screen_scroll

        for x in range (10):
            speed = 0.5
            for i in self.images:
                screen.blit(i,((x*SCREEN_WIDTH) - self.scroll*speed,0))
                speed+=0.1