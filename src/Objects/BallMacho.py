import pygame

from src.SpriteManager import SpriteManager

import src.Objects.Ball as Ball

# STONK Ball, used in StrongerBallPowerup
# Inherits regular Ball so I don't have to write again (DUH)
class BallMacho(Ball.Ball):
    # Only thing overridden is the constructor. This behaves kind of like a copy constructor
    def __init__(self, weak_ball: Ball.Ball):
        self.id = weak_ball.id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_strong_ball_surface(self.id)
        self.rect = self.image.get_rect( center=weak_ball.rect.center )
        self.max_resultant_velocity = weak_ball.max_resultant_velocity
        self.dx = weak_ball.dx
        self.dy = weak_ball.dy
        self.ball_power = 2