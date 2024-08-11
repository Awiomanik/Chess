"""
This module defines the `Main_menu` class, responsible for handling the main menu UI of the chess game based on the base(UI) class.

Classes:
    - Main_menu: Manages the display and interaction of the main menu, including loading assets, handling user input, and rendering the menu screen.

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
    - gfx_dir: str - The directory path to graphical assets.
    - main_menu_background: pygame.Surface - The surface representing the main menu background.
    - rook_gfx: pygame.image - The image of a rook piece used as a cursor in the menu.
    - font: pygame.font.Font - The font used for rendering text in the menu.
    - title: pygame.Surface - The rendered title of the game.
    - title_coord: tuple(int, int) - The coordinates for placing the title on the screen.
    - options: list[pygame.Surface] - A list of rendered options (Play, Load, Exit) in the menu.
    - current_option: int - Index of the currently selected menu option.
    - temp_surface: pygame.Surface - A semi-transparent rectangle for visual effects in the menu.
    - render_queue: list[tuple(pygame.Surface, tuple(int, int))] - A list of elements to be displayed on the screen.

    Methods:
    - __init__(root_dir: str) -> None: Initialize the main menu by loading assets and preparing the UI elements.
    - load_assets() -> None: Load the necessary graphical assets for the main menu and prepare the UI elements.
    - display_menu() -> str: Display the main menu and handle user input until a menu option is selected or the window is closed.
    - handle_input() -> str | None: Handle the user input to navigate through the menu options or select an option.
    """
    def __init__(self, root_dir: str) -> None:
        """
        Initialize the main menu by loading assets and preparing the UI elements.

        Parameters:
        - root_dir: str - The root directory of the project where assets are located.
        """
        super().__init__(root_dir)
        self.load_assets()

    def load_assets(self) -> None:
        """
        Load the necessary graphical assets for the main menu and prepare the UI elements.

        This method loads the background image, option piece image, and font for the title and menu options. 
        It also prepares a semi-transparent rectangle for visual effects.
        """
        # prepare background image surface
        main_menu_background_img: pygame.image = pygame.image.load(
            os.path.join(self.gfx_dir, "MainMenu", "ChessBoardTileWood240x240px.png"))
        
        self.main_menu_background: pygame.Surface = pygame.Surface((1920, 1080))

        for x in range(0, 1920, 240):
            for y in range(0, 1080, 240):
                self.main_menu_background.blit(main_menu_background_img, (x, y))

        # prepare option piece image
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
        pygame.draw.rect(self.temp_surface, (0, 0, 0, 75), (0, 0, 840, 720), border_radius=20)

    def display_menu(self) -> str:
        """
        Display the main menu and handle user input until a menu option is selected or the window is closed.

        This method enters a loop where it continuously checks for user input, updates the UI elements based 
        on that input, and renders the updated menu on the screen.

        Returns:
        - str: The action to be taken based on the selected menu option ("Play", "Load", "Exit", or "Terminated").
        """
        while True:

            # get and menege user input
            # Whether the window was closed
            if self.get_input():
                return "Terminated"
            # Wheter any interaction happened
            if self.event_callbacks.stack:
                # Whether interaction triggered state change
                if (action:=self.handle_input()):
                    return action

            # prepare elements to be displayed\
            # (main menu has 16 columns)
            # background
            self.render_queue.append((self.main_menu_background, (0, 0)))
            # semi-transparent rectangle
            self.render_queue.append((self.temp_surface, (540, 60)))
            # option piece
            self.render_queue.append((self.rook_gfx, 
                                      (self.title_coord[0] + 10, 370 + 120 * self.current_option)))
            # title text
            self.render_queue.append((self.title, self.title_coord))
            # options text
            option_coord_y = 360
            option_coord_x = self.title_coord[0] + 120
            for opt in self.options:
                self.render_queue.append((opt, (option_coord_x, option_coord_y)))
                option_coord_y += 120

            # Update UI
            self.update()

    def handle_input(self) -> str | None:
        """
        Handle the user input to navigate through the menu options or select an option.

        This method checks the last input event in the stack and updates the current menu option 
        or returns the selected action.

        Returns:
        - str | None: The action based on the selected option ("Play", "Load", "Exit"), or None if no action is taken.
        """
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

        return None