import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

from src.Objects.ParallaxBackground import ParallaxBackground
from src.Objects.Paddle import Paddle
from src.Objects.Ball import Ball
from src.Objects.TileGroup import TileGroup

import src.Audio as Audio
from src.FontFactory import FontFactory

import src.States.AbstractState as AbstractState
import src.States.InGameStates.Serve as Serve
import src.States.Quit as Quit


# --- Substate for InGame State, which is a state machine
# When a level first starts, show which level they are in, before proceeding to Serving state
class SplashScreen(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, paddle: Paddle, ball: Ball, tilegroup: TileGroup,
                 background: ParallaxBackground, level: int, score: int, lives_left: int):
        self._screen = pygame.display.get_surface()
        self._clock = clock

        self.paddle = paddle
        self.ball = ball
        self.level = level
        self.score = score
        self.lives_left = lives_left
        self.background = background
        self.tilegroup = tilegroup
        self.next_state = self

        self._timer = CF.DESIRED_FPS * 4

        # Text:
        self._splash_text = FontFactory.generate_xl_text(f'Level {self.level + 1}', C.YELLOW_1, C.YELLOW_2)
        self._text_size = [self._splash_text.get_width() * 2, self._splash_text.get_height() * 2]

        # Audio
        Audio.stop_music()
        Audio.play_level_proceed()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = Quit.Quit()
            else:
                self.paddle.handle_event(event)

    def update(self):
        dt = self._clock.tick(CF.DESIRED_FPS) * 0.001 * CF.DESIRED_FPS

        # Updates the timer of Splash Screen
        self._timer -= dt
        if self._timer < 0:
            self.next_state = Serve.Serve(self._clock, self.paddle, self.ball, self.tilegroup,
                                          self.background, self.level, self.score, self.lives_left)

        # Update paddle position as well as ball above the paddle
        self.paddle.update(dt)
        self.background.update(self.paddle.get_rect().centerx)
        self.ball.get_rect().centerx = self.paddle.get_rect().centerx

        # Text Animation
        self._text_size[0] = max(self._splash_text.get_width(), self._text_size[0] * 0.993 ** round(dt) )
        self._text_size[1] = max(self._splash_text.get_height(), self._text_size[1] * 0.993 ** round(dt) )


    @utils.show_fps_if_set
    @utils.show_score_and_heart
    def render(self):
        self.background.render()
        self.paddle.render()
        self.ball.render()
        self.tilegroup.draw(self._screen)

        # Text Animation
        transformed_text = pygame.transform.scale(self._splash_text, (int(self._text_size[0]), int(self._text_size[1])))
        self._screen.blit(
            transformed_text,
            transformed_text.get_rect(center=self._screen.get_rect().center) )


    def get_next_state(self):
        return self.next_state
