# This file contains following dictionaries facilitating future coding:
# dictionary assosiating file-rank with place in array
# dictonary assosiating piece letter from fen to number in fields array

# dictionary assosiating file-rank with place in array
# eg a1 -> 0, b2  -> 9, hg -> 63 ...
file_rank_string2board_index = {} 
all_possible_ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
all_possible_files = ['1', '2', '3', '4', '5', '6', '7', '8']
temp_value = 0
for file in all_possible_files:
    for rank in all_possible_ranks:
        file_rank_name = rank + file
        file_rank_string2board_index[file_rank_name] = temp_value
        temp_value += 1
board_index2file_rank_string = {v: k for k, v in file_rank_string2board_index.items()}
del all_possible_files, all_possible_ranks, temp_value

# dictonaries assosiating piece letter from fen to number in fields array (and the otherway)
# 0 - empty
# 1 - p = pawn
# 2 - r = rook
# 3 - n = knight
# 4 - b = bishop
# 5 - q = queen
# 6 - k = king
# ^ + 8 - whites (capital letters)
piece_character2number = {'empty': 0,
                          'p': 1, 'r': 2,  'n': 3,  'b': 4,  'q': 5,  'k': 6,
                          'P': 9, 'R': 10, 'N': 11, 'B': 12, 'Q': 13, 'K': 14,}
number2piece_character = {v: k for k, v in piece_character2number.items()}




