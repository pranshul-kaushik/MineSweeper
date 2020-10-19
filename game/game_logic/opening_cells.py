import numpy as np
import random
from .bring_board import createBoard
from game.models import board_info, user_info

def new_board(num_row, num_col, user_id):
    try:
        user = user_info.objects.get(user_id = user_id)
    except:
        user = user_info(
            user_id= user_id
        )
        user.save()

    # board = board_info.objects.filter()
    # if board.count():
    #     return board[0].to_give_board

    # else:
    board =createBoard(num_row,num_col)
    _to_give_board = np.array(['.']*num_row*num_col).reshape(num_row,num_col)
    _board_info = board_info(
        true_board = board,
        user_id= user,
        to_give_board = _to_give_board,
        cell_left = num_row*num_col,
        number_bombs = int(0.15*(num_row*num_col))
    )    

    _board_info.save()
    return _board_info.to_give_board
        
def update_board(choice ,action, user_id, time):
    _board_info = board_info.objects.filter(user_id__user_id = user_id).latest('id')
    _board_info.timer = time
    _board_info.save()
    
    board = _board_info.true_board
    given_board = _board_info.to_give_board
    number_bomb = _board_info.number_bombs
    cell_left  = _board_info.cell_left
    num_row = board.shape[0]
    num_col = board.shape[1]

    #print(given_board,'-'*20,'\n\n')

    def Given_board(choice):
        if Cell(choice).is_flaged == False:
            given_board[choice[0]][choice[1]] = Number(choice)
        if Cell(choice).is_flaged == True:
            given_board[choice[0]][choice[1]] = '#'


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
    
    def Press_land(cell, open_cell):
        if cell == None or cell.number != 0:
            return
        adj=list(cell.adj.values())
        
        for this_adj in adj:
            if this_adj != None:
                this_adj = Cell(this_adj)
            if this_adj != None and cell.number == 0 and this_adj.is_checked == False:
                this_adj.is_checked = True
                open_cell.append(cell.pos)
                Given_board(this_adj.pos)
                Press_land(this_adj, open_cell)
        cell.is_checked = True
        Given_board(cell.pos)
        return open_cell
    def Hide(choice):
        given_board[choice[0], choice[1]] = '.'

    if action == 1 and Cell(choice).is_flaged:
        action = -1

    if cell_left != 0:
        if action == -1:
            Cell(choice).is_flaged = False
            Is_checked(choice ,False)
            Hide(choice)
            cell_left+=1

        
        elif action == 1:
            Cell(choice).is_flaged = True
            Is_checked(choice ,True)
            Given_board(choice)
            cell_left-=1
        else:
            if Cell(choice).is_flaged != True:
                if Number(choice) == -1:
                    _to_give_board = np.array([
                        str(Number((i,j))) for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)
                    _board_info.true_board = board
                    _board_info.to_give_board = _to_give_board
                    _board_info.cell_left = num_row*num_col
                    _board_info.number_bombs = int(0.15*(num_row*num_col))
                    _board_info.save()              
                    return board,_to_give_board , -1
                else:
                    if Number(choice) != 0:
                        Is_checked(choice , True)
                        Given_board(choice)
                        cell_left-=1
                    else:
                        open_cell = []
                        cell_left -= len(Press_land(Cell(choice), open_cell))
        print(given_board, choice)

        _board_info.true_board = board
        _board_info.to_give_board = given_board
        _board_info.cell_left = cell_left
        _board_info.number_bombs = int(0.15*(num_row*num_col))
        _board_info.save() 

        if cell_left == 0:
            return board, given_board, 1
        else:
            return board, given_board, 0
    
    else:
        return board, given_board, 1
