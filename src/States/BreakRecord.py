import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

from src.FontFactory import FontFactory
from src.HighscoreManager import HighscoreManager

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.HighScore as HighScore
import src.States.Quit as Quit


# BreakRecord state - User successfully broke the record. Asks for name input
class BreakRecord(AbstractState.AbstractState):
    _OVERRIDDEN_FPS = 40

    def __init__(self, clock: pygame.time.Clock, final_score: int):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self._final_score = final_score

        self._name = ['A','A','A']
        # Selection of 0,1,2 corresponds to the 3 characters in name selection. Selection of 4 means highlight 'CONFIRM'
        self._selection = 0

        centerx, centery = self._screen.get_rect().center

        # Background related
        self._background = utils.get_random_scrolling_background(self._screen)

        ###############
        # Texts
        ###############
        self._title = FontFactory.generate_xl_text('NEW RECORD', C.YELLOW_1, C.YELLOW_2)
        self._prompt = FontFactory.generate_m_text('Enter Name:', C.WHITE, C.WHITE_2)
        self._char1 = FontFactory.generate_xl_text( self._name[0], C.BLUE_1, C.BLUE_2 )
        self._char2 = FontFactory.generate_xl_text( self._name[1], C.BLUE_1, C.BLUE_2 )
        self._char3 = FontFactory.generate_xl_text( self._name[2], C.BLUE_1, C.BLUE_2)
        self._confirm = FontFactory.generate_l_text('CONFIRM', C.WHITE, C.WHITE_3)
        self._confirm_h = FontFactory.generate_l_text('CONFIRM', C.YELLOW_1, C.YELLOW_2)

        self._up_arrow = pygame.transform.rotate( FontFactory.generate_m_text('>', C.YELLOW_1, C.YELLOW_2), 90)
        self._down_arrow = pygame.transform.rotate( FontFactory.generate_m_text('>', C.YELLOW_1, C.YELLOW_2), -90)

        self._title_rect = self._title.get_rect(center=(centerx, centery-180) )
        self._prompt_rect = self._prompt.get_rect(center=(centerx, centery-90) )
        self._char1_rect = self._char1.get_rect(center=(centerx-100, centery+20) )
        self._char2_rect = self._char2.get_rect(center=(centerx, centery+20) )
        self._char3_rect = self._char3.get_rect(center=(centerx+100, centery+20) )
        self._confirm_rect = self._confirm.get_rect(center=(centerx, centery+200) )

        # Audio
        Audio.play_main_menu()


    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                # Enter key / Spacebar
                if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and self._selection == 3:
                    name = ''.join( self._name )
                    HighscoreManager.insert_score( ''.join(name), self._final_score )
                    self._next_state = HighScore.HighScore( self._clock, name )
                    Audio.play_selected()
                # Down key / S key
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self._selection != 3:
                    c = self._name[ self._selection ]
                    self._name[ self._selection ] = chr( max(ord('A'), (ord(c) + 1) % (ord('Z') + 1 )))
                    Audio.play_change_selection()
                # Up key / W key
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self._selection != 3:
                    c = self._name[ self._selection ]
                    self._name[ self._selection ] = chr( ord('Z') if c == 'A' else ord(c) - 1 )
                    Audio.play_change_selection()
                # Left key / A key
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self._selection = max(0, self._selection - 1)
                    Audio.play_change_selection()
                # Right key / D key
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self._selection = min(3, self._selection + 1)
                    Audio.play_change_selection()



    def update(self):
        dt = self._clock.tick( BreakRecord._OVERRIDDEN_FPS or CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self._background.update(dt)

        # Update the image of name selection
        self._char1 = FontFactory.generate_xl_text( self._name[0],
                                                    C.YELLOW_1 if self._selection == 0 else C.BLUE_1,
                                                    C.YELLOW_2 if self._selection == 0 else C.BLUE_2)
        self._char2 = FontFactory.generate_xl_text(self._name[1],
                                                   C.YELLOW_1 if self._selection == 1 else C.BLUE_1,
                                                   C.YELLOW_2 if self._selection == 1 else C.BLUE_2)
        self._char3 = FontFactory.generate_xl_text(self._name[2],
                                                   C.YELLOW_1 if self._selection == 2 else C.BLUE_1,
                                                   C.YELLOW_2 if self._selection == 2 else C.BLUE_2)


    @utils.show_fps_if_set
    def render(self):
        self._background.render()

        # Render Texts
        self._screen.blit(self._title, self._title_rect )
        self._screen.blit(self._prompt, self._prompt_rect)
        self._screen.blit(self._char1, self._char1_rect)
        self._screen.blit(self._char2, self._char2_rect)
        self._screen.blit(self._char3, self._char3_rect)
        self._screen.blit(self._confirm_h if self._selection == 3 else self._confirm, self._confirm_rect)

        # Render arrow for text selection
        if self._selection == 0:
            self._screen.blit(self._up_arrow, self._up_arrow.get_rect(center=self._char1_rect.center).move(-5, -60) )
            self._screen.blit(self._down_arrow, self._down_arrow.get_rect(center=self._char1_rect.center).move(-5, 70))
        elif self._selection == 1:
            self._screen.blit(self._up_arrow, self._up_arrow.get_rect(center=self._char2_rect.center).move(-5, -60) )
            self._screen.blit(self._down_arrow, self._down_arrow.get_rect(center=self._char2_rect.center).move(-5, 70))
        elif self._selection == 2:
            self._screen.blit(self._up_arrow, self._up_arrow.get_rect(center=self._char3_rect.center).move(-5, -60) )
            self._screen.blit(self._down_arrow, self._down_arrow.get_rect(center=self._char3_rect.center).move(-5, 70))

    def get_next_state(self):
        return self._next_state
