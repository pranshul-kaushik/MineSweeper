import numpy as np
import random

bomb_pos= []
adj= [(-1,-1),(-1,0),(-1,+1),(0,-1),(0,+1),(1,-1),(1,0),(1,1)]
W_L= 1

def createBoard(num_row , num_col):
    number_bomb= int(0.1*(num_col*num_row))
    board= np.array([0]*num_row*num_col).reshape(num_row,num_col)
    check_bombs=0
    while check_bombs != number_bomb:
        i=random.randrange(0,num_row-1,2)
        j=random.randrange(0,num_col-1,2)
        if(board[i][j] != -1):
            board[i][j] = -1
            bomb_pos.append([(i,j)])
            check_bombs+=1
            for x in adj:
                acceptable = i+x[0]!=-1 and i+x[0] != num_row and j+x[1]!= -1 and j+x[1]!= num_col
                if( board[i+x[0]][j+x[1]] != -1 and acceptable):
                    board[i+x[0]][j+x[1]]+=1   
    return board

def logic(W_L):
    num_row =10
    num_col =10
    board = createBoard(num_row , num_col)

    click = None

    
    #not_checked_area = np.array([False]*num_row*num_col)
    backend_board = board.flatten()
    given_board = np.array([' ']*num_row*num_col).reshape(num_row,num_col)
    choice_list = []
    for p in range(0,num_row):
        for q in range(0, num_col):
            choice_list.append(str(p)+str(q))


    while len(choice_list) != 0:
        print(len(choice_list))
        choice= random.choice(choice_list)
        
        i=int(choice[0])
        j=int(choice[1])
        click = board[i][j]
        print(f"{click}  of {(i,j)}")
        
        """ When pressed a bomb """

        if click == -1:
           gameOver()
           W_L = 0
           return W_L
        else:
            given_board[i][j] = click






          








            #generated_values = pressLand(click)

            index = np.argwhere(choice_list == str(i)+str(j))
            choice_list=np.delete(choice_list , index)
            print(choice_list)
            masterKey= None
            print(given_board)
            while(masterKey != 'A'):
                masterKey= input()    

def pressLand(click):
    pass


def gameOver():
    print("program  ended")

#def youWin():
#    print("Program ended")

W_L= logic(W_L)
if(W_L == 0):
   print("LOST")
else:
   print("win")

