import pygame

# A parallax effect background used when In Game. It takes in an image, which will be scaled up by a constant scale
# Every iteration of game loop, update(x_pos) will be called. Depending on the x position given, it determines how
# much x offset to be applied to the background.
# The maximum x offset should be the screen width, which will cause the rightmost of background to appear. The opposite
# applies to leftmost too.
class ParallaxBackground:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface, scale: float):
        self._screen = screen
        centerx, centery = self._screen.get_rect().center
        self._image = pygame.transform.smoothscale(image, (int(centerx * 2 * scale), int(centery * 2 * scale) ) )
        self._rect = self._image.get_rect(center=(centerx, centery) )
        self._diff = self._rect.width - self._screen.get_width()

    def update(self, x_pos):
        supposed_left = -( x_pos * self._diff / self._screen.get_width() )
        diff = self._rect.left - supposed_left
        self._rect.left -= diff / 10

    def render(self):
        self._screen.blit(self._image, self._rect)
