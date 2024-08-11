"""

Authors: WK-K
"""
# DICTIONARIES:
piece_character2number = {'empty': 0,
                          'p': 1, 'r': 2,  'n': 3,  'b': 4,  'q': 5,  'k': 6,
                          'P': 9, 'R': 10, 'N': 11, 'B': 12, 'Q': 13, 'K': 14,}
"""
dictonary assosiating piece letter from fen to number in fields array:
0 - empty
1 - p = pawn
2 - r = rook
3 - n = knight
4 - b = bishop
5 - q = queen
6 - k = king
^ + 8 - whites (capital letters)
"""
number2piece_character = {v: k for k, v in piece_character2number.items()}
"""
dictonary assosiating number in fields array to piece letter from fen:
0 - empty
1 - p = pawn
2 - r = rook
3 - n = knight
4 - b = bishop
5 - q = queen
6 - k = king
^ + 8 - whites (capital letters)
"""
file_rank_string2board_index = {} 
"""
dictionary assosiating file-rank string with place in array:
a1 -> 0,
...,
b2  -> 9,
...,
h8 -> 63.
"""
all_possible_ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
all_possible_files = ['1', '2', '3', '4', '5', '6', '7', '8']
temp_value = 0
for file in all_possible_files:
    for rank in all_possible_ranks:
        file_rank_name = rank + file
        file_rank_string2board_index[file_rank_name] = temp_value
        temp_value += 1
board_index2file_rank_string = {v: k for k, v in file_rank_string2board_index.items()}
"""
dictionary assosiating file-rank string with place in array:
0 -> a1,
...,
9  -> b2,
...,
63 -> h8.
"""
del all_possible_files, all_possible_ranks, temp_value

# FUNCTIONS:
# -- FEN --
def fen2piece_count(fen: str) -> int:
    """Returns number of pieces that are on a given board from fen notation."""
    fen: str = fen.split(' ')[0] # extrcts part of fen with pieces
    piece_count: int = 0
    for char in fen:
        if char.isalpha():
            piece_count += 1 # if leetter in fen is char it is a piece
    return piece_count

def fen2array_of_fields(fen: str) -> list[int]:
    """Returns board as a 64 elemnt list with numbers from translator file corresponding to to pieces from FEN"""
    arr: list = [0] *64
    fen: str = fen.split(' ')[0]
    rank: int = 7
    file: int = 0

    for char in fen:
        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            arr[rank*8 + file] = piece_character2number[char]
            file +=1

    return arr

def fen2castling_arr(fen: str) -> list[bool]:
    """Returns boolian array size 4 with castling abilities based on FEN string, that is: K, Q, k, q."""
    fen: str = fen.split(' ')[2] # Extracting castling abilities part of fen
    arr: list = [True]*4
    for index, char in enumerate(fen):
        if char == '-': arr[index] = False
    return arr

def array_of_fields2fen(arr: list[int]) -> str:
    """
    Returns part of FEN string with piece placement based on board
    as a 64 element array of fields as intigers from number2piece_character dict:
    0 - empty
    1 - p = pawn
    2 - r = rook
    3 - n = knight
    4 - b = bishop
    5 - q = queen
    6 - k = king
    ^ + 8 - whites (capital letters).
    """
    fen: str = ''
    rank: int = 7
    file: int = 0

    while rank > 0:
        if file >= 8:
            fen += "/"
            rank -= 1
            file = 0

        while file < 8:
            piece_in_arr = arr[rank * 8 + file]
            if piece_in_arr != 0:
                fen += number2piece_character[piece_in_arr]
            else:
                empty_count = 0
                while file < 8 and arr[rank * 8 + file] == 0:
                    empty_count += 1
                    file += 1
                file -= 1
                fen += str(empty_count)
            if file >= 8:
                break
            file += 1

    return fen




"""
import traceback
import pygame
import copy

# -- NOT USED --
# returns array of indexies of pieces in given color ('w' or 'b') from fields array
def ind_of_colored_pieces(arr, color):
    out_arr = []
    if color == 'b':
        for index, element in enumerate(arr):
            if element<8 and element!=0: out_arr.append(index)
    elif color == 'w':
        for index, element in enumerate(arr):
            if element>8: out_arr.append(index)
    else:
        print("MY ERROR: NO CONDITION CHOSEN")
        traceback.print_stack()
    return out_arr


# -- SCREEN --
# returns rectangle that outlines field on board with mouse
def mouse_rect(x, y):
    for i in range(8): 
        for j in range(8):
            if i*100 < x < (i+1)*100 and j*100 < y < (j+1)*100:
                return (i*100,j*100)
# returns index in 64 int array of fields on board from board coordinates (800x800)
def board_coords2field_index(coords):
    for i in range(8):
        for j in range(8):
            # if coursor is on that field
            if i*100 < coords[0] < (i+1)*100 and j*100 < coords[1] < (j+1)*100: return i + j*8
# returns board coordinates for given element of 64 element array of fields
def field2board_coords_of_piece(field):
    file = (field % 8) * 100
    rank = (7 - field // 8) * 100
    return file, rank
# returns pygame.image for a given piece
def piece2graphic(piece):
    if piece == 1: picture = pygame.image.load(param.g_pawn_b).convert_alpha()
    elif piece == 9: picture = pygame.image.load(param.g_pawn_w).convert_alpha()
    elif piece == 2: picture = pygame.image.load(param.g_rook_b).convert_alpha()
    elif piece == 10: picture = pygame.image.load(param.g_rook_w).convert_alpha()
    elif piece == 3: picture = pygame.image.load(param.g_knight_b).convert_alpha()
    elif piece == 11: picture = pygame.image.load(param.g_knight_w).convert_alpha()
    elif piece == 4: picture = pygame.image.load(param.g_bishop_b).convert_alpha()
    elif piece == 12: picture = pygame.image.load(param.g_bishop_w).convert_alpha()
    elif piece == 5: picture = pygame.image.load(param.g_queen_b).convert_alpha()
    elif piece == 13: picture = pygame.image.load(param.g_queen_w).convert_alpha()
    elif piece == 6: picture = pygame.image.load(param.g_king_b).convert_alpha()
    elif piece == 14: picture = pygame.image.load(param.g_king_w).convert_alpha()
    else:
        picture = None
        print("MY ERROR: NO CONDITION CHOSEN")
        traceback.print_stack()
    return picture
# draws pieces on screen from a given layout
def draw_pieces(screen, layout, excluded_pieces_index):
    for index,f in enumerate(layout.fields):
        if index != excluded_pieces_index:
            if f != 0:
                screen.blit(piece2graphic(f), [pos + 10 for pos in field2board_coords_of_piece(index)])
# draws marks around the board on a given screen
def draw_marks(ml, mn, screen):
    '''
    INPUT:
    ml - list of marks letters
    mn - list of marks numbers
    '''
    for i in range(8):
        screen.blit(ml[i],(i*100+40,800))
        screen.blit(mn[7-i],(810,i*100+35)) # 7-i reverses ranks so they would mach


# -- POSSIBLE MOVES --
# checking if a given field is under attack of a given color pieces
def if_field_under_attack(layout, index, under_black_attack, is_field_empty):
    # Create a temporary layout copy to simulate piece moves for attack checking
    layout_temp = copy.deepcopy(layout)
    # first list for possible_moves, secound for capturing moves
    list_index = 0 if is_field_empty else 1
    # Check if field is under attack by black pieces
    if under_black_attack:
        layout_temp.white_moves = False
        # Loop through each field to find black pieces
        for i, field in enumerate(layout.fields):
            # If field with black piece
            if field < 8 and field != 0:
                # Check if the piece at index i can attack the given index
                if (index in all_possible_moves_for_piece(layout_temp, i, False)[list_index]): return True

    # Check if field is under attack by white pieces
    else:
        layout_temp.white_moves = True
        # Loop through each field to find white pieces
        for i, field in enumerate(layout.fields):
            # If field with white piece
            if field > 8:
                # Check if the piece at index i can attack the given index
                if index in all_possible_moves_for_piece(layout_temp, i, False)[list_index]: return True

    del layout_temp
    # If no attacking piece found, return False
    return False
# check if a king of a given color is in check
def is_king_in_check(layout, white_king_bool):
    king_piece = 6 if white_king_bool else 14
    for i, field in enumerate(layout.fields):
        if field == king_piece:
           return if_field_under_attack(layout, i, not white_king_bool, False)
# takes list of possible moves and removes moves that would lead to king in check
def moves_without_check(layout, list_of_moves, piece_index):
    layout_temp = copy.deepcopy(layout)
    piece_temp = 0

    for move in list_of_moves:
        piece_temp = layout_temp.fields[move]
        layout_temp.fields[move] = layout_temp.fields[piece_index]
        layout_temp.fields[piece_index] = 0

        if is_king_in_check(layout_temp, layout_temp.white_moves): list_of_moves.remove(move)

        layout_temp.fields[piece_index]= layout_temp.fields[move]
        layout_temp.fields[move] = piece_temp
    
    del layout_temp
# added moves without check
def all_possible_moves_for_piece2(possible_moves, capturing_moves, index, layout):
    moves_without_check(layout, possible_moves, index)
    moves_without_check(layout, capturing_moves, index)
    return possible_moves, capturing_moves


"""
























