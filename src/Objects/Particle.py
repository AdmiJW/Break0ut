import pygame
import random

import src.CONFIG as CF

# When the ball hits the tile, several particle will be generated.
# This is the class responsible for one such particle
class Particle(pygame.sprite.Sprite):
    # The ball will be initialized such that it is located above the paddle
    def __init__(self, color: pygame.Color, left:int, top:int ):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._sidelength = random.randint( CF.PARTICLE_MIN_SIZE, CF.PARTICLE_MAX_SIZE )
        self.image = pygame.Surface( (self._sidelength, self._sidelength) ).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(left=left, top=top)

    def update(self,dt):
        self.rect.top += CF.PARTICLE_SPEED * dt
        self.image.set_alpha( int(self.image.get_alpha() - CF.PARTICLE_FADING_SPEED * dt) )

    # Simple check if the particle is expired or not
    def is_expired(self):
        return not self.image.get_alpha()

