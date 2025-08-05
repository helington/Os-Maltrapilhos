from os import path
from pathlib import Path

# Game settings
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 800
GAME_NAME = "Os Maltrapilhos"
FPS = 60

# Colors

# Paths
ROOT_PATH = Path(__file__).resolve().parents[0]
ASSETS_PATH = path.join(ROOT_PATH, "assets")
FONTS_PATH = path.join(ASSETS_PATH, "fonts")
GRAPHICS_PATH = path.join(ASSETS_PATH, "graphics")
BACKGROUND_PATH = path.join(GRAPHICS_PATH, "background")
GROUND_PATH = path.join(GRAPHICS_PATH, "ground")
SOUNDS_PATH = path.join(ASSETS_PATH, "sounds")