import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

from src.Objects.ParallaxBackground import ParallaxBackground
from src.Objects.Paddle import Paddle
from src.Objects.Ball import Ball
from src.Objects.TileGroup import TileGroup

from src.FontFactory import FontFactory

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.InGameStates.Playing as Playing
import src.States.Quit as Quit


# --- Substate for InGame State, which is a state machine
# Serve state: Ball follows the paddle, a prompt text on screen to serve. Transitions to Playing state when
# user presses Spacebar
class Serve(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, paddle: Paddle, ball: Ball, tilegroup: TileGroup,
                 background: ParallaxBackground, level: int, score: int, lives_left: int, powerup=None,
                 powerup_timeleft=0):
        self._screen = pygame.display.get_surface()
        self._clock = clock

        self.paddle = paddle
        self.ball = ball
        self.level = level
        self.score = score
        self.lives_left = lives_left
        self.background = background
        self.tilegroup = tilegroup

        self.powerup = powerup
        self.powerup_timeleft = powerup_timeleft
        self.next_state = self

        # Centers the ball above the paddle
        self.ball.get_rect().centerx = self.paddle.get_rect().centerx
        self.ball.get_rect().bottom = self.paddle.get_rect().top

        # Text:
        self._prompt = FontFactory.generate_m_text('Press Spacebar to Serve!', C.YELLOW_1, C.YELLOW_2)
        self._prompt_rect = self._prompt.get_rect(center=(self._screen.get_width() // 2,
                                                          self._screen.get_height() - 100))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ball.launch()
                    self.next_state = Playing.Playing(self._clock, self.paddle, self.ball, self.tilegroup,
                                                      self.background, self.level, self.score, self.lives_left,
                                                      self.powerup, self.powerup_timeleft)
                    Audio.play_paddle_collision()
                else:
                    self.paddle.handle_event(event)
            elif event.type == pygame.KEYUP:
                self.paddle.handle_event(event)

    def update(self):
        dt = self._clock.tick(CF.DESIRED_FPS) * 0.001 * CF.DESIRED_FPS

        # Update paddle position, and the ball follows.
        self.paddle.update(dt)
        self.background.update(self.paddle.get_rect().centerx)
        self.ball.get_rect().centerx = self.paddle.get_rect().centerx


    @utils.show_fps_if_set
    @utils.show_score_and_heart
    def render(self):
        self.background.render()
        self.paddle.render()
        self.ball.render()
        self.tilegroup.draw(self._screen)

        self._screen.blit(self._prompt, self._prompt_rect)


    def get_next_state(self):
        return self.next_state
