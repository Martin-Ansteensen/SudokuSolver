from tkinter import *  # Python 3.x
#http://newcoder.io/gui/part-3/

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
LINEWIDTH = 2 # The width of the lines
class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.x_size = 3
        self.y_size = 3
        self.grid_size = self.x_size* self.y_size

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width = WIDTH, height = HEIGHT)
        self.canvas.pack(fill = BOTH, side = TOP)
        
        # Button for solving the sudoku
        solve_button = Button(self, text = "Solve sudoku", command = self.__solve_sudoku)
        solve_button.pack(fill=BOTH, side=BOTTOM)

        # Button for submiting the sudoku
        submit_button = Button(self, text = "Submit sudoku", command = self.__sumbit_sudoku)
        submit_button.pack(fill=BOTH, side=BOTTOM)

        self.canvas.input_field = Entry(self)
        self.canvas.input_field.pack(fill=BOTH, side=BOTTOM)
        self.canvas.input_field.insert(END, 'Submit your sudoku')

        #Create empty board
        board = [3,3]
        for i in range(81):
            board.append(0) 

        
        self.game = SudokuGame(board)
        #self.game.start(self.x_size, self.y_size)

        self.__draw_grid()
        self.__draw_puzzle()

    def __solve_sudoku(self):
        pass


    def __sumbit_sudoku(self):
        sudoku = self.canvas.input_field.get()      #Gets the field's value
        self.canvas.input_field.delete(0, 'end')    #Clears the input field
        valid = 0  
        sudoku = sudoku.replace(".", str(0))
        if not sudoku.isdigit():
            self.canvas.input_field.insert(END, 'The sudoku can only contain numbers')
        
        else:
            self.x_size = int(sudoku[0])    #Number of rows in each subregion on the board (grid)
            self.y_size = int(sudoku[1])     #Number of columns in each subregion on the board (grid)
            self.grid_size = self.x_size*self.y_size      #The size of the board/grid
            
            
            print(len(sudoku))

            if len(sudoku) != self.grid_size*self.grid_size + 2:
                self.canvas.input_field.insert(END, 'The number of digits does not match the size of the board')


            else:
                sudokuArray = []
                for i in sudoku:
                    sudokuArray.append(i)
                sudoku = sudokuArray
                board = sudoku
                self.game = SudokuGame(board)
                #self.game.start(self.x_size, self.y_size)

                self.__draw_grid()
                self.__draw_puzzle()

    def __draw_grid(self):
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * self.grid_size  # Width and height of the whole board

        self.canvas.delete("all")

        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(self.grid_size+1):
            #Horizontal
            color = "black" if i % self.x_size == 0 else "gray"
            LINEWIDTH = 2 if i % self.x_size == 0 else 1
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill = color, width = LINEWIDTH)
            
            #Vertical
            color = "black" if i % self.y_size == 0 else "gray"
            LINEWIDTH = 2 if i % self.x_size == 0 else 1
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill = color, width = LINEWIDTH)

            
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                #     original = self.game.start_puzzle[i][j]
                    color = "black" #if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )


class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    
    def __init__(self, board):
        self.board, self.lengde, self.subGridHorizontal, self.subGridVertical = self.__create_board(board)


    def __create_board(self, inputSudoku):
        #Prints some basic info about the board to the console
        boardInput = inputSudoku[2:]     #Removes the row and column data from the board
        rowInSubGrid = int(inputSudoku[0])    #Number of rows in each subregion on the board (grid)
        columnInSubGrid = int(inputSudoku[1])     #Number of columns in each subregion on the board (grid)
        gridSize = rowInSubGrid*columnInSubGrid      #The size of the board/grid
        
        horizontalSubGridsInBoard = gridSize//columnInSubGrid #// Avoids a decimal mark (.0) in the answer
        varticalSubGridsInBoard = gridSize//rowInSubGrid
        print("The board is:" , gridSize , "*" , gridSize)
        print("Number of subgrids on the x-axis:", str(horizontalSubGridsInBoard), "\nNumber of subgrids on the y-axis:", str(varticalSubGridsInBoard))

        #Converts the inputSudoku to a nested dictionary
        sudoku = {} 
        rowCount = 0    #Keeps track of in which row the number should be placed
        columnCount = 0     #Keeps track of in which column the number should be placed
        sudoku[rowCount] = {}   #Creates the first row in the dictionary
        
        for rute in boardInput:
            if columnCount == gridSize:  #If a row is full
                rowCount += 1 #Row
                columnCount = 0 #Column
                sudoku[rowCount] = {} #Creates a new empty row

            if rute == ".":     #Replaces . with no value (empty cell)
                rute = 0
            else:   #Use int() to remove '' (has been a string)
                rute = int(rute)
                
            sudoku[rowCount][columnCount] = rute #Adds the number to the sudoku
            columnCount += 1 #Increments the column number by one

        #print(str(sudoku) + "\n") #Prints the sudoku  
        return sudoku, gridSize, horizontalSubGridsInBoard, varticalSubGridsInBoard

    def __input_board(self, board):
        #Ask the user for a board
        pass
    


class SudokuGame(object):

    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board):
        self.board = board
        self.start_puzzle = SudokuBoard(board).board
        self.puzzle = self.start_puzzle

    #Creates a list with empty numbers
    def start(self, x, y):
        self.x = x*y
        self.y = y*x
        self.puzzle = []
        for i in range(self.x):
            self.puzzle.append([])
            for j in range(self.y):
                self.puzzle[i].append(self.start_puzzle[i][j])

        print(self.puzzle)

if __name__ == '__main__':
    #board = "33.63....85.....1......67..34..57.34..6...2...7..91.42..84..39......5.....59....36."
    root = Tk()
    SudokuUI(root)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 100))
    root.mainloop()