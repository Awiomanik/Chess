"""
This module defines the `Main_menu` class, which handles the main menu UI of the chess game. 
It extends the `UI_base` class to manage the display, user interaction, and asset handling for the menu.

Classes:
    - Main_menu: 
        Manages the display, asset loading, and interaction of the main menu, 
        including rendering UI elements and handling user input.

Author: WK-K
"""

# standard modules
import pygame
import os
# project modules
from Classes.UI.Base import UI_base


class Main_menu(UI_base):
    """
    A class to represent and manage the main menu of the chess game.

    Attributes:
        - gfx_dir (str): The directory path to graphical assets.
        - dirty_rectangles (list[tuple[pygame.Rect, list[pygame.Surface]]]): List of dirty rectangles to optimize rendering.
        - main_menu_background (pygame.Surface): The surface representing the main menu background.
        - rook_gfx (pygame.Surface): The image of a rook piece used as a cursor in the menu.
        - font (pygame.font.Font): The font used for rendering text in the menu.
        - title (pygame.Surface): The rendered title of the game.
        - title_coord (tuple[int, int]): The coordinates for placing the title on the screen.
        - options (list[pygame.Surface]): A list of rendered option texts (Play, Load, Exit) in the menu.
        - current_option (int): Index of the currently selected menu option.
        - semi_transparent_surface (pygame.Surface): A semi-transparent rectangle for visual effects in the menu.
        - option_piece_rects (list[pygame.Rect]): List of rectangles that encapsulate the option piece.

    Methods:
        - __init__(root_dir: str) -> None: Initialize the main menu by loading assets and preparing the UI elements.
        - load_assets() -> None: Load the necessary graphical assets for the main menu and prepare the UI elements.
        - display_menu() -> str | None: Display the main menu and handle user input until a menu option is selected or the window is closed.
        - screen_init() -> None: Render the initial screen of the main menu.
        - handle_input() -> str | None: Handle user input to navigate through the menu options or select an option.
    """
    def __init__(self, root_dir: str) -> None:
        """
        Initialize the main menu by loading assets and preparing the UI elements.

        Parameters:
            - root_dir (str): The root directory of the project for easy relative path operations.
        """
        super().__init__(root_dir)
        self.load_assets()

    def load_assets(self) -> None:
        """
        Load the necessary graphical assets for the main menu and prepare the UI elements.

        This method loads the background image, option piece image, and font for the title and menu options. 
        It also prepares a semi-transparent rectangle for visual effects and stores these elements as 
        `pygame.Surface` objects for optimal rendering.
        """
        options_txt = ["Play", "Load", "Exit"]

        # prepare background image surface
        main_menu_background_img: pygame.Surface = pygame.image.load(
            os.path.join(self.gfx_dir, "MainMenu", "ChessBoardTileWood240x240px.png")).convert()
        
        self.main_menu_background: pygame.Surface = pygame.Surface((1920, 1080)).convert()

        for x in range(0, 1920, 240):
            for y in range(0, 1080, 240):
                self.main_menu_background.blit(main_menu_background_img, (x, y))

        # prepare text
        self.font = pygame.font.Font(os.path.join(self.gfx_dir, "Fonts", "handdrawn.ttf"), 100)

        self.title = self.font.render("The  Chess  Game", False, (225, 225, 225))
        self.title_coord = ((1920 - self.title.get_rect().width)//2, 130)

        self.options: list[pygame.Surface] = []
        """List of rendered options texts."""
        for opt in options_txt:
            self.options.append(self.font.render(opt, False, (225, 225, 225)))
        self.current_option: int = 0

        # prepare option piece image
        self.rook_gfx: pygame.Surface = \
            pygame.image.load(os.path.join(self.gfx_dir, "MainMenu", "rook.png")).convert_alpha()
        self.option_piece_rects: list[pygame.Rect] = []
        """List of rectangles that encapsulate option piece"""
        rook_width, rook_height = self.rook_gfx.get_width(), self.rook_gfx.get_height()
        for i in range(len(self.options)):
             self.option_piece_rects.append(pygame.Rect(self.title_coord[0] + 10, 370 + 120 * i,
                                                        rook_width, rook_height))
             
        # semi-transparent rectangle
        self.semi_transparent_surface = pygame.Surface((840, 720), pygame.SRCALPHA)
        pygame.draw.rect(self.semi_transparent_surface, (0, 0, 0, 75), (0, 0, 840, 720), border_radius=20)

    def display_menu(self) -> str | None:
        """
        Display the main menu and handle user input until a menu option is selected or the window is closed.

        This method enters a loop where it continuously checks for user input, 
        updates the UI elements based on that input, 
        and renders the updated menu on the screen.

        Returns:
            - str | None: 
                The action to be taken based on the selected menu option 
                ("Play", "Load", "Exit", or "Terminated"), or None if no option is selected yet.

        Note:
            - The main menu layout includes 16 columns..
        """
        self.screen_init()

        while True:

            # get and menege user input
            # Whether the window was closed
            if self.get_input():
                self.screen.fill((0, 0,0))
                return "Terminated"
            # Wheter any interaction happened
            if self.event_callbacks.stack:
                # Whether interaction triggered state change
                if (action:=self.handle_input()):
                    return action

            # Update UI
            self.update()

    def screen_init(self) -> None:
        """
        Renders the initial screen of the main menu 
        by drawing the background, title, options, and other UI elements.

        This method also saves the current screen as a mask for future rendering optimizations.
        """
        self.screen.blit(self.main_menu_background, (0, 0))
        self.screen.blit(self.semi_transparent_surface, (540, 60))
        self.screen.blit(self.title, self.title_coord)
        option_coord_y = 360
        option_coord_x = self.title_coord[0] + 120
        for opt in self.options:
            self.screen.blit(opt, (option_coord_x, option_coord_y))
            option_coord_y += 120

        # save screen as mask
        self.background_mask = self.screen.copy()
        
        self.screen.blit(self.rook_gfx, (self.title_coord[0] + 10, 370))
        
    def handle_input(self) -> str | None:
        """
        Handle user input to navigate through the menu options or select an option.

        This method processes the most recent input event, 
        updates the current menu option based on user input (e.g., arrow keys), 
        and handles the selection of an option (e.g., Enter key).

        Returns:
            - str | None: 
                The action based on the selected option 
                ("Play", "Load", "Exit"), or None if no action is taken.
        """
        event = self.event_callbacks.pop()

        # keyboard
        if event.event_type == "key":
            # adjust current option
            if event.data in ["DOWN", "UP"]:
                # Add the current position to the dirty rectangles list before moving the option piece
                self.dirty_rectangles.append((pygame.Rect(self.option_piece_rects[self.current_option]), []))
                
                # Update the current option index
                if event.data == "DOWN":
                    self.current_option = (self.current_option + 1) % len(self.options)
                if event.data == "UP":
                    self.current_option = (self.current_option - 1) % len(self.options)
                
                # Add the new position to the dirty rectangles list after moving the option piece
                self.dirty_rectangles.append((pygame.Rect(self.option_piece_rects[self.current_option]), [self.rook_gfx]))

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

        return None