import pygame
from sys import exit # used to exit the while loop
import chess_preparation as prep
import chess_functions as func
import chess_classes as cl
import chess_parameters as param


# szach
# zasady pata
# zasady mata 
# wyświetlanie zbitych (osobne okno na informacje)
# przeżuć funkcje na layout do metod layout
# dokumentacja
# random ai
# cofanie ruchu
# zapis gier i ich wznawianie i odtwarzanie
# UI obraz i dźwięk (wybór przy promocji)
# AI

# USEFULL FUNCTIONS
def loosing_grabbed_piece():
    prep.grabbed_piece_field = None
    prep.grabbed_piece_picture = None # deleting grabbed piece picture
def grabb_new_piece(clicked_field, clicked_piece):
    prep.grabbed_piece_field = clicked_field
    prep.grabbed_piece_picture = func.piece2graphic(clicked_piece)
    prep.possible_moves_arr, prep.possible_captures_arr = func.all_possible_moves_for_piece(layout, clicked_field)
def draw_whoose_move_text(whoose_move):
    if whoose_move:
        whose_move_txt = prep.whose_move_fnt.render(param.s_move_indicator_white, False, param.fc_move_indicator_white)
        prep.screen.blit(prep.whose_move_rect, param.fp_move_indicator_placement_blacks)
        prep.screen.blit(whose_move_txt,param.fp_move_indicator_placement_whites)
    else: 
        whose_move_txt = prep.whose_move_fnt.render(param.s_move_indicator_black, False, param.fc_move_indicator_black)   #False-Antiaiasing
        prep.screen.blit(prep.whose_move_rect, param.fp_move_indicator_placement_whites)
        prep.screen.blit(whose_move_txt,param.fp_move_indicator_placement_blacks)


# inicializing layout
#layout = cl.layout(param.test_fen2)
#layout = cl.layout(param.test_fen_en_passant)
#layout = cl.layout(param.test_fen_castle)
#layout = cl.layout(param.test_fen_attack_black)
#layout = cl.layout()
print('Staring layoutout: ', layout)


# EVENT HANDLING FUNCTIONS
def mouse_motion_handling(pos):
    # check if in board
    if 0 < pos[0] < 800 and 0 < pos[1] < 800: 
        # mouse rectangle
        prep.m_rect_coord = func.mouse_rect(pos[0], pos[1])
    else:
        # mouse rect deletion
        prep.m_rect_coord = None
        # loosing grabbed piece
        if prep.grabbed_piece_field != None: loosing_grabbed_piece()
    return False
def mouse_down_handling(pos):
    """
    - Checks if the mouse click occurred within the chessboard boundaries.
    - Determines the field clicked on the chessboard based on the position.
    - Retrieves the piece value of the clicked field.
    - If a piece is already grabbed:
        - If the clicked field is a valid move, updates the layout by moving the piece to the new field.
        - If the clicked field is not a valid move:
            - Checks if there is another piece of the same color on the clicked field.
            - If so, grabs the new piece and updates the grabbed piece field and picture.
        - Releases the grabbed piece by clearing the grabbed piece field.
    - If no piece is currently grabbed:
        - Checks if there is a piece of the same color on the clicked field.
        - If so, grabs the piece and updates the grabbed piece field and picture.
    """
    # if on board
    if 0 <= pos[0] <= 800 and 0 <= pos[1] <= 800:

        # check on which field
        clicked_field = func.board_coords2field_index((pos[0], 800 - pos[1]))
        print("\nSearching for a bug I cannot replicate, but it is coralated with clicked_field: ", clicked_field)
        clicked_piece = layout.fields[clicked_field]
        print("\nclicked_piece: ", clicked_piece)

        # piece grabbed
        if prep.grabbed_piece_field != None:
            # move possible -> do move
            if clicked_field in prep.possible_moves_arr or clicked_field in prep.possible_captures_arr :
                layout.update(prep.grabbed_piece_field, clicked_field)  # update layout
                loosing_grabbed_piece()
                draw_whoose_move_text(layout.white_moves)
                print(layout)
            # move not possible
            else:
                # clicked on same field to loose piece
                if clicked_field == prep.grabbed_piece_field: loosing_grabbed_piece()
                # there is other piece in same color (information is in the fourth bit)
                elif (clicked_piece != 0 and (clicked_piece >> 3) & 1 == (layout.fields[prep.grabbed_piece_field] >> 3) & 1):
                    loosing_grabbed_piece()
                    grabb_new_piece(clicked_field, clicked_piece)
        # no piece grabbed
        else:
            # there is piece in same color (information is in the fourth bit)
            if clicked_piece != 0 and (layout.white_moves == bool(clicked_piece >> 3 & 1)): grabb_new_piece(clicked_field, clicked_piece)

    return False


# if event happened (inicialization)
if_mouse_motion = False
if_mouse_down = False


# DRAW BEFOREHAND
# file and rank marks
func.draw_marks(prep.mrks_lttrs, prep.mrks_nmbrs, prep.screen)
# whose move text
whose_move_txt = prep.whose_move_fnt.render(param.s_move_indicator_white, False, param.fc_move_indicator_white)
prep.screen.blit(whose_move_txt,param.fp_move_indicator_placement_whites)


# MAIN LOOP OF THE GAME
while True:
    # LOPP THROUGH ALL EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # <- pressing X to close window
            pygame.quit()   #closes window
            exit()          #exits while loop
        if event.type == pygame.MOUSEMOTION:
            if_mouse_motion = True
            prep.m_pos = event.pos #saving mouse position
        if event.type == pygame.MOUSEBUTTONDOWN:
            if_mouse_down = True
            prep.m_pos = event.pos #saving mouse position
            

    # EVENT HANDLING
    if if_mouse_motion: if_mouse_motion = mouse_motion_handling(prep.m_pos)
    if if_mouse_down: if_mouse_down = mouse_down_handling(prep.m_pos)


    # DRAWING ELEMENTS
    # board
    prep.screen.blit(prep.board_pctr,(0,0))
    # mouse rectangle
    if prep.m_rect_coord: prep.screen.blit(prep.mouse_rect, prep.m_rect_coord)
    # pieces
    func.draw_pieces(prep.screen, layout, prep.grabbed_piece_field)
    # grabbed piece, possible moves rectangles, capture rectangles
    if prep.grabbed_piece_field != None:
        # drawing possible moves rectangles
        for f in prep.possible_moves_arr:  prep.screen.blit(prep.possible_moves_rectangle, func.field2board_coords_of_piece(f))
        # drawing possible captures
        for f in prep.possible_captures_arr: prep.screen.blit(prep.capture_rectangle, func.field2board_coords_of_piece(f))
        # drawing grabbed piece
        prep.screen.blit(prep.grabbed_piece_picture, (prep.m_pos[0]-50, prep.m_pos[1]-50))
    # white king in check text
    if func.is_king_in_check(layout, False): prep.screen.blit(prep.white_in_check_txt, param.fp_check)
    # black king in check text
    if func.is_king_in_check(layout, True): prep.screen.blit(prep.black_in_check_txt, param.fp_check)
    
    

    # UPDATE THINGS:
    pygame.display.update() #updates the window (frame)
    prep.clck.tick(prep.max_frm_rt)  #setting maximum framerate
