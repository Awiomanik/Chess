import chess_functions as func

fields = [10, 11, 12, 13, 14, 12, 11, 10,
                       9, 9, 9, 9, 9, 9, 9, 9,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1, 1, 1,
                       2, 3, 4, 5, 6, 4, 3, 2]
fields_with_white_pieces = func.ind_of_colored_pieces(fields, 'w')
print(fields_with_white_pieces)