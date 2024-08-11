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

        return """\n\n------LAYOUT OBJECT------\n
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
        en_passant_happened = (new_field == self.en_passant and (old_piece == 9 or old_piece == 1))
        # if capture happend
        if new_piece != 0 or en_passant_happened: capture_bool = True
        else: capture_bool = False

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
            if self.white_moves: self.fields[new_field + 8] = 0
            # white capturing (moves are reversed earlier)
            else: self.fields[new_field - 8] = 0
        self.en_passant = None
        # en passant capture not happend
        # white pawn moved two spaces
        if old_piece == 9 and new_field - old_field == 16: self.en_passant = old_field + 8
        # black pawn moved two spaces
        if old_piece == 1 and old_field - new_field == 16: self.en_passant = old_field - 8

        # clock
        if capture_bool or \
            self.fields[old_field] == 1 or \
            self.fields[old_field] == 9:
            self.clock = 0
        else: self.clock += 1

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
    def all_possible_moves_for_piece(self, index: int, with_castling_bool: bool=True) -> tuple[list[int], list[int]]:
        """
        Calculate all possible moves for a specific piece on the board.

        For the piece located at the given `index`, this method returns a tuple containing two lists:
        - A list of indices representing possible non-capturing moves.
        - A list of indices representing capturing moves.

        If `with_castling_bool` is set to `False`, castling moves will not be considered.

        Arguments:
        - index (int): The board index (0-63) of the piece for which to calculate possible moves.
        - with_castling_bool (bool): Whether to include castling moves in the possible moves (default is True).

        Returns:
        - tuple[list[int], list[int]]: 
            - The first list contains indices of all valid non-capturing moves.
            - The second list contains indices of all valid capturing moves.

        Process flow:
        - Checks whose move it is (white or black).
        - Determines the type of piece at the given index.
        - Uses helper methods (`get_moves_at_offsets`, `get_moves_in_directions`) to populate the lists of possible moves.
        - Special handling for pawns (including en passant) and kings (including castling).
        """
        piece = self.fields[index]
        possible_moves = []
        capturing_moves = []

        if self.white_moves:
            # PAWN
            if piece == 9:
                offset = 8
                start_row = 1
                left_capture = index + offset - 1
                right_capture = index + offset + 1

                # capture
                # if not on left edge
                if index % 8 != 0:
                    # if black piece or en passant on the left
                    if (self.fields[left_capture] != 0 and self.fields[left_capture] < 8) or left_capture == self.en_passant:
                        capturing_moves.append(left_capture)
                # if not on right edge
                if index % 8 != 7:
                    # if black piece or en passant on the right
                    if (self.fields[right_capture] != 0 and self.fields[right_capture] <8) or right_capture == self.en_passant:
                        capturing_moves.append(right_capture)

                # move
                if self.fields[index + offset] == 0:
                    possible_moves.append(index + offset) # move one up

                    if index // 8 == start_row and self.fields[index + offset * 2] == 0:
                        possible_moves.append(index + offset * 2) # move two up
            # ROOK
            elif piece == 10: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.ROOK_MOVEMENT_DIRECTIONS, self.white_moves)
            # KNIGHT
            elif piece == 11: possible_moves, capturing_moves = self.get_moves_at_offsets(self.fields, index, self.KNIGHT_MOVEMENT_OFFSET, self.white_moves)
            # BISHOP
            elif piece == 12: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.BISHOP_MOVEMENT_DIRECTIONS, self.white_moves)
            # QUEEN
            elif piece == 13: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.QUEEN_MOVEMENT_DIRECTIONS, self.white_moves)
            # KING
            elif piece == 14: 
                king_move_offsets = self.QUEEN_MOVEMENT_DIRECTIONS
                # castle
                if with_castling_bool:
                    # check if kings castling possible
                    if self.castling[0]:
                        # check if fields between king and rook are empty
                        if self.fields[index + 1] == 0 and self.fields[index + 2] == 0:
                            # check if fields king moves through are under attack
                            if not (self.if_field_under_attack(index, True, True) or self.if_field_under_attack(index + 1, True, True) or self.if_field_under_attack(index + 2, True, True)):
                                # add kings castling move to list of offsets
                                king_move_offsets.append((0, 2))
                    # check if queens castling possible
                    if self.castling[1]:
                        # check if fields between king and rook are empty
                        if all(f == 0 for f in self.fields[index-3 : index]):
                            # check if fields king moves through are under attack
                            if not (self.if_field_under_attack(index, True, True) or self.if_field_under_attack(index - 1, True, True) or self.if_field_under_attack(index - 2, True, True)):
                                # add queens castling move to list of offsets
                                king_move_offsets.append((0, -2))

                possible_moves, capturing_moves= self.get_moves_at_offsets(self.fields, index, king_move_offsets, self.white_moves)

        else: # Code for black pieces
            # PAWN
            if piece == 1:
                offset = -8
                start_row = 6
                left_capture = index + offset - 1
                right_capture = index + offset + 1
                
                # capture
                # if not on left edge
                if index % 8 != 0:
                    # if white piece or en passant on the left
                    if self.fields[left_capture] > 8 or left_capture == self.en_passant:
                        capturing_moves.append(left_capture)
                # if not on right edge
                if index % 8 != 7:
                    # if white piece or en passant on the right
                    if self.fields[right_capture] > 8 or right_capture == self.en_passant:
                        capturing_moves.append(right_capture)

                # move
                if self.fields[index + offset] == 0:
                    possible_moves.append(index + offset) # move one down

                    if index // 8 == start_row and self.fields[index + offset * 2] == 0:
                        possible_moves.append(index + offset * 2) # move two down
            # ROOK
            elif piece == 2: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.ROOK_MOVEMENT_DIRECTIONS, self.white_moves)
            # KNIGHT
            elif piece == 3: possible_moves, capturing_moves = self.get_moves_at_offsets(self.fields, index, self.KNIGHT_MOVEMENT_OFFSET, self.white_moves)
            # BISHOP
            elif piece == 4: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.BISHOP_MOVEMENT_DIRECTIONS, self.white_moves)
            # QUEEN
            elif piece == 5: possible_moves, capturing_moves = self.get_moves_in_directions(self.fields, index, self.QUEEN_MOVEMENT_DIRECTIONS, self.white_moves)
            # KING
            elif piece == 6:  
                king_move_offsets = self.QUEEN_MOVEMENT_DIRECTIONS
                # castle
                if with_castling_bool:
                    # check if kings castling possible
                    if self.castling[2]:
                        # check if fields between king and rook are empty
                        if self.fields[index + 1] == 0 and self.fields[index + 2] == 0:
                            # check if fields king moves through are under attack
                            if not (self.if_field_under_attack(index, False, True) or self.if_field_under_attack(index + 1, False, True) or self.if_field_under_attack(index + 2, False, True)):
                                # add kings castling move to list of offsets
                                king_move_offsets.append((0, 2))
                    # check if queens castling possible
                    if self.castling[3]:
                        # check if fields between king and rook are empty
                        if all(f == 0 for f in self.fields[index-3 : index]):
                            # check if fields king moves through are under attack
                            if not (self.if_field_under_attack(index, False, True) or self.if_field_under_attack(index - 1, False, True) or self.if_field_under_attack(index - 2, False, True)):
                                # add queens castling move to list of offsets
                                king_move_offsets.append((0, -2))

                possible_moves, capturing_moves = self.get_moves_at_offsets(self.fields, index, king_move_offsets, self.white_moves)
                
        return possible_moves, capturing_moves
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
