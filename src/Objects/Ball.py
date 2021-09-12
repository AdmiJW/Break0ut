import pygame
import math

import src.utils as utils
import src.CONFIG as CF

import src.Audio as Audio

from src.SpriteManager import SpriteManager

import src.Objects.Paddle as Paddle

# Regular ball used in game
class Ball(pygame.sprite.Sprite):
    # The ball will be initialized such that it is located above the paddle
    # The max_resultant_velocity indicates the maximum velocity the ball can go.
    # One might implement the ball such that dy is constant throughout the game (just changing signs), but that will
    # result in a ball that is slow when dx = 0, but fast when the magnitude of dx is high
    def __init__(self, ball_id: int, max_resultant_velocity:int = CF.BALL_BASE_RESULTANT_VELOCITY):
        super().__init__()
        self.id = ball_id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_ball_surface(ball_id)
        self.rect = self.image.get_rect()
        self.max_resultant_velocity = max_resultant_velocity
        self.dx = 0
        self.dy = 0
        self.ball_power = 1

    # Copy constructor to another ball
    @staticmethod
    def copy_constructor(ball):
        new_ball = Ball(ball.id, ball.max_resultant_velocity)
        new_ball.rect = ball.rect.copy()
        new_ball.dx = ball.dx
        new_ball.dy = ball.dy
        new_ball.ball_power = ball.ball_power
        return new_ball

    # Updates the max resultant velocity
    # Useful if, say you have a powerup to slow down time ( Not implemented yet lmao )
    def set_max_resultant_velocity(self, new_value):
        self.max_resultant_velocity = new_value

    # Move horizontally
    def update_horizontal(self, dt):
        self.rect.left += round(self.dx * dt)
        if self.rect.left <= 0 or self.rect.right >= self._screen.get_width():
            self.dx *= -1
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(self._screen.get_width(), self.rect.right)

    # Move vertically
    def update_vertical(self, dt):
        self.rect.top += round(self.dy * dt)
        if self.rect.top <= 0:
            self.dy *= -1
            self.rect.top = max(0, self.rect.top)

    # Launch() is called during Serving state, which launches the ball upwards
    def launch(self):
        self.dx = 0
        self.dy = -self.max_resultant_velocity

    # Handles tile collision from the sides
    # The tiles are Tile instances THAT ARE ALREADY CONFIRMED TO BE COLLIDING
    # We only take the first tile for sampling, no need to handle all tiles, as it may cause implementation to be harder
    def handle_tile_collision_horizontal(self, tiles):
        sample_tile = tiles[0]
        if self.dx > 0:
            self.rect.right = sample_tile.rect.left
        else:
            self.rect.left = sample_tile.rect.right
        self.dx = -self.dx

    # Handles tile collision from above and below
    # The tiles are Tile instances THAT ARE ALREADY CONFIRMED TO BE COLLIDING
    # We only take the first tile for sampling, no need to handle all tiles, as it may cause implementation to be harder
    def handle_tile_collision_vertical(self, tiles):
        sample_tile = tiles[0]
        if self.dy > 0:
            self.rect.bottom = sample_tile.rect.top
        else:
            self.rect.top = sample_tile.rect.bottom
        self.dy = -self.dy


    # Handles paddle collision from the sides
    # If hit from the side, the ball will have same dx velocity as the paddle, and have its position adjusted
    def handle_paddle_collision_horizontal(self, paddle: Paddle.Paddle):
        if self.rect.colliderect(paddle.get_rect()):
            Audio.play_paddle_collision()
            self.adjust_ball_collision_horizontal(paddle)

    # A method to adjust ball's dy and position after colliding horizontally
    def adjust_ball_collision_horizontal(self, paddle: Paddle.Paddle):
        paddle_rect = paddle.get_rect()
        self.dx = -self.dx
        # If ball's bottom point is still above paddle's center, then let it rebounce
        # Otherwise, the ball's dy direction won't change (the ball keep going downwards)
        if self.rect.bottom < paddle_rect.centery:
            self.dy = -self.dy

        if self.rect.left < paddle_rect.left:
            self.rect.right = paddle_rect.left
        else:
            self.rect.left = paddle_rect.right

    # Handles ball collision with paddle from above. This method does not implement collision from below the paddle
    def handle_paddle_collision_vertical(self, paddle: Paddle.Paddle):
        if self.rect.colliderect(paddle.get_rect()):
            Audio.play_paddle_collision()
            self.adjust_ball_collision_vertical(paddle)

    # A method to adjust ball's dy and position after colliding vertically
    def adjust_ball_collision_vertical(self, paddle: Paddle.Paddle):
        paddle_rect = paddle.get_rect()
        self.dx = utils.clamp(-self.max_resultant_velocity + 1,
                              (self.rect.centerx - paddle_rect.centerx) // 6,
                              self.max_resultant_velocity - 1)
        self.dy = -math.sqrt(self.max_resultant_velocity ** 2 - self.dx ** 2)
        self.rect.bottom = paddle_rect.top

    def get_rect(self):
        return self.rect

    def render(self):
        self._screen.blit( self.image, self.rect )
