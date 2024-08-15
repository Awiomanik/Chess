"""
This module defines the `layout` class, which represents the layout of a chessboard and handles various operations 
such as updating the board state based on moves, converting between FEN notation and the internal board representation, 
and calculating possible moves for pieces.

Classes:
    - layout: Represents the layout of a chessboard, including the state of the board, castling rights, en passant square, 
      and the move clock.

Author: WK-K
"""

from Classes.Chess.Common import *

class Layout:
    '''
    Represents the layout of a chessboard.

    ATTRIBUTES:
        - piece_count (int): Total count of pieces on the board
        - fields (list[int]): Array of fields on the board (0 = a1, 1 = a2, ..., 63 = h8) with numbers indicating occupation:
            0 - empty
            1 - p = pawn
            2 - r = rook
            3 - n = knight
            4 - b = bishop
            5 - q = queen
            6 - k = king
            ^ + 8 - whites (represented as capital letters)
        - white_moves (bool): Flag indicating whether it's currently white's turn to move
        - moves_made (int): Number of moves made so far
        - castling (list(bool)): Castling availability (as in FEN notation, i.e. [K, Q, k, q]).
        - en_passan (int | None): Index of the square over which a pawn has passed by moving two squares forward (None if different move was done).
        - clock (int): Number of moves made since the last capture or pawn advance (used in the 50-move rule)
    
    METHODS:
        - __init__(fen: str | None=None) -> None: 
            Initializes the layout instance from FEN (If 'fen' is None, initializes with the default layout).
        
        - _init_default() -> None: 
            Initializes the layout with the default piece positions.
        
        - __str__() -> str: 
            Returns string representation of the current layout instance (multiline).
        
        - fen2layout(fen: str) -> None: 
            Initializes the layout from the given FEN notation.
        
        - layout2fen() -> str: 
            Returns the FEN notation representation of the layout.
        
        - update(old_field: int, new_field: int) -> None: 
            Updates layout attributes based on a move from old_field to new_field.
        
        - castling_update(old_piece: int, old_field: int, new_field: int) -> None: 
            Handles the castling logic when updating the layout.
        
        - all_possible_moves_for_piece(index: int, with_castling_bool: bool=True) -> tuple[list[int], list[int]]:
            Calculates all possible moves for a specific piece at the given index, including special handling for castling 
            and en passant, and returns a tuple containing lists of possible non-capturing and capturing moves.
    '''
    
    # ATRIBUTES
    piece_count: int = 0
    fields: list[int] = [] * 64 # Array of fields on the board (0 = a1, 1 = a2, ..., 63 = h8) with numbers indicating occupation
    white_moves: bool = True
    moves_made: int = 0
    castling: list[bool] = [True] * 4 # Castling availability as in FEN notation, that is: K, Q, k, q.
    en_passant: int = None # fields array index of squere over whitch a pawn has passed by moving two squeres forward
    clock: int = 0 # number of moves made since last capture or pawn advance used in 50-move rule
    # constants
    ROOK_MOVEMENT_DIRECTIONS: list[tuple[int, int]] =      [(1, 0), (-1, 0), (0, 1), (0, -1)]
    KNIGHT_MOVEMENT_OFFSET: list[tuple[int, int]] =        [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    BISHOP_MOVEMENT_DIRECTIONS: list[tuple[int, int]] =    [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    QUEEN_MOVEMENT_DIRECTIONS: list[tuple[int, int]] =     [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    # METHODS
    # magic methods
    def __init__(self, fen: str | None=None) -> None:
        '''
        Initializes the layout instance from FEN.
        If 'fen' is None, initializes with the default layout).
        '''
        if fen is None: 
            self._init_default()
        else: 
            self.fen2layout(fen) 
    def _init_default(self) -> None:
        '''Initializes layout with standard arrangement of pieces'''
        self.piece_count: int = 32
        self.fields: list[int] = [10, 11, 12, 13, 14, 12, 11, 10,
                                9, 9, 9, 9, 9, 9, 9, 9,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                2, 3, 4, 5, 6, 4, 3, 2]
    def __str__(self) -> str:
        ''''Return string representation of all atributes'''
        if self.en_passant == None: 
            temp_ep: str = '-'
        else: 
            temp_ep: str = board_index2file_rank_string[self.en_passant]

        return """------LAYOUT OBJECT------\n
- FEN: {out_fen}\n
- All fields:\n
{f1}\n
{f2}\n
{f3}\n
{f4}\n
{f5}\n
{f6}\n
{f7}\n
{f8}\n
- Whose move: {whose_move}\n
- Moves made: {moves}\n
- Castling capabilities:\n
white king: {cK}\n
white queen: {cQ}\n
black king: {ck}\n
black queen: {cq}\n
- En Passsant: {ep}\n
- Halfmove clock: {clock}""".format(
            out_fen = self.layout2fen(),
            f8 = '\t'.join([number2piece_character[piece] for piece in self.fields[0:8]]),
            f7 = '\t'.join([number2piece_character[piece] for piece in self.fields[8:16]]),
            f6 = '\t'.join([number2piece_character[piece] for piece in self.fields[16:24]]),
            f5 = '\t'.join([number2piece_character[piece] for piece in self.fields[24:32]]),
            f4 = '\t'.join([number2piece_character[piece] for piece in self.fields[32:40]]),
            f3 = '\t'.join([number2piece_character[piece] for piece in self.fields[40:48]]),
            f2 = '\t'.join([number2piece_character[piece] for piece in self.fields[48:56]]),
            f1 = '\t'.join([number2piece_character[piece] for piece in self.fields[56:64]]),
            whose_move = "White" if self.white_moves else "Black",
            moves = self.moves_made,
            cK = self.castling[0],
            cQ = self.castling[1],
            ck = self.castling[2],
            cq = self.castling[3],
            ep = temp_ep,
            clock = self.clock) 
    # fen operations
    def fen2layout(self, fen: str) -> None:
        ''''Sets layout atributes to coresponding to FEN string'''
        # piece count
        self.piece_count: int = fen2piece_count(fen)
        # fields
        self.fields: list[int] = fen2array_of_fields(fen)
        # white moves
        if fen.split(' ')[1] == 'b': 
            self.white_moves: bool = False
        # moves made
        self.moves_made: int = int(fen.split(' ')[5])
        # castling
        self.castling: list[bool] = fen2castling_arr(fen)
        # en passant
        if fen.split(' ')[3] != '-': 
            self.en_passant: int = file_rank_string2board_index[fen.split(' ')[3]]
        # clock
        self.clock: int = int(fen.split(' ')[4])
    def layout2fen(self) -> str:
        '''Returns FEN notation string corresponding to layout atributes.'''
        # white moves
        if self.white_moves: 
            color: str = 'w'
        else: 
            color: str = 'b'
        # castling
        cast_temp_arr: list[str] = ['K', 'Q', 'k', 'q']
        castling_characters: list[str] = [cast_temp_arr[i] if self.castling[i] else '-' for i in range(4) ]
        # en passant
        temp_passant: str = '-'
        if self.en_passant != None: 
            temp_passant: str = board_index2file_rank_string[self.en_passant]

        # composing FEN
        fen: str = \
        array_of_fields2fen(self.fields) + ' ' + \
        color + ' ' + \
        ''.join([castling_characters[i] if self.castling[i] else '-' for i in range(4)]) + ' ' + \
        temp_passant + ' ' + \
        str(self.clock) + ' ' + \
        str(self.moves_made)

        return fen   
    # updating layout
    def update(self, old_field: int, new_field: int) -> None:
        '''
        Updates all atributes based on a given move.

        Arguments:
        - old_field (int), new_field (int): made move from old_field to new_field

        Note:
        Promotion functionality not finnished.
        '''
        old_piece = self.fields[old_field]
        new_piece = self.fields[new_field]

        # if en passant happened
        en_passant_happened = new_field == self.en_passant and old_piece in (1, 9)

        # if capture happend
        capture_bool = new_piece != 0 or en_passant_happened

        # piece_count
        if capture_bool: 
            self.piece_count -=1 # one piece captured

        # fields
        self.fields[new_field] = old_piece # piece from prvious field on new field
        self.fields[old_field] = 0 # old field to empty 

        # white_moves
        self.white_moves = not self.white_moves

        # moves_made
        self.moves_made += 1

        # castling
        self.castling_update(old_piece, old_field, new_field)
        
        # en_passant
        # en passant capture happend
        if en_passant_happened:
            # black capturing (moves are reveresed earlier)
            if self.white_moves: 
                self.fields[new_field + 8] = 0
            # white capturing (moves are reversed earlier)
            else: 
                self.fields[new_field - 8] = 0
        self.en_passant = None
        # en passant capture not happend
        # white pawn moved two spaces
        if old_piece == 9 and new_field - old_field == 16: 
            self.en_passant = old_field + 8
        # black pawn moved two spaces
        if old_piece == 1 and old_field - new_field == 16: 
            self.en_passant = old_field - 8

        # clock
        self.clock = 0 if capture_bool or old_piece in (1, 9) else self.clock + 1

        # Promotion
        # white
        if old_piece == 9 and new_field > 55:
            self.fields[new_field] = 13
            try:
                raise NotImplementedError("Promotion changes pawn to a queen, does not let user choose otherwise.")
            except NotImplementedError as e:
                import traceback
                traceback.print_exc()
                print(f"Handled {e}")
        # black
        if old_piece == 1 and new_field < 8:
            self.fields[new_field] = 5
            try:
                raise NotImplementedError("Promotion changes pawn to a queen, does not let user choose otherwise.")
            except NotImplementedError as e:
                import traceback
                traceback.print_exc()
                print(f"Handled {e}")
    def castling_update(self, old_piece: int, old_field: int, new_field: int) -> None:
        '''Part of update() that meneges castling, etracted for more readability'''
        offset: int = old_field - new_field

        # king moved
        # white king castling possibility
        if old_piece == 14:
            self.castling[0:2] = False, False
            # white queen's rook castle
            if offset == 2:
                self.fields[3] = 10 # rook to king jump
                self.fields[0] = 0 # old rook's field to empty 
            # white king's rook castle
            if offset == -2:
                self.fields[5] = 10 # rook to king jump
                self.fields[7] = 0 # old rook's field to empty
        # black king castling possibility
        if old_piece == 6:
            self.castling[2:4] = False, False
            # black queen's rook cstle
            if offset == 2:
                self.fields[59] = 2 # rook to king jump
                self.fields[56] = 0 # old rook's field to empty 
            # black king's rook castle
            if offset == -2:
                self.fields[61] = 2 # rook to king jump
                self.fields[63] = 0 # old rook's field to empty
        # rook moved
        # white king's rook castling possibility     
        if old_field == 7:
            self.castling[0] = False
        # white queen's rook castling possibility
        if old_field == 0:
            self.castling[1] = False
        # black king's rook castling possibility
        if old_field == 63:
            self.castling[2] = False
        # black queen's rook castling possibility
        if old_field == 56:
            self.castling[3] = False
    def all_possible_moves_for_piece(self, 
                                     index: int, 
                                     with_castling_bool: bool=True) -> tuple[list[int], list[int]]:
        """
        Compute all valid moves for a specific piece on the board.

        This method calculates the possible moves for the piece located at the specified `index` on the board. 
        It returns a tuple containing two lists:
        
        - A list of board indices for valid non-capturing moves.
        - A list of board indices for valid capturing moves.

        The behavior of the method can be controlled by the `with_castling_bool` parameter:
        - If `with_castling_bool` is set to `True` (default), the method will consider castling as a valid move option for the king.
        - If set to `False`, castling moves will be excluded from the possible moves for the king.

        Parameters:
        index : int
            The board index (0-63) of the piece for which to calculate possible moves.
        
        with_castling_bool : bool, optional
            A flag indicating whether to include castling in the king's possible moves (default is `True`).
        
        Returns:
        tuple[list[int], list[int]]
            A tuple containing two lists:
            - The first list includes indices of all valid non-capturing moves for the piece.
            - The second list includes indices of all valid capturing moves for the piece.

        Notes:
        - The method first determines the type of piece at the given index and whose turn it is to move.
        - Depending on the piece type, it uses helper methods (`get_moves_at_offsets`, `get_moves_in_directions`) 
        to generate potential moves.
        - Special handling is included for pawns (considering forward movement, diagonal captures, and en passant) 
        and kings (considering standard movement and castling).
        - The method does not check for move legality in terms of leaving the king in check.
        """
        piece = self.fields[index]
        possible_moves, capturing_moves = [], []

        # Pawn moves
        if piece in (9, 1):  
            self.handle_pawn_moves(index, piece, possible_moves, capturing_moves)
        # Rook moves
        elif piece in (10, 2):  
            possible_moves, capturing_moves = \
                self.get_moves_in_directions(index, self.ROOK_MOVEMENT_DIRECTIONS)
        # Knight moves
        elif piece in (11, 3):  
            possible_moves, capturing_moves = \
                self.get_moves_at_offsets(index, self.KNIGHT_MOVEMENT_OFFSET)
        # Bishop moves
        elif piece in (12, 4):  
            possible_moves, capturing_moves = \
                self.get_moves_in_directions(index, self.BISHOP_MOVEMENT_DIRECTIONS)
        # Queen moves
        elif piece in (13, 5):  
            possible_moves, capturing_moves = \
                self.get_moves_in_directions(index, self.QUEEN_MOVEMENT_DIRECTIONS)
        # King moves
        elif piece in (14, 6):  
            possible_moves, capturing_moves = \
                self.get_moves_at_offsets(index, self.QUEEN_MOVEMENT_DIRECTIONS) # should work as offset
            if with_castling_bool:
                self.handle_castling_moves(index, possible_moves)

        return possible_moves, capturing_moves
    def handle_pawn_moves(self, 
                          index: int, 
                          piece: int, 
                          possible_moves: list[int], 
                          capturing_moves: list[int]) -> None:
        """
        """
        offset = 8 if piece == 9 else -8
        start_row = 1 if piece == 9 else 6
        left_capture, right_capture = index + offset - 1, index + offset + 1

        if index % 8 != 0 and \
            (self.fields[left_capture] not in (0, piece) or \
            left_capture == self.en_passant):
            capturing_moves.append(left_capture)
        if index % 8 != 7 and \
            (self.fields[right_capture] not in (0, piece) or \
             right_capture == self.en_passant):
            capturing_moves.append(right_capture)

        if self.fields[index + offset] == 0:
            possible_moves.append(index + offset)
            if index // 8 == start_row and self.fields[index + 2 * offset] == 0:
                possible_moves.append(index + 2 * offset)
    def handle_castling_moves(self, index: int, possible_moves: list[int]) -> None:
        """
        Append valid castling moves to the list of possible moves for a king.

        Parameters:
        index : int
            The current index of the king on the board.
        
        possible_moves : list[int]
            A list of indices representing possible moves for the king, to which valid castling moves will be added.
        
        Notes:
        - The method assumes that `self.castling` is a list where:
        - Index 0: White kingside castling (if True, it's allowed).
        - Index 1: White queenside castling.
        - Index 2: Black kingside castling.
        - Index 3: Black queenside castling.
        - The `self.fields` array represents the board state, where each element is a piece or empty square.
        """
        
        if self.white_moves():
            # White king's castling options
            if index == 4:  # Ensure the piece is actually a white king on e1
                # Kingside castling for white
                if self.castling[0] and \
                    self.fields[5] == 0 and \
                    self.fields[6] == 0:
                    possible_moves.append(6)
                # Queenside castling for white
                if self.castling[1] and \
                    self.fields[1] == 0 and \
                    self.fields[2] == 0 and \
                    self.fields[3] == 0:
                    possible_moves.append(2)
        
        elif not self.white_moves():
            # Black king's castling options
            if index == 60:  # Ensure the piece is actually a black king on e8
                # Kingside castling for black
                if self.castling[2] and \
                    self.fields[61] == 0 and \
                    self.fields[62] == 0:
                    possible_moves.append(62)
                # Queenside castling for black
                if self.castling[3] and \
                    self.fields[57] == 0 and \
                    self.fields[58] == 0 and \
                    self.fields[59] == 0:
                    possible_moves.append(58)
    def get_moves_in_directions(self, index: int, directions: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
        """
        Calculate all possible moves in specified directions for a piece on the board.

        Given the board `index` of a piece and a list of movement `directions`, this method returns a tuple containing:
        - A list of indices representing possible non-capturing moves.
        - A list of indices representing capturing moves.

        Arguments:
        - index (int): The board index (0-63) of the piece for which to calculate possible moves.
        - directions (list[tuple[int, int]]): A list of tuples representing the movement directions 
            (e.g., [(1, 0), (0, 1)] for rook movements).

        Returns:
        - tuple[list[int], list[int]]: 
            - The first list contains indices of all valid non-capturing moves in the given directions.
            - The second list contains indices of all valid capturing moves in the given directions.

        Process flow:
        - For each direction, the method iteratively checks squares in that direction.
        - If a square is empty, it is added to the possible non-capturing moves.
        - If a square contains a piece of the opposite color, it is added to the capturing moves.
        - The iteration in a given direction stops upon encountering a non-empty square.
        - The method ensures that moves remain within the bounds of the board.
        """
        possible_moves = []
        capturing_moves = []

        # loop through each direction
        for direction in directions:
            row, col = divmod(index, 8) # returns quotient and reminder
            row_offset, col_offset = direction

            # loop in a specific direction
            while True:
                row += row_offset
                col += col_offset

                # check if the new position is within the bounds of the board
                if not (0 <= row < 8 and 0 <= col < 8): break

                # setting current index
                temp_index = row * 8 + col

                # if the target square is empty, add it to the possible_moves array
                if self.fields[temp_index] == 0:
                    possible_moves.append(temp_index)

                else:
                    # if the target square is occupied, check if the piece belongs to the opposite color
                    # using bitwise operations to check the 4th bit (color bit) of the piece
                    if bool((self.fields[temp_index] >> 3) & 1) != self.white_moves:
                        # If the colors are different, it means a capture is possible, so add it to capturing moves
                        capturing_moves.append(temp_index)
                    break

        return possible_moves, capturing_moves
    def get_moves_at_offsets(self, index, offsets) -> tuple[list[int], list[int]]:
        """
        Calculate all possible moves based on specific offsets for a piece on the board.

        Given the board `index` of a piece and a list of movement `offsets`, this method returns a tuple containing:
        - A list of indices representing possible non-capturing moves.
        - A list of indices representing capturing moves.

        Arguments:
        - index (int): The board index (0-63) of the piece for which to calculate possible moves.
        - offsets (list[tuple[int, int]]): A list of tuples representing the movement offsets 
        (e.g., [(2, 1), (1, 2)] for knight movements).

        Returns:
        - tuple[list[int], list[int]]: 
            - The first list contains indices of all valid non-capturing moves at the given offsets.
            - The second list contains indices of all valid capturing moves at the given offsets.

        Process flow:
        - For each offset, the method calculates the target square by adding the offset to the current piece's position.
        - If the target square is empty, it is added to the possible non-capturing moves.
        - If the target square contains a piece of the opposite color, it is added to the capturing moves.
        - The method ensures that the calculated moves are within the bounds of the board.
        """
        possible_moves = []
        possible_captures = []

        # iterate over each offset to calculate potential moves.
        for offset in offsets:
            row, col = divmod(index, 8)  # divmod returns the quotient and remainder of the division.
            row_offset, col_offset = offset

            # update the row and column positions with the offset values.
            row += row_offset
            col += col_offset

            # check if the new position is within the board boundaries (0-7 for both row and column).
            if 0 <= row < 8 and 0 <= col < 8:
                temp_index = row * 8 + col

                # if the board position is empty, it's a possible move.
                if self.fields[temp_index] == 0: possible_moves.append(temp_index)
                else:
                    # if there's a piece at the position, check if it's an opponent's piece (different color).
                    # the bitwise operations check the fourth bit of the piece value to determine the color.
                    if bool((self.fields[temp_index] >> 3) & 1) != self.white_moves: possible_captures.append(temp_index)

        return possible_moves, possible_captures
    def is_square_attacked(self, index: int, by_white: bool) -> bool:
        """
        """
        for i in range(64):
            if (self.fields[i] > 8) == by_white:
                _, captures = self.all_possible_moves_for_piece(i, False)
                if index in captures:
                    return True
        return False
    def is_king_in_check(self, by_white: bool) -> bool:
        """
        """
        king_index = self.fields.index(14 if by_white else 6)
        return self.is_square_attacked(king_index, not by_white)
    def all_possible_moves(self) -> list[str]:
        """
        """
        moves = []
        for i in range(64):
            if self.fields[i] != 0 and (self.fields[i] > 8) == self.white_moves:
                possible_moves, capturing_moves = self.all_possible_moves_for_piece(i)
                for move in possible_moves + capturing_moves:
                    backup_layout = Layout(self.layout2fen())
                    backup_layout.update(i, move)
                    if not backup_layout.is_king_in_check(not self.white_moves):
                        moves.append((i, move))
        return moves
    def is_checkmate(self) -> bool:
        """"""
        return self.is_king_in_check(not self.white_moves) and not self.all_possible_moves()
    def is_stalemate(self) -> bool:
        """"""
        return not self.is_king_in_check(not self.white_moves) and not self.all_possible_moves()
