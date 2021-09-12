import random

import pygame

import src.CONSTANTS as C
import src.CONFIG as CF


# A class to handle requests to retrieve sprites. Main job is to extract individual sprite from spritesheets
class SpriteManager:
    _SPRITE_SHEETS = [
        pygame.image.load(C.SPRITE.PATH).convert_alpha(),
        pygame.image.load(C.SPRITE.POWERUP_PATH).convert_alpha()
    ]

    # A general method to retrieve a sprite from a sprite sheet associated with SpriteManager
    # sprite_id: the 'index' of the sprite in the group. 0 means first element, 1 means second element...
    # offset: (x,y) offset in the actual spritesheet to the topleft of the group, in pixels
    # size: (x,y) in pixels, size of each sprite element
    # margin: (x,y) in pixels, the spacing between each of the elements.
    # n_rows, n_cols: Number of rows and columns in the grid system of the group in the spritesheet
    # is_row_direction: whether the elements are indexed from top to bottom, or left to right
    @staticmethod
    def _retrieve_sprite(sheet_id: int, sprite_id: int, offset: tuple, size: tuple, margin: tuple, n_rows: int, n_cols: int,
                         is_row_direction=True):
        row = (sprite_id // n_cols) if is_row_direction else (sprite_id % n_rows)
        col = (sprite_id % n_cols) if is_row_direction else (sprite_id // n_rows)
        top_position = offset[1] + row * (margin[1] + size[1])
        left_position = offset[0] + col * (margin[0] + size[0])
        return SpriteManager._SPRITE_SHEETS[sheet_id].subsurface((left_position, top_position, *size))

    @staticmethod
    def get_tile_surface(tier: int):
        if tier >= C.SPRITE.TILE_COUNT:
            raise AttributeError(f"Tier of tiles only go as high as {C.SPRITE.TILE_COUNT - 1}!")
        target_size = tuple( map(int, (size * C.SPRITE.TILE_SCALE for size in C.SPRITE.TILE_SIZE) ) )
        original = SpriteManager._retrieve_sprite(0, tier, C.SPRITE.TILE_OFFSET, C.SPRITE.TILE_SIZE,
                                                  C.SPRITE.TILE_MARGIN, C.SPRITE.TILE_ROWS, C.SPRITE.TILE_COLS, True)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_pad_surface(id: int):
        if id >= C.SPRITE.PAD_COUNT:
            raise AttributeError(f"ID of pads only go as high as {C.SPRITE.PAD_COUNT - 1}!")
        target_size = tuple( map(int, (size * C.SPRITE.PAD_SCALE for size in C.SPRITE.PAD_SIZE) ) )
        original = SpriteManager._retrieve_sprite(0, id, C.SPRITE.PAD_OFFSET, C.SPRITE.PAD_SIZE, C.SPRITE.PAD_MARGIN,
                                                  C.SPRITE.PAD_ROWS, C.SPRITE.PAD_COLS, False)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_longer_pad_surface(id: int):
        if id >= C.SPRITE.PAD_COUNT:
            raise AttributeError(f"ID of pads only go as high as {C.SPRITE.PAD_COUNT - 1}!")
        target_size = (int(C.SPRITE.PAD_SIZE[0] * C.SPRITE.PAD_SCALE * CF.LONG_PADDLE_SCALE),
                       int(C.SPRITE.PAD_SIZE[1] * C.SPRITE.PAD_SCALE) )
        original = SpriteManager._retrieve_sprite(0, id, C.SPRITE.PAD_OFFSET, C.SPRITE.PAD_SIZE, C.SPRITE.PAD_MARGIN,
                                                  C.SPRITE.PAD_ROWS, C.SPRITE.PAD_COLS, False)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_ball_surface(id: int):
        if id >= C.SPRITE.BALL_COUNT:
            raise AttributeError(f"ID of balls only go as high as {C.SPRITE.BALL_COUNT - 1}!")
        target_size = tuple( map(int, (size * C.SPRITE.BALL_SCALE for size in C.SPRITE.BALL_SIZE) ) )
        original = SpriteManager._retrieve_sprite(0, id, C.SPRITE.BALL_OFFSET, C.SPRITE.BALL_SIZE, C.SPRITE.BALL_MARGIN,
                                                  C.SPRITE.BALL_ROWS, C.SPRITE.BALL_COLS)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_strong_ball_surface(id: int):
        if id >= C.SPRITE.S_BALL_COUNT:
            raise AttributeError(f"ID of balls only go as high as {C.SPRITE.S_BALL_COUNT - 1}!")
        target_size = tuple( map(int, (size * C.SPRITE.S_BALL_SCALE for size in C.SPRITE.S_BALL_SIZE) ) )
        original = SpriteManager._retrieve_sprite(0, id, C.SPRITE.S_BALL_OFFSET, C.SPRITE.S_BALL_SIZE,
                                                  C.SPRITE.S_BALL_MARGIN, C.SPRITE.S_BALL_ROWS, C.SPRITE.S_BALL_COLS)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_heart_surface(is_empty: int):
        target_size = tuple( map(int, (size * C.SPRITE.HEART_SCALE for size in C.SPRITE.HEART_SIZE) ) )
        original = SpriteManager._retrieve_sprite(0, 1 if is_empty else 0, C.SPRITE.HEART_OFFSET, C.SPRITE.HEART_SIZE,
                                                  C.SPRITE.HEART_MARGIN, C.SPRITE.HEART_ROWS, C.SPRITE.HEART_COLS)
        return pygame.transform.scale(original, target_size)

    @staticmethod
    def get_random_background():
        return pygame.transform.scale(
            pygame.image.load(C.BG_PATHS[random.randint(0, len(C.BG_PATHS) - 1)]).convert(),
            (C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        )

    @staticmethod
    def get_tile_color(tile: pygame.sprite.Sprite):
        return tile.image.get_at( C.SPRITE.TILE_COLOR_SAMPLING_PIXEL )

    @staticmethod
    def get_powerup_ball_surface(id: int):
        if id >= C.SPRITE.POWERUP_COUNT:
            raise AttributeError(f"ID of powerups only go as high as {C.SPRITE.POWERUP_COUNT - 1}!")
        target_size = tuple( map(int, (size * C.SPRITE.POWERUP_SCALE for size in C.SPRITE.POWERUP_SIZE) ) )
        original = SpriteManager._retrieve_sprite(1, id, C.SPRITE.POWERUP_OFFSET, C.SPRITE.POWERUP_SIZE,
                                                  C.SPRITE.POWERUP_MARGIN, C.SPRITE.POWERUP_ROWS,
                                                  C.SPRITE.POWERUP_COLS)
        return pygame.transform.scale(original, target_size)
