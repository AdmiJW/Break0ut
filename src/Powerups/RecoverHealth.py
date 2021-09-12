# If removed, will cause circular import issue:
# - Playing state imports Powerup, Powerup also import Playing state, although it is used for Type Hinting onlys
from __future__ import annotations

import src.CONFIG as CF

import src.Audio as Audio

import src.Powerups.BasePowerup as BasePowerup
import src.States.InGameStates.Playing as Playing

# Simplest out of all the powerups
# Simply add 1 to the lives, if depleted.
class RecoverHealth(BasePowerup.BasePowerup):
    def __init__(self, state: Playing.Playing):
        state.lives_left = min(3, state.lives_left + CF.RECOVER_HEALTH_POWER)
        state.powerup_timeleft = -1

        Audio.play_recover_health()
