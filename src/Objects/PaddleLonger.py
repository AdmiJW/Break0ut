import pygame
from src.SpriteManager import SpriteManager

from src.Objects.Paddle import Paddle

# Paddle but longer. Used in LongerPaddlePowerup powerup
# Simply inherits regular Paddle
class PaddleLonger( Paddle ):
    def __init__(self, short_paddle: Paddle):
        self.id = short_paddle.id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_longer_pad_surface(self.id)
        self.rect = self.image.get_rect(center=short_paddle.get_rect().center)
        self.dx = short_paddle.dx
        self.x_acceleration = short_paddle.x_acceleration
