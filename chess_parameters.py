'''
GAME PARAMETERS:
- GRAPHICS
- FONTS
- SOUNDS
- SIZES
- COLORS
- STRINGS
- FEN
'''

######## add all of them

# GRAPHICS
g_board = "Graphics/board.png"
g_pawn_b = "Graphics/pieces/pawnb.png"
g_pawn_w = "Graphics/pieces/pawn.png"
g_rook_b = "Graphics/pieces/rookb.png"
g_rook_w = "Graphics/pieces/rook.png"
g_knight_b = "Graphics/pieces/knightb.png"
g_knight_w = "Graphics/pieces/knight.png"
g_bishop_b = "Graphics/pieces/bishopb.png"
g_bishop_w = "Graphics/pieces/bishop.png"
g_queen_b = "Graphics/pieces/queenb.png"
g_queen_w = "Graphics/pieces/queen.png"
g_king_b = "Graphics/pieces/kingb.png"
g_king_w = "Graphics/pieces/king.png"

# FONTS
f_whose_move = "Fonts/handdrawn.ttf"
fs_whose_move = 45
f_file_rank_marks = "Fonts/handdrawn.ttf"
fs_file_rank_marks = 40
fc_ranks_files = 'White'
fc_move_indicator_black = 'Grey'
fc_move_indicator_white = 'White'
fp_move_indicator_placement_whites = (840,600)
fp_move_indicator_placement_blacks = (840,200)
f_check = "Fonts/handdrawn.ttf"
fs_check = 50
fc_check = "Grey"
fp_check = (170, 350)

# SOUNDS

# SIZES
size_of_a_single_squere = (100,100) # (width,hight) in pixels
screen_size = (1150,850) # (width,hight) in pixels (board: 800 x 800, 50 x 50 marks, 300 x 850 additional space)
size_of_whose_move_rect = (310,50) # (width, hight) rectangle covering previous writing

# COLORS
transparency_of_possible_moves_rectangle = 75   # % transparency
transparency_of_mouse_hovering_rectangle = 75   # % transparency
transparency_of_capture_rectangle = 95          # % transparency
color_of_mouse_hovering_rectangle = (255,0,0)   # red
color_of_possible_moves_rectangle = (0,255,0)   # green
color_of_capture_rectangle = (255,0,0)          # red

# STRINGS
s_windows_name = "Wojciech\'s chess" # windows caption
s_move_indicator_white = "WHITES MOVE" 
s_move_indicator_black = "BLACKS MOVE"
s_white_in_check = "WHITE'S KING IN CHECK"
s_black_in_check = "BLACK'S KING IN CHECK"

# FEN (Forsyth-Edward Notation)
test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
test_fen2 = "rrrrrrrr/rrrrrrrr/rrrrrrrr/rrrrrrrr/rrrrrrrr/r2r3r/rrrrrrrr/rNBrrBNr w KQkq - 0 1"
test_fen_castle = "r3k2r/pppppppp/8/8/8/8/8/R3K2R w KQkq - 0 1"
test_fen_promotion = "4k3/PPPPPPPP/8/8/8/8/1p1p1p1p/R7 b KQ-- - 0 1"
test_fen_en_passant = "rnbqkbnr/ppppppp1/8/7p/8/8/PPPPPPPP/RNBQKBNR w KQkq h6 0 1"
test_fen_attack = "r3k2r/pppppppp/rrrrrrrr/8/8/8/8/R3K2R w KQkq - 0 1"
test_fen_attack_black = "r3k2r/8/8/8/8/RRRRRRRR/8/R3K2R b KQkq - 0 1" 
#test_fen_king = "8/8/8/3Kk3/8/8/8/8 w KQkq - 0 1"
# starting possition : rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
# lowercase - blacks
# upeercase - whites
# knights - n
# 2'nd temr - who moves next (w/b)
# 3'rd term  - castling abilities (with side (kings or queens))
# 4'th term - possible en passant field (if non possible: '-')
# 5'th term - moves made since last pawn advance or piece capture
# 6'th term - turns made