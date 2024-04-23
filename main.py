from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from game_manager.galactic_defender import GalacticDefender


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = GalacticDefender()
    ai.run_game()
