
# def new_board(num_row, num_col):
#     board = board_info.objects.filter()
#     if board.count():
#         return board[0].to_give_board

#     else:
#         board =createBoard(num_row,num_col)
#         _to_give_board = np.array(['.']*num_row*num_col).reshape(num_row,num_col)
#         _board_info = board_info(
#             true_board = board,
#             to_give_board = _to_give_board,
#             cell_left = num_row*num_col,
#             number_bombs = int(0.15*(num_row*num_col))
#         )    

#         _board_info.save()
#         return _board_info.to_give_board


def update_board(choice ,action, num_row,num_col, board ,given_board, number_bomb, cell_left):
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
                    #changed for convinience
                    return board,given_board, -1
                else:
                    if Number(choice) != 0:
                        Is_checked(choice , True)
                        Given_board(choice)
                        cell_left-=1
                    else:
                        open_cell = []
                        cell_left -= len(Press_land(Cell(choice), open_cell))

        if cell_left == 0:
            return board,given_board, 1
        else:
            return board,given_board, 0
    
    else:
        return board,given_board, 1
