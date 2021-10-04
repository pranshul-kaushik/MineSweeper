import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from bring_board import createBoard
from opening_cells import update_board
import time
import os
import warnings
from enum import Enum

warnings.filterwarnings("ignore")

from scipy.interpolate.rbf import Rbf
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

class kernel(str, Enum):
    inverse = "inverse"
    gaussian = 'gaussian'
    multiquadric = 'multiquadric'

def Number(board, choice):
    return board[choice[0]][choice[1]].number

def Is_checked(board, choice, put =None):
    
    if put != None:
        board[choice[0]][choice[1]].is_checked = put
    
    else:
        return board[choice[0]][choice[1]].is_checked

def Adj(board, choice):
    return board[choice[0]][choice[1]].adj

def Cell(board, choice):
    return board[choice[0]][choice[1]]

def prob_of_bomb_in_area(board, prob_board, cell):
    bomb_left_to_mark = cell.number
    number_of_places_bomb_can_be = 0
    for each_adj in cell.adj.values():
        if each_adj and Cell(board, each_adj).is_flaged:
            bomb_left_to_mark -= 1
        if each_adj and not Cell(board, each_adj).is_checked:
            number_of_places_bomb_can_be += 1
    if bomb_left_to_mark != 0:
        prob = combination(number_of_places_bomb_can_be -1 , bomb_left_to_mark -1) / \
            combination(number_of_places_bomb_can_be, bomb_left_to_mark)
    else:
        prob = 0.00001
           
    for each_adj in cell.adj.values():
        if each_adj and not Cell(board, each_adj).is_checked:
            position = Cell(board, each_adj).pos
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

def new_solver(board, num_row, num_col, alpha, kernel):
    given_board = np.array(["*" for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)
    number_bomb = number_bomb = int(0.15*(num_col*num_row))
    cell_left  = num_col * num_row
    prob_board = np.array([0.0 for i in range(num_row) for j in range(num_col)
                    ]).reshape(num_row, num_col)

    status = 0
    df = pd.DataFrame()
    
    def safe(x,y):
        return x == 0 or y == 0 or x == num_row-1 or y == num_col-1
    
    while not status:
        action_type = "random"
        choice_list = [[i,j] for i in range(num_row) for j in range(num_col) if not board[i][j].is_checked]
        opened_list = [[i,j] for i in range(num_row) for j in range(num_col) if board[i][j].is_checked]
        cell_left = len(choice_list)
        action = 0
        for i in range(num_row):
            for j in range(num_col):
                if board[i][j].is_checked and not board[i][j].is_flaged:
                    total_number_of_adj_checked=0
                    total_number_of_adj_none=0
                    for each_adj in board[i][j].adj.values():
                        try:
                            total_number_of_adj_checked += int(Cell(board, each_adj).is_checked)
                        except:
                            total_number_of_adj_none += 1
                    if (8 - total_number_of_adj_none - total_number_of_adj_checked) > 0:
                        prob_of_bomb_in_area(board, prob_board, board[i][j])

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
                    for each_adj in Cell(board, [i,j]).adj.values():
                        try:
                            total_number_of_adj_checked += int(Cell(board, each_adj).is_checked)
                            total_number_of_adj_flag += int(Cell(board, each_adj).is_flaged)
                        except:
                            continue

                    if total_number_of_adj_checked - total_number_of_adj_flag > 0:
                        if prob_board[i][j] < min_prob_of_bomb[0]:
                            min_prob_of_bomb[0] = prob_board[i][j]
                            min_prob_of_bomb[1] = [i,j]

        if max_prob_of_bomb[0] > 1 - alpha or min_prob_of_bomb[0] < alpha:
            action_type = "probability"
            if max_prob_of_bomb[0] > 1 - alpha:
                x,y = max_prob_of_bomb[1]
                action = 1
            if min_prob_of_bomb[0] < alpha:
                x,y = min_prob_of_bomb[1]
                action = 0
        else:
            action_type = "random"
            if opened_list:
                x ,y = list(zip(*opened_list))
                z = [1]*len(x)
                rbf_adj = Rbf(x, y, z, function=kernel, epsilon = 0.03 * num_row * num_col)
                x_fine, y_fine = list(zip(*[[i,j] for i in range(num_row) for j in range(num_col)]))
                x_grid, y_grid = np.meshgrid(x_fine, y_fine)
                weight = 1 - rbf_adj(x_grid.ravel(), y_grid.ravel()).reshape(x_grid.shape)
            
                left_cell_prob = [[prob_board[x][y],[x,y]] for x,y in choice_list]
                pick_in_this = [prob_cell[1] for prob_cell in left_cell_prob if prob_cell[0] == min(left_cell_prob)[0]]
                left_weights = [weight[x][y] for x,y in pick_in_this]
                #random.shuffle(pick_in_this)
                x,y =pick_in_this[len(left_weights)-1-left_weights[::-1].index(max(left_weights))]
                #x,y = random.choices(pick_in_this, weights = left_weights)[0]
                
            else:
                left_cell_prob = [[prob_board[x][y],[x,y]] for x,y in choice_list if safe(x,y)]
                pick_in_this = [prob_cell[1] for prob_cell in left_cell_prob if prob_cell[0] == min(left_cell_prob)[0]]
                random.shuffle(pick_in_this)
                x,y = random.choices(pick_in_this)[0]
        try:
            if len(choice_list):
                choice_list.remove([x,y])
        except:
            pass
        
        board, given_board, status = update_board((x,y), action, num_row,num_col, board,given_board,number_bomb,cell_left)
        prob_board = np.array([0.0 for i in range(num_row) for j in range(num_col)
                        ]).reshape(num_row, num_col)
        if status == 0:
            print("\n\n", given_board)
        elif status == 1:
            print("\n\n", given_board)        
        else:
            print("\n\n", given_board)     

        data = {
            "action_type": [action_type],
            "action" : [action]
        }
        df = pd.concat([df, pd.DataFrame(data)])   

    #return df, {"action_type": [action_type],"status": [status], "clicks": [num_row*num_col-len(choice_list)]}, given_board
    return df, {"action_type": action_type,"status": status}

def check_threshold(threshold):
    if threshold < 0.0 or threshold > 0.5:
        console.print(f"Threshold is the cutoff value to classify a mine. It has to be within 0.0 to 0.5 not {threshold}", style= 'red')
        raise typer.Exit(code= 1)
    return threshold

@app.command()
def main(num_row: int = typer.Option(15, help = "Number of Rows"), 
         num_col: int = typer.Option(15, help = "Number of Columns"),
         threshold: float = typer.Option(0.1, 
                                         callback= check_threshold,
                                         help = "Threshold is the cutoff value to classify a mine. It has to be within 0.0 to 0.5"),
         kernel : kernel = kernel.inverse):
    board = createBoard(num_row, num_col)
    df, status = new_solver(board, num_row, num_col, threshold, kernel = kernel.value)
    df.action = df.action.replace({0: "left", 1: "right"})
    ct = pd.crosstab(df.action_type, df.action)
    print(ct,"\n", status)
    stacked = ct.stack().reset_index().rename(columns={0:'value'})
    sns.barplot(x=stacked.action_type, y=stacked.value, hue=stacked.action)
    plt.title("Lost" if status["status"] == -1 else "Win")
    plt.show()
    os. system("pause")

if __name__ == "__main__":
    console.print(
        """
Each symbol has a meaning  discribed below


* -> Uncovered Cell

(0 - 8) -> Number of the Cell

# -> Flag
        """,
        style= "bold green"
    )
    sure = typer.confirm("Shall will start?")    
    if sure:
        app()
    else:
        console.print("Cool", style= "bold red")
    
