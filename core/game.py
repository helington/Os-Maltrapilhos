import pygame

from settings import *

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""

        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

    def handle_events(self):
        """Processes all Pygame events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def draw(self):
        """Draws the current game state to the screen."""
        
        pass

    def run(self):
        """Runs the main game loop."""

        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()