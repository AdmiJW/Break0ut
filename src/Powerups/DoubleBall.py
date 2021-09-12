# If removed, will cause circular import issue:
# - Playing state imports Powerup, Powerup also import Playing state, although it is used for Type Hinting onlys
from __future__ import annotations

import src.CONFIG as CF
import src.utils as utils
from src.Objects.Ball import Ball
from src.Objects.NullBall import NullBall

import src.Audio as Audio

import src.Powerups.BasePowerup as BasePowerup
import src.States.InGameStates.Playing as Playing

# Second ball: Bonjour
class DoubleBall(BasePowerup.BasePowerup):
    def __init__(self, state: Playing.Playing):
        # Overrides the render and update method. Introduce ball2
        state.ball2 = Ball.copy_constructor(state.ball)
        state.ball2.image.set_alpha(128)
        state.ball2.get_rect().centerx = state.paddle.get_rect().centerx
        state.ball2.get_rect().bottom = state.paddle.get_rect().top
        state.ball2.dx = 0
        state.ball2.dy = state.ball2.max_resultant_velocity

        # Strategy: Overriding method
        state.overridden_update_strategy = DoubleBall.update
        state.overridden_render_strategy = DoubleBall.render

        state.powerup_timeleft = CF.DESIRED_FPS * CF.DOUBLE_BALL_DURATION

        Audio.play_double_ball()


    def teardown(self, state: Playing.Playing):
        # Revert the render and update method. Eliminate ball2
        state.ball2 = NullBall()
        state.overridden_update_strategy = None
        state.overridden_render_strategy = None

    ######################################################
    # Strategy pattern: Update method for double ball
    @staticmethod
    def update(self: Playing.Playing):
        dt = self._clock.tick(CF.DESIRED_FPS) * 0.001 * CF.DESIRED_FPS

        self.update_paddle(dt)
        self.update_background()

        self.update_powerup_drops(dt)
        self.handle_powerup_paddle_collision()

        self.update_ball_horizontal(dt, self.ball)
        self.update_ball_horizontal(dt, self.ball2)
        self.handle_ball_paddle_collision_horizontal(self.ball)
        self.handle_ball_paddle_collision_horizontal(self.ball2)
        self.handle_ball_tile_collision_horizontal(self.ball)
        self.handle_ball_tile_collision_horizontal(self.ball2)

        self.update_ball_vertical(dt, self.ball)
        self.update_ball_vertical(dt, self.ball2)
        self.handle_ball_paddle_collision_vertical(self.ball)
        self.handle_ball_paddle_collision_vertical(self.ball2)
        self.handle_ball_tile_collision_vertical(self.ball)
        self.handle_ball_tile_collision_vertical(self.ball2)

        # The logic to check ball below screen is overwritten:
        # If a ball falls, another ball is still there. We'll allow for that to happen.
        if self.ball.get_rect().top > self._screen.get_height():
            self.ball = self.ball2
            self.ball.image.set_alpha(255)
            self.powerup_timeleft = 0
        elif self.ball2.get_rect().top > self._screen.get_height():
            self.powerup_timeleft = 0

        self.update_tilegroup()
        self.check_level_cleared()
        self.update_particle_system(dt)
        self.update_powerup_expiration(dt)

    # Strategy pattern: Render method for double ball
    @staticmethod
    @utils.show_fps_if_set
    @utils.show_score_and_heart
    def render(self: Playing.Playing):
        self.background.render()
        self.paddle.render()
        self.ball.render()
        self.ball2.render()
        self.tilegroup.draw(self._screen)
        self._particlesystem.draw(self._screen)
        self.powerup_drop_group.draw(self._screen)
