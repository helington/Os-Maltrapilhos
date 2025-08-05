import pygame

from settings import *
from entities.background import Background
from entities.player import Player

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""

        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

        self.background = Background()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(200, 64))

    def handle_events(self):
        """Processes all Pygame events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def draw(self):
        """Draws the current game state to the screen."""

        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.player.update()

    def run(self):
        """Runs the main game loop."""

        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()