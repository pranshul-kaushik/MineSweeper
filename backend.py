import numpy as np
import random
from board import createBoard


W_L= 1
adj= [(-1,-1),(-1,0),(-1,+1),(0,-1),(0,+1),(1,-1),(1,0),(1,1)]
num_row = 17
num_col = 17
not_checked_area = np.array([False]*num_row*num_col).reshape(num_row,num_col)
board =createBoard(num_row, num_col)
choice_list =[]

def refresh(choice_list):
    to_check_choice_list =[(j,i) for j in range(not_checked_area.shape[1]) for i in range(not_checked_area.shape[0])]
    for i in to_check_choice_list:
        if not_checked_area[i[0]][i[1]] == False:
            choice_list.append([i[0], i[1]])
    return choice_list


def brain(choice_list):
    choice= random.choice(choice_list)
    i=int(choice[0])
    j=int(choice[1])
    left_click = board[i][j]
    choice_list =refresh([])
    return choice ,i, j,left_click ,choice_list



def userView(W_L,num_row,num_col):
    global choice_list
    left_click = None
    given_board = np.array(['.']*num_row*num_col).reshape(num_row,num_col)
    choice_list =[[p,q] for p in range(0,num_row) for q in range(0, num_col)]

    while len(choice_list) != 0:
        f=0

        choice ,i ,j ,left_click , choice_list=brain(choice_list)


        print(f"{left_click}  of {(i,j)}")

        """ When pressed a bomb """
        if left_click == -1:
           gameOver(given_board)
           W_L = 0
           return W_L
        else:
            if left_click != 0:
                not_checked_area[i][j] =True
                given_board[i][j] = left_click
            else:
                
                generated_values=[]
                pressLand(board ,i,j,num_row,num_col ,generated_values)
                generated_values_rem =len(generated_values)
                while(len(generated_values) != 0):
                    choice = generated_values[0]
                    i =choice[0]
                    j= choice[1]
                    given_board[i,j]= board[i,j]
                    generated_values = generated_values [1:]
        choice_list =refresh([])
        print(len(choice_list))

        masterKey= None
        print(given_board)
        while(masterKey != 'A'):
            masterKey= input()    
        


def pressLand(board,i,j,num_row,num_col ,generated_values):
    
    f=0
    if i<0 or i>= num_row or j<0 or j>= num_col or not_checked_area[i][j] or board[i][j] != 0:
        return 
    if i-1 >= 0 and j-1 >= 0 and board[i-1][j-1] == 0 :
        f+=1
    if i-1 >= 0 and board[i-1][j] == 0 :
        f+=1
    if i-1 >= 0 and j+1 <num_col and board[i-1][j+1] == 0 :
        f+=1    
    if  j-1 >= 0 and board[i][j-1] == 0 :
        f+=1
    if  j+1 < num_col and board[i][j+1] == 0 :
        f+=1
    if  j-1 >= 0 and i+1 < num_row and board[i+1][j-1] == 0 :
        f+=1
    if  i+1 < num_row and board[i+1][j] == 0 :
        f+=1   
    if  i+1 < num_row and j+1 < num_col and board[i+1][j+1] == 0:
        f+=1
    if f == 0:
        return   
    if i-1 >= 0 and j-1 >= 0 and board[i-1][j-1] != 0 and not_checked_area[i-1][j-1] == False:
        generated_values.append([i-1,j-1])    
        not_checked_area[i-1][j-1] = True
    if i-1 >= 0 and  board[i-1][j] != 0 and not_checked_area[i-1][j] == False:
        generated_values.append([i-1,j])    
        not_checked_area[i-1][j] = True
    if i-1 >= 0 and j+1 <num_col and board[i-1][j+1] != 0 and not_checked_area[i-1][j+1] == False:
        generated_values.append([i-1,j+1])    
        not_checked_area[i-1][j+1] = True
    if j-1 >= 0 and board[i][j-1] != 0 and not_checked_area[i][j-1] == False:
        generated_values.append([i,j-1])    
        not_checked_area[i][j-1] = True
    if j+1 < num_col and board[i][j+1] != 0 and not_checked_area[i][j+1] == False:
        generated_values.append([i,j+1])    
        not_checked_area[i][j+1] = True
    if j-1 >= 0 and i+1 < num_row and board[i+1][j-1] != 0 and not_checked_area[i+1][j-1] == False:
        generated_values.append([i+1,j-1])    
        not_checked_area[i+1][j-1] = True
    if i+1 < num_row and board[i+1][j] != 0 and not_checked_area[i+1][j] == False:
        generated_values.append([i+1,j])    
        not_checked_area[i+1][j] = True
    if i+1 < num_row and j+1 < num_col and board[i+1][j+1] != 0 and not_checked_area[i+1][j+1] == False:
        generated_values.append([i+1,j+1])    
        not_checked_area[i+1][j+1] = True
    generated_values.append([i,j])
    not_checked_area[i][j] = True
    
    pressLand(board , i+1,j,num_row,num_col,generated_values)    
    pressLand(board , i-1,j,num_row,num_col,generated_values)
    pressLand(board , i,j+1,num_row,num_col,generated_values)
    pressLand(board , i,j-1,num_row,num_col,generated_values)

def gameOver(given_board):
    for i in range(given_board.shape[0]): 
        for j in range(given_board.shape[1]): 
            given_board[i][j] =str(board[i][j])

    print(given_board)
    to_exit =None
    while(to_exit == None):
        to_exit =input()         
    print("program  ended")

   
W_L= userView(W_L,num_row,num_col)
if(W_L == 0):
   print("LOST")      
else:
   print("win")