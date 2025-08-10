import pygame
from os import path

from ..config.settings import *
from ..config.paths import TILES_PATH, MENUS_PATH, BUTTONS_PATH
from ..entities import World, Player
from ..entities.entities_enum import Character_type, Collectable_item
from ..entities.collectable.collectable import Collectable, Collectable_Props
from ..entities.world import TILES_TYPE
from ..off_game_screens.button import Button

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.start_game = False

        self.tiles_image_list = list()
        self.get_tiles_images()

        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group() # this group currently exists for the bubble effect

        self.main_menu_img = pygame.image.load(path.join(MENUS_PATH, 'Main_Menu.jpeg'))
        self.main_menu_img = pygame.transform.scale(self.main_menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = Button(SCREEN_WIDTH //2 - 100, 300, pygame.image.load(path.join(BUTTONS_PATH, 'start_button.jpeg')))
        self.start_button.image = pygame.transform.scale(self.start_button.image, (200, 100))
        self.exit_button = Button(SCREEN_WIDTH //2 - 100, 500, pygame.image.load(path.join(BUTTONS_PATH, 'exit_button.jpg')))
        self.exit_button.image = pygame.transform.scale(self.exit_button.image, (200, 100))

        self.world = World(self)
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(Character_type.PLAYER_1.value, 230, 600))

        self.collectables = pygame.sprite.Group()
        rifle_props = Collectable_Props(640, 330, Collectable_item.RIFLE_ITEM)
        minigun_props = Collectable_Props(100, 535, Collectable_item.MINIGUN_ITEM)
        self.collectables.add(Collectable(rifle_props))
        self.collectables.add(Collectable(minigun_props))
        
        bubble_props = Collectable_Props(40, 535, Collectable_item.BUBBLE_ITEM)
        self.collectables.add(Collectable(bubble_props))

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
        self.effects.update(self)
        self.world.water_group.update(self.screen_scroll)
        # todo remover

    def draw(self):
        """Draws the current game state to the screen."""
        self.world.draw(self.screen, self)
        self.player.draw(self.screen)
        self.collectables.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.effects.draw(self.screen)

    def run(self):
        """Runs the main game loop."""

        while self.running:
            
            if not self.start_game:
                self.screen.blit(self.main_menu_img, (0,0))
                if self.start_button.draw(self.screen, selected=True):
                    self.start_game = True
                if self.exit_button.draw(self.screen, selected=False):
                    self.running = False
            else:
                self.update()
                self.draw()
            
            self.handle_events()

            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()