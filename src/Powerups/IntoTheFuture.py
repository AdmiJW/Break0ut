# If removed, will cause circular import issue:
# - Playing state imports Powerup, Powerup also import Playing state, although it is used for Type Hinting onlys
from __future__ import annotations
import pygame

import src.CONFIG as CF
import src.utils as utils
from src.Objects.PreviewerBall import PreviewerBall

import src.Audio as Audio

import src.Powerups.BasePowerup as BasePowerup
import src.States.InGameStates.Playing as Playing

# Predicts where the ball will move next. WOW
class IntoTheFuture(BasePowerup.BasePowerup):
    def __init__(self, state: Playing.Playing):
        # Overrides the render method.
        state.overridden_render_strategy = IntoTheFuture.render

        state.powerup_timeleft = CF.DESIRED_FPS * CF.INTO_THE_FUTURE_DURATION

        Audio.play_see_future()


    def teardown(self, state: Playing.Playing):
        # Revert the render method.
        state.overridden_render_strategy = None


    # Strategy pattern: Render method for double ball
    @staticmethod
    @utils.show_fps_if_set
    @utils.show_score_and_heart
    def render(self: Playing.Playing):
        self.background.render()
        self.paddle.render()
        self.ball.render()

        # Here, we'll really simulate the ball movement.
        shadow_ball = PreviewerBall(self.ball)
        shadow_ball.image.set_alpha( CF.INTO_THE_FUTURE_BASE_ALPHA )
        alpha_decrement = CF.INTO_THE_FUTURE_BASE_ALPHA // CF.INTO_THE_FUTURE_PREDICTIONS

        # How many predictions to be done?
        for i in range(CF.INTO_THE_FUTURE_PREDICTIONS):
            # Move horizontal
            self.update_ball_horizontal( CF.INTO_THE_FUTURE_STEP, shadow_ball )
            self.handle_ball_paddle_collision_horizontal( shadow_ball )
            collided_tiles = pygame.sprite.spritecollide(shadow_ball, self.tilegroup, False)
            if len(collided_tiles):
                shadow_ball.handle_tile_collision_horizontal(collided_tiles)

            # Move vertical
            self.update_ball_vertical( CF.INTO_THE_FUTURE_STEP, shadow_ball )
            self.handle_ball_paddle_collision_vertical( shadow_ball )
            collided_tiles = pygame.sprite.spritecollide(shadow_ball, self.tilegroup, False)
            if len(collided_tiles):
                shadow_ball.handle_tile_collision_vertical(collided_tiles)

            shadow_ball.render()
            shadow_ball.image.set_alpha( max(10, shadow_ball.image.get_alpha() - alpha_decrement ) )

        self.tilegroup.draw(self._screen)
        self._particlesystem.draw(self._screen)
        self.powerup_drop_group.draw(self._screen)
