import random

import pygame
import src.CONFIG as CF
import src.CONSTANTS as C
from functools import wraps

import src.FontFactory as FontFactory
from src.Objects.ScrollingBackground import ScrollingBackground
from src.SpriteManager import SpriteManager

#########################
# Utility functions
#########################

# Given an image, will return a new Surface that is the outline of the given image (with provided color, except (0,0,0))
# (0,0,0) is used as set_colorkey, otherwise the outline will have a black background over it.
# If you want a image with outline, consider using below - compile_outlines() function!
def generate_outline(image: pygame.Surface, color=(1, 1, 1), outline_width=6):
    if color == (0, 0, 0):
        raise AttributeError('Cannot use color of (0,0,0) in get_outline() method. Consider other colors that are close'
                             'to black if you insist, like (1,1,1)')

    result = pygame.Surface((image.get_width() + outline_width, image.get_height() + outline_width))

    # The mask surface is an image of black and white. Black - Transparent pixels. White - Opaque pixels
    mask = pygame.mask.from_surface(image)
    mask_surface = mask.to_surface()

    # Replace the white parts with the provided color
    mask = pygame.PixelArray(mask_surface)
    mask.replace((255, 255, 255), color)  # Replacing white to the provided color
    mask_surface = mask.surface
    del mask
    mask_surface.set_colorkey((0, 0, 0))

    # Blit the outline around the edges
    result.blit(mask_surface, (0, 0))
    result.blit(mask_surface, (outline_width, 0))
    result.blit(mask_surface, (0, outline_width))
    result.blit(mask_surface, (outline_width, outline_width))
    result.set_colorkey((0, 0, 0))

    return result


# Given an image you wanted to add outline(s), as indicated in outlines list:
#       [ (color1, width1), (color2, width2)... ]
# will return a final Surface which is the image with outlines blitted unders it.
# (Outline will be blitted from left to right in the list, thus leftmost outline is the bottom layer!)
def compile_outlines(image: pygame.Surface, outlines: list[tuple, int]):
    final_surface = image

    for ol in outlines:
        new_layer = generate_outline(final_surface, *ol)
        center = new_layer.get_rect().center
        new_layer.blit(final_surface, final_surface.get_rect(center=center))
        new_layer.set_colorkey((0, 0, 0))
        final_surface = new_layer

    return final_surface


# You've seen texts that the upper half is some lighter color, and the bottom half is darker color.
# This is the utility function you're looking to achieve that effect
#
# color1 is the color of upper half
# color2 is the color of lower half
def get_shaded_text(font: pygame.font.Font, text: str, color1, color2, antialias=True):
    text_1 = font.render(text, antialias, color1)
    width, height = text_1.get_size()
    text_2_lower = font.render(text, antialias, color2).subsurface((0, height / 2, width, height / 2))
    text_2_lower_rect = text_2_lower.get_rect()
    text_2_lower_rect.top = text_1.get_height() // 2

    text_1.blit(text_2_lower, text_2_lower_rect)
    return text_1


# A decorator to be put on state's render() method.
# Will render a fps text at leftmost corner, if CONFIG.SHOW_FPS is True
_FPS_FONT = pygame.font.SysFont('Arial', 15)
def show_fps_if_set(render_func):
    @wraps(render_func)
    def decorated_render_func(self):
        render_func(self)

        if CF.SHOW_FPS:
            fps_txt = _FPS_FONT.render(f'FPS: { int(self._clock.get_fps() ) }', True, C.RED)
            self._screen.blit(fps_txt, (4, 4))

    return decorated_render_func

# A decorator to render the score as well as the hearts in the render() method
def show_score_and_heart(render_func):
    HEART_FULL = SpriteManager.get_heart_surface(False)
    HEART_EMPTY = SpriteManager.get_heart_surface(True)
    HEART_RECTS = [
        HEART_EMPTY.get_rect(top=11, centerx=C.SCREEN_WIDTH // 2 - HEART_FULL.get_width() ),
        HEART_EMPTY.get_rect(top=11, centerx=C.SCREEN_WIDTH // 2),
        HEART_EMPTY.get_rect(top=11, centerx=C.SCREEN_WIDTH // 2 + HEART_FULL.get_width() ),
    ]

    @wraps(render_func)
    def decorated_render_func(self):
        render_func(self)

        # Blit the score
        score = FontFactory.FontFactory.generate_m_text(f"Score: {self.score}", C.YELLOW_1, C.YELLOW_2)
        self._screen.blit(score, score.get_rect(top=0, right=self._screen.get_width() - 2) )
        # Blit the hearts
        for i in range(1,4):
            self._screen.blit( HEART_FULL if self.lives_left >= i else HEART_EMPTY, HEART_RECTS[i-1] )
    return decorated_render_func

# A decorator to show how much powerup time left
def show_powerup_timeleft(render_func):
    @wraps(render_func)
    def decorated_render_func(self):
        render_func(self)

        if self.powerup is not None:
            progress_bar = pygame.Surface( (self.powerup_timeleft // 15, 10) )
            progress_bar.fill( (C.YELLOW_2) )
            progress_bar = compile_outlines( progress_bar, [(C.BLACK, 8)] )
            self._screen.blit( progress_bar, (5,5) )
    return decorated_render_func

# Creates a ScrollingBackground with random configuration
def get_random_scrolling_background(screen: pygame.Surface):
    return ScrollingBackground( screen, SpriteManager.get_random_background(),
                                random.choice((True, False)))


# Return value clamped by the minimum and maximum value.
def clamp(minimum, val, maximum):
    return max(minimum, min(maximum, val) )
