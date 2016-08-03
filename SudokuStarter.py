# Sebastian Rodriguez, Haley De Boom, Ben Sandeen,

#!/usr/bin/env python
import struct, string, math
import time
from copy import deepcopy
from functools import partial
from operator import ne
from math import sqrt as square_root
from multiprocessing import *

poss_vals = {} # global dict to store the legal moves for each square
constrainedness = {}
counter = 0

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added

        # print("set_value's return val:", SudokuBoard(self.BoardSize, self.CurrentGameBoard))
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)   

    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    # subsquare = int(square_root(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in xrange(size):
        for col in xrange(size):
            if BoardArray[row][col]==0:
                return False
            for i in xrange(size):
                if BoardArray[row][i] == BoardArray[row][col]:
                    if i != col:
                        return False
                elif BoardArray[i][col] == BoardArray[row][col]:
                    if i != row:
                        return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in xrange(subsquare):
                if (SquareRow*subsquare + i != row):
                    for j in xrange(subsquare):
                        if (SquareCol*subsquare + j != col):
                            if ((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])):
                                return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def is_legit(sudoku_board,roww, column, num):
    """Function to evaluate moves to see if they're valid (ie: not illegal).
       Returns True if valid, otherwise False"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    # subsquare = int(square_root(size))
    SquareRow = roww // subsquare
    SquareCol = column // subsquare
    # global counter
    # counter += 1

    # if any rows or columns have num, we can't put num in current square
    if num in BoardArray[roww]:  
        return False
    for roww in xrange(size):
        if num == BoardArray[roww][column]:
            return False

    # if any subsquare has num, we can't put num in current square
    for r in xrange(size):
        if (r//subsquare==SquareRow):
            for c in xrange(size):
                if (c//subsquare==SquareCol):
                    if BoardArray[r][c] == num:
                        return False
    return True # otherwise, we can play num

def constrained(sudoku_board,roww, column):
    """Function to evaluate moves to see if they're valid (ie: not illegal).
       Returns True if valid, otherwise False"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = roww // subsquare
    SquareCol = column // subsquare
    constrainment = 0 # counter to keep track of how constrained current square is

    for row in xrange(size):        
        if (row//subsquare==SquareRow):
            for c in xrange(size):
                if (c//subsquare==SquareCol):
                    if BoardArray[row][c] == 0: # looks through subsquare
                        constrainment += 1 # constrains current square if empty...
                    else:
                        constrainment -= 1 # ...but not if it has value
                else:
                    if row != roww:
                        if BoardArray[row][c] == 0: # looks through
                            constrainment += 1 # constrains current square if empty...
                        else:
                            constrainment -= 1 # ...but not if it has value
        else:
            for c in xrange(size):
                if (c//subsquare!=SquareCol):
                    if BoardArray[row][c] == 0: # looks through subsquare
                        constrainment += 1 # constrains current square if empty...
                    else:
                        constrainment -= 1 # ...but not if it has value
    return constrainment

def MCV_and_LCV(initial_board,order=1):
    """Finds square with most unassigned squares that it is affected by, and tries
       to assign a value to it"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    global poss_vals # gets global dict of possible values for each square
    global constrainedness # gets global dict of how constrained each square is
    global counter

    if is_complete(initial_board): # return board if it's been finished properly
        return initial_board

    # select next square to play in by looping through dict of constrainedness
    # by most-constrained first
    if order == 0:
        for key, value in reversed(sorted(constrainedness.iteritems(), key=lambda (k,v): (v,k))):
            row = key[0] # get row from key
            col = key[1] # get col from key
            if BoardArray[row][col] == 0:# if valid number can be put in square
                counter+=1
                lcv_rank = []
                for n in xrange(1,size+1): # loop through all numbers
                    if n in poss_vals[row,col]: # if it's playable
                        # calculate the amount of possible moves for every legal value
                        initial_board = initial_board.set_value(row, col, n) # set number for square
                        # make copy of current poss_vals in case we need to backtrack
                        last_poss_vals = dict(poss_vals)
                        # since we're setting value, we need to update poss_vals to reflect it
                        poss_vals[row, col] = [n]
                        valid = validator(initial_board) # see if attempted move is legal
                        # poss_moves = sum(len(v) for v in poss_vals.itervalues())
                        lcv_rank.append((n, sum(len(v) for v in poss_vals.itervalues())))
                        poss_vals = last_poss_vals
                        initial_board = initial_board.set_value(row, col, 0)

                # sort the list of lcvs, least first
                lcv_rank.sort(key=lambda x: x[1])
                # enter value and go recursive
                for n, v in lcv_rank:
                    initial_board = initial_board.set_value(row, col, n)
                    last_poss_vals = dict(poss_vals)
                    poss_vals[row, col] = [n]
                    valid = validator(initial_board)
                    if valid:
                        newBoard = LCV(initial_board)
                        if newBoard != False:
                            return newBoard
                    poss_vals = last_poss_vals
                    initial_board = initial_board.set_value(row, col, 0)
                else:
                    return False
    else:
        for key,value in (sorted(constrainedness.iteritems(), key=lambda (k,v): (v,k))):
            row = key[0] # get row from key
            col = key[1] # get col from key
            if BoardArray[row][col] == 0:# if valid number can be put in square
                counter+=1
                lcv_rank = []
                for n in xrange(1,size+1): # loop through all numbers
                    if n in poss_vals[row,col]: # if it's playable
                        # calculate the amount of possible moves for every legal value
                        initial_board = initial_board.set_value(row, col, n) # set number for square
                        # make copy of current poss_vals in case we need to backtrack
                        last_poss_vals = dict(poss_vals)
                        # since we're setting value, we need to update poss_vals to reflect it
                        poss_vals[row, col] = [n]
                        valid = validator(initial_board) # see if attempted move is legal
                        # poss_moves = sum(len(v) for v in poss_vals.itervalues())
                        lcv_rank.append((n, sum(len(v) for v in poss_vals.itervalues())))
                        poss_vals = last_poss_vals
                        initial_board = initial_board.set_value(row, col, 0)

                # sort the list of lcvs, least first
                lcv_rank.sort(key=lambda x: x[1])
                # enter value and go recursive
                for n, v in lcv_rank:
                    initial_board = initial_board.set_value(row, col, n)
                    last_poss_vals = dict(poss_vals)
                    poss_vals[row, col] = [n]
                    valid = validator(initial_board)
                    if valid:
                        newBoard = LCV(initial_board)
                        if newBoard != False:
                            return newBoard
                    poss_vals = last_poss_vals
                    initial_board = initial_board.set_value(row, col, 0)
                else:
                    return False



def MRV_and_LCV(initial_board):
    """Same as FC, except now it chooses square with fewest legal values to play next"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals
    global counter
    len_poss_vals = {}

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for key in poss_vals.keys():
            len_poss_vals[key] = len(poss_vals[key])
        for key, value in sorted(len_poss_vals.iteritems(), key=lambda (k,v): (v,k)):
            row = key[0]
            col = key[1]
            if BoardArray[row][col] == 0:
                counter+=1
                # if valid number can be put in square
                lcv_rank = []
                for n in xrange(1,size+1):
                    if n in poss_vals[row,col]:
                        # calculate the amount of possible moves for every legal value
                        initial_board = initial_board.set_value(row, col, n)
                        last_poss_vals = dict(poss_vals)
                        poss_vals[row, col] = [n]
                        valid = validator(initial_board)
                        # poss_moves = sum(len(v) for v in poss_vals.itervalues())
                        # keep track of how many squares each number constrains
                        lcv_rank.append((n, sum(len(v) for v in poss_vals.itervalues())))
                        # restore dict of poss_vals to loop through rest of numbers
                        poss_vals = last_poss_vals
                        # restore board to loop through rest of numbers
                        initial_board = initial_board.set_value(row, col, 0)

                # sort the list of lcvs, least first
                lcv_rank.sort(key=lambda x: x[1])
                # enter value and go recursive
                for n, v in lcv_rank:
                    initial_board = initial_board.set_value(row, col, n)
                    last_poss_vals = dict(poss_vals)
                    poss_vals[row, col] = [n]
                    valid = validator(initial_board)
                    if valid:
                        newBoard = LCV(initial_board)
                        if newBoard != False:
                            return newBoard
                    poss_vals = last_poss_vals
                    initial_board = initial_board.set_value(row, col, 0)
                else:
                    return False

def MRV(initial_board):
    """Same as FC, except now it chooses square with fewest legal values to play next"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals
    global counter
    len_poss_vals = {}

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for key in poss_vals.keys():
            len_poss_vals[key] = len(poss_vals[key])
        for key, value in sorted(len_poss_vals.iteritems(), key=lambda (k,v): (v,k)):
            row = key[0]
            col = key[1]
            if BoardArray[row][col] == 0:
                counter+=1
                # if valid number can be put in square
                for n in xrange(1,size+1):
                    # if is_legit(initial_board,row,col,n):
                    if n in poss_vals[row,col]:
                        initial_board=initial_board.set_value(row,col,n)
                        # last_poss_vals = deepCopyDict(poss_vals) #deepcopy(poss_vals)
                        last_poss_vals = dict(poss_vals)
                        poss_vals[row,col] = [n]
                        # poss_vals, valid = validator(initial_board)
                        valid = validator(initial_board)
                        # if valid: # if move creates no squares with invalid moves
                        newBoard = MRV(initial_board)
                        if newBoard != False:
                            return newBoard
                        poss_vals = last_poss_vals
                        initial_board=initial_board.set_value(row,col,0)
                else:
                    return False
        
def MCV(initial_board):
    """Finds square with most unassigned squares that it is affected by, and tries
       to assign a value to it"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    global poss_vals
    global constrainedness
    global counter

    if is_complete(initial_board):
        return initial_board
    # select next square to play in
    for key, value in reversed(sorted(constrainedness.iteritems(), key=lambda (k,v): (v,k))):
        row = key[0]
        col = key[1]
        if BoardArray[row][col] == 0:
            counter+=1
            # if valid number can be put in square
            for n in xrange(1,size+1):
                # if is_legit(initial_board,row,col,n):
                if n in poss_vals[row,col]:
                    initial_board=initial_board.set_value(row,col,n)
                    # last_poss_vals = deepcopy(poss_vals)
                    last_poss_vals = dict(poss_vals)
                    poss_vals[row,col] = [n]
                    # poss_vals, valid = validator(initial_board)
                    valid = validator(initial_board)
                    if valid: # if move creates no squares with invalid moves
                        constrainedness[row,col] = constrained(initial_board,row,col)
                        newBoard = MCV(initial_board)
                        if newBoard != False:
                            return newBoard
                    poss_vals = last_poss_vals
                    initial_board=initial_board.set_value(row,col,0)
            else:
                return False

def LCV(initial_board):
    """LCV function to look through the current board to see how the placement of
       a given value will constrain other squares, and returns the one that 
       constrains others the least"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals
    global counter

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
                    counter+=1
                    # if valid number can be put in square
                    for n in xrange(1,size+1):
                        # if is_legit(initial_board,row,col,n):
                        if n in poss_vals[row,col]:
                            initial_board=initial_board.set_value(row,col,n)
                            # last_poss_vals = deepcopy(poss_vals)
                            last_poss_vals = dict(poss_vals)
                            poss_vals[row,col] = [n]
                            # poss_vals, valid = validator(initial_board)
                            valid = validator(initial_board)
                            # if valid: # if move creates no squares with invalid moves
                            newBoard = LCV(initial_board)
                            if newBoard != False:
                                return newBoard
                            poss_vals = last_poss_vals
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def FC(initial_board):
    """Does the forward checking by updating the possible values remaining
       for each square and backtracking immediately when any square has no
       remaining possible values"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    # global var implicitly passes dict of poss_vals, rather than explicitly,
    # which is probably less efficient
    global poss_vals
    global counter

    if is_complete(initial_board): # if board is done, return it
        return initial_board
    else: # otherwise, pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
                    counter+=1
                    # if valid number can be put in square
                    for n in xrange(1,size+1):
                        # if is_legit(initial_board,row,col,n):
                        if n in poss_vals[row,col]:
                            initial_board=initial_board.set_value(row,col,n)
                            # last_poss_vals = deepcopy(poss_vals)
                            last_poss_vals = dict(poss_vals)
                            poss_vals[row,col] = [n]
                            # poss_vals, valid = validator(initial_board)
                            valid = validator(initial_board)#,row,col)
                            if valid: # if move creates no squares with invalid moves
                                newBoard = FC(initial_board)
                                if newBoard != False:
                                    return newBoard
                            poss_vals = last_poss_vals
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def validator(board):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals

    # this happens after we assign a square a val to ensure that it didn't remove the last 
    # possible value from any square still unassigned
    if is_complete(board):
        # return poss_vals,True
        return True
    for r in xrange(size):
        for c in xrange(size):
            if BoardArray[r][c] == 0: # if the square's val == 0
                if len(poss_vals[r,c]) == 0:
                    # return poss_vals,False
                    return False
                valids = []
                validAppender = valids.append # localizes append() so it's faster    
                # valids = filter(partial(ne, True), valids)
                # valids = [i for i in xrange(len(valids)) if bool(valids[i])] #!= valids[i]] 
                for x in poss_vals[r,c]:
                    if is_legit(board,r,c,x):
                        validAppender(x)
                poss_vals[r,c] = valids
    # return poss_vals,True
    return True

#################################################################################

def Solver(initial_board):#,poss_vals):
    """Solves with only backtracking"""

    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global counter

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if not BoardArray[row][col]:
                    counter+=1
                    # if valid number can be put in square
                    for n in xrange(1,size+1):
                        if is_legit(initial_board,row,col,n):
                            initial_board=initial_board.set_value(row,col,n)
                            newBoard = Solver(initial_board)#,poss_vals)
                            if newBoard != False:
                                return newBoard
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False


# def solve(initial_board,forward_checking=False,mrv=False,mcv=False,lcv=False,order):
def solve(initial_board,forward_checking=False,mrv=False,mcv=False,lcv=False,order=0):
    """Takes an initial SudokuBoard and calls the appropriate helper functions to 
    solve the board using back tracking and the specified heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    # passes backtracking function an empty dict and the CSPs
    row = 0
    col = 0

    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    global poss_vals
    global counter
    counter = 0

    # initializes a dict of each square's possible values
    for row in xrange(size):
        for col in xrange(size):
            poss_vals[row,col] = []
            for n in xrange(1,size+1):
                # put the appropriate values in the square.  If the square has a
                # number already, also include that
                if is_legit(initial_board,row,col,n) or BoardArray[row][col] == n:
                    poss_vals[row,col].append(n)


    # initializes a dict to count number of squares which constrain
    # each square are unassigned
    for row in xrange(size):
        for col in xrange(size):
            constrainedness[row,col] = constrained(initial_board,row,col)
                #or jump out of nested for loops
    
    if mrv & mcv: # if user gives conflicting inputs, use mrv (since it's better)
        mcv = 0
    # creates a binary out of the the values of the constraints, each constraint
    # represented by a single bit.  FC is the leftmost bit (highest value), LCV is rightmost
    constraint_mask = int(0b1111 & ((forward_checking<<3)|(mrv<<2)|(mcv<<1)|(lcv)))

    # dict (essentially a switch table) for choosing what methods to use based on what
    # the calling function requests, with the last 5 five items implicitly using FC
    switch = {}
    switch[0] = Solver
    switch[1] = LCV # these ignore the user's incorrect inputs and use FC anyways...
    switch[2] = MCV # ...since FC is necessary for them to work
    switch[3] = MCV_and_LCV
    switch[4] = MRV
    switch[5] = MRV_and_LCV
    switch[8] = FC
    switch[9] = LCV # all these are above FC because they require FC to run
    switch[10] = MCV
    switch[11] = MCV_and_LCV
    switch[12] = MRV
    switch[13] = MRV_and_LCV

    # print('constraint_mask: ',constraint_mask)
    print((switch[constraint_mask]))
    result = switch[(constraint_mask)](initial_board)#,{})
    # result = switch[(constraint_mask)](initial_board,order)
    # if __name__ == '__main__':
    #     # pool = Pool(processes=4)              # start 4 worker processes
    #     # second_results = pool.map(f, xrange(1,1000000))
    #     # second_results = Pool(processes=2).map(MCV, range(1,10000000))
    #     p = []
    #     print(cpu_count())
    #     # for i in xrange()

    # # return second_results
    return result

def get_next_move(sudoku_board, row, col, value):
    """Returns all the possible moves of the board in a list."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for row in xrange(size):
        for col in xrange(size):
            for val in xrange(size):
                # if sudoku_board.is_legit(row, col, value):
                if is_legit(sudoku_board, row, col, value):
                    return sudoku_board.set_value(row, col, value), row, col, val
    return False;

# execfile("SudokuStarter.py")
totalTime = time.clock()

sb = init_board("input_puzzles/easy/4_4.sudoku")
sb.print_board()
sb = solve(sb, False, False, True, True)
sb.print_board()

t0 = time.clock()
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()
sb = solve(sb, True, False, True,True)
sb.print_board()
print time.clock() - t0

with open("consistency_check.txt", 'a') as outfile:
    for i in xrange(1,21):

        #####################################
        # The following is an attempt to parallelize this program.  It doesn't work
        # yet because the program relies on global variables, which causes conflicts
        #

        # if __name__ == '__main__':
        #     t0 = time.clock()
        #     boards = [init_board("input_puzzles/more/9x9/9x9.%s.sudoku" %str(i)) for a in xrange(cpu_count())]
        #     p = []
        #     for i in xrange(cpu_count()):
        #         boards[i].print_board()
        #         p.append(Process(target=solve, args=(boards[i],True,False,True,True,i)))

        #     for i in p:
        #         i.start()
        #     for i in p:
        #         i.join()    
        #####################################


        sb = init_board("input_puzzles/more/9x9/9x9.%s.sudoku" %str(i))
        sb.print_board()
        # sb = solve(sb, True, True,True,True)
        sb = solve(sb, True, False,True,True,0)
        sb.print_board()
        t0 = time.clock()
        # sb1 = init_board("input_puzzles/more/9x9/9x9.%s.sudoku" %str(i))
        # sb1.print_board()
        # # sb1 = solve(sb1, True, True,True,True)
        # sb1 = solve(sb1, True, False,True,True,1)
        # sb1.print_board()
        print('counter: ',counter)
        outfile.write("9x9 #%s took this many checks: "%str(i)+str(counter)+'\n')
        print time.clock() - t0

    for i in xrange(1,21):
        t0 = time.clock()
        sb = init_board("input_puzzles/more/16x16/16x16.%s.sudoku" %str(i))
        sb.print_board()
        sb = solve(sb, True, False, True, True)
        sb.print_board()
        print('counter: ',counter)
        print time.clock() - t0

    # sb = init_board("input_puzzles/more/16x16/16x16.%s.sudoku" %str(i))
    # sb.print_board()
    # # sb = solve(sb, True, True,True,True)
    # sb = solve(sb, True, False,True,True,0)
    # sb.print_board()
    # t0 = time.clock()
    # sb1 = init_board("input_puzzles/more/16x16/16x16.%s.sudoku" %str(i))
    # sb1.print_board()
    # # sb1 = solve(sb1, True, True,True,True)
    # sb1 = solve(sb1, True, False,True,True,1)
    # sb1.print_board()
    # print('counter: ',counter)
    # outfile.write("16x16 #%s took this many checks: "%str(i)+str(counter)+'\n')
    # print time.clock() - t0

# for i in xrange(1,21):
#      sb = init_board("input_puzzles/more/25x25/25x25.%s.sudoku" %str(i))
#      sb.print_board()
#      sb = solve(sb, True, True, False, False)
#      sb.print_board()

# t0 = time.clock()
# sb = init_board("input_puzzles/easy/16_16.sudoku")
# sb.print_board()
# sb = solve(sb, True, False, True, False)
# sb.print_board()
# print time.clock() - t0

# sb = init_board("input_puzzles/easy/16_16.sudoku")
# sb.print_board()
# sb = solve(sb, 0, False, False, False)
# sb.print_board()

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, False,False,False)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, False,False,False)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, True,False,False)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, True, False,True,False)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, True, False,False,True)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, True, True,False,True)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, True, False,True,True)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, False,False,True)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, True,False,True)
# sb.print_board()
# print('counter: ',counter)

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, False, False,True,True)
# sb.print_board()
# print('counter: ',counter)

print('totalTime: ', time.clock() - totalTime)
