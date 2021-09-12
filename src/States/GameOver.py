import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
import src.utils as utils

from src.SpriteManager import SpriteManager
from src.FontFactory import FontFactory
from src.HighscoreManager import HighscoreManager

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.MainMenu as MainMenu
import src.States.BreakRecord as BreakRecord
import src.States.Quit as Quit


# Game Over State
class GameOver(AbstractState.AbstractState):
    _OVERRIDDEN_FPS = 40
    _BOUNCING_BALL_GRAVITY = 1

    def __init__(self, clock: pygame.time.Clock, final_score: int, paddle_id: int, ball_id: int):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self._final_score = final_score

        centerx, centery = self._screen.get_rect().center

        # Background related
        self._background = utils.get_random_scrolling_background(self._screen)

        # Paddles and Balls
        self._paddle = SpriteManager.get_pad_surface(paddle_id)
        self._ball = SpriteManager.get_ball_surface(ball_id)
        self._ball_dy = 0
        self._paddle_rect = self._paddle.get_rect(center=(centerx+200, centery+100))
        self._ball_rect = self._ball.get_rect(center=(centerx+200, centery-80))

        ###############
        # Texts
        ###############
        self._title = FontFactory.generate_xl_text('GAME OVER', C.WHITE, C.WHITE_3)
        self._final_score_t1 = FontFactory.generate_l_text('FINAL', C.BLUE_1, C.BLUE_2)
        self._final_score_t2 = FontFactory.generate_l_text('SCORE:', C.BLUE_1, C.BLUE_2)
        self._final_score_t3 = FontFactory.generate_xl_text(f'{self._final_score}', C.YELLOW_1, C.YELLOW_2)
        self._continue = FontFactory.generate_m_text('CONTINUE', C.YELLOW_1, C.YELLOW_2)

        self._title_rect = self._title.get_rect(center=(centerx, centery-180) )
        self._final_score_t1_rect = self._final_score_t1.get_rect(left=centerx-230, centery=centery-60)
        self._final_score_t2_rect = self._final_score_t2.get_rect(left=centerx-230, centery=centery+10)
        self._final_score_t3_rect = self._final_score_t3.get_rect(left=centerx-230, centery=centery+100)
        self._continue_rect = self._continue.get_rect(center=(centerx, centery+200))

        # Play game over
        Audio.stop_music()
        Audio.play_game_end()


    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                # Enter key / Spacebar
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if HighscoreManager.is_on_rank(self._final_score):
                        self._next_state = BreakRecord.BreakRecord(self._clock, self._final_score)
                    else:
                        self._next_state = MainMenu.MainMenu(self._clock)
                    Audio.play_selected()



    def update(self):
        dt = self._clock.tick( GameOver._OVERRIDDEN_FPS or CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS

        self._background.update(dt)

        # Animate ball
        self._ball_dy += GameOver._BOUNCING_BALL_GRAVITY
        self._ball_rect.top += self._ball_dy

        if self._ball_rect.colliderect(self._paddle_rect):
            self._ball_dy = -self._ball_dy
            self._ball_rect.bottom = self._paddle_rect.top


    @utils.show_fps_if_set
    def render(self):
        self._background.render()

        # Render paddle and ball selection
        self._screen.blit( self._ball, self._ball_rect )
        self._screen.blit( self._paddle, self._paddle_rect )
        # Render Texts
        self._screen.blit(self._title, self._title_rect )
        self._screen.blit(self._final_score_t1, self._final_score_t1_rect)
        self._screen.blit(self._final_score_t2, self._final_score_t2_rect)
        self._screen.blit(self._final_score_t3, self._final_score_t3_rect)
        self._screen.blit(self._continue, self._continue_rect)


    def get_next_state(self):
        return self._next_state
