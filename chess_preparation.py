'''
initializing pygame
initializing window
FEN
Pictures
Variables used in main loop
'''
import pygame
import chess_parameters as param 

# INICIALIZING GRAPHICS
# initializing pygame
pygame.init()
# initializing window
screen = pygame.display.set_mode(param.screen_size)
# setting window name
pygame.display.set_caption(param.s_windows_name)
# setting framerate
clck = pygame.time.Clock() #This variable is used in the while loop to set framerate
max_frm_rt = 60             #Maximum framerate (1/60 of a secound)


# PICTURES
# Board
board_pctr = pygame.image.load(param.g_board).convert()

# Text
whose_move_fnt = pygame.font.Font(param.f_whose_move, param.fs_whose_move)
whose_move_rect = pygame.Surface(param.size_of_whose_move_rect)
pygame.draw.rect(whose_move_rect, 'Black', whose_move_rect.get_rect(), param.size_of_whose_move_rect[0])
check_fnt = pygame.font.Font(param.f_check, param.fs_check)
white_in_check_txt = check_fnt.render(param.s_white_in_check, False, param.fc_check)
black_in_check_txt = check_fnt.render(param.s_black_in_check, False, param.fc_check)

marks_fnt = pygame.font.Font(param.f_file_rank_marks, param.fs_file_rank_marks)
mrks_lttrs=[]
mrks_nmbrs=[]
for l in list(map(chr, range(65, 73))): mrks_lttrs.append(marks_fnt.render('{}'.format(l), False, param.fc_ranks_files)) # marks files (letters)
for n in range(1,9): mrks_nmbrs.append(marks_fnt.render('{}'.format(n), False, param.fc_ranks_files))    # marks ranks (numbers)

# mouse rectangle
mouse_rect = pygame.Surface(param.size_of_a_single_squere)
mouse_rect.set_alpha(param.transparency_of_mouse_hovering_rectangle)
pygame.draw.rect(mouse_rect,param.color_of_mouse_hovering_rectangle,mouse_rect.get_rect(),param.size_of_a_single_squere[0])
m_rect_coord = (-200,-200) # out of range

# possible moves rectangle
possible_moves_rectangle = pygame.Surface(param.size_of_a_single_squere)
possible_moves_rectangle.set_alpha(param.transparency_of_possible_moves_rectangle)
pygame.draw.rect(possible_moves_rectangle, param.color_of_possible_moves_rectangle, possible_moves_rectangle.get_rect(),param.size_of_a_single_squere[0])

# capture rectangles
capture_rectangle = pygame.Surface(param.size_of_a_single_squere)
capture_rectangle.set_alpha(param.transparency_of_capture_rectangle)
pygame.draw.rect(capture_rectangle, param.color_of_capture_rectangle,capture_rectangle.get_rect(),param.size_of_a_single_squere[0])


# VARIABLES USED IN MAIN LOOP
grabbed_piece_picture = None 
grabbed_piece_field = None  #index of grabbed piece
m_pos = (0,0)
possible_moves_arr = []     # possible moves array (without captures)
possible_captures_arr = []  # possible captures array


