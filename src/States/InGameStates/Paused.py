from __future__ import annotations
import pygame

import src.CONSTANTS as C
import src.CONFIG as CF
from src.FontFactory import FontFactory

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.InGameStates.Playing as Playing
import src.States.MainMenu as MainMenu
import src.States.Quit as Quit

# Paused State.
# How it works is simple. The constructor takes in the playing state, and hold it
# When unpaused, simply return that state back.
class Paused(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, playing_state: Playing.Playing):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._playing_state = playing_state
        self.next_state = self

        self._choice = 0

        centerx, centery = self._screen.get_rect().center
        #######################
        # Text and Background
        #######################
        self._overlay = pygame.Surface( self._screen.get_size() ).convert_alpha()
        self._overlay.fill( (0,0,0,128) )
        self._title = FontFactory.generate_xl_text('Paused', C.YELLOW_1, C.YELLOW_2)
        self._resume = FontFactory.generate_m_text('Resume', C.WHITE, C.WHITE_3)
        self._resume_h = FontFactory.generate_m_text('Resume', C.YELLOW_1, C.YELLOW_2)
        self._togglefull = FontFactory.generate_m_text('Show/Hide FPS', C.WHITE, C.WHITE_3)
        self._togglefull_h = FontFactory.generate_m_text('Show/Hide FPS', C.YELLOW_1, C.YELLOW_2)
        self._togglefps = FontFactory.generate_m_text('Toggle Fullscreen', C.WHITE, C.WHITE_3)
        self._togglefps_h = FontFactory.generate_m_text('Toggle Fullscreen', C.YELLOW_1, C.YELLOW_2)
        self._mainmenu = FontFactory.generate_m_text('Back to Main Menu', C.WHITE, C.WHITE_3)
        self._mainmenu_h = FontFactory.generate_m_text('Back to Main Menu', C.YELLOW_1, C.YELLOW_2)

        self._title_rect = self._title.get_rect(center=(centerx, centery-150))
        self._resume_rect = self._resume.get_rect(center=(centerx, centery))
        self._togglefull_rect = self._togglefull.get_rect(center=(centerx,centery+50))
        self._togglefps_rect = self._togglefps.get_rect(center=(centerx, centery+100))
        self._mainmenu_rect = self._mainmenu.get_rect(center=(centerx,centery+150))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self._choice == 0:
                        # Remember to set playing's next state to itself, so it don't end up in a
                        # Playing <-> Paused loop!
                        self._playing_state.next_state = self._playing_state
                        self.next_state = self._playing_state
                    elif self._choice == 1:
                        CF.SHOW_FPS = not CF.SHOW_FPS
                    elif self._choice == 2:
                        pygame.display.toggle_fullscreen()
                    else:
                        # For this, we have to destroy the references as Playing.next_state -> Paused.
                        # and Paused._playing_state -> Playing
                        # If we don't release, it will end up as memory leak!
                        self._playing_state.next_state = None
                        self.next_state = MainMenu.MainMenu(self._clock)
                    Audio.play_selected()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self._choice = max(0, self._choice - 1)
                    Audio.play_change_selection()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self._choice = min(3, self._choice + 1)
                    Audio.play_change_selection()

    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS

    def render(self):
        self._playing_state.render()
        # Overlay
        self._screen.blit( self._overlay, (0,0) )
        # Texts
        self._screen.blit(self._title, self._title_rect)
        self._screen.blit(self._resume_h if self._choice == 0 else self._resume, self._resume_rect)
        self._screen.blit(self._togglefull_h if self._choice == 1 else self._togglefull, self._togglefull_rect)
        self._screen.blit(self._togglefps_h if self._choice == 2 else self._togglefps, self._togglefps_rect)
        self._screen.blit(self._mainmenu_h if self._choice == 3 else self._mainmenu, self._mainmenu_rect)

    def get_next_state(self):
        return self.next_state
