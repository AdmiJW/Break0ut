import json
import os

import src.CONSTANTS as C

# Handles reading highscores save file from disk, and provides interface to insert highscore
# This should be a singleton class
class HighscoreManager:
    # _HIGHSCORES are an array of size 10, each containing (NAME, SCORE)
    _HIGHSCORES = None

    # Load highscores from saves/highscore.json and save it in HighscoreManager._HIGHSCORES
    # When the game first runs on user's machine, there is no highscore.json file. This method will
    # also handle the case by initializing it
    @staticmethod
    def load_highscore():
        # No highscore.json
        if not os.path.exists( C.HIGHSCORE_SAVE_DIR ):
            os.mkdir( C.HIGHSCORE_SAVE_DIR )
        if not os.path.exists( C.HIGHSCORE_SAVE_PATH ):
            default_scores = [ ("AAA", 1000), ("BBB", 900), ("CCC", 800), ("DDD", 700), ("EEE", 600),
                               ("FFF", 500), ("GGG", 400), ("HHH", 300), ("III", 200), ("JJJ", 100) ]
            HighscoreManager._HIGHSCORES = default_scores

            with open( C.HIGHSCORE_SAVE_PATH, 'w+' ) as file:
                json.dump(default_scores, file)
        # otherwise simply load highscore.json
        else:
            with open( C.HIGHSCORE_SAVE_PATH ) as file:
                HighscoreManager._HIGHSCORES = json.load(file)

    # Obtain the list of highscores (To be blit in highscores screen)
    @staticmethod
    def get_highscores():
        if HighscoreManager._HIGHSCORES is None:
            HighscoreManager.load_highscore()
        return HighscoreManager._HIGHSCORES

    # Returns True if the provided score is ranked in the leaderboard (TOP 10)
    @staticmethod
    def is_on_rank(score:int ):
        return any( score > hi_score for _, hi_score in HighscoreManager._HIGHSCORES )

    # Updates the highscore leaderboard by inserting a new name, and new score.
    # If the score does not go into top 10, then the resulting leaderboard will remain
    @staticmethod
    def insert_score(name: str, score: int):
        HighscoreManager._HIGHSCORES.append( (name, score) )
        HighscoreManager._HIGHSCORES.sort( key=lambda v: v[1], reverse=True )
        HighscoreManager._HIGHSCORES.pop()

    # Overwrites the records in highscore.json with the current highscore leaderboard instance in
    # HighscoreManager._HIGHSCORES
    @staticmethod
    def write_highscores():
        with open( C.HIGHSCORE_SAVE_PATH, 'w+' ) as file:
            json.dump( HighscoreManager._HIGHSCORES, file )


# Run highscore initialization
HighscoreManager.load_highscore()