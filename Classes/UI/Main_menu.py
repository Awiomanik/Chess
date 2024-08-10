"""
"""

# standard modules
import pygame
import os
# project modules
from Classes.UI.Base import UI_base


class Main_menu(UI_base):
    """
    """
    def __init__(self, root_dir: str) -> None:
        super().__init__(root_dir)
        self.load_assets()

    def load_assets(self) -> None:
        """
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
        """
        # main menu has 16 columns

        menu_loop_running = True
        while menu_loop_running:

            # get and menege user input
            if self.get_input():
                menu_loop_running = False
            if self.event_callbacks.stack:
                if self.handle_input():
                     menu_loop_running = False

            # prepare elements to be displayed
            # background
            self.render_queue.append((self.main_menu_background, (0, 0)))
            # semi-transparent rectangle
            self.render_queue.append((self.temp_surface, (540, 60)))
            # option piece
            self.render_queue.append((self.rook_gfx, (self.title_coord[0] + 10, 370 + 120 * self.current_option)))
            # title text
            self.render_queue.append((self.title, self.title_coord))
            # options text
            option_coord_y = 360
            option_coord_x = self.title_coord[0] + 120
            for opt in self.options:
                self.render_queue.append((opt, (option_coord_x, option_coord_y)))
                option_coord_y += 120

            # Update screen, pygame and clock every FPS'th of a secound
            self.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def handle_input(self) -> bool:
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
                     raise NotImplementedError()
                # Load
                if self.current_option == 1: 
                     raise NotImplementedError()
                # Exit
                if self.current_option == 2:
                    return True

        return False