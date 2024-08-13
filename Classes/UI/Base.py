"""
UI classes for managing user interaction, including:
displaying the game window, handling audio, and collecting user input.

Additional Info:
    The game runs in full-screen mode with a constant resolution of 1920 x 1080 pixels.

Author: WK-K
"""

# standard modules
import pygame
import os
# project modules
from Classes.UI.Common import InputStack

class UI_base():
    """
    Manages the game window and user interaction for a full-screen game with a resolution of 1920 x 1080 pixels.

    Attributes:
        Class Attributes:
            FPS (int): The frame rate of the game.
            RES (tuple[int, int]): The resolution of the game window (Full-HD).

        Instance Attributes:
            root_dir (str): Path to the main directory of the project 
                            for asset loading and other operations.
            gfx_dir (str): Path to the directory containing graphical assets.
            mouse_pos (tuple[int, int]): Current mouse position in pixels.
            dirty_rectangles (list[tuple[pygame.Rect, list[pygame.Surface]]]):
                List of dirty rectangles to optimize rendering. 
                Each rectangle is associated with a list of surfaces to be blitted.
            background_mask (pygame.Surface): Mask for the static background used to fill dirty rectangles.
            screen (pygame.Surface): The main game display surface.
            clock (pygame.time.Clock): Clock for managing the frame rate.
            event_callbacks (InputStack): Stack for managing and processing user input events.
            key_map (dict[int, str]): Dictionary mapping key constants 
                                      to string representations of key actions.

    Methods:
        __init__(root_dir: str) -> None:
            Initializes the game window and sets up essential paths and input handling.
            
            Arguments:
                root_dir (str): 
                    Path to the main directory of the project for asset loading and other operations.

        window_set_up(window_caption: str = "The Szaszki Game") -> None:
            Initializes pygame and configures the game window for full-screen mode.
            
            Arguments:
                window_caption (str): 
                    The title to display on the game window. Defaults to "The Szaszki Game".

        update() -> None:
            Updates the screen by redrawing only the dirty rectangles using memoization for mask subsurfaces.

            Note:
                As the program grows, this method may consume significant memory 
                due to memoization of `pygame.Surface` objects.
                Adjustments may be needed if memory usage becomes a concern.

        get_input() -> bool:
            Processes user input events and updates the event stack.

            Returns:
                - bool: 
                    Returns True if a quit event (window close) is detected; 
                    otherwise, returns False to continue the game loop.

        intro() -> None:
            Placeholder method for introductory actions or animations.

            This method should be implemented in subclasses to provide specific 
            introductory actions or animations.

        outro() -> None:
            Placeholder method for concluding actions or animations.

            This method should be implemented in subclasses to provide specific 
            concluding actions or animations.
    """

    # Class atributes
    FPS: int = 30 # framerate
    RES: tuple[int, int] = 1920, 1080 # resolution (Full-HD)

    # Constructor methods
    def __init__(self, root_dir) -> None:
        """
        Initializes the game window and sets up essential paths and input handling.

        Arguments:
            root_dir (str): Path to the main directory of the project for asset loading and other operations.
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
            - window_caption (str): Name for the game window (Defaults to `The Szaszki Game).
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
        Processes user input events and updates the event stack.

        This method handles all pending input events, including mouse movements, clicks, and key presses. It updates the internal event stack and processes specific actions such as closing the window.

        Returns:
        - bool: Returns True if a quit event (window close) is detected; otherwise, returns False to continue the game loop.

        Events Handled:
        - pygame.QUIT: When the user attempts to close the window.
        - pygame.MOUSEMOTION: Updates the current position of the mouse cursor.
        - pygame.MOUSEBUTTONDOWN: Records mouse click events and stores cursor position.
        - pygame.KEYDOWN: Detects key presses, storing either a mapped key or unicode character.

        Key Handling:
        - Keys not in self.key_map are stored directly.
        - Special keys (e.g., arrow keys) are mapped using self.key_map.
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
        """Placeholder method for concluding setup or animations."""
        raise NotImplementedError()

    def outro(self) -> None:
        """Placeholder method for concluding setup or animations."""
        raise NotImplementedError()
    
   
