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
            gfx_dir (str): Path to the folder with graphical assets.
            mouse_pos (tuple[int, int]): Current mouse position in pixels.
            dirty_rectangles (list[tuple[pygame.Rect, list[pygame.Surface]]]): 
                List of dirty rectangls to optimize rendering.
                Every reectangle has list of surfacesto be blitted upon mask.
            background_mask (pygame.Surface): Mask for a non-changeble background to fill dirty rectangles.
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
        self.mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        self.dirty_rectangles: list[tuple[pygame.Rect, list[pygame.Surface]]] = []
        """
        List of dirty rectangls to optimize rendering.
        Every reectangle has list of surfacesto be blitted upon mask.
        """
        self.background_mask: pygame.Surface = None
        """Mask for a non-changeble background to fill dirty rectangles"""
        
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
        """
        Updates the screen by redrawing only the dirty rectangles.
        Uses memoization for mask subsurfaces.

        Note:
        In the future, as the program grows this might be the function
        that consumes sizable amount of memory due to memoization of `pygame.Surface` objects.
        Might need adjustment if memory usage will be a concern.
        """
        # memoization
        memo: dict[tuple[int, int, int, int], pygame.Surface] = {}
        # loop through dirty rectangles
        for rect, surfaces in self.dirty_rectangles:
            # check memory
            key = tuple(rect)
            if key in memo:
                submask: pygame.Surface = memo[key]
            else:
                submask: pygame.Surface = self.background_mask.subsurface(rect)
                memo[key] = submask

            # blit mask and updates
            self.screen.blit(submask, rect)
            for surface in surfaces:
                self.screen.blit(surface, rect)
                
        # Update pygame and clock every FPS'th of a secound
        # update() can redraw only 'dirty rectangles' and not tot the whole screen
        # that can optimize rendering of the game
        pygame.display.update()
        self.clock.tick(self.FPS)

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
    
   

        









