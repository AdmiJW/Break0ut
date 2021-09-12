

# Abstract Powerup interface to be used in Playing state.
# All powerups must inherit this interface.
# How powerups work (At least, from what I thought):
#   > In constructor, pass in the state itself to be manipulated
#   > Save all the data required to revert to the state before the powerup effect
#   > (Optional) After some set time, the powerup's teardown() method will be called
#
#
# IMPORTANT THINGS TO DO:
# - In init(), set state's powerup attribute to self


class BasePowerup:
    # Pass in the state, and you can modify whatever needed to the state
    # For example, you could implement strategy pattern and change the implementation of render()
    # or update()
    def __init__(self, state): pass

    # Revert the changes done by this powerup to the state.
    # For example, if you used strategy pattern and changed the render() and update() method,
    # You should change it back when the powerup's teardown is called.
    def teardown(self, state): pass
