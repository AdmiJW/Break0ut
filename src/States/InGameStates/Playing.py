import pygame

import src.CONFIG as CF
import src.utils as utils

from src.Objects.ParallaxBackground import ParallaxBackground
from src.Objects.Paddle import Paddle
from src.Objects.Ball import Ball
from src.Objects.NullBall import NullBall
from src.Objects.Tile import Tile
from src.Objects.TileGroup import TileGroup
from src.Objects.ParticleSystem import ParticleSystem
from src.Objects.PowerupDrop import PowerupDrop

import src.Audio as Audio

import src.States.AbstractState as AbstractState
import src.States.InGameStates.Serve as Serve
import src.States.InGameStates.Initialization as Initialization
import src.States.InGameStates.Paused as Paused
import src.States.GameOver as GameOver
import src.States.Quit as Quit

# --- Substate for InGame State, which is a state machine
# Playing State: The ball moves, collision with tile is taken into account. Scores are updated. Collision with paddle
# are checked. Once ball goes below boundary, decrement self life. If no lives left, go to GameOver state
# In this state, the render() and update() will use Strategy pattern, which the render() and update() algorithm can be
# easily swapped
class Playing(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, paddle: Paddle, ball: Ball, tilegroup: TileGroup,
                 background: ParallaxBackground, level: int, score: int, lives_left: int, powerup=None,
                 powerup_timeleft=0):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self.paddle = paddle
        self.ball = ball
        self.level = level
        self.score = score
        self.background = background
        self.tilegroup = tilegroup
        self.lives_left = lives_left
        self.next_state = self

        # Particle system
        self._particlesystem = ParticleSystem()

        # Powerup related
        self.powerup = powerup
        self.powerup_timeleft = powerup_timeleft
        self.powerup_drop_group = pygame.sprite.Group()
        self.ball2 = NullBall()
        # Strategies to override algorithm. Used by powerups
        self.overridden_update_strategy = None
        self.overridden_render_strategy = None

        # Audio
        Audio.play_in_game()


    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = Quit.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = Paused.Paused(self._clock, self)
                    Audio.play_selected()
                else:
                    self.paddle.handle_event(event)
            elif event.type == pygame.KEYUP:
                self.paddle.handle_event(event)

    # Update() method consists of pieces of logics. See Logic Pieces section below
    def update(self):
        if self.overridden_update_strategy is not None:
            self.overridden_update_strategy(self)
        else:
            Playing.default_update_strategy(self)



    @utils.show_fps_if_set
    @utils.show_score_and_heart
    @utils.show_powerup_timeleft
    def render(self):
        if self.overridden_render_strategy is not None:
            self.overridden_render_strategy(self)
        else:
            Playing.default_render_strategy(self)

    # I noticed a memory leak back then, when the next_state keep pointing to itself even though it has transitioned,
    # resulting in huge memory leak. Therefore, I have to set self.next_state to None. Don't ask why
    def get_next_state(self):
        return self.next_state

    # Function to set powerup. Ensures that powerup is properly teardown before new one is applied
    def apply_powerup(self, powerup_class):
        if self.powerup is not None:
            self.powerup.teardown(self)
        self.powerup = powerup_class(self)

    ###################################
    # Default Strategies - No Powerups
    ###################################
    @staticmethod
    def default_render_strategy(state):
        state.background.render()
        state.paddle.render()
        state.ball.render()
        state.tilegroup.draw(state._screen)
        state._particlesystem.draw(state._screen)
        state.powerup_drop_group.draw(state._screen)

    @staticmethod
    def default_update_strategy(state):
        dt = state._clock.tick(CF.DESIRED_FPS) * 0.001 * CF.DESIRED_FPS

        state.update_paddle(dt)
        state.update_background()

        state.update_powerup_drops(dt)
        state.handle_powerup_paddle_collision()

        state.update_ball_horizontal(dt, state.ball)
        state.handle_ball_paddle_collision_horizontal(state.ball)
        state.handle_ball_tile_collision_horizontal(state.ball)

        state.update_ball_vertical(dt, state.ball)
        state.handle_ball_paddle_collision_vertical(state.ball)
        state.handle_ball_tile_collision_vertical(state.ball)

        state.check_ball_below_screen()
        state.update_tilegroup()
        state.check_level_cleared()
        state.update_particle_system(dt)
        state.update_powerup_expiration(dt)


    ##########################################################################################################
    # For update(), I've broken down each logic into separate pieces, so it can be assembled like a puzzle :)
    # Although it has function call overhead, it does make implementing powerups easier. Take note!
    ###########################################################################################################
    # Logic Pieces
    ########################
    def update_paddle(self, dt):
        self.paddle.update(dt)

    def update_background(self):
        self.background.update(self.paddle.get_rect().centerx)

    # Moves the ball horizontally
    def update_ball_horizontal(self, dt, ball: Ball):
        ball.update_horizontal(dt)

    # Performs collision checking between paddle and ball, horizontally
    def handle_ball_paddle_collision_horizontal(self, ball: Ball):
        ball.handle_paddle_collision_horizontal(self.paddle)

    # Performs collision checking between tile and ball, horizontally.
    # Does the following:
    # - Update score based on tile_id
    # - Ball collision update
    # - Tile collision update
    # - Generate particles
    # - Attempt generation of powerup
    def handle_ball_tile_collision_horizontal(self, ball: Ball):
        collided_tiles: list[Tile] = pygame.sprite.spritecollide( ball, self.tilegroup, False)
        if len(collided_tiles):
            Audio.play_brick_hit()
            ball.handle_tile_collision_horizontal(collided_tiles)
            for tile in collided_tiles:
                self.score += tile.tile_id + 1
                tile.on_collision(ball.ball_power)
                self._particlesystem.generate_particles(tile)
                self.attempt_powerup_generation(tile)

    def attempt_powerup_generation(self, tile: Tile):
        powerup_generated = PowerupDrop.attempt_generation(tile)
        if powerup_generated is not None:
            self.powerup_drop_group.add(powerup_generated)

    # Moves the ball vertically
    def update_ball_vertical(self, dt, ball: Ball):
        ball.update_vertical(dt)

    # Performs collision checking between paddle and ball, vertically
    def handle_ball_paddle_collision_vertical(self, ball: Ball):
        ball.handle_paddle_collision_vertical(self.paddle)

    # Performs collision checking between tile and ball, vertically.
    # Does the following:
    # - Update score based on tile_id
    # - Ball collision update
    # - Tile collision update
    # - Generate particles
    def handle_ball_tile_collision_vertical(self, ball: Ball):
        collided_tiles: list[Tile] = pygame.sprite.spritecollide(ball, self.tilegroup, False)
        if len(collided_tiles):
            Audio.play_brick_hit()
            ball.handle_tile_collision_vertical(collided_tiles)
            for tile in collided_tiles:
                self.score += tile.tile_id + 1
                tile.on_collision(ball.ball_power)
                self._particlesystem.generate_particles(tile)
                self.attempt_powerup_generation(tile)

    # Updates the powerups (Falling, and removing those who fall out of screen)
    def update_powerup_drops(self, dt):
        self.powerup_drop_group.update(dt)
        self.powerup_drop_group.remove( filter(lambda sp: sp.is_expired(), self.powerup_drop_group.sprites() ) )

    # Check for powerup colliding with the paddle, and applying the powerup when really collides
    def handle_powerup_paddle_collision(self):
        collided_powerup = pygame.sprite.spritecollide(self.paddle, self.powerup_drop_group, False)
        for pu in collided_powerup:
            self.powerup_drop_group.remove(pu)
            self.apply_powerup( pu.retrieve_powerup() )

    # Update and eliminate expired particles
    def update_particle_system(self, dt):
        self._particlesystem.update(dt)
        self._particlesystem.eliminate_expired()

    # Update tilegroup, eliminating destroyed tiles.
    def update_tilegroup(self):
        self.score += self.tilegroup.update()

    # Check if the tiles are all destroyed, which proceeds us to next level
    def check_level_cleared(self):
        if self.tilegroup.is_cleared():
            self.next_state = Initialization.Initialization(self._clock, self.paddle.id, self.ball.id,
                                                            self.level + 1, self.score, self.lives_left)

    # Check if the ball has fallen below screen, which means deduct lives.
    def check_ball_below_screen(self):
        if self.ball.get_rect().top > self._screen.get_height():
            Audio.play_paddle_collision()
            self.lives_left -= 1
            if self.lives_left:
                self.next_state = Serve.Serve(self._clock, self.paddle, self.ball, self.tilegroup,
                                              self.background, self.level, self.score, self.lives_left,
                                              self.powerup, self.powerup_timeleft)
            else:
                self.next_state = GameOver.GameOver(self._clock, self.score, self.paddle.id, self.ball.id)

    def update_powerup_expiration(self, dt):
        if self.powerup is not None:
            self.powerup_timeleft -= dt

            if self.powerup_timeleft <= 0:
                self.powerup.teardown(self)
                self.powerup = None

    ##########################
    # End of Logic Pieces
    ##########################

