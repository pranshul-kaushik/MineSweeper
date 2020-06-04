import numpy as np
import random

adj= [(-1,-1),(-1,0),(-1,+1),(0,-1),(0,+1),(1,-1),(1,0),(1,1)]


def createBoard(num_row , num_col):

    number_bomb= int(0.15*(num_col*num_row))
    board= np.array([0]*num_row*num_col).reshape(num_row,num_col)
    check_bombs=0
    while check_bombs != number_bomb:
        i=random.randrange(0,num_row-1)
        j=random.randrange(0,num_col-1)
        if(board[i][j] != -1):
            board[i][j] = -1
            check_bombs+=1
            for x in adj:
                acceptable = i+x[0]!=-1 and i+x[0] != num_row and j+x[1]!= -1 and j+x[1]!= num_col
                if( board[i+x[0]][j+x[1]] != -1 and acceptable):
                    board[i+x[0]][j+x[1]]+=1   
    return board
