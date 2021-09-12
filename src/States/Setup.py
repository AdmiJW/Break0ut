import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

from src.SpriteManager import SpriteManager
from src.FontFactory import FontFactory

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.MainMenu as MainMenu
import src.States.InGameStates.Initialization as Initialization
import src.States.Quit as Quit


# Setup State - Allows player to select paddle and ball
class Setup(AbstractState.AbstractState):
    _OVERRIDDEN_FPS = 40
    _NUM_CHOICES = 4

    def __init__(self, clock: pygame.time.Clock):
        self._screen = pygame.display.get_surface()
        self._clock = clock

        self._next_state = self
        self._current_selection = 0
        self._paddle_selection = 0
        self._ball_selection = 0

        centerx, centery = self._screen.get_rect().center

        # Background related
        self._background = utils.get_random_scrolling_background(self._screen)

        # Paddles and Balls
        self._paddles = [SpriteManager.get_pad_surface(i) for i in range(C.SPRITE.PAD_COUNT)]
        self._balls = [SpriteManager.get_ball_surface(i) for i in range(C.SPRITE.BALL_COUNT)]
        self._paddle_rects = [
            self._paddles[i].get_rect(center=((1+2*i)*centerx, centery-80)) for i in range(len(self._paddles))
        ]
        self._ball_rects = [
            self._balls[i].get_rect(center=((1 + 2 * i) * centerx, centery + 65)) for i in range(len(self._paddles))
        ]

        ###############
        # Texts
        ###############
        self._title = FontFactory.generate_l_text('SETUP', C.WHITE, C.WHITE_3)
        self._selections = [
            (FontFactory.generate_m_text('SELECT PADDLE', C.WHITE, C.WHITE_2),
             FontFactory.generate_m_text('SELECT PADDLE', C.YELLOW_1, C.YELLOW_2)),
            (FontFactory.generate_m_text('SELECT BALL', C.WHITE, C.WHITE_2),
             FontFactory.generate_m_text('SELECT BALL', C.YELLOW_1, C.YELLOW_2)),
            (FontFactory.generate_l_text('PROCEED!!!', C.WHITE, C.WHITE_2),
             FontFactory.generate_l_text('PROCEED!!!', C.YELLOW_1, C.YELLOW_2)),
            (FontFactory.generate_m_text('Back To Main Menu', C.WHITE, C.WHITE_2),
             FontFactory.generate_m_text('Back To Main Menu', C.YELLOW_1, C.YELLOW_2)),
        ]
        self._left_arrow = FontFactory.generate_m_text('<', C.YELLOW_1, C.YELLOW_2)
        self._right_arrow = FontFactory.generate_m_text('>', C.YELLOW_1, C.YELLOW_2)

        self._title_rect = self._title.get_rect(center=(centerx, centery - 200))
        self._selection_rects = [
            self._selections[0][0].get_rect(center=(centerx, centery - 140)),
            self._selections[1][0].get_rect(center=(centerx, centery - 20)),
            self._selections[2][0].get_rect(center=(centerx, centery + 150)),
            self._selections[3][0].get_rect(center=(centerx, centery + 210)),
        ]
        self._paddle_l_rect = self._left_arrow.get_rect(center=(centerx-200, centery-80))
        self._paddle_r_rect = self._right_arrow.get_rect(center=(centerx+200, centery-80))
        self._ball_l_rect = self._left_arrow.get_rect(center=(centerx-200, centery+65))
        self._ball_r_rect = self._right_arrow.get_rect(center=(centerx+200, centery+65))



    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                # Down key / S key
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self._current_selection = (self._current_selection + 1) % Setup._NUM_CHOICES
                    Audio.play_change_selection()
                # Up key / W key
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self._current_selection = Setup._NUM_CHOICES - 1 if self._current_selection == 0 else self._current_selection - 1
                    Audio.play_change_selection()
                # Left key / A key
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self._current_selection == 0:
                        self._paddle_selection = max(0, self._paddle_selection - 1)
                    elif self._current_selection == 1:
                        self._ball_selection = max(0, self._ball_selection - 1)
                    Audio.play_change_selection()
                # Right key / D key
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self._current_selection == 0:
                        self._paddle_selection = min(C.SPRITE.PAD_COUNT - 1, self._paddle_selection + 1)
                    elif self._current_selection == 1:
                        self._ball_selection = min(C.SPRITE.BALL_COUNT - 1, self._ball_selection + 1)
                    Audio.play_change_selection()
                # Enter key / Spacebar
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self._current_selection == 2:
                        self._next_state = Initialization.Initialization(self._clock,
                                                                         self._paddle_selection,
                                                                         self._ball_selection,
                                                                         0, 0, 3)
                    elif self._current_selection == 3:
                        self._next_state = MainMenu.MainMenu(self._clock)
                    Audio.play_selected()



    def update(self):
        dt = self._clock.tick( Setup._OVERRIDDEN_FPS or CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS

        self._background.update(dt)
        centerx = self._screen.get_width() // 2
        # Update the smooth animation of paddle / ball selection
        for i in range(C.SPRITE.PAD_COUNT):
            supposed_x_pos = centerx * (1 + 2 * (i - self._paddle_selection) )
            self._paddle_rects[i].centerx += (supposed_x_pos - self._paddle_rects[i].centerx) // 4
        for i in range(C.SPRITE.BALL_COUNT):
            supposed_x_pos = centerx * (1 + 2 * (i - self._ball_selection) )
            self._ball_rects[i].centerx += (supposed_x_pos - self._ball_rects[i].centerx) // 4



    @utils.show_fps_if_set
    def render(self):
        self._background.render()

        # Render paddle and ball selection
        for paddle, paddle_rect in zip(self._paddles, self._paddle_rects):
            self._screen.blit(paddle, paddle_rect)
        for ball, ball_rect in zip(self._balls, self._ball_rects):
            self._screen.blit(ball, ball_rect)
        # Render left and right arrow
        if self._paddle_selection != 0:
            self._screen.blit( self._left_arrow, self._paddle_l_rect )
        if self._paddle_selection != C.SPRITE.PAD_COUNT - 1:
            self._screen.blit(self._right_arrow, self._paddle_r_rect)
        if self._ball_selection != 0:
            self._screen.blit(self._left_arrow, self._ball_l_rect)
        if self._ball_selection != C.SPRITE.BALL_COUNT - 1:
            self._screen.blit(self._right_arrow, self._ball_r_rect)

        self._screen.blit(self._title, self._title_rect )
        for i, (selection_txt, selection_rect) in enumerate( zip( self._selections, self._selection_rects ) ):
            self._screen.blit(selection_txt[1] if self._current_selection == i else selection_txt[0], selection_rect)


    def get_next_state(self):
        return self._next_state

