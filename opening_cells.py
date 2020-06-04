import numpy as np
import random
from bring_board import createBoard

#Gives the choice and if it want to flag or not ; 
#Takes input as choice list 'what are the choices' and ;
#Flaged list 'flagged cells'
   
def brain(choice_list , flaged_list ,number_bomb):
    '''This is a random working brain ; like a person who do not know how MS works'''
    if len(flaged_list) < number_bomb and len(flaged_list) != 0:
        
        '''remove flag (right click)= -1'''
        '''left click = 0'''
        '''add flag (right click) = 1'''
        want_to_flag =random.choice([-1,0,1])
    
    elif len(flaged_list) < number_bomb:
        want_to_flag =random.choice([0,1])
    else:
        want_to_flag = 0
        
    if want_to_flag == -1:
        choice = random.choice(flaged_list)
    else:        
        choice= random.choice(choice_list)

    '''Returns the choice's *position* and what it want to do with it'''    
    return choice ,want_to_flag
        


def createGame(num_row, num_col):
    print('To see the next step --> A')
    print('To see the complete board for yourself --> Z\n\n\n')
    
    '''Build the board of particular number of raws and columns'''
    board= createBoard(num_row , num_col)

    '''Build an array and hide all the cells by '.' '''
    given_board = np.array(['.']*num_row*num_col).reshape(num_row,num_col)

    #Function is for 
    #Printing tne Given Board or 
    #Reveal the particular cell or
    #Flag the cell '#'
    def Given_board(choice = None):
        if choice != None and Cell(choice).is_flaged == False:
            given_board[choice[0]][choice[1]] = Number(choice)
        elif choice != None and Cell(choice).is_flaged == True:
            given_board[choice[0]][choice[1]] = '#'
        else:
            print(given_board)

    #Rturns the Number of that cell
    def Number (choice):
        return board[choice[0], choice[1]].number

    #Function is for
    #Return the cell's checked status or
    #Update the cell's checked statue
    def Is_checked (choice, put =None):
        
        '''If put is not None then it must be that 
        we need to Put something on cell having postion *choice*'''
        if put != None:
            board[choice[0], choice[1]].is_checked = put
        
        else:
            return board[choice[0], choice[1]].is_checked

    #Return all Adjacent of the cell *it is in the form of Dictionary* 
    def Adj(choice):
        return board[choice[0], choice[1]].adj

    #Return  the cell *object* by the help of Position
    def Cell(choice):
        return board[choice[0], choice[1]]

    #It Refresh the Choice List and Flaged list after every event
    def Refresh():
        new_choice_list= []
        new_flaged_list= []
        for i in board:
            for j in i:
                if j.is_checked == False:
                    '''If cell is not checked then append the cell position to choice list'''
                    new_choice_list.append(j.pos)
                else:
                    '''Check the cell of being Flaged '''
                    if j.is_flaged == True:
                        '''If cell is flaged then append the cell position to flaged list '''
                        new_flaged_list.append(j.pos)
                    
                    '''Update the given board'''
                    Given_board(j.pos)
        
        '''Return the refreshed choice list and flaged list'''
        return new_choice_list, new_flaged_list

    #Function is for Revealing all the cells number
    def Reveal_all():
        true_board =[]
        for i in board:
            for j in i:

                '''-1 is converted to '-' for visual convenience'''
                true_board.append(str(j.number) if j.number != -1 else '-')
        
        '''Ruturn the True board'''
        return np.array(true_board).reshape(num_row,num_col)        
    
    #Function is based on FillFlood Algo
    #It is for if the choice is having cell number 0
    #Then we have to reveal a whole chunk of cells
    #Take input a Cell *object* not its position 
    def Press_land(cell):
        '''Base case is the if the cell is not 0 or out of bound return'''
        if cell == None or cell.number != 0:
            return
        '''Take all the Adjecent and convert *dictionary* --> *List*'''    
        adj=list(cell.adj.values())
        
        '''Iterate over all cell's adjecent cells *object* '''
        for this_adj in adj:

            '''If adjecent cells *object* is not out of bound and cell's number is 0
            and is not checked then -->
            Check it and move to that Cell *object* by Recuression'''
            if this_adj != None and cell.number == 0 and this_adj.is_checked == False:
                this_adj.is_checked = True
                Press_land(this_adj)

        '''Check the Cell *object* where the control is'''        
        cell.is_checked = True
    
    #To hide the Flag '#' --> '.' when it removes the Flag
    def Hide(choice):
        given_board[choice[0], choice[1]] = '.'

    '''Create the Given board ,Choice list ,flaged list 
    and number of bomb there is in the board'''
    given_board = np.array(['.']*num_row*num_col).reshape(num_row,num_col)
    choice_list =[[p,q] for p in range(0,num_row) for q in range(0, num_col)]
    flaged_list =[]
    number_bomb = int(0.15*(num_col*num_row))

    
    #Main Program of Opening cells 
    #We need to loop till either you lose or the Choice is empty in that case it won
    while len(choice_list) != 0:
        '''Take the choice and what is want to do with that choice from brain'''
        choice ,want_to_flag=brain(choice_list ,flaged_list ,number_bomb)    
        
        print(f'cell having number {Number(choice)}')
        print(f'cell at postion {Cell(choice).pos}')
        print(f'want to {want_to_flag}')
        
        
        if want_to_flag == -1:
            '''Right Click'''
            Cell(choice).is_flaged = False
            Is_checked(choice ,False)
            Hide(choice)

        
        elif want_to_flag == 1:
            '''Right Click'''
            Cell(choice).is_flaged = True
            Is_checked(choice ,True)
            Given_board(choice)
        else:
            '''Left Click'''
            '''If Clicked Bomb'''
            if Number(choice) == -1:
                print(Reveal_all())
                '''This is just to watch the miskates'''

                masterKey= None
                while(masterKey != 'A'):
                    masterKey= input()  

                return "U LOST!! YOU DUMB RND BOT"
            else:
                '''If not a 0'''
                if Number(choice) != 0:
                
                    Is_checked(choice , True)
                    Given_board(choice)
                
                else:
                    '''If a 0'''
                    Press_land(Cell(choice))
        choice_list, flaged_list= Refresh()
        
        '''A trap that is just to watch the program to run'''
        masterKey= None
        print()
        Given_board()
        while(masterKey != 'A'):
            masterKey= input()  
            if masterKey == 'Z':
                print(Reveal_all())

createGame(17,17)

