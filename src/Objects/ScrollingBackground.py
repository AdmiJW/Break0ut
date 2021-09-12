import pygame

# A infinite scrolling background. It takes in an image (which can be infinite scrolled)
# The infinite scrolling works by blitting the same image two times, side by side.
# If left_to_right is True (default), the image scrolls left to right. Otherwise, top to bottom
class ScrollingBackground:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface, left_to_right: bool=True, speed: int=2):
        self._screen = screen
        self._image = image
        self._rect_1 = self._image.get_rect()
        self._rect_2 = self._image.get_rect()
        self._is_left_to_right = left_to_right
        self._speed = speed

        if self._is_left_to_right:
            self._rect_2.left = self._rect_1.right
        else:
            self._rect_2.top = self._rect_1.bottom

    def update(self, dt):
        if self._is_left_to_right:
            self._rect_1.left -= round(self._speed * dt)
            if self._rect_1.right < 0:
                self._rect_1.left = 0
            self._rect_2.left = self._rect_1.right
        else:
            self._rect_1.top -= round(self._speed * dt)
            if self._rect_1.bottom < 0:
                self._rect_1.top = 0
            self._rect_2.top = self._rect_1.bottom

    def render(self):
        self._screen.blit(self._image, self._rect_1 )
        self._screen.blit(self._image, self._rect_2 )