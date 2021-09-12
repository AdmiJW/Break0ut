import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

import src.Audio as Audio

from src.FontFactory import FontFactory
from src.HighscoreManager import HighscoreManager

import src.States.AbstractState as AbstractState
import src.States.MainMenu as MainMenu
import src.States.Quit as Quit


class HighScore(AbstractState.AbstractState):
    _OVERRIDDEN_FPS = 40

    def __init__(self, clock: pygame.time.Clock, highlighted_name:str = None):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        centerx, centery = self._screen.get_rect().center

        # Background related
        self._background = utils.get_random_scrolling_background(self._screen)

        ###############
        # Texts
        ###############
        self._title = FontFactory.generate_l_text('High Scores', C.WHITE, C.WHITE_3)
        self._ranks = [
            FontFactory.generate_m_text(f'{i+1}.   {name}   {score}',
                                        C.YELLOW_1 if name == highlighted_name else C.BLUE_1,
                                        C.YELLOW_2 if name == highlighted_name else C.BLUE_2)
            for i, (name, score) in enumerate( HighscoreManager.get_highscores() )
        ]
        self._back = FontFactory.generate_l_text('BACK', C.YELLOW_1, C.YELLOW_2)

        self._title_rect = self._title.get_rect(center=(centerx, centery - 200))
        self._rank_rects = [
            txt.get_rect(left=(centerx-220)+(i//5 * 270), centery=(centery-100)+(i%5 * 40) )
            for i, txt in enumerate(self._ranks)
        ]
        self._back_rect = self._back.get_rect(center=(centerx, centery+200) )



    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._next_state = MainMenu.MainMenu( self._clock )
                    Audio.play_selected()


    def update(self):
        dt = self._clock.tick( HighScore._OVERRIDDEN_FPS or CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self._background.update(dt)


    @utils.show_fps_if_set
    def render(self):
        self._background.render()

        self._screen.blit(self._title, self._title_rect )
        for rank_txt, rank_rect in zip( self._ranks, self._rank_rects ):
            self._screen.blit(rank_txt, rank_rect)

        self._screen.blit(self._back, self._back_rect)


    def get_next_state(self):
        return self._next_state
