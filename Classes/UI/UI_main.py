"""
UI classes for menaging interaction with user.
Takes care of displaying window, playing audio and collecting user input.

Additional info:
    The game always runs in full-screen mode with constant resolution of 1920 x 1080 pixels.

Author: WK-K
"""

# Imports
import pygame

class UI():
    """
    Initializes game window and menages user interaction.
    The game always runs in full-screen mode with constant resolution of 1920 x 1080 pixels.

    Atributes:
        Class:
        FPS (int): The frame rate of the game.
        RESOLUTION (tuple[int, int]): The resolution of the game window.

        Instance:
        root_dir (str): Path to the main catalogue of the repository for relative path operations.
        clock (pygame.time.Clock): variable for menaging frame rate.

    Methods:
        window_set_up() -> None: Initializes pygame and sets up the game window.
    """

    # Class atributes
    FPS: int = 60 # framerate
    RES: tuple[int, int] = 1920, 1080 # resolution (Full-HD)

    def init(self, root_dir) -> None:
        """
        Sets up the game window.
        
        Arguments:
            root_dir (str): Path to the main catalogue of the repository for relative path operations.
        """

        self.root_dir: str = root_dir

        # SET UP WONDOW AND PYGAME
        self.window_set_up()
        
    def window_set_up(self) -> None:
        """Initializes pygame and sets up the game window."""

        # initialize Pygame
        pygame.init()
        # set up the full-screen mode and resolution
        self.screen: pygame.Surface = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption("The Chess Game")
        # set the variable for menaging frame rate
        self.clock: pygame.time.Clock = pygame.time.Clock() 