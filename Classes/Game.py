"""
Game class for menaging all other classes file.
Initializes all needed classes and takes care of data flow between them.

Author: WK-K
"""

# Project modules
from Classes.UI.Main_menu import Main_menu

class Game():
    """
    Manages the entire game instance including UI, player, and bots interactions.

    Attributes:
        root_dir (str): Directory in which the main script was called for easy relative path operations.
        ui (UI.UI_main.UI): UI Instance for meaging user interaction.

    Methods:

    """
    def __init__(self, root_dir: str) -> None:
        """
        Initializes the Game instance.
        
        Arguments:
            root_dir (str): Path to the main catalogue of the repository for relative path operations.
        """

        self.root_dir: str = root_dir

        # testing main_menu
        self.ui: Main_menu = Main_menu(self.root_dir)
        self.ui.display_menu()
