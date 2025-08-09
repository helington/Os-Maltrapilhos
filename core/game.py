import pygame

from settings import *
from entities import World, Player
from entities.entities_enum import Character_type
from entities.character import Enemy

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

        self.tiles_image_list = list()
        self.get_tiles_images()

        self.world = World(self.tiles_image_list)
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(Character_type.PLAYER_1.value, 230, 600))

        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(Character_type.ENEMY.value, 630, 600))
        self.bullets = pygame.sprite.Group()

        self.screen_scroll = 0


    def get_tiles_images(self):
        """Get all images of tiles and transform them in surfaces, and then put them into 'tiles_image_list' variable."""

        for i in range(TILE_TYPES):
            current_image_path = path.join(TILES_PATH, f"{i}.png")
            current_image = pygame.image.load(current_image_path)
            if i == 15:
                pass
            elif i == 16:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE * 2, TILE_SIZE * 2))
            else:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE, TILE_SIZE))
            self.tiles_image_list.append(current_image)

    def handle_events(self):
        """Processes all Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
    
    def update(self):
        """Updates all entities of the game."""
        self.bullets.update(self)
        self.player.update(self)
        self.world.water_group.update(self.screen_scroll)
        # todo remover
        self.enemies.update(self)

    def draw(self):
        """Draws the current game state to the screen."""
        self.world.draw(self.screen, self)
        self.player.draw(self.screen)
        self.bullets.draw(self.screen)
        # todo remover
        self.enemies.draw(self.screen)

    def run(self):
        """Runs the main game loop."""

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()