# If removed, will cause circular import issue:
# - Playing state imports Powerup, Powerup also import Playing state, although it is used for Type Hinting onlys
from __future__ import annotations

import src.CONFIG as CF
from src.Objects.BallMacho import BallMacho

import src.Audio as Audio

import src.Powerups.BasePowerup as BasePowerup
import src.States.InGameStates.Playing as Playing

# The ball will now deal 2x damage, for set amount of time
class StrongerBallPowerup(BasePowerup.BasePowerup):
    def __init__(self, state: Playing.Playing):
        self.old_ball = state.ball
        self.macho_ball = BallMacho(self.old_ball)
        state.ball = self.macho_ball
        # Set time here
        state.powerup_timeleft = CF.DESIRED_FPS * CF.STRONG_BALL_DURATION

        Audio.play_stronger_ball()


    def teardown(self, state: Playing.Playing):
        # Update position of old ball, then swap back.
        self.old_ball.get_rect().center = self.macho_ball.get_rect().center
        self.old_ball.dx = self.macho_ball.dx
        self.old_ball.dy = self.macho_ball.dy
        state.ball = self.old_ball
