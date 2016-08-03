#!/usr/bin/env python
import struct, string, math
import time

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
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

{
    # # first attempt
    # def is_legit(sudoku_board):
    #     BoardArray = sudoku_board.CurrentGameBoard
    #     size = len(BoardArray)
    #     subsquare = int(math.sqrt(size))

    #     #check each cell on the board for a 0, or if the value of the cell
    #     #is present elsewhere within the same row, column, or square
    #     for row in range(size):
    #         for col in range(size):
    #             if BoardArray[row][col]==0:
    #                 for i in range(size):
    #                     if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
    #                         return False
    #                     if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
    #                         return False
    #                 #determine which square the cell is in
    #                 SquareRow = row // subsquare
    #                 SquareCol = col // subsquare
    #                 for i in range(subsquare):
    #                     for j in range(subsquare):
    #                         if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
    #                                 == BoardArray[row][col])
    #                             and (SquareRow*subsquare + i != row)
    #                             and (SquareCol*subsquare + j != col)):
    #                                 return False
    #     return True
}

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
            for c in xrange(size):
                if (r//subsquare==SquareRow) and (c//subsquare==SquareCol):
                    if BoardArray[r][c] == num:
                        return False
        return True

def BTSearch(assign,row,col,forward_checking=False,MRV=False,MCV=False,LCV=False):
    """create function to do backtracking for solve"""
    # if assign is complete -> return assign
    # complete means that each dict key has only one val and none contradict each other
    # we'll need a function to create a board from dict vals so we can check it each time with is_legit
    # 

def LCV(board, row, col):
    """LCV function to look through the current board to see how the placement of
       a given value will constrain other squares, and returns the one that 
       constrains others the least"""
    print("oppaooasfjsadofij")

def FC(initial_board,poss_vals):
    """creates dict of each square's possible values"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    # subsquare = int(math.sqrt(size))

    # poss_vals = {(row,col): for (row,col) }
    # we want to pass in the dictionary (or some value that indicates whether or not 
    # a global dict that we can use already exists)
    # poss_vals = {}

    # checks if dict already has been created
    if not poss_vals:
        for row in xrange(size):
            for col in xrange(size):
                poss_vals[row,col] = []
                    #or jump out of nested for loops
        for row in xrange(size):
            for col in xrange(size):
                for n in xrange(1,size+1):
                    if is_legit(initial_board,row,col,n) or BoardArray[row][col] == n:
                        poss_vals[row,col].append(n)
    # backtracking with forwardchecking
    if is_complete(initial_board):
        return initial_board
    else:
        #pick next square to fill in
        for row in xrange(size):
            for col in xrange(size):
                if BoardArray[row][col] == 0:
                    # if valid number can be put in square
                    for n in xrange(1,size+1):
                        if is_legit(initial_board,row,col,n):
                            initial_board=initial_board.set_value(row,col,n)
                            # print('before: ',poss_vals[row,col])
                            valid = validator(initial_board,poss_vals)
                            # print('after:  ',poss_vals[row,col])
                            # if move creates no squares that have no valid moves
                            if valid:
                                # print('before1: ',poss_vals[row,col])
                                removed = [x for x in poss_vals[row,col] if x!=n]
                                poss_vals[row,col] = [n]
                                # print('after1:  ',poss_vals[row,col])
                                newBoard = FC(initial_board,poss_vals)
                                # print('after2: ',poss_vals[row,col])
                                if newBoard != False:
                                    return newBoard
                                # [poss_vals[row,col].append(x) for x in removed]
                                # alt method:
                                for x in removed:
                                    poss_vals[row,col].append(x)
                                initial_board=initial_board.set_value(row,col,0)
                    else:
                        return False

def validator(board,poss_vals):#,row,col)
    """Does the actual forward checking"""    
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    # subsquare = int(math.sqrt(size))

    # this happens after we assign a square a val to ensure that it didn't remove the last 
    # possible value from any square still unassigned
    # print('poss_vals: ', poss_vals.values())
    if is_complete(board):
        return True
    # Y=[len(x) for x in poss_vals.values()]
    # print(Y)
    for r in xrange(size):
        for c in xrange(size):
            # L = []
            if BoardArray[r][c] == 0: # if the square's val == 0
                # isValid = False
                # print(poss_vals[r,c])
                # print([is_legit(board,r,c,x) for x in poss_vals[r,c]])
                # print(sum([is_legit(board,r,c,x) for x in poss_vals[r,c]]))

                # isValid = bool(sum([is_legit(board,r,c,x) for x in poss_vals[r,c]]))
                for x in poss_vals[r,c]:
                    if is_legit(board,r,c,x):
                        # L.append(x)
                        return True
    return False
    #             isValid = sum(L)
    #             if isValid == False:
    #                 return isValid
    # return isValid

def Solver(initial_board,poss_vals):
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    # result= initial_board
    # newBoard = initial_board

    if is_complete(initial_board):
        return initial_board
    # elif (initial_board == initial_board):
    #     return False
    else:
        #pick next square to fill in
        for row in xrange(size):
#             # print('row',BoardArray[row])
            for col in xrange(size):
#                 # print('col: ', BoardArray[row][col]) 
                if BoardArray[row][col] == 0:
                    # if valid number can be put in square
                    for n in xrange(1,size+1):
                        if is_legit(initial_board,row,col,n):
                            # newBoard=newBoard.set_value(row,col,n)
                            initial_board=initial_board.set_value(row,col,n)
                            newBoard = Solver(initial_board,poss_vals)
                        # assign the square that value
                            # return finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
                            # attemptBoard = finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
                            # if attemptBoard == False:
                            if newBoard != False:
                                return newBoard
                            initial_board=initial_board.set_value(row,col,0)
                            # return finder(attemptBoard,initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
                    else:
                        return False


def solve(initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    # passes backtracking function an empty dict and the CSPs
    row = 0
    col = 0
    # return BTSearch({},row,col,forward_checking=False,MRV=False,MCV=False,LCV=False)
    # finder(initial_board,initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)

    # creates a binary out of the the values of the constraints, each constraint
    # represented by a single bit.  FC is the leftmost bit (highest value), LCV is rightmost
    constraint_mask = 0b1111 & ((forward_checking<<3)|(MRV<<2)|(MCV<<1)|(LCV))
    # dict (essentially a switch table) for choose what methods to use based on  
    switch = {}
    switch[0] = Solver
    switch[8] = FC
    switch[9] = LCV
    switch[10] = MCV
    switch[11] = MCV + LCV
    switch[12] = MRV
    switch[13] = MRV + LCV
    # switch[1] = LCV
    # switch[2] = MCV
    # switch[3] = MCV + LCV
    # switch[4] = MRV
    # switch[5] = MRV + LCV
    # switch[8] = FC
    # switch[9] = forward_checking + LCV
    # switch[10] = forward_checking + MCV
    # switch[11] = forward_checking + LCV + MCV
    # switch[12] = forward_checking + MRV
    # switch[13] = forward_checking + MRV + LCV

    # type(switch[int(constraint_mask)](initial_board,{}))
    result = switch[int(constraint_mask)](initial_board,{})

    return result

    # BoardArray = initial_board.CurrentGameBoard
    # size = len(BoardArray)
    # subsquare = int(math.sqrt(size))
    # result= initial_board
    # newBoard = initial_board
{
    #     if is_complete(initial_board):
    #         return initial_board
    #     # elif (initial_board == initial_board):
    #     #     return False
    #     else:
    #         # print('pants')
    #         #pick next square to fill in
    #         for row in xrange(size):
    # #             # print('row',BoardArray[row])
    #             for col in xrange(size):
    # #                 # print('col: ', BoardArray[row][col]) 
    #                 if BoardArray[row][col] == 0:
    #                     # if valid number can be put in square
    #                     for n in xrange(1,size+1):
    #                         if is_legit(initial_board,row,col,n):
    #                             # newBoard=newBoard.set_value(row,col,n)
    #                             initial_board=initial_board.set_value(row,col,n)
    #                             newBoard = solve(initial_board,forward_checking,MRV,MCV,LCV)
    #                         # assign the square that value
    #                             # return finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                             # attemptBoard = finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                             # if attemptBoard == False:
    #                             if newBoard != False:
    #                                 return newBoard
    #                             initial_board=initial_board.set_value(row,col,0)
    #                             # return finder(attemptBoard,initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                     else:
    #                         return False
}
{
    # def finder(initial_board,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False):
    #     return "poop"
    #     BoardArray = initial_board.CurrentGameBoard
    #     size = len(BoardArray)
    #     subsquare = int(math.sqrt(size))
    #     # result= initial_board
    #     newBoard = initial_board

    #     if is_complete(initial_board):
    #         return initial_board
    #     elif (initial_board == initial_board):
    #         return False
    #     else:
    #         print('pants')
    #         #pick next square to fill in
    #         for row in xrange(size):
    # #             # print('row',BoardArray[row])
    #             for col in xrange(size):
    # #                 # print('col: ', BoardArray[row][col]) 
    #                 if BoardArray[row][col] == 0:
    #                     # if valid number can be put in square
    #                     for n in range(1,size+1):
    #                         if is_legit(newBoard,row,col,n):
    #                             newBoard=newBoard.set_value(row,col,n)
    #                         # assign the square that value
    #                             # return finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                             attemptBoard = finder(newBoard,prev_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                             if attemptBoard == False:
    #                                 return False
    #                             return finder(attemptBoard,initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)
    #                     else:
    #                         return False#newBoard

        # initial_board.set_value(0,0,'penguin')
        # initial_board.print_board()
        
        # solve(initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)

        # newBoard = solve(initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False)

        # print(BoardArray)
    #     if is_complete(initial_board):
    #         # print(is_complete(initial_board))
    #         initial_board.print_board()
    #         return initial_board
    #     else:
    #         for row in xrange(size):
    #             # print('row',BoardArray[row])
    #             for col in xrange(size):
    #                 # print('col: ', BoardArray[row][col]) 
    #                 if BoardArray[row][col] == 0:
    #                     for n in range(1,size+1):
    #                         if is_legit(initial_board,row,col,n):
    #                             newBoard=newBoard.set_value(row,col,n)

    # ###########################################
    # #BACKTRACKING NOT WORKING
    # ###########################################
            
    #                             if is_complete(newBoard):
    #                                 return newBoard
    #                             return solve(newBoard,forward_checking,MRV,MCV,LCV)
    #                             # newBoard = solve(newBoard,forward_checking,MRV,MCV,LCV)

    #                     return newBoard#initial_board#newBoard
    #             # return newBoard
    #         return newBoard # nearly works for 9x9
    #     return newBoard#initial_board#False # no ostensible effect between newBoard and initial_board
}

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
sb = solve(sb, False, False, False, False)
sb.print_board()

t0 = time.clock()
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.2.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.3.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.4.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.5.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.6.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.7.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()

t0 = time.clock()
sb = init_board("input_puzzles/more/9x9/9x9.1.sudoku")
sb.print_board()
sb = solve(sb, True, False, False, False)
sb.print_board()
print time.clock() - t0

# t0 = time.clock()
# sb = init_board("input_puzzles/easy/16_16.sudoku")
# sb.print_board()
# sb = solve(sb, True, False, False, False)
# sb.print_board()
# print time.clock() - t0

# sb = init_board("input_puzzles/easy/16_16.sudoku")
# sb.print_board()
# sb = solve(sb, 0, False, False, False)
# sb.print_board()

# sb = init_board("input_puzzles/easy/25_25.sudoku")
# sb.print_board()
# sb = solve(sb, True, True, False, False)
# sb.print_board()

print('totalTime: ', time.clock() - totalTime)