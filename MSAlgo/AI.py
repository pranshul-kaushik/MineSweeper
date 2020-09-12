import numpy as np
import random
from bring_board import createBoard
from opening_cells import update_board
import time
num_row, num_col = 29,17
board = createBoard(num_row, num_col)
given_board = np.array(["*" for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)
number_bomb = number_bomb = int(0.15*(num_col*num_row))
cell_left  = num_col * num_row
prob_board = np.array([0.0 for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)
#choice_list = [[i,j] for i in range(num_row) for j in range(num_col)]

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
    global prob_board
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
status = 0
while not status:
    #start = time.time()
    choice_list = [[i,j] for i in range(num_row) for j in range(num_col) if not board[i][j].is_checked]

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
    
    #print(prob_board)
    if max_prob_of_bomb[0] > 0.9 or min_prob_of_bomb[0] < 0.2:
        if max_prob_of_bomb[0] > 0.9:
            x,y = max_prob_of_bomb[1]
            action = 1
        if min_prob_of_bomb[0] < 0.2:
            x,y = min_prob_of_bomb[1]
            action = 0
    else:
        while True:
            print("a")
            x,y = random.choice(choice_list)
            if prob_board[x][y] == 0:
                break  
        x,y = random.choice(choice_list)
    try:
        if len(choice_list):
            choice_list.remove([x,y])
    except:
        pass
    #print(status)
    #print("\nmin prob :- ",min_prob_of_bomb, " max prob :- ", max_prob_of_bomb, " choice :-", (x,y))
    board, given_board, status = update_board((x,y), action, num_row,num_col, board,given_board,number_bomb,cell_left)
    prob_board = np.array([0.0 for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)
    print(given_board,"\n\n")
    #while master != "A":
    #    master = input()
    #end = time.time()
    #time_l.append(end - start)
    #print(int(max(time_l)* 1000))
#print("WON" if status == 1 else "LOST")
 
