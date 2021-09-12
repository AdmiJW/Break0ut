import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

import src.Audio as Audio

from src.FontFactory import FontFactory
from src.Objects.MenuBall import MenuBall

import src.States.AbstractState as AbstractState
import src.States.Setup as Setup
import src.States.HighScore as HighScore
import src.States.Quit as Quit

class MainMenu(AbstractState.AbstractState):
    _NUM_CHOICES = 5
    _OVERRIDDEN_FPS = 40

    def __init__(self, clock: pygame.time.Clock):
        self._screen = pygame.display.get_surface()
        self._clock = clock

        self._next_state = self
        self._choice = 0

        centerx, centery = self._screen.get_rect().center

        # Background related
        self._background = utils.get_random_scrolling_background(self._screen)
        self._balls = [ MenuBall(i) for i in range(C.SPRITE.BALL_COUNT) ]

        ###############
        # Texts
        ###############
        self._title = FontFactory.generate_xl_text('Break0ut', C.WHITE, C.WHITE_3)
        self._choice_texts = [
            FontFactory.generate_m_text("Start Game", C.WHITE, C.WHITE_2),
            FontFactory.generate_m_text("Show/Hide FPS", C.WHITE, C.WHITE_2),
            FontFactory.generate_m_text("Toggle Fullscreen", C.WHITE, C.WHITE_2),
            FontFactory.generate_m_text("High Scores", C.WHITE, C.WHITE_2),
            FontFactory.generate_m_text("Quit Game", C.WHITE, C.WHITE_2)
        ]
        self._credit = FontFactory.generate_s_text('Created by AdmiJW', C.YELLOW_1)
        self._title_rect = self._title.get_rect(center=(centerx, centery - 150))
        self._choice_rects = [
            txt.get_rect(center=(centerx, centery + i * 50) ) for i, txt in enumerate(self._choice_texts)
        ]
        self._credit_rect = self._credit.get_rect(top=5, right=self._screen.get_width() - 5)

        # Audio
        Audio.play_main_menu()



    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self._choice = (self._choice + 1) % MainMenu._NUM_CHOICES
                    Audio.play_change_selection()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self._choice = MainMenu._NUM_CHOICES - 1 if self._choice == 0 else self._choice - 1
                    Audio.play_change_selection()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self._choice == 0:
                        self._next_state = Setup.Setup(self._clock)
                    elif self._choice == 1:
                        CF.SHOW_FPS = not CF.SHOW_FPS
                    elif self._choice == 2:
                        pygame.display.toggle_fullscreen()
                    elif self._choice == 3:
                        self._next_state = HighScore.HighScore(self._clock)
                    else:
                        self._next_state = Quit.Quit()
                    Audio.play_selected()


    def update(self):
        dt = self._clock.tick( MainMenu._OVERRIDDEN_FPS or CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS

        self._background.update(dt)
        for ball in self._balls:
            ball.update(dt)


    @utils.show_fps_if_set
    def render(self):
        self._background.render()
        for ball in self._balls:
            ball.render()

        self._screen.blit(self._title, self._title_rect )
        for choice_txt, choice_rect in zip( self._choice_texts, self._choice_rects ):
            self._screen.blit(choice_txt, choice_rect)
        self._screen.blit(self._credit, self._credit_rect)

        # Blit selected choice
        centerx = self._choice_rects[self._choice].left - 50
        centery = self._choice_rects[self._choice].centery
        pygame.draw.circle( self._screen, C.BLACK, (centerx, centery), 10 )
        pygame.draw.circle(self._screen, C.WHITE_2, (centerx, centery), 7)


    def get_next_state(self):
        return self._next_state
