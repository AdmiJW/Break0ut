import pygame

import src.CONFIG as CF

from src.Objects.ParallaxBackground import ParallaxBackground
from src.SpriteManager import SpriteManager
from src.Objects.Paddle import Paddle
from src.Objects.Ball import Ball
from src.Objects.TileGroup import TileGroup

import src.States.AbstractState as AbstractState
import src.States.InGameStates.SplashScreen as SplashScreen


# Initialization state is a one iteration state, which only serves to initialize everything for a level.
class Initialization(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, paddle_id: int, ball_id: int, level: int,
                 score: int, lives_left: int):
        # Background related
        screen = pygame.display.get_surface()
        centerx = screen.get_rect().centerx
        background = ParallaxBackground(screen, SpriteManager.get_random_background(), CF.PARALLAX_BG_SCALE)

        # Paddles and Balls.
        # Ball's maximum resultant velocity is set according to the current level.
        # Reset to located at center
        paddle = Paddle(paddle_id)
        ball = Ball(ball_id, min(CF.BALL_MAX_RESULTANT_VELOCITY, CF.BALL_BASE_RESULTANT_VELOCITY + level / 2))
        paddle.get_rect().centerx = centerx
        paddle.get_rect().bottom = screen.get_height() - 10
        ball.get_rect().centerx = centerx
        ball.get_rect().bottom = paddle.get_rect().top

        # Tiles
        tilegroup = TileGroup( level )

        self.next_state = SplashScreen.SplashScreen( clock, paddle, ball, tilegroup, background,
                                                     level, score, lives_left )

    def get_next_state(self):
        return self.next_state
