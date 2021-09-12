import random

import pygame

from src.SpriteManager import SpriteManager

# A basic ball. Bounces off the screen boundary only.
# Used in Main Menu, not really useful in game
class MenuBall(pygame.sprite.Sprite):
    def __init__(self, ball_id: int):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_ball_surface(ball_id)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(50, self._screen.get_width() - 50 )
        self.rect.centery = random.randrange(50, self._screen.get_height() - 50 )
        self.dx = random.choice( (-2, 2) )
        self.dy = random.choice( (-2, 2) )

    def update(self, dt):
        self.rect.left += round(self.dx * dt)
        if self.rect.left <= 0 or self.rect.right >= self._screen.get_width():
            self.dx *= -1
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(self._screen.get_width(), self.rect.right)

        self.rect.top += round(self.dy * dt)
        if self.rect.top <= 0 or self.rect.bottom >= self._screen.get_height():
            self.dy *= -1
            self.rect.top = max(0, self.rect.top)
            self.rect.bottom = min(self._screen.get_height(), self.rect.bottom)

    def render(self):
        self._screen.blit( self.image, self.rect )