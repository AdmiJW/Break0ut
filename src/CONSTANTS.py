import os.path as path

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

HIGHSCORE_SAVE_DIR = 'saves'
HIGHSCORE_SAVE_PATH = path.join( HIGHSCORE_SAVE_DIR, 'highscore.json')

FONT_PATH = path.join('assets', 'SpaceObsessed-5dzv.ttf')
BG_PATHS = [
    path.join('assets', 'bg1.JPG'),
    path.join('assets', 'bg2.JPG'),
    path.join('assets', 'bg3.JPG'),
    path.join('assets', 'bg4.JPG'),
    path.join('assets', 'bg5.JPG'),
]


# Colors
BLACK = (1,1,1)
WHITE = (255,255,255)
WHITE_2 = (236, 240, 241)
WHITE_3 = (189, 195, 199)
WHITE_4 = (149, 165, 166)
WHITE_5 = (127, 140, 141)
RED = (255,0,0)
YELLOW_1 = (241, 196, 15)
YELLOW_2 = (243, 156, 18)
BLUE_1 = (52, 152, 219)
BLUE_2 = (41, 128, 185)

#################################################
# Sprite Sheet / Texture Atlas Related Constants
# Each group shall contain
#   - offset
#   - size
#   - margin
#   - rows
#   - columns
#   - count
class SPRITE:
    PATH = path.join('assets', 'breakout_pieces.png')
    POWERUP_PATH = path.join('assets', 'powerups.png')

    TILE_OFFSET = (8,8)
    TILE_SIZE = (32,16)
    TILE_MARGIN = (0,4)
    TILE_ROWS = 7
    TILE_COLS = 1
    TILE_COUNT = 7
    TILE_SCALE = 1.5
    TILE_COLOR_SAMPLING_PIXEL = (8,5)   # x,y offset used to retrieve the color that represents a tile

    PAD_OFFSET = (48, 72)
    PAD_SIZE = (64,16)
    PAD_MARGIN = (4,4)
    PAD_ROWS = 3
    PAD_COLS = 3
    PAD_COUNT = 7
    PAD_SCALE = 1.5

    BALL_OFFSET = (48, 136)
    BALL_SIZE = (8,8)
    BALL_MARGIN = (1,0)
    BALL_ROWS = 1
    BALL_COLS = 7
    BALL_COUNT = 7
    BALL_SCALE = 2

    # Stronger ball variant
    S_BALL_OFFSET = (145, 135)
    S_BALL_SIZE = (10, 10)
    S_BALL_MARGIN = (1,0)
    S_BALL_ROWS = 1
    S_BALL_COLS = 7
    S_BALL_COUNT = 7
    S_BALL_SCALE = 2

    HEART_OFFSET = (120, 135)
    HEART_SIZE = (10, 9)
    HEART_MARGIN = (1, 0)
    HEART_ROWS = 1
    HEART_COLS = 2
    HEART_COUNT = 2
    HEART_SCALE = 2.5

    POWERUP_OFFSET = (0,0)
    POWERUP_SIZE = (16,16)
    POWERUP_MARGIN = (0,0)
    POWERUP_ROWS = 1
    POWERUP_COLS = 5
    POWERUP_COUNT = 5
    POWERUP_SCALE = 2

