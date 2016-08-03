#!/usr/bin/env python
import struct, string, math

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
    # print(num)
    # should be able to eliminate this later
    if BoardArray[roww][column]!=0:
        return False
    else:
        # print(BoardArray[roww])
        # print('row: ',roww,'    num: ',num)
        if num in BoardArray[roww]:  
            # print('sugarpants')
            return False
        # if BoardArray[i][column] != num:
        # print(num)
        # print(BoardArray[column])
        # print(num in BoardArray[column])
        for roww in xrange(size):
            # print('column: ',column,'     array: ',BoardArray[roww][column],'    num: ',num)
            if num == BoardArray[roww][column]:
                # print('sugar')
                return False
        # for i in xrange(size):

        # for i in range(subsquare):
        #     for j in range(subsquare):

        for r in xrange(size):
            for c in xrange(size):
                if (r//subsquare==SquareRow) and (c//subsquare==SquareCol):
            #     for i in range(subsquare):
            #         for j in range(subsquare):
                    # print('r: ',r,'     c: ',c)    
                    if BoardArray[r][c] == num:
               
                        # print('boarr:',BoardArray)
                        # print('sqrow:',SquareRow,'   subsquare:',subsquare,'   sqcol:',SquareCol)
                        # print('BA1: ',BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j],'   BA2: ',BoardArray[roww][column])
                        # print('roww:',roww,'    column:',column)
                        # if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                        #             == BoardArray[roww][column])):
                        #     # print(SquareRow, subsquare,i, roww)
                        #     # print(SquareRow*subsquare+i != roww)
                        #     if (SquareRow*subsquare+i != roww):
                        #         # and (SquareRow*subsquare + i != roww)
                        #         # print(SquareCol,j,column)
                        #         # print(SquareCol*subsquare+j != column)
                        #         if (SquareCol*subsquare+j != column):
                        #         # and (SquareCol*subsquare + j != column)):
                    # print('boob')

                    # for i in range(subsquare):
                    #     for j in range(subsquare):
                    # if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                    #         == BoardArray[roww][column])
                    #     and (SquareRow*subsquare + i != roww)
                    #     and (SquareCol*subsquare + j != column)):
                        return False
                            # return False
    # else:
        # print('pants')
        return True

def solve(initial_board,forward_checking=False,MRV=False,MCV=False,LCV=False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    # set_value(self, row, col, value)
    # print(board)
    # print(initial_board)
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    # result= initial_board
    newBoard = initial_board

    # print(BoardArray)
    if is_complete(initial_board):
        # print(is_complete(initial_board))
        initial_board.print_board()
        return result#initial_board
    else:
        for row in xrange(size):
            # print('row',BoardArray[row])
            for col in xrange(size):
                # print('col: ', BoardArray[row][col]) 
                if BoardArray[row][col] == 0:
                    # use list compreh. to create list of valid moves later
                    for n in range(1,size+1):
                        # if is_legit(BoardArray,row,col,n):
                        # print('row: ',row,'     col: ',col,'    num: ',n)
                        if is_legit(initial_board,row,col,n):
                            # newBoard=initial_board.set_value(row,col,n) # place this directly in recursive call (if works)
                            # newBoard=initial_board
                            newBoard=newBoard.set_value(row,col,n)
                        # if get_next_move(initial_board,row,col,n):
                            # print('hi')
                            # print(newBoard.print_board())

###########################################
#BACKTRACKING NOT WORKING
###########################################
        
                            if is_complete(newBoard):
                                return newBoard
                            # result = solve(newBoard,forward_checking,MRV,MCV,LCV)
                            # newBoard = solve(newBoard,forward_checking,MRV,MCV,LCV)
                            return solve(newBoard,forward_checking,MRV,MCV,LCV)
                           
                            # print(result)
                            # if newBoard:
                            #     if is_complete(newBoard):
                            #         return newBoard

                            # if result:
                            #     if is_complete(result):
                            #         return result
                            
                            # if result == initial_board:
                            #     return initial_board
                            # solve(initial)
                    # else:
        # return newBoard#initial_board # works identically to the below

                            # return initial_board # nearly works for 9x9
                            return newBoard
            return newBoard
        # return initial_board # nearly works for 9x9
        return newBoard # nearly works for 9x9
    return newBoard#initial_board#False # no ostensible effect between newBoard and initial_board
                
{

                # if  and set value to 

                # print('here')
                # BoardArray=initial_board.set_value(row,col,2)
                # newBoard=BoardArray.set_value(row,col,2)
                # print(BoardArray)
#{}   
    # print(is_complete(initial_board))
    # BoardArray=initial_board.set_value(0, 0, 1)
    # print(BoardArray)

    # for 
    #     if is_complete(board):
    #         return board

    # for item in tree:
    #     if type(item)==int:
    #         print(item)
    #         if item == elem:
    #             return True
    #     else:
    #         dfs(item, elem)
    # return False
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
sb = init_board("input_puzzles/easy/4_4.sudoku")
sb.print_board()
fb = solve(sb, True, True, False, False)
sb.print_board()
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()
fb = solve(sb, True, True, False, False)
sb.print_board()
