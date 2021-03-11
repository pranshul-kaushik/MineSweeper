import numpy as np
import random
import sys
sys.path.append(".")
from game.game_logic.bring_board import createBoard
from game.game_logic.opening_cells import update_board
from game.models import *
import time

def AI(user_id , timer):

    _board_info = board_info.objects.filter(user_id__user_id = user_id).latest('updated_on')
    _board_info.timer = timer
    _board_info.save()

    board = _board_info.true_board
    given_board = _board_info.to_give_board
    number_bomb = _board_info.number_bombs
    cell_left  = _board_info.cell_left
    prob_board = _board_info.prob_board
    status = _board_info.status
    num_row, num_col = board.shape[0], board.shape[1]

    def Number (choice):
        return board[choice[0]][choice[1]].number

    def Is_checked (choice, put =None):

        if put != None:
            board[choice[0]][choice[1]].is_checked = put

        else:
            return board[choice[0]][choice[1]].is_checked

    def Adj(choice):
        return board[choice[0]][choice[1]].adj

    def Cell(choice):
        return board[choice[0]][choice[1]]

    def prob_of_bomb_in_area(cell):
        
        bomb_left_to_mark = cell.number
        number_of_places_bomb_can_be = 0
        for each_adj in cell.adj.values():
            if each_adj and Cell(each_adj).is_flaged:
                bomb_left_to_mark -= 1
            if each_adj and not Cell(each_adj).is_checked:
                number_of_places_bomb_can_be += 1
        if bomb_left_to_mark != 0:
            prob = combination(number_of_places_bomb_can_be -1 , bomb_left_to_mark -1) / \
                combination(number_of_places_bomb_can_be, bomb_left_to_mark)
        else:
            prob = 0.00001

        for each_adj in cell.adj.values():
            if each_adj and not Cell(each_adj).is_checked:
                position = Cell(each_adj).pos
                if prob != 0.00001 and prob_board[position[0]][position[1]] != 0.00001:
                    max_prob = max(prob_board[position[0]][position[1]],
                                                              prob)
                    prob_board[position[0]][position[1]] = max_prob                                          
                if prob == 0.00001:
                    prob_board[position[0]][position[1]] = 0.00001


    def combination(n, r):
        n_fact = 1
        r_fact = 1
        n_r_fact = 1
        n_r = n - r
        for i in range(1, n+1):
            n_fact *= i
        for i in range(1, r+1):
            r_fact *= i
        for i in range(1, n_r+1):
            n_r_fact *= i
        return n_fact/ (r_fact * n_r_fact)
    time_l = []
    if not status:
        choice_list = [[i,j] for i in range(board.shape[0]) for j in range(board.shape[1]) if not board[i][j].is_checked]
        action = 0
        master = ""
        for i in range(num_row):
            for j in range(num_col):
                if board[i][j].is_checked and not board[i][j].is_flaged:
                    total_number_of_adj_checked=0
                    total_number_of_adj_none=0
                    for each_adj in board[i][j].adj.values():
                        try:
                            total_number_of_adj_checked += int(Cell(each_adj).is_checked)
                        except:
                            total_number_of_adj_none += 1
                    if (8 - total_number_of_adj_none - total_number_of_adj_checked) > 0:
                        prob_of_bomb_in_area(board[i][j])

        max_prob_of_bomb = [0, [-1,-1]]
        min_prob_of_bomb = [1, [-1,-1]]
        for i in range(num_row):
            for j in range(num_col):
                if [i,j] in choice_list:
                    if prob_board[i][j] > max_prob_of_bomb[0]:
                        max_prob_of_bomb[0] = prob_board[i][j]
                        max_prob_of_bomb[1] = [i,j]

                    total_number_of_adj_checked=0
                    total_number_of_adj_flag=0
                    for each_adj in Cell([i,j]).adj.values():
                        try:
                            total_number_of_adj_checked += int(Cell(each_adj).is_checked)
                            total_number_of_adj_flag += int(Cell(each_adj).is_flaged)
                        except:
                            continue

                    if total_number_of_adj_checked - total_number_of_adj_flag > 0:
                        if prob_board[i][j] < min_prob_of_bomb[0]:
                            min_prob_of_bomb[0] = prob_board[i][j]
                            min_prob_of_bomb[1] = [i,j]
                
        if max_prob_of_bomb[0] > 1 - 0.15 or min_prob_of_bomb[0] < 0.15:
            if max_prob_of_bomb[0] > 1 - 0.15:
                x,y = max_prob_of_bomb[1]
                action = 1
            if min_prob_of_bomb[0] < 0.15:
                x,y = min_prob_of_bomb[1]
                action = 0
        else: 
            left_cell_prob = [[prob_board[x][y],[x,y]] for x,y in choice_list]
            pick_in_this = [prob_cell[1] for prob_cell in left_cell_prob if prob_cell[0] == min(left_cell_prob)[0]]
            if len(pick_in_this):
                x,y = random.choice(pick_in_this)
            else:
                pass
        try:
            if len(choice_list):
                choice_list.remove([x,y])
        except:
            pass

        board, given_board, status, action = update_board(
            (x,y), 
            action, 
            user_id,
            timer
            )
        
        _board_info.true_board = board
        _board_info.to_give_board = given_board
        _board_info.cell_left  = len(choice_list)
        _board_info.prob_board = prob_board
        _board_info.status = status
        _board_info.save()

        return x, y, action, status, given_board 
    
    else:
        return -1,-1, -9999, _board_info.status, given_board

    
