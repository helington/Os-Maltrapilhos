from os import path
from pathlib import Path

# Game settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 640
GAME_NAME = "Os Maltrapilhos"
FPS = 60

SCROLLING_THRESHOLD = 500

# Bullet
DISTANCE_FROM_PLAYER = 48
Y_AXIS_BULLET = 16

# Player
PLAYER_SPEED = 5
PLAYER_HP = 6

# ENEMY
ENEMY_HP = 6
ENEMY_SPEED = 5
AI_DECISION_COOLDOWN = 500 # ms

# Paths
ROOT_PATH = Path(__file__).resolve().parents[0]
ASSETS_PATH = path.join(ROOT_PATH, "assets")
FONTS_PATH = path.join(ASSETS_PATH, "fonts")
GRAPHICS_PATH = path.join(ASSETS_PATH, "graphics")
BACKGROUND_PATH = path.join(GRAPHICS_PATH, "background")
PLAYER_PATH = path.join(GRAPHICS_PATH, "player")
IDLE_PATH = path.join(PLAYER_PATH, "Idle")
JUMP_PATH = path.join(PLAYER_PATH, "Jump")
DEATH_PATH = path.join(PLAYER_PATH, "Death")
RUN_PATH = path.join(PLAYER_PATH, "Run")
BULLET_PATH = path.join(GRAPHICS_PATH, "bullet")
ENEMY_PATH = path.join(GRAPHICS_PATH, "enemy")
ENEMY_IDLE_PATH = path.join(ENEMY_PATH, "Idle")
ENEMY_DEATH_PATH = path.join(ENEMY_PATH, "Death")
ENEMY_RUN_PATH = path.join(ENEMY_PATH, "Run")
TILES_PATH = path.join(GRAPHICS_PATH, "tiles")
GROUND_PATH = path.join(GRAPHICS_PATH, "ground")
SOUNDS_PATH = path.join(ASSETS_PATH, "sounds")
LEVELS_PATH = path.join(ASSETS_PATH, "levels")

WOLRD_CSV_ROWS = 16
WOLRD_CSV_COLLUNMS = 150
TILE_SIZE = SCREEN_HEIGHT // WOLRD_CSV_ROWS
TILE_TYPES = 21

FLOOR_Y = SCREEN_HEIGHT - 128