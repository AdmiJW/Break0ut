
# This is the final state that will be run.
# Running this state will quit the game. However, this state exists so I can potentially run some code
# before exiting the game
import sys
import pygame

import src.States.AbstractState as AbstractState

class Quit(AbstractState.AbstractState):
    def __init__(self):
        # Quit the game and program
        pygame.quit()
        sys.exit()

    def get_next_state(self): return None

