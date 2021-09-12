import pygame
import sys

import src.CONSTANTS as C

# Pygame initialization
pygame.init()
# Initialize screen here
pygame.display.set_mode( (C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SCALED )
pygame.display.set_caption('Break0ut')

from src.SpriteManager import SpriteManager
pygame.display.set_icon( SpriteManager.get_ball_surface(0) )

import src.States.MainMenu as MainMenu

#########################
# MEMORY DEBUGGING tools
#########################
# import gc
# import weakref

# Game class is a State Machine that has a self.state and run the states
class Game:
    def __init__(self):
        self._state = None
        self._screen = pygame.display.get_surface()
        self._clock = pygame.time.Clock()

        self._state = MainMenu.MainMenu( self._clock )

        #############
        # DEBUGGING
        ##############
        # self._states = set()

    def start(self):
        # while self.state is not None:
        while self._state is not None:
            self._state.handle_event()
            self._state.update()
            self._state.render()
            pygame.display.flip()
            self._state = self._state.get_next_state()

            # ! DEBUGGING
            # Used to detect memory leak
            # if weakref.ref(self._state) not in self._states:
            #     self._states.add( weakref.ref(self._state) )
            # for st in self._states:
            #     state = st()
            #     if state is not None:
            #         print(type(state))
            #         print(len(gc.get_referrers(state)))
            #         # for ref in gc.get_referrers(state):
            #         #     print(ref)
            # print('\n\n\n')

        # If state no longer returns next state, quit the game
        pygame.quit()
        sys.exit()
