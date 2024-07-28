"""
Game class for menaging all other classes.
Initializes all needed classes and takes care of data flow between them.

Author: WK-K
"""

# Project modules
import UI.UI_main as ui_main

class Game():
    """
    Manages the entire game instance including UI, player, and bots interactions.

    Attributes:
        root_dir (str): Directory in which the main script was called for easy relative path operations.
        ui (UI.UI_main.UI): UI Instance for meaging user interaction.

    Methods:

    """
    def init(self, root_dir: str) -> None:
        """
        Initializes the Game instance.
        
        Arguments:
            root_directory (str): Path to the main catalogue of the repository for relative path operations.
        """

        self.root_dir: str = root_dir
        self.ui: ui_main.UI = ui_main.UI(root_dir)
