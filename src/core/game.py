import pygame
from pygame import mixer
from os import path

from ..config.settings import *
from ..config.paths import TILES_PATH, MENUS_PATH, BUTTONS_PATH, SOUNDS_PATH
from ..entities import World, Player
from ..entities.entities_enum import Character_type, Collectable_item
from ..entities.collectable.collectable import Collectable, Collectable_Props
from ..entities.world import TILES_TYPE
from ..off_game_screens.button import Button
from ..entities.character.health_bar import Healthbar
from ..entities.boss.boss import Boss
from ..config.paths import GRAPHICS_PATH
from ..entities.character.price_hud import Price_hud
from ..entities.character.faces_hud import Faces_hud
from ..entities.character.money_hud import Money_hud

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializates pygame and the game attributes."""
        pygame.init()
        mixer.init()
        pygame.display.set_caption(GAME_NAME)
        icon = pygame.image.load(path.join(MENUS_PATH, 'icon_game.png'))
        pygame.display.set_icon(icon)
        self.level = 0
        self.initialize_config_vars()
        self.initialize_assets()
        self.initialize_groups_levels()
        self.get_tiles_images()

    def initialize_config_vars(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.start_game = False
        self.multiplayer_count = 1
        self.debug_count = 0
        self.win = False


        self.tiles_image_list = list()
        self.get_tiles_images()

        # load background music
        mixer.music.load(path.join(SOUNDS_PATH, 'bgm.mp3'))
        mixer.music.set_volume(0.10)
        mixer.music.play(-1,0.0,5000)  # -1 means loop indefinitely

        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group() # this group currently exists for the bubble effect

    def initialize_assets(self):
        self.main_menu_img = pygame.image.load(path.join(MENUS_PATH, 'Main_Menu.jpeg'))
        self.main_menu_img = pygame.transform.scale(self.main_menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = Button(SCREEN_WIDTH //2 - 100, 420, pygame.image.load(path.join(BUTTONS_PATH, 'Default.png')))
        self.start_button.image = pygame.transform.scale(self.start_button.image, (200, 200))
        mixer.music.load(path.join(SOUNDS_PATH, 'bgm.mp3'))
        mixer.music.set_volume(0.10)
        mixer.music.play(-1,0.0,5000)  # -1 means loop indefinitely

        # Imagem de Game Over pré-carregada
        self.game_over_img = pygame.image.load(path.join(MENUS_PATH, 'Game_Over.jpeg'))
        self.game_over_img = pygame.transform.scale(self.game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Botões
        restart_img = pygame.image.load(path.join(BUTTONS_PATH, 'restart.png'))
        exit_img = pygame.image.load(path.join(BUTTONS_PATH, 'exit.png'))

        restart_img = pygame.transform.scale(restart_img, (200, 200))
        exit_img = pygame.transform.scale(exit_img, (200, 200))

        cx = SCREEN_WIDTH // 2
        y = 420
        self.restart_button = Button(cx - 220, y, restart_img)
        self.exit_button = Button(cx + 20, y, exit_img)

    def initialize_groups_levels(self):
        self.effects = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.health_bar = pygame.sprite.Group()

        player1 = Player(Character_type.PLAYER_1.value, 230, 600, False)
        self.health_bar.add(Healthbar(50, -50 + self.multiplayer_count * 50, True, player1))
        self.health_bar.add(Money_hud(200, -50 + self.multiplayer_count * 50, player1))
        self.health_bar.add(Price_hud())
        self.health_bar.add(Faces_hud())
        self.players.add(player1)
        
        # levels
        self.world = World(self.level)

        self.world.screen_scroll = 0

    def load_next_level(self):
        if self.level >= 2: return 
        self.level += 1
        new_players = pygame.sprite.Group()
        self.world = World(self.level)
        for player in self.players:
            player.rect.x = 230
            player.rect.y = 200
            new_players.add(player)
        self.players = new_players

    def reset_game(self, reset_level=False):
        """Reseta o estado do jogo sem fechar a aplicação."""
        self.win = False
        self.multiplayer_count = 1

        if reset_level:
            self.level = 0  # reinicia do nível inicial

        self.initialize_groups_levels()
        self.start_game = True

        if hasattr(self.world, "screen_scroll"):
            self.world.screen_scroll = 0

    def get_follow_player(self): 
        if hasattr(self, 'follow_player'):
            previous = self.follow_player
        else: previous = None
        for player in self.players:
            if player.hp > 0:
                self.follow_player = player
                if previous is not self.follow_player:
                    if player.rect.x > 1120:
                        player.rect.x -= 30
                return
        self.follow_player = None

    def get_tiles_images(self):
        for i in range(TILE_TYPES):
            current_image_path = path.join(TILES_PATH, f"{i}.png")
            current_image = pygame.image.load(current_image_path)
            if i == TILES_TYPE.PLAYER:
                pass
            elif i == TILES_TYPE.ENEMY:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE * 2, TILE_SIZE * 2))
            else:
                current_image = pygame.transform.scale(current_image, (TILE_SIZE, TILE_SIZE))

    def handle_events(self):
        """Processes all Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_1:
                    # todo block respawn
                    if self.multiplayer_count < 4: 
                        self.multiplayer_count += 1
                        player_info = self.select_player(self.multiplayer_count)
                        new_player = Player(player_info, 230, 400, True)
                        self.players.add(new_player)
                        self.health_bar.add(Healthbar(50, -50 + self.multiplayer_count * 50, True, new_player))
                        self.health_bar.add(Money_hud(200, -50 + self.multiplayer_count * 50, new_player))
                if event.key == pygame.K_2:
                    self.debug_count += 1
                    if self.debug_count == 5:
                        new_player = Player(Character_type.PLAYER_DEBUG.value, 230, 400, True)
                        self.players.add(new_player)

    def select_player(self, player_i):
        if player_i == 1: return Character_type.PLAYER_1.value
        if player_i == 2: return Character_type.PLAYER_2.value
        if player_i == 3: return Character_type.PLAYER_3.value
        if player_i == 4: return Character_type.PLAYER_4.value

    def update(self):
        self.get_follow_player()

        # Atualizações normais
        self.world.bullets.update(self)
        self.world.collectables.update(self)
        for enemy in self.world.enemies: enemy.update(self, None)
        for player in self.players: player.update(self, self.follow_player)
        self.health_bar.update(self)
        self.effects.update(self)
        self.world.water_group.update(self.world.screen_scroll)

        self.world.boss.update(self)

    def draw(self):
        """Draws the current game state to the screen."""
        self.world.draw(self.screen)
        self.world.boss.draw(self.screen)
        self.players.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.world.collectables.draw(self.screen)
        self.world.bullets.draw(self.screen)
        self.world.enemies.draw(self.screen)
        self.effects.draw(self.screen)

    def are_all_players_died(self):
        return not any(player.alive for player in self.players)
        
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
                if self.world.boss:
                    self.world.boss.sprite.draw_boss_health_bar(self.screen, 400, 50, 400, 25)
            
            self.handle_events()


            if self.are_all_players_died():
                for player in self.players:
                    player.kill()

                # Fundo Game Over pré-carregado
                self.screen.blit(self.game_over_img, (0, 0))

                # Botões
                if self.restart_button.draw(self.screen, selected=False):
                    self.reset_game(reset_level=True)  # sempre recomeça do nível 0

                if self.exit_button.draw(self.screen, selected=False):
                    self.running = False

                # Atalho: Enter = Restart (não sai do jogo)
                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    self.reset_game(reset_level=True)
            
            if self.win:
                for player in self.players:
                    player.kill()

                # Fundo Vitória (pré-carregado para otimizar, se quiser seguir a mesma ideia do game_over_img)
                win_screen = pygame.image.load(path.join(MENUS_PATH, 'Win.png'))
                win_screen = pygame.transform.scale(win_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(win_screen, (0, 0))

                # Botão para jogar novamente
                if self.restart_button.draw(self.screen, selected=False):
                    self.reset_game(reset_level=True)  # volta ao nível inicial

                # Botão para sair do jogo
                if self.exit_button.draw(self.screen, selected=False):
                    self.running = False

                # Atalho: Enter = Restart
                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    self.reset_game(reset_level=True)

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()