import pygame
import chess_functions as func
import chess_translator as trans

class layout:
    '''
    Represents the layout of a chessboard.
    ATTRIBUTES:
        - piece_count: Total count of pieces on the board
        - fields: Array of fields on the board (0 - a1, 1 - a2, 63 - h8) with numbers indicating occupation:
            0 - empty
            1 - p = pawn
            2 - r = rook
            3 - n = knight
            4 - b = bishop
            5 - q = queen
            6 - k = king
            ^ + 8 - whites (capital letters)
        - white_moves: Flag indicating whether it's currently white's turn to move
        - moves_made: Number of moves made so far
        - castling: Castling availability as in FEN notation, i.e., [K, Q, k, q]
        - en_passant: Index of the square over which a pawn has passed by moving two squares forward ('-' if none)
        - clock: Number of moves made since the last capture or pawn advance (used in the 50-move rule)
    METHODS:
        - __init__(fen=None): Initializes the layout object. If 'fen' is None, initializes with the default layout.
        - _init_default(): Initializes the layout with the default piece positions.
        - fen2layout(fen): Initializes the layout from the given FEN notation.
        - layout2fen(): Returns the FEN notation representation of the layout.
        - update(new_field, old_field): updates layout atributes after the move
        - casttling_update(old_piece, old_field, new_field): part of update, extracted for clarity
    '''
    
    # ATRIBUTES
    piece_count = 0
    fields = [] *64 # array of fields on the board (0 - a1, 1 - a2, 63 - h8) with numbers indicating occupation:
    white_moves = True
    moves_made = 0
    castling = [True]*4 # Castling availability as in FEN notation, that is: K, Q, k, q
    en_passant = None # fields array index of squere over whitch a pawn has passed by moving two squeres forward
    clock = 0 # number of moves made since last capture or pawn advance used in 50-move rule
    # constants
    ROOK_MOVEMENT_DIRECTIONS =      [(1, 0), (-1, 0), (0, 1), (0, -1)]
    KNIGHT_MOVEMENT_OFFSET =        [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    BISHOP_MOVEMENT_DIRECTIONS =    [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    QUEEN_MOVEMENT_DIRECTIONS =     [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    # METHODS
    # magic methods
    def __init__(self, fen=None):
        '''Initialize chess game with standard leyout (if no FEN given), or from FEN'''
        if fen is None: self._init_default()
        else: self.fen2layout(fen) 
    def __str__(self):
        ''''Returnsz string representation of all atributes'''
        if self.en_passant == None: temp_ep = '-'
        else: temp_ep = trans.board_index2file_rank_string[self.en_passant]

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
            f8 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[0:8]]),
            f7 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[8:16]]),
            f6 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[16:24]]),
            f5 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[24:32]]),
            f4 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[32:40]]),
            f3 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[40:48]]),
            f2 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[48:56]]),
            f1 = '\t'.join([trans.number2piece_character[piece] for piece in self.fields[56:64]]),
            whose_move = "White" if self.white_moves else "Black",
            moves = self.moves_made,
            cK = self.castling[0],
            cQ = self.castling[1],
            ck = self.castling[2],
            cq = self.castling[3],
            ep = temp_ep,
            clock = self.clock) 
    def _init_default(self):
        '''Initializes layout with standard arrangement of pieces'''
        self.piece_count = 32
        self.fields = [10, 11, 12, 13, 14, 12, 11, 10,
                       9, 9, 9, 9, 9, 9, 9, 9,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1, 1, 1,
                       2, 3, 4, 5, 6, 4, 3, 2]
    # fen operations
    def fen2layout(self, fen):
        ''''Sets layout atributes to coresponding to FEN string'''
        # piece count
        self.piece_count = func.fen2piece_count(fen)
        # fields
        self.fields = func.fen2array_of_fields(fen)
        # white moves
        if fen.split(' ')[1] == 'b': self.white_moves = False
        # moves made
        self.moves_made = int(fen.split(' ')[5])
        # castling
        self.castling = func.fen2castling_arr(fen)
        # en passant
        if fen.split(' ')[3] != '-': self.en_passant = trans.file_rank_string2board_index[fen.split(' ')[3]]
        # clock
        self.clock = int(fen.split(' ')[4])
    def layout2fen(self):
        '''Returns FEN notation string corresponding to layout'''
        # white moves
        if self.white_moves: color = 'w'
        else: color = 'b'
        # castling
        cast_temp_arr = ['K', 'Q', 'k', 'q']
        castling_characters = [cast_temp_arr[i] if self.castling[i] else '-' for i in range(4) ]
        # en passant
        temp_passant = '-'
        if self.en_passant != None: temp_passant = trans.board_index2file_rank_string[self.en_passant]

        # FEN
        fen = (func.array_of_fields2fen(self.fields) + ' '
        + color + ' '
        + ''.join([castling_characters[i] if self.castling[i] else '-' for i in range(4)]) + ' '
        + temp_passant + ' '
        + str(self.clock) + ' '
        + str(self.moves_made))

        return fen   
    # changing layout
    def update(self, old_field, new_field):
        ''''Updates all atributes based on a given move (old_field -> new_field)'''
        old_piece = self.fields[old_field]
        new_piece = self.fields[new_field]
        # if en passant happened
        en_passant_happened = (new_field == self.en_passant and (old_piece == 9 or old_piece == 1))
        # if capture happend
        if new_piece != 0 or en_passant_happened: capture_bool = True
        else: capture_bool = False

        # piece_count
        if capture_bool: self.piece_count -=1 # one piece captured

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
        # en passant not happend
        # white pawn moved two spaces
        if old_piece == 9 and new_field - old_field == 16: self.en_passant = old_field + 8
        # black pawn moved two spaces
        if old_piece == 1 and old_field - new_field == 16: self.en_passant = old_field - 8

        # clock
        if capture_bool or self.fields[old_field] == 1 or self.fields[old_field] == 9: self.clock = 0
        else: self.clock += 1

        # Promotion
        # white
        if old_piece == 9 and new_field > 55: self.fields[new_field] = 13
        # black
        if old_piece == 1 and new_field < 8: self.fields[new_field] = 5
    def castling_update(self, old_piece, old_field, new_field):
        '''Part of update(), etracted for more readability'''
        offset = old_field - new_field

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
        if old_field == 7: self.castling[0] = False
        # white queen's rook castling possibility
        if old_field == 0: self.castling[1] = False
        # black king's rook castling possibility
        if old_field == 63: self.castling[2] = False
        # black queen's rook castling possibility
        if old_field == 56: self.castling[3] = False
    def all_possible_moves_for_piece(self, index, with_castling_bool=True):
        '''
        For a given piece (index of it's field on the board) returns tuple of lists containing:
        possible in this moment moves (indicies of ending fields), excluding move that would end with capture,
        moves that would end with capture.
        If with_castling_bool is set to False, methods doesn't consider castling as possible move
        
        Process flow:
        (exept for pawn and king)
        - checks whoes move is it
        - checks kind of piece
        - uses get_moves_at_offsets() and get_moves_in_direction() to populate returned array
        '''
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
    def get_moves_in_directions(self, index, directions):
        '''
        For a given directions (in indexed board fields dimention)
        and given index on the board
        returns tuple with two lists containing:
        possible in this moment moves (indicies of ending fields), excluding move that would end with capture,
        moves that would end with capture.
        '''
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
    def get_moves_at_offsets(self, index, offsets):
        '''
        For a given offsets (in indexed board fields dimention)
        and given index on the board
        returns tuple with two lists containing:
        possible in this moment moves (indicies of ending fields), excluding move that would end with capture,
        moves that would end with capture.
        '''
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


# przerób inny input do posible moves I UNDER attack
# if field under attack






