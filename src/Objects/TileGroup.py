import pygame
import random

import src.CONSTANTS as C
import src.CONFIG as CF

from src.SpriteManager import SpriteManager
from src.Objects.Tile import Tile


# A TileGroup consists of collection of tiles that is present in a level.
class TileGroup(pygame.sprite.Group):
    def __init__(self, level: int):
        super().__init__()
        self._screen = pygame.display.get_surface()

        ######################
        # Tile Generation
        ######################
        sample_tile = SpriteManager.get_tile_surface(0)
        left_pad = (self._screen.get_width() - CF.TILE_PER_ROW * sample_tile.get_width()) // 2
        top_pad = 40

        # Generate the tiles
        for i in range(CF.TILE_ROW_COUNT):
            row = TileGroup._generate_row( min(C.SPRITE.TILE_COUNT - 1, level) )
            for j, tile_id in enumerate(row):
                if tile_id == -1: continue
                self.add( Tile(tile_id, j * sample_tile.get_width() + left_pad, i * sample_tile.get_height() + top_pad))


    # Checks for any tiles that are actually destroyed, and removes them
    # Also, returns the sum of tile_id from destroyed tiles
    def update(self):
        destroyed_tiles =  [sp for sp in self.sprites() if sp.is_destroyed() ]
        self.remove( destroyed_tiles )
        return sum( tile.tile_id + 1 for tile in destroyed_tiles )

    # Simply return a boolean value whether all the tiles are destroyed
    def is_cleared(self):
        return not bool( len(self.spritedict))


    #############################
    # Static Methods
    #############################
    # Generates a row of tile_id
    @staticmethod
    def _generate_row(max_id: int):
        return random.choice((
            TileGroup._generate_full_row,
            TileGroup._generate_spacial_odd_row,
            TileGroup._generate_spacial_even_row
        ))(max_id, random.choice((True,False)))

    # Generate two random tile_id in range of [0,max_id], (MAY REPEAT)
    @staticmethod
    def _generate_two_random_id(max_id: int):
        return random.randint(0, max_id), random.randint(0, max_id)

    # Generates a row like this:
    #   |XXXXXXXXXX|
    @staticmethod
    def _generate_full_row(max_id: int, is_alternate:bool = False):
        tile_id = TileGroup._generate_two_random_id(max_id)
        if is_alternate:
            return [ tile_id[i % 2] for i in range(CF.TILE_PER_ROW) ]
        else:
            return [ tile_id[0] ] * CF.TILE_PER_ROW

    # Generates a row like this:
    #   |X X X X X |
    @staticmethod
    def _generate_spacial_odd_row(max_id: int, is_alternate:bool = False):
        tile_id = TileGroup._generate_two_random_id(max_id)
        if is_alternate:
            return [ tile_id[ i // 2 % 2 ] if i % 2 == 0 else -1 for i in range(CF.TILE_PER_ROW) ]
        else:
            return [ tile_id[0] if i % 2 == 0 else -1 for i in range(CF.TILE_PER_ROW) ]

    # Generates a row like this:
    #   | X X X X X|
    @staticmethod
    def _generate_spacial_even_row(max_id: int, is_alternate:bool = False):
        tile_id = TileGroup._generate_two_random_id(max_id)
        if is_alternate:
            return [ tile_id[i // 2 % 2] if i % 2 else -1 for i in range(CF.TILE_PER_ROW) ]
        else:
            return [ tile_id[0] if i % 2 else -1 for i in range(CF.TILE_PER_ROW) ]