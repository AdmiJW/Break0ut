# Singleton audio instance for sound effects and music
import pygame
import os.path as path

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(10)

class SFX:
    SFX = {
        "BRICK_HIT_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'brickhit.ogg')),
        "CHG_SELECTION_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'change_selection.ogg')),
        "DOUBLE_BALL_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'doubleball.ogg')),
        "GAMEEND_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'gameend.ogg')),
        "LONGERPADDLE_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'longerpaddle.ogg')),
        "PADDLE_COLLISION_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'paddlehit.ogg')),
        "RECOVER_HEALTH_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'recoverhealth.ogg')),
        "SEE_FUTURE_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'seefuture.ogg')),
        "SELECTED_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'selected.ogg')),
        "STRONG_BALL_SFX" : pygame.mixer.Sound(path.join('assets', 'audio', 'strongerball.ogg')),
        'LEVEL_PROCEED_SFX': pygame.mixer.Sound(path.join('assets', 'audio', 'levelopening.ogg'))
    }
    VOLUMES = [0.2, 0.2, 0.25, 0.2, 0.2, 0.3, 0.2, 0.25, 0.2, 0.25, 0.15]
    def __init__(self):
        for sfx, vol in zip(SFX.SFX.values(), SFX.VOLUMES):
            sfx.set_volume(vol)
    def __getattr__(self, item):
        return SFX.SFX[item]


class Music:
    MUSIC = {
        "MAIN_MENU": path.join("assets", 'audio', 'mainmenu.ogg'),
        "IN_GAME": path.join('assets', 'audio', 'ingame.ogg')
    }
    VOLUMES = {
        "MAIN_MENU": 0.2,
        "IN_GAME": 0.1
    }
    def __init__(self):
        self.CURR_MUSIC = None

    def __getattr__(self, item):
        return Music.MUSIC[item]

sfx = SFX()
music = Music()

def play_brick_hit(): sfx.BRICK_HIT_SFX.play()
def play_change_selection(): sfx.CHG_SELECTION_SFX.play()
def play_double_ball(): sfx.DOUBLE_BALL_SFX.play()
def play_game_end(): sfx.GAMEEND_SFX.play()
def play_long_paddle(): sfx.LONGERPADDLE_SFX.play()
def play_paddle_collision(): sfx.PADDLE_COLLISION_SFX.play()
def play_recover_health(): sfx.RECOVER_HEALTH_SFX.play()
def play_see_future(): sfx.SEE_FUTURE_SFX.play()
def play_selected(): sfx.SELECTED_SFX.play()
def play_stronger_ball(): sfx.STRONG_BALL_SFX.play()
def play_level_proceed(): sfx.LEVEL_PROCEED_SFX.play()


def stop_music():
    pygame.mixer.music.stop()
    music.CURR_MUSIC = None


def play_main_menu():
    if music.CURR_MUSIC != music.MAIN_MENU:
        pygame.mixer.music.stop()
        pygame.mixer.music.load( music.MAIN_MENU )
        pygame.mixer.music.set_volume( music.VOLUMES['MAIN_MENU'] )
        pygame.mixer.music.play(-1)
        music.CURR_MUSIC = music.MAIN_MENU

def play_in_game():
    if music.CURR_MUSIC != music.IN_GAME:
        pygame.mixer.music.stop()
        pygame.mixer.music.load( music.IN_GAME )
        pygame.mixer.music.set_volume( music.VOLUMES['IN_GAME'] )
        pygame.mixer.music.play(-1)
        music.CURR_MUSIC = music.IN_GAME
