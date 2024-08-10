"""
UI classes for menaging interaction with user.
Takes care of displaying window, playing audio and collecting user input.

Additional info:
    The game always runs in full-screen mode with constant resolution of 1920 x 1080 pixels.

Author: WK-K
"""

# standard modules
import pygame
import os
# project modules
from Classes.UI.Common import InputStack

class UI_base():
    """
    Initializes game window and menages user interaction.
    The game always runs in full-screen mode with constant resolution of 1920 x 1080 pixels.

    Atributes:
        Class:
            FPS (int): The frame rate of the game.
            RESOLUTION (tuple[int, int]): The resolution of the game window.

        Instance:
            root_dir (str): Path to the main catalogue of the repository for relative path operations.
            dfx_dir (str): Path to the folder with graphical assets.
            pygame:
                screen (pygmae.Surface): The main game display surface.
                clock (pygame.time.Clock): variable for menaging frame rate.

    Methods:
        window_set_up() -> None: Initializes pygame and sets up the game window.
    """

    # Class atributes
    FPS: int = 30 # framerate
    RES: tuple[int, int] = 1920, 1080 # resolution (Full-HD)

    # Constructor methods
    def __init__(self, root_dir) -> None:
        """
        Sets up the game window.
        
        Arguments:
            root_dir (str): Path to the main catalogue of the repository for relative path operations.
        """
        # set up window and pygame
        self.window_set_up()

        # paths
        self.root_dir: str = root_dir
        self.gfx_dir: str = os.path.join(root_dir, "Assets", "GFX")
        # inputs
        self.event_callbacks: InputStack = InputStack()
        self.key_map = {
        pygame.K_DOWN: "DOWN",
        pygame.K_UP: "UP",
        pygame.K_LEFT: "LEFT",
        pygame.K_RIGHT: "RIGHT",
        pygame.K_RETURN: "ENTER",
        }
        self.mouse_pos = pygame.mouse.get_pos()
        # usefull constants
        self.render_queue = []
        
    def window_set_up(self, window_caption: str = "The Szaszki Game") -> None:
        """
        Initializes pygame and sets up the game window by:
        - setting resolution and full-screen mode
        - setting caption to window_caption argument
        - initializing screen surface and clock variables
        
        Arguments:
            - window_caption (str): Name for the game window.
        """

        # initialize Pygame
        pygame.init()
        # set up the full-screen mode and resolution
        self.screen: pygame.Surface = pygame.display.set_mode(self.RES, pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption(window_caption)
        # set the variable for menaging frame rate
        self.clock: pygame.time.Clock = pygame.time.Clock() 

    # Updating UI state
    def update(self) -> None:
        for surface, coords in self.render_queue:
            self.screen.blit(surface, coords)

    def get_input(self) -> bool:
        """
        Handle user input events and update the event stack.

        This method processes all pending input events, including mouse movements, 
        mouse button clicks, and key presses. It updates the internal event stack 
        with the detected events and handles specific actions such as closing the window.

        Returns:
        - bool: Returns True if a quit event (closing the window) is detected, otherwise returns False to continue the game loop.

        Events Handled:
        - pygame.QUIT: Triggers when the user attempts to close the window.
        - pygame.MOUSEMOTION: Tracks the current position of the mouse cursor.
        - pygame.MOUSEBUTTONDOWN: Records mouse click events and stores the cursor position in the event stack.
        - pygame.KEYDOWN: Detects key presses and stores the key information (either as a unicode character or mapped key) in the event stack.

        Key Handling:
        - If the key pressed is not in special keys dict (`self.key_map`) character, it is stored directly.
        - If the key pressed is a special key (e.g., arrow keys), it is mapped to a specific string using `self.key_map`.
        """
        for event in pygame.event.get():

            # detect closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            
            # mouse
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.event_callbacks.push("mouse", pygame.mouse.get_pos())

            # keyboard
            if event.type == pygame.KEYDOWN:
                self.event_callbacks.push("key", self.key_map.get(event.key, event.unicode))
                

        return False

    # Additional 
    def intro(self) -> None:
        raise NotImplementedError()

    def outro(self) -> None:
        raise NotImplementedError()
    
   

        









