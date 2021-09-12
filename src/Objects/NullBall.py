import pygame

import src.Objects.Paddle as Paddle

# Null object pattern applied to Ball
class NullBall(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect((0,0,0,0))
    def set_max_resultant_velocity(self, new_value): pass
    def update_horizontal(self, dt): pass
    def update_vertical(self, dt): pass
    def launch(self): pass
    def handle_tile_collision_horizontal(self, tiles): pass
    def handle_tile_collision_vertical(self, tiles): pass
    def handle_paddle_collision_horizontal(self, paddle: Paddle.Paddle): pass
    def handle_paddle_collision_vertical(self, paddle: Paddle.Paddle): pass
    def get_rect(self): return self.rect
    def render(self): pass
