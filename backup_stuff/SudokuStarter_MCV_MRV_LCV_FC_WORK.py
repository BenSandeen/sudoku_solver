# Sebastian Rodriguez, Haley De Boom, Ben Sandeen,

#!/usr/bin/env python
import struct, string, math
import time
from copy import deepcopy
from functools import partial
from operator import ne 
# from joblib import Parallel, delayed

poss_vals = {} # global dict to store the legal moves for each square
constrainedness = {}

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
            for i in range(subsquare):
                if (SquareRow*subsquare + i != row):
                    for j in range(subsquare):
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
    SquareRow = roww // subsquare
    SquareCol = column // subsquare
    if BoardArray[roww][column]!=0:
        return False
    else:
        if num in BoardArray[roww]:  
            return False
        for roww in xrange(size):
            if num == BoardArray[roww][column]:
                return False

        for r in xrange(size):
            if (r//subsquare==SquareRow):
                for c in xrange(size):
                    if (c//subsquare==SquareCol):
                        if BoardArray[r][c] == num:
                            return False
        return True

def constrained(sudoku_board,roww, column):
    """Function to evaluate moves to see if they're valid (ie: not illegal).
       Returns True if valid, otherwise False"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = roww // subsquare
    SquareCol = column // subsquare
    # global constrainedness
    constrainment = 0

    # for square in BoardArray[roww]:
    for row in xrange(size): 
       
        if (row//subsquare==SquareRow):
            for c in xrange(size):
                if (c//subsquare==SquareCol):
                    if BoardArray[row][c] == 0:
                        constrainment += 1
                    else:
                        constrainment -= 1
                elif BoardArray[row][c] == 0:
                    constrainment += 1
                else:
                    constrainment -= 1

        elif BoardArray[row][column] == 0:
            constrainment += 1
        else:
            constrainment -= 1

    return constrainment
        # elif square:
        #     constrainment += 1
        # for col in xrange(size):
        #     if not BoardArray[row][col]:
        #         constrainment += 1

    # for r in xrange(size):
    #     if (r//subsquare==SquareRow):
    #         for c in xrange(size):
    #             if (c//subsquare==SquareCol):
    #                 if BoardArray[r][c] == num:
    #                     return False
    # return True

def MCV_and_LCV(initial_board):
    """"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
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
                                newBoard = MCV_and_LCV(initial_board)
                                if newBoard != False:
                                    return newBoard
                            poss_vals = last_poss_vals
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def MRV_and_LCV(initial_board):
    """"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
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
                                newBoard = MRV_and_LCV(initial_board)
                                if newBoard != False:
                                    return newBoard
                            poss_vals = last_poss_vals
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def MRV(initial_board):
    """Same as FC, except now it chooses square with fewest legal values to play next"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals
    len_poss_vals = {}

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        # t0 = time.clock()
        for key in poss_vals.keys():
            len_poss_vals[key] = len(poss_vals[key])
        # print('time: ',time.clock() - t0)

        # print(sorted(len_poss_vals.values()))
        for key, value in sorted(len_poss_vals.iteritems(), key=lambda (k,v): (v,k)):
            # print "%s: %s" % (key, value)
            # print(key.split())
            row = key[0]
            col = key[1]
            if BoardArray[row][col] == 0:
                # print "%s: %s" % (key, value)
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
                        if valid: # if move creates no squares with invalid moves
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
    # SquareRow = roww // subsquare
    # SquareCol = column // subsquare
    global poss_vals
    global constrainedness

    # for row in xrange(size):
    #     for col in xrange(size):
    #         constrainedness[row,col] = constrained(initial_board,row,col)

    # print('\n',constrainedness)
    if is_complete(initial_board):
        return initial_board
    # select next square to play in
    for key, value in reversed(sorted(constrainedness.iteritems(), key=lambda (k,v): (v,k))):
        # print "%s: %s" % (key, value)
        # print(key.split())
        row = key[0]
        col = key[1]
        if BoardArray[row][col] == 0:
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
                        # for row in xrange(size):
                        #     for col in xrange(size):
                        constrainedness[row,col] = constrained(initial_board,row,col)
                        newBoard = MCV(initial_board)
                        if newBoard != False:
                            return newBoard
                    poss_vals = last_poss_vals
                    initial_board=initial_board.set_value(row,col,0)
            else:
                return False

    # else:
    #     #pick next square to fill in
    #     for row in xrange(size):
    #         for col in xrange(size):
    #             if BoardArray[row][col] == 0:
    #                 # if valid number can be put in square
    #                 for n in xrange(1,size+1):
    #                     # if is_legit(initial_board,row,col,n):
    #                     if n in poss_vals[row,col]:
    #                         initial_board=initial_board.set_value(row,col,n)
    #                         # last_poss_vals = deepcopy(poss_vals)
    #                         last_poss_vals = dict(poss_vals)
    #                         poss_vals[row,col] = [n]
    #                         # poss_vals, valid = validator(initial_board)
    #                         valid = validator(initial_board)
    #                         if valid: # if move creates no squares with invalid moves
    #                             newBoard = MCV(initial_board)
    #                             if newBoard != False:
    #                                 return newBoard
    #                         poss_vals = last_poss_vals
    #                         initial_board=initial_board.set_value(row,col,0)
    #                 else:
    #                     return False


def LCV(initial_board):
    """LCV function to look through the current board to see how the placement of
       a given value will constrain other squares, and returns the one that 
       constrains others the least"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
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
                                newBoard = LCV(initial_board)
                                if newBoard != False:
                                    return newBoard
                            poss_vals = last_poss_vals
                            initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def FC(initial_board):#,poss_vals_exists):
# def FC(sudoku_board,roww,column,num): 
    """"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    global poss_vals

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
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

# def f(x):
#     return x
# l = range(5)
# results = Parallel(n_jobs=-1)(delayed(f)(i) for i in l))

def validator(board):#,poss_vals):#,row,col)
# def validator(initial_board,roww, column):
#     """Does the actual forward checking"""    
#     BoardArray = initial_board.CurrentGameBoard
#     size = len(BoardArray)
#     subsquare = int(math.sqrt(size))
#     global poss_vals

#     SquareRow = roww // subsquare
#     SquareCol = column // subsquare
#     # if BoardArray[roww][column]!=0:
#     #     return False
#     # else:
#     for num in xrange(1,size+1):
#         if num in BoardArray[roww]:  
#             return False
#         for row in xrange(size):
#             if num == BoardArray[row][column]:
#                 return False
#     for r in xrange(size):
#         if (r//subsquare==SquareRow):
#             for c in xrange(size):
#                 if (c//subsquare==SquareCol):
#                     for num in xrange(1,size+1):
#                         if BoardArray[r][c] == num:
#                             return False
#     return True

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

    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if not BoardArray[row][col]:
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


def solve(initial_board,forward_checking=False,mrv=False,mcv=False,lcv=False):
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

    # initializes a dict of each square's possible values
    for row in xrange(size):
        for col in xrange(size):
            poss_vals[row,col] = []

    # initializes a dict to count number of squares which constrain
    # each square are unassigned
    for row in xrange(size):
        for col in xrange(size):
            constrainedness[row,col] = constrained(initial_board,row,col)
                #or jump out of nested for loops
    for row in xrange(size):
        for col in xrange(size):
            for n in xrange(1,size+1):
                # put the appropriate values in the square.  If the square has a
                # number already, also include that
                if is_legit(initial_board,row,col,n) or BoardArray[row][col] == n:
                    poss_vals[row,col].append(n)
    

    # creates a binary out of the the values of the constraints, each constraint
    # represented by a single bit.  FC is the leftmost bit (highest value), LCV is rightmost
    constraint_mask = int(0b1111 & ((forward_checking<<3)|(mrv<<2)|(mcv<<1)|(lcv)))

    # if user accidentally tells us to use mutually exclusive MCV and MRV
    if constraint_mask == 14:
        constraint_mask = 12 # picks MRV

    # dict (essentially a switch table) for choosing what methods to use based on what
    # the calling function requests, with the last 5 five items implicitly using FC
    switch = {}
    switch[0] = Solver
    switch[1] = LCV # these ignore the user's incorrect inputs and use FC anyways
    switch[2] = MCV
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
    # print((switch[constraint_mask]))
    result = switch[(constraint_mask)](initial_board)#,{})

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
sb = solve(sb, False, False, True, False)
sb.print_board()

t0 = time.clock()
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()
sb = solve(sb, True, True, True,False)
sb.print_board()
print time.clock() - t0

for i in xrange(1,21):
    t0 = time.clock()
    sb = init_board("input_puzzles/more/9x9/9x9.%s.sudoku" %str(i))
    sb.print_board()
    sb = solve(sb, True, False, True, False)
    sb.print_board()
    print time.clock() - t0

# for i in xrange(1,21):
#     t0 = time.clock()
#     sb = init_board("input_puzzles/more/16x16/16x16.%s.sudoku" %str(i))
#     sb.print_board()
#     sb = solve(sb, True, True, False, False)
#     sb.print_board()
#     print time.clock() - t0

# for i in xrange(1,21):
#     sb = init_board("input_puzzles/more/25x25/25x25.%s.sudoku" %str(i))
#     sb.print_board()
#     sb = solve(sb, True, True, False, False)
#     sb.print_board()

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
# sb = solve(sb, True, True, True, False)
# sb.print_board()

print('totalTime: ', time.clock() - totalTime)