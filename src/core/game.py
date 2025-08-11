import pygame
from pygame import mixer
from os import path

from ..config.settings import *
from ..config.paths import TILES_PATH, MENUS_PATH, BUTTONS_PATH, SOUNDS_PATH
from ..entities import World, Player
from ..entities.entities_enum import Character_type, Collectable_item, Character_action
from ..entities.collectable.collectable import Collectable, Collectable_Props
from ..entities.world import TILES_TYPE
from ..off_game_screens.button import Button
from ..entities.character.health_bar import Healthbar

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""
        pygame.init()
        mixer.init()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.start_game = False
        self.multiplayer_active = False

        self.tiles_image_list = list()
        self.get_tiles_images()

        # load background music
        mixer.music.load(path.join(SOUNDS_PATH, 'bgm.mp3'))
        mixer.music.set_volume(0.10)
        mixer.music.play(-1,0.0,5000)  # -1 means loop indefinitely

        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group() # this group currently exists for the bubble effect

        self.main_menu_img = pygame.image.load(path.join(MENUS_PATH, 'Main_Menu.jpeg'))
        self.main_menu_img = pygame.transform.scale(self.main_menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = Button(SCREEN_WIDTH //2 - 100, 500, pygame.image.load(path.join(BUTTONS_PATH, 'Default.png')))
        self.start_button.image = pygame.transform.scale(self.start_button.image, (200, 100))
        

        self.world = World(self)
        self.players = pygame.sprite.Group()
        player1 = Player(Character_type.PLAYER_1.value, 230, 600, False)
        self.players.add(player1)

        self.health_bar = pygame.sprite.Group()
        self.health_bar.add(Healthbar(80, 100, False, player1))


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
                if event.key == pygame.K_m:
                    # todo block respawn
                    if not self.multiplayer_active: 
                        self.multiplayer_active = True
                        player2 = Player(Character_type.PLAYER_2.value, 230, 400, True)
                        self.players.add(player2)
                        self.health_bar.add(Healthbar(80, 180, True, player2))
         
    def update(self):
        """Updates all entities of the game."""
        self.bullets.update(self)
        self.enemies.update(self)
        self.players.update(self)
        self.health_bar.update(self)
        self.collectables.update(self)
        self.effects.update(self)
        self.world.water_group.update(self.screen_scroll)

    def draw(self):
        """Draws the current game state to the screen."""
        self.world.draw(self.screen, self)
        self.players.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.collectables.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.effects.draw(self.screen)

    def are_all_players_died(self):
        """Check if all players in game are died."""

        for player in self.players.sprites():
            if player.alive == True:
                return False
        return True

    def run(self):
        """Runs the main game loop."""

        while self.running:
            
            if not self.start_game:
                self.screen.blit(self.main_menu_img, (0,0))
                if self.start_button.draw(self.screen, selected=True):
                    self.start_game = True
                
            else:
                self.update()
                self.draw()
            
            self.handle_events()

            if self.are_all_players_died():
                game_over_screen = pygame.image.load(path.join(MENUS_PATH, 'Game_Over.jpeg'))
                game_over_screen = pygame.transform.scale(game_over_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(game_over_screen, (0, 0))
                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    self.running = False


            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()