from enum import Enum


class GameStateTypes(Enum):
    """
    Game State Types for different state of the game
    """
    MENU = "MENU"
    SETTING = "SETTING"
    START = "START"
    QUIT = "QUIT"
    EXIT = "EXIT"

    DEFAULT = MENU
