# The abstract state. All the states should implement the following
# methods
#
# Note on state machine. If get_next_state() returns None, it means the
# state machine had finished its job and no longer need to run its state.
#
# Constrcutor vary by states. Some state require certain informations that other state do not need

class AbstractState:
    def update(self): pass
    def handle_event(self): pass
    def render(self): pass
    def get_next_state(self): pass