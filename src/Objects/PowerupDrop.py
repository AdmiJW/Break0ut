import pygame
import random

import src.CONFIG as CF
from src.SpriteManager import SpriteManager
from src.Objects.Tile import Tile

import src.Powerups.RecoverHealth as RecoverHealth
import src.Powerups.StrongerBallPowerup as StrongerBallPowerup
import src.Powerups.LongerPaddlePowerup as LongerPaddlePowerup
import src.Powerups.DoubleBall as DoubleBall
import src.Powerups.IntoTheFuture as IntoTheFuture

# A Powerup Drop, which when collided with the paddle, will apply a powerup to
# the paddle
class PowerupDrop(pygame.sprite.Sprite):
    POWERUPS = ( RecoverHealth.RecoverHealth, StrongerBallPowerup.StrongerBallPowerup,
                 LongerPaddlePowerup.LongerPaddlePowerup, DoubleBall.DoubleBall, IntoTheFuture.IntoTheFuture )

    def __init__(self, powerup_id: int, centerx: int, centery: int):
        super().__init__()
        self.id = powerup_id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_powerup_ball_surface(self.id)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)

    def update(self, dt):
        self.rect.top += round( CF.POWERUP_DROP_SPEED * dt)

    # Returns the corresponding Powerup class, which will be used in Playing.apply_powerup()
    def retrieve_powerup(self):
        return PowerupDrop.POWERUPS[ self.id ]

    # If is expired, remove from sprite Group
    def is_expired(self):
        return self.rect.top > self._screen.get_height()

    # Makes an attempt to generate a powerdrop centered at the tile provided.
    # If generation fails (diceroll fail), then return None
    # Otherwise, an instance of PowerupDrop is returned.
    @staticmethod
    def attempt_generation(tile: Tile):
        if random.random() < CF.POWERUP_DROP_CHANCE:
            return PowerupDrop(
                random.choices( tuple(range(len(PowerupDrop.POWERUPS))), CF.POWERUP_WEIGHTS )[0],
                *tile.rect.center
            )
        return None
