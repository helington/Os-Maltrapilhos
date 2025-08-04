import pygame

from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handle_events()
        
        pygame.quit()