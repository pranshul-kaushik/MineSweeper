import numpy as np
import random


class cell:
    def __init__(self, **kwargs):
        self.number = kwargs.get("number")
        self.adj = kwargs.get("adj")
        self.is_bomb = kwargs.get("is_bomb")
        self.pos= kwargs.get("pos")
        self.is_checked= False
        self.is_flaged =False
        
#Create the Board
def createBoard(num_row ,num_col):
    '''Number of bomb that is needed to be placed randomly'''
    number_bomb = int(0.15*(num_col*num_row))

    '''Create all the postion in a Cell *object*  with no adj and no bomb for now'''
    cell_list =[]
    for i in range(num_row):
        for j in range(num_col):
            cell_list.append(cell(number = 0 ,adj =None , is_bomb =None))
 
    '''Reshape it into num_row and num_col'''
    board =np.array(cell_list).reshape(num_row, num_col)
    
    '''Check bomb is for the number of bomb placed'''
    check_bombs=0

    def Cell(choice):
        return board[choice[0]][choice[1]]

    '''This is for filling the attributes of each Cell *object* '''
    for i in range(num_row):
        for j in range(num_col): 
            board[i][j].pos= (i,j)
            board[i][j].is_bomb = False
            board[i][j].adj ={
                "top_left": [i-1 ,j-1] if i>0 and j>0 else None,
                "top" : [i-1,j] if i>0 else None,
                "top_right": [i-1,j+1] if i>0 and j<num_col-1 else None,
                "left": [i,j-1] if j>0 else None,
                "right": [i,j+1] if j<num_col-1 else None,
                "bottom_left": [i+1,j-1] if i<num_row-1 and j>0 else None,
                "bottom": [i+1,j] if i<num_row-1 else None,
                "bottom_right": [i+1,j+1] if i<num_row-1 and j<num_col-1 else None
            }

    '''Now to fill randomly bombs equal to number_bomb'''        
    while check_bombs != number_bomb:

        '''Random choice'''
        x=random.randrange(0,num_row-1)
        y=random.randrange(0,num_col-1)

        '''For those random choice postion change the attribute of the 
        Cell (accessed by board[x][y]) *object* and increasing check bomb by 1'''
        #Only place the bomb on that postion
        #If there is no bomb on that place already 
        if board[x][y].is_bomb is False:
            board[x][y].number = -1
            board[x][y].is_bomb = True
            check_bombs+=1
            
            for i,j in board[x][y].adj.items():
                
                acceptable = True if j != None else False
                if acceptable:
                    j = Cell(j)
                
                '''If acceptable and there is no bomb in its adjecent'''
                if acceptable and Cell(board[x][y].adj[i]).is_bomb == False:

                    '''Increment the Cell's number by 1'''
                    Cell(board[x][y].adj[i]).number+=1   
    return board
