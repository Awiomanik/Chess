"""
This module defines the `Gameplay` classes, responsible for handling the Gameplay UI of the chess game based on the base(UI) class.

Classes:
    - AbstractGameplay:     Parent class for managing the display and interaction of the game, 
                            including loading assets, handling user input, 
                            and rendering the chessboard, HUD and all elements on the screen.
                            It's an abstract class that is meant to be the base for the gameplay classes
                            with different themes (different UI layouts).

    - DeveloperGameplay:    Basic UI for testing functionality and UX. 
                            It is meant to not be perfect nor pretty, but to for example
                            display much more information then other UIs.

Functions:
    - gameplay(root_dir: str, theme: str="Developer") -> None:
        Factory function that returns an instance of the appropriate Gameplay class based on the theme.

Author: WK-K
"""

# standard modules
import pygame
import os
from abc import ABC, abstractmethod
# project modules
from Classes.UI.Base import UI_base
from Classes.Chess.Layout import Layout

# -- Abstract class --
class AbstractGameplay(UI_base, ABC):
    """
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
        self.gfx_grabbed_piece: pygame.Surface | None = None
        """Graphic of the grabbed piece"""
        self.mouse_clicked: bool = False
        """Whether the mouse was clicked"""
        self.grabbed_piece_field: int | None = None
        """Index of grabbed piece on the board (0-63)"""
        self.possible_moves_arr: list[int] = []
        """List of available moves, without captures"""
        self.possible_captures_arr: list[int] = []
        """List of available moves that end in capture"""

        self.set_parameters()
        self.load_assets()

    @abstractmethod
    def set_parameters(self) -> None:
        """
        This method sets atributes corresponding to positioning of UI elements for a given theme.
        
        Must be implemented by subclasses
        """
        pass

    @abstractmethod
    def load_assets(self) -> None:
        """
        Abstract method to load the necessary graphical assets for the gameplay screen
        and prepare the UI elements.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def gameplay(self, layout: Layout) -> str:
        """
        Abstract method to display the gameplay screen and handle user input.

        Must be implemented by subclasses.
        """
        pass

    def handle_input(self) -> None:
        """
        Handle the user input by popping the last element of input stack and adjusting the atributes.

        Returns:
        - str | None: The action based on the input, or None if no action is taken.
        """
        event = self.event_callbacks.pop()

        # keyboard
        if event.event_type == "key":
            #if event.data == "DOWN":
            #if event.data == "UP":
            if event.data == "ENTER":
                raise NotImplementedError()
        
        # mouse click
        if event.event_type == "mouse":
            self.mouse_clicked = True

# -- Subclasses --
class DeveloperGameplay(AbstractGameplay):
    """
    """
    # Constructors
    def set_parameters(self) -> None:
        """Sets atributes corresponding to positioning of the UI elements."""
        self.param_board_size: tuple[int, int] = (960, 960)
        self.param_board_pos: tuple[int, int] = (60, 60)
        self.param_board_rect: pygame.Rect = pygame.Rect(self.param_board_pos + self.param_board_size)
        self.param_tile_size: tuple[int, int] = (120, 120)
        self.colors = {
            "Board_background": (33, 110, 46), # Dark green
            "Info_block": (100, 100, 100), # Grey
            "Info_text": (255, 255, 255),
            "Text": (255, 215, 0), # Golden
            "Mouse_hover": (255, 215, 0, 100) # Gold semi-transparent
        }
        self.empty_chessboard_mask: pygame.Surface = None
        self.whether_layout_has_changed: bool = False
    def load_assets(self) -> None:
        """
        """
        # path to graphical elements in chosen theme
        self.theme_path: str = os.path.join(self.gfx_dir, "Gameplay", self.theme)

        # CHESSBOARD GRAPHIC
        # chessboard
        tile: pygame.image = pygame.image.load(
            os.path.join(self.theme_path, "ChessBoardTileGrey.png")).convert()
        self.gfx_chessboard: pygame.Surface = pygame.Surface((1080, 1080)).convert()
        self.gfx_chessboard.fill(self.colors["Board_background"])
        for x in range(60, 1020, 240):
            for y in range(60, 1020, 240):
                self.gfx_chessboard.blit(tile, (x, y))

        # text
        self.main_font = pygame.font.Font(os.path.join(self.gfx_dir, "Fonts", "handdrawn.ttf"), 50)
        self.small_font = pygame.font.SysFont("consolas", 23)
        
        # marks files (letters)
        marks_letters=[]
        for l in list(map(chr, range(65, 73))): 
            marks_letters.append(self.main_font.render('{}'.format(l), False, self.colors["Text"]))
        # marks ranks (numbers)
        marks_numbers=[]
        for n in range(1,9):
            marks_numbers.append(self.main_font.render('{}'.format(n), False, self.colors["Text"]))

        # blit marks onto chessboard surface
        for i in range(8):
            self.gfx_chessboard.blit(marks_letters[i], (i * 120 + 100, 5)) # top
            self.gfx_chessboard.blit(marks_letters[i], (i * 120 + 100, 1025)) # bottom
            # ranks are blitted in revers so they would mach
            self.gfx_chessboard.blit(marks_numbers[7 - i], (15, i * 120 + 90)) # left
            self.gfx_chessboard.blit(marks_numbers[7 - i], (1035, i * 120 + 90)) # right
        
        # PIECES
        self.gfx_pieces = {}
        for i, piece in enumerate(zip(["pawn", "rook", "knight", "bishop", "queen", "king"],
                                ["pawnb", "rookb", "knightb", "bishopb", "queenb", "kingb"]), 1):
            for j in [0, 1]:
                self.gfx_pieces[i + j * 8] = pygame.image.load(
                    os.path.join(self.theme_path, "Pieces", piece[j] + ".png")).convert_alpha()
                
        # MOUSE RECTANGLES
        # hover rectangle
        self.gfx_mouse_hover_rect: pygame.Surface = \
            pygame.Surface(self.param_tile_size, pygame.SRCALPHA).convert_alpha()
        self.gfx_mouse_hover_rect.fill((0, 0, 0, 0))
        pygame.draw.rect(self.gfx_mouse_hover_rect, 
                         self.colors["Mouse_hover"],
                         self.gfx_mouse_hover_rect.get_rect())

        # INFORMATION BLOCK
        self.gfx_info_background: pygame.Surface = pygame.Surface((860, 1080)).convert()
        self.gfx_info_background.fill(self.colors["Info_block"])
        #self.gfx_info_background.blit(self.main_font.render("Current player:", False, self.colors["Info_text"]), (20, 20))
        #self.gfx_info_background.blit(self.main_font.render("Current FEN:   ", False, self.colors["Info_text"]), (20, 120))
        #self.gfx_info_background.blit(self.main_font.render("...            ", False, self.colors["Info_text"]), (20, 220))
   
    # Utils
    def mouse_field_rect(self) -> pygame.Rect | None:
        """
        """
        x, y = self.mouse_pos[0] - 60, self.mouse_pos[1] - 60
        if 0 < x < self.param_board_size[0] and \
           0 < y < self.param_board_size[1]:
            for i in range(8): 
                for j in range(8):
                    tx, ty = self.param_tile_size
                    if i * tx < x < (i + 1) * tx and \
                        j * ty < y < (j + 1) * ty:
                        return pygame.Rect(i * tx + 60, j * ty + 60, 120, 120)
        else:
            return None
    def mouse_rect(self) -> pygame.Rect:
        """"""
        return pygame.Rect(self.mouse_pos[0] - 60, self.mouse_pos[1] - 60, 120, 120)
    def field_index_of_a_mouse(self) -> int | None:
        """Returns index in 64 int array of fields on board (60-1020, 60-1020) from board mouse coordinates."""
        x, y = self.mouse_pos[0] - 60, self.mouse_pos[1] - 60
        for i in range(8):
            for j in range(8):
                # if coursor is on that field
                if i * 120 < x < (i + 1) * 120 and \
                   j * 120 < y < (j + 1) * 120: 
                    return i + j * 8
        return None
    def mouse_down_handling(self, layout: Layout) -> None:
        """
        - Checks if the mouse click occurred within the chessboard boundaries.
        - Determines the field clicked on the chessboard based on the position.
        - Retrieves the piece value of the clicked field.
        - If a piece is already grabbed:
        ----- If the clicked field is a valid move, updates the layout by moving the piece to the new field.
        ----- If the clicked field is not a valid move:
        --------- Checks if there is another piece of the same color on the clicked field.
        --------- If so, grabs the new piece and updates the grabbed piece field and picture.
        ----- Releases the grabbed piece by clearing the grabbed piece field.
        - If no piece is currently grabbed:
        ----- Checks if there is a piece of the same color on the clicked field.
        ----- If so, grabs the piece and updates the grabbed piece field and picture.
        """
        # if on board
        if self.param_board_rect.collidepoint(self.mouse_pos):

            def grabb_new_piece():
                self.dirty_rectangles.append((self.mouse_field_rect(), []))
                self.grabbed_piece_field = clicked_field
                self.gfx_grabbed_piece = self.gfx_pieces[clicked_piece]
                self.possible_moves_arr, self.possible_captures_arr = \
                    layout.all_possible_moves_for_piece(clicked_field)

            def loosing_grabbed_piece():
                self.grabbed_piece_field = None
                self.gfx_grabbed_piece = None
                    
            # check on which field
            clicked_field: int = self.field_index_of_a_mouse()
            clicked_piece: pygame.Surface = layout.fields[clicked_field]

            # piece grabbed
            if self.grabbed_piece_field != None:
                # move possible -> do move
                if clicked_field in self.possible_moves_arr or \
                    clicked_field in self.possible_captures_arr :
                    layout.update(self.grabbed_piece_field, clicked_field)  # update layout
                    loosing_grabbed_piece()
                    self.whether_layout_has_changed = True
                    print(layout)
                # move not possible
                else:
                    # clicked on same field to loose piece
                    if clicked_field == self.grabbed_piece_field: 
                        loosing_grabbed_piece()
                    # there is other piece in same color (information is in the fourth bit)
                    elif (clicked_piece != 0 and \
                          (clicked_piece >> 3) & 1 == (layout.fields[self.grabbed_piece_field] >> 3) & 1):
                        loosing_grabbed_piece()
                        grabb_new_piece()
            # no piece grabbed
            else:
                # there is piece in the same color (information is in the fourth bit)
                if clicked_piece != 0 and \
                    (layout.white_moves == bool(clicked_piece >> 3 & 1)): 
                    grabb_new_piece()

    # Main loop
    def gameplay(self, layout: Layout) -> str:
        """
        Display the gameplay screen and handle user input until 
        user goes back to the main menu or the window is closed.

        This method enters a loop where it continuously checks for user input,
        updates the UI elements based on that input
        and renders the updated screen.
        """
        # display initial gameplay screen
        self.gamplay_init(layout)

        def mouse_hover():
            if not self.grabbed_piece_field and \
                (mhr_rect := self.mouse_field_rect()) != mhr_rect_old:

                # clear old
                if mhr_rect_old:
                    self.dirty_rectangles.append((mhr_rect_old, []))

                # draw new
                if mhr_rect:
                    self.dirty_rectangles.append((mhr_rect, [self.gfx_mouse_hover_rect]))

                    # check for piecce in the hovered field
                    if (piece_index_temp := layout.fields[self.field_index_of_a_mouse()]):
                        # append the piece
                        self.dirty_rectangles[-1][1].append((self.gfx_pieces[piece_index_temp]))
        def grabbed_piece():
            if self.grabbed_piece_field:
                # clear old
                self.dirty_rectangles.append((mouse_old_position_rect, []))

                # whether in board
                if self.param_board_rect.collidepoint(self.mouse_pos):
                    # draw new
                    self.dirty_rectangles.append((self.mouse_rect(), [self.gfx_grabbed_piece]))
                    
                # moved out of the board
                else:                    
                    # loose piece
                    self.grabbed_piece_field = None
        def info_block():
            if self.whether_layout_has_changed:
                # Current Player
                self.dirty_rectangles.append((pygame.Rect(1100, 80, 800, 200),
                                            [self.small_font.render("White" if layout.white_moves else "Black", 
                                                                    False, 
                                                                    self.colors["Info_text"])]))
                # FEN
                self.dirty_rectangles.append((pygame.Rect(1100, 190, 800, 200),
                                            [self.small_font.render(layout.layout2fen(), 
                                                                    False, 
                                                                    self.colors["Info_text"])]))
        
        while True:
            # save old mouse position
            mouse_old_position_rect: pygame.Rect = self.mouse_rect()
            mhr_rect_old: pygame.Rect = self.mouse_field_rect()

            # get and menege user input
            # Whether the window was closed
            if self.get_input():
                return "Terminated"
            
            # Wheter any interaction happened
            if self.event_callbacks.stack:
                self.handle_input()

            # Whether mouse was clicked
            if self.mouse_clicked:
                self.mouse_down_handling(layout)
                self.mouse_clicked = False

            # Mouse hovering rectangle
            mouse_hover()

            # grabbed piece
            grabbed_piece()

            # Information block
            info_block()

            # Reset variables
            self.whether_layout_has_changed = False

            # Update UI
            self.update()
        
        return "Game ended"
    def gamplay_init(self, layout: Layout) -> None:
        """
        """
        def render_multiline_text(text: str, position: tuple[int, int], font: pygame.font.Font,
                                  color: tuple[int, int, int] | tuple[int, int, int, int],
                                  tabulator_width: int=8):
            """
            Renders a multiline text on the screen.

            Parameters:
            - text (str): The multiline text to render.
            - position (tuple[int, int]): The top-left position to start rendering the text.
            - font (pygame.Font): The font object used to render the text.
            - color (tuple[int, int, int]): The color of the text.
            - tabulator_width (int): Maximum width of the tabulator to be swapped with spaces
            """
            # Split the text into lines
            lines = text.splitlines()
            
            # Initial position
            x, y = position
            
            # Render each line
            for line in lines:
                # change tabulators to spaces
                line_splitted = line.split('\t')
                if len(line_splitted) > 1:
                    temp_line = ''
                    for part in line_splitted:
                        temp_line += part
                        temp_line += ' ' * (tabulator_width - (len(temp_line) % tabulator_width))
                    line = temp_line
                # Render the text for the current line
                line_surface = font.render(line, True, color)
                # Draw the line on the screen
                self.screen.blit(line_surface, (x, y))
                # Move the y position down for the next line
                y += line_surface.get_height() // 1.2

        # background
        self.screen.blit(self.gfx_chessboard, (0, 0))
        self.screen.blit(self.gfx_info_background, (1080, 0))

        # save empty chessboard as mask
        self.empty_chessboard_mask = self.screen.subsurface(self.param_board_rect)

        # pieces
        for i, piece in enumerate(layout.fields):
            if piece:
                self.screen.blit(self.gfx_pieces[piece], 
                                            (60 + 120 * (i % 8), 60 + 120 * (i//8)))
                                            # 80 - board shift on screen
                                            # 120 - tile size
                                            # % or // - ranks and files
        # save screen as mask             
        self.background_mask = self.screen.copy()

        # Info Block
        render_multiline_text(str(layout), (1090, -60), self.small_font, self.colors["Info_text"])

# -- Factory function --
def gameplay_factory(root_dir: str, theme: str="Developer") -> AbstractGameplay:
    """
    Factory function that returns an instance of the appropriate Gameplay class based on the theme.

    Parameters:
    - theme: str - The graphical theme in which the game is displayed.
    - root_dir: str - The root directory of the project for easy relative path operations.

    Returns:
    - An instance of a class derived from AbstractGameplay.

    Raises:
    - ValueError - When passed theme parameter is not assosiated with any class.
    """
    if theme == "Developer":
        return DeveloperGameplay(root_dir=root_dir, theme=theme)
    # Implement other class choices here
    else:
        raise ValueError(f"Unknown theme: {theme}")