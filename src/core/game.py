import pygame
from os import path

from ..config.settings import *
from ..config.paths import TILES_PATH
from ..entities import World, Player
from ..entities.entities_enum import Character_type, Collectable_item
from ..entities.collectable.collectable import Collectable, Collectable_Props
from ..entities.world import TILES_TYPE

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

        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.world = World(self)
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(Character_type.PLAYER_1.value, 230, 600))

        self.collectables = pygame.sprite.Group()
        rifle_props = Collectable_Props(640, 330, Collectable_item.RIFLE_ITEM)
        minigun_props = Collectable_Props(100, 535, Collectable_item.MINIGUN_ITEM)
        self.collectables.add(Collectable(rifle_props))
        self.collectables.add(Collectable(minigun_props))
        
        self.screen_scroll = 0


    def get_tiles_images(self):
        """Get all images of tiles and transform them in surfaces, and then put them into 'tiles_image_list' variable."""

        for i in range(TILE_TYPES):
            current_image_path = path.join(TILES_PATH, f"{i}.png")
            current_image = pygame.image.load(current_image_path)
            if i == TILES_TYPE.PLAYER:
                pass
            elif i == TILES_TYPE.ENEMY:
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
        self.enemies.update(self)
        self.player.update(self)
        self.collectables.update(self)
        self.world.water_group.update(self.screen_scroll)
        # todo remover

    def draw(self):
        """Draws the current game state to the screen."""
        self.world.draw(self.screen, self)
        self.player.draw(self.screen)
        self.collectables.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        # todo remover

    def run(self):
        """Runs the main game loop."""

        while self.running:
            self.handle_events()
            self.update()
            self.draw()


            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()