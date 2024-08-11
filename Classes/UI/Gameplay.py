"""
This module defines the `Gameplay` class, responsible for handling the Gameplay UI of the chess game based on the base(UI) class.

Classes:
    - Gameplay: Manages the display and interaction of the game, including loading assets, handling user input, and rendering the chessboard, HUD and all elements on the screen.

Author: WK-K
"""

# standard modules
import pygame
import os
# project modules
from Classes.UI.Base import UI_base


class Gameplay(UI_base):
    """
    A class to represent and manage the gameplay screen and interactions of the chess game.

    """
    def __init__(self, root_dir: str, theme: str="Developer") -> None:
        """
        Initialize the gameplay UI by loading assets and preparing the UI elements.

        Parameters:
        - root_dir: str - The root directory of the project where assets are located.
        - theme: str - Grphical theme in which the game is displayed (themes include: `Developer`,..)
        """
        super().__init__(root_dir)
        self.theme: str = theme
        self.load_assets()

    def load_assets(self) -> None:
        """
        Load the necessary graphical assets for the gameplay screen and prepare the UI elements.

        This method loads the...

        Grphical themes include: 
        - `Developer`
        """
        # path to graphical elements in chosen theme
        self.theme_path: str = os.path.join(self.gfx_dir, "Gameplay", self.theme)

        # CHESSBOARD GRAPHIC
        tile: pygame.image = pygame.image.load(
            os.path.join(self.theme_path, "ChessBoardTileWood240x240px.png"))
        self.gfx_chessboard: pygame.Surface = pygame.Surface((1080, 1080))
        self.gfx_chessboard.fill((102, 51, 0)) # Brown
        for x in range(60, 1020, 240):
            for y in range(60, 1020, 240):
                self.gfx_chessboard.blit(tile, (x, y))
        marks_font = pygame.font.Font(os.path.join(self.gfx_dir, "Fonts", "handdrawn.ttf"), 50)
        # marks files (letters)
        marks_letters=[]
        for l in list(map(chr, range(65, 73))): 
            marks_letters.append(marks_font.render('{}'.format(l), False, (255, 229, 204))) # light brown
        # marks ranks (numbers)
        marks_numbers=[]
        for n in range(1,9):
            marks_numbers.append(marks_font.render('{}'.format(n), False, (250, 220, 200)))
        # blit marks onto chessboard surface
        for i in range(8):
            self.gfx_chessboard.blit(marks_letters[i], (i*120 + 100, 5)) # top
            self.gfx_chessboard.blit(marks_letters[i], (i*120 + 100, 1025)) # bottom
            # ranks are blitted in revers so they would mach
            self.gfx_chessboard.blit(marks_numbers[7-i], (15, i*120 + 90)) # left
            self.gfx_chessboard.blit(marks_numbers[7-i], (1035, i*120 + 90)) # right

        # INFORMATION BLOCK
        self.gfx_info: pygame.Surface = pygame.Surface((860, 1080))
        self.gfx_info.fill((60, 30, 0)) # dark brown
        self.gfx_info.blit(marks_font.render("Current player:", False, (255, 229, 204)), (20, 20))
        self.gfx_info.blit(marks_font.render("Current FEN:   ", False, (255, 229, 204)), (20, 120))
        self.gfx_info.blit(marks_font.render("...            ", False, (255, 229, 204)), (20, 220))
        



        """# prepare option piece image
        self.rook_gfx: pygame.image = pygame.image.load(os.path.join(self.gfx_dir, "MainMenu", "rook.png"))

        # prepare text
        self.font = pygame.font.Font(os.path.join(self.gfx_dir, "Fonts", "handdrawn.ttf"), 100)

        self.title = self.font.render("The  Chess  Game", False, (225, 225, 225))
        self.title_coord = ((1920 - self.title.get_rect()[2])//2, 130)

        self.options = []
        for opt in ["Play", "Load", "Exit"]:
            self.options.append(self.font.render(opt, False, (225, 225, 225)))
        self.current_option = 0

        # semi-transparent rectangle
        self.temp_surface = pygame.Surface((840, 720), pygame.SRCALPHA)
        pygame.draw.rect(self.temp_surface, (0, 0, 0, 75), (0, 0, 840, 720), border_radius=20)"""

    def gameplay(self) -> None:
        """
        Display the gameplay screen and handle user input until 
        user goes back to the main menu or the window is closed.

        This method enters a loop where it continuously checks for user input,
        updates the UI elements based on that input
        and renders the updated screen.
        """
        while True:

            # get and menege user input
            # Whether the window was closed
            if self.get_input():
                return "Terminated"
            # Wheter any interaction happened
            if self.event_callbacks.stack:
                self.handle_input()

            # prepare elements to be displayed\
            # (main menu has 16 columns)
            # background
            self.render_queue.append((self.gfx_chessboard, (0, 0)))
            self.render_queue.append((self.gfx_info, (1080, 0)))

            # Update UI
            self.update()

    def handle_input(self) -> str | None:
        raise NotImplementedError()
        """
        Handle the user input to navigate through the menu options or select an option.

        This method checks the last input event in the stack and updates the current menu option 
        or returns the selected action.

        Returns:
        - str | None: The action based on the selected option ("Play", "Load", "Exit"), or None if no action is taken.
        
        event = self.event_callbacks.pop()

        # keyboard
        if event.event_type == "key":
            # adjust current option
            if event.data == "DOWN":
                        self.current_option = (self.current_option + 1) % len(self.options)
            if event.data == "UP":
                        self.current_option = (self.current_option - 1) % len(self.options)

            # handle chosen option
            if event.data == "ENTER":
                # Play
                if self.current_option == 0:
                     return "Play"
                # Load
                if self.current_option == 1: 
                     raise NotImplementedError()
                # Exit
                if self.current_option == 2:
                    return "Exit"

        return None"""