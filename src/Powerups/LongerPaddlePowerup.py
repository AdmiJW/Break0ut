# If removed, will cause circular import issue:
# - Playing state imports Powerup, Powerup also import Playing state, although it is used for Type Hinting onlys
from __future__ import annotations

import src.CONFIG as CF
from src.Objects.PaddleLonger import PaddleLonger

import src.Audio as Audio

import src.Powerups.BasePowerup as BasePowerup
import src.States.InGameStates.Playing as Playing

# The paddle will be L O N G E R ;)
class LongerPaddlePowerup(BasePowerup.BasePowerup):
    def __init__(self, state: Playing.Playing):
        self.old_paddle = state.paddle
        self.long_paddle = PaddleLonger(self.old_paddle)
        state.paddle = self.long_paddle
        # Set time here
        state.powerup_timeleft = CF.DESIRED_FPS * CF.LONG_PADDLE_DURATION

        Audio.play_long_paddle()


    def teardown(self, state: Playing.Playing):
        # Update position of old ball, then swap back.
        self.old_paddle.get_rect().center = self.long_paddle.get_rect().center
        self.old_paddle.dx = self.long_paddle.dx
        self.old_paddle.x_acceleration = self.long_paddle.x_acceleration
        state.paddle = self.old_paddle
