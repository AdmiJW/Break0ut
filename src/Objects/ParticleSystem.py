import pygame
import random

import src.CONFIG as CF

from src.Objects.Tile import Tile
from src.SpriteManager import SpriteManager
from src.Objects.Particle import Particle

class ParticleSystem(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    # Remove all sprites that are expired.
    def eliminate_expired(self):
        self.remove( [ sp for sp in self.sprites() if sp.is_expired() ] )

    # Generates a Particle instance around the tile provided
    def generate_particles(self, tile: Tile):
        for i in range( random.randint(CF.MIN_PARTICLE_ON_COLLISION, CF.MAX_PARTICLE_ON_COLLISION) ):
            self.add( Particle(
                SpriteManager.get_tile_color(tile),
                random.randrange(tile.rect.left - CF.PARTICLE_MAX_SIZE, tile.rect.right),
                random.randrange(tile.rect.top, tile.rect.bottom) ) )
