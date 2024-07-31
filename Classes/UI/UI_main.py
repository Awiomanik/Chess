"""
UI classes for menaging interaction with user.
Takes care of displaying window, playing audio and collecting user input.

Additional info:
    The game always runs in full-screen mode with constant resolution of 1920 x 1080 pixels.

Author: WK-K
"""

# Imports
import pygame
import os

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

    def __init__(self, root_dir) -> None:
        """
        Sets up the game window.
        
        Arguments:
            root_dir (str): Path to the main catalogue of the repository for relative path operations.
        """

        self.root_dir: str = root_dir
        self.gfx_dir: str = os.path.join(root_dir, "Assets", "GFX")

        # SET UP WONDOW AND PYGAME
        self.window_set_up()
        
    def window_set_up(self) -> None:
        """Initializes pygame and sets up the game window."""

        # initialize Pygame
        pygame.init()
        # set up the full-screen mode and resolution
        self.screen: pygame.Surface = pygame.display.set_mode(self.RES, pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption("The Chess Game")
        # set the variable for menaging frame rate
        self.clock: pygame.time.Clock = pygame.time.Clock() 

    def update(self) -> None:
        pass

    def intro(self) -> None:
        pass

    def outro(self) -> None:
        pass
    
    def main_menu(self) -> str:
        """
        """
        # Prepare background image surface
        main_menu_background_img: pygame.image = pygame.image.load(
            os.path.join(self.gfx_dir, "MainMenu", "ChessBoardTileWood240x240px.png"))
        main_menu_background: pygame.Surface = pygame.Surface((1920, 1080))
        for x in range(0, 1920, 240):
            for y in range(0, 1080, 240):
                main_menu_background.blit(main_menu_background_img, (x, y))

        # pawn image
        rook_gfx: pygame.image = pygame.image.load(os.path.join(self.gfx_dir, "MainMenu", "rookb.png"))

        # Text
        font = pygame.font.Font(os.path.join(self.gfx_dir, "Fonts", "handdrawn.ttf"), 100)

        title = font.render("The  Chess  Game", False, (0, 0, 0))
        title_coord = ((1920 - title.get_rect()[2])//2, 130)

        options = []
        for opt in ["Play", "Load", "Exit"]:
            options.append(font.render(opt, False, (0, 0, 0)))
        current_option = 0

        menu_loop_running = True

        # main menu has 16 columns

        while menu_loop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # <- pressing X to close window
                    pygame.quit()   #closes window
                    exit()          #exits while loop
                if event.type == pygame.MOUSEMOTION:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_option = (current_option + 1) % len(options)
                    if event.key == pygame.K_UP:
                        current_option = (current_option - 1) % len(options)
                    if event.key == pygame.K_RETURN:
                        if current_option == 2:
                            menu_loop_running = False

            self.screen.blit(main_menu_background, (0, 0))
            self.screen.blit(rook_gfx, (title_coord[0] + 10, 370 + 120 * current_option))
            self.screen.blit(title, title_coord)
            option_coord_y = 360
            option_coord_x = title_coord[0] + 120
            for opt in options:
                self.screen.blit(opt, (option_coord_x, option_coord_y))
                option_coord_y += 120

            # Update pygame and clock every FPS'th of a secound
            pygame.display.flip()
            self.clock.tick(self.FPS)

        









