import pygame

import src.Objects.Ball as Ball

# Ball used for IntoTheFuture Powerup
# Only difference is no sound on paddle collision
class PreviewerBall(Ball.Ball):
    def __init__(self, real_ball: Ball.Ball):
        self.id = real_ball.id
        self._screen = pygame.display.get_surface()
        self.image = real_ball.image.copy()
        self.rect = self.image.get_rect( center=real_ball.rect.center )
        self.max_resultant_velocity = real_ball.max_resultant_velocity
        self.dx = real_ball.dx
        self.dy = real_ball.dy
        self.ball_power = 0

    def handle_paddle_collision_horizontal(self, paddle):
        if self.rect.colliderect(paddle.get_rect()):
            self.adjust_ball_collision_horizontal(paddle)
    def handle_paddle_collision_vertical(self, paddle):
        if self.rect.colliderect(paddle.get_rect()):
            self.adjust_ball_collision_vertical(paddle)