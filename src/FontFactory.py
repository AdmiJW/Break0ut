import pygame

import src.CONSTANTS as C
import src.utils as utils

# Class Specified to generate game-themed texts
class FontFactory:
    S_FONT = pygame.font.Font( C.FONT_PATH, 15 )
    M_FONT = pygame.font.Font( C.FONT_PATH, 30 )
    L_FONT = pygame.font.Font( C.FONT_PATH, 70 )
    XL_FONT = pygame.font.Font( C.FONT_PATH, 100 )

    @staticmethod
    def generate_s_text(text:str, color:tuple):
        return utils.compile_outlines(
            FontFactory.S_FONT.render(text, True, color),
            [(C.BLACK, 2)]
        )

    @staticmethod
    def generate_m_text(text:str, color1:tuple, color2:tuple):
        return utils.compile_outlines(
            utils.get_shaded_text(FontFactory.M_FONT, text, color1, color2),
            [(C.BLACK, 6)]
        )

    @staticmethod
    def generate_l_text(text:str, color1:tuple, color2:tuple):
        return utils.compile_outlines(
            utils.get_shaded_text(FontFactory.L_FONT, text, color1, color2),
            [(C.BLACK, 8), (C.WHITE, 4)]
        )

    @staticmethod
    def generate_xl_text(text:str, color1:tuple, color2:tuple):
        return utils.compile_outlines(
            utils.get_shaded_text(FontFactory.XL_FONT, text, color1, color2),
            [(C.BLACK, 8), (C.WHITE, 6)]
        )