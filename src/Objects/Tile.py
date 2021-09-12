import pygame

from src.SpriteManager import SpriteManager

# Regular ball used in game
class Tile(pygame.sprite.Sprite):
    # The ball will be initialized such that it is located above the paddle
    def __init__(self, tile_id: int, left:int, top:int):
        super().__init__()
        self.tile_id = tile_id
        self._screen = pygame.display.get_surface()
        self.image = SpriteManager.get_tile_surface(tile_id)
        self.rect = self.image.get_rect(left=left, top=top)

        # Determines how many collisions needed until the tile is destroyed
        # -1 means destroyed
        self._life = tile_id

    # Called when the ball collides with this single tile.
    def on_collision(self, ball_power:int):
        self._life = max(-1, self._life - ball_power)
        if not self.is_destroyed():
            self.image = SpriteManager.get_tile_surface(self._life)

    # Simple check if the tile is destroyed or not
    def is_destroyed(self):
        return self._life == -1

