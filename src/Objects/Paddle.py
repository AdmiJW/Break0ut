import pygame
from src.SpriteManager import SpriteManager

import src.CONFIG as CF

# Smooth Moving Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddle_id: int):
        super().__init__()
        self.id = paddle_id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_pad_surface(paddle_id)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.x_acceleration = 0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.x_acceleration = max(-CF.PADDLE_ACCELERATION, self.x_acceleration - CF.PADDLE_ACCELERATION)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.x_acceleration = min(CF.PADDLE_ACCELERATION, self.x_acceleration + CF.PADDLE_ACCELERATION)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.x_acceleration = min(CF.PADDLE_ACCELERATION, self.x_acceleration + CF.PADDLE_ACCELERATION)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.x_acceleration = max(-CF.PADDLE_ACCELERATION, self.x_acceleration - CF.PADDLE_ACCELERATION)

    def update(self, dt):
        # Update on velocity
        self.dx += self.x_acceleration
        # Update friction
        self.dx += -CF.PADDLE_FRICTION if self.dx > 0 else CF.PADDLE_FRICTION if self.dx < 0 else 0

        self.dx = min(CF.PADDLE_TERMINAL_VELO, self.dx)
        self.dx = max(-CF.PADDLE_TERMINAL_VELO, self.dx)


        # Update position
        self.rect.left += round(self.dx * dt)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self._screen.get_width(), self.rect.right)

    def render(self):
        self._screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect