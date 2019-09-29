from tkinter import *  # Python 3.x
#http://newcoder.io/gui/part-3/

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

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
        #Create empty board
        board = [3,3]
        for i in range(81):
            board.append(0) 

        self.game = SudokuBoard(board)

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width = WIDTH, height = HEIGHT+100)
        self.canvas.pack(fill = BOTH, side = TOP)
        self.winHeight = self.canvas.winfo_reqheight()

        # Button for solving the sudoku
        self.solve_button = Button(self, text = "Solve sudoku", command = self.game.solve_sudoku)
        self.solve_button.place(y=self.winHeight-37, relwidth=1)

        # Button for submiting the sudoku
        self.submit_button = Button(self, text = "Submit sudoku", command = self.submit_sudoku)
        self.submit_button.place(y=self.winHeight-70, relwidth=1)

        # Inputfield were the user can type in the sudoku
        self.canvas.input_field = Entry(self)
        self.canvas.input_field.place(y=self.winHeight-98, relwidth=1)
        self.canvas.input_field.insert(END, 'Submit your sudoku')
        
        self.__draw_grid()
        self.__draw_puzzle()

    def submit_sudoku(self):
        sudoku = self.canvas.input_field.get()      #Gets the field's value
        self.canvas.input_field.delete(0, 'end')    #Clears the input field
        valid = 0  
        sudoku = sudoku.replace(".", str(0))
        if not sudoku.isdigit():
            self.canvas.input_field.insert(END, 'The sudoku can only contain numbers and dots: .')
        
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
                self.game = SudokuBoard(board)
                
                self.__draw_grid()
                self.__draw_puzzle()

    def __draw_grid(self):
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * self.grid_size  # Width and height of the whole board
        root.geometry('{}x{}'.format(WIDTH, HEIGHT+100))
        
        self.winHeight = HEIGHT + 100
        self.submit_button.place(y=self.winHeight-70, relwidth=1)
        self.canvas.input_field.place(y=self.winHeight-98, relwidth=1)
        self.solve_button.place(y=self.winHeight-37, relwidth=1)


        self.canvas.delete("all")

        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(self.grid_size+1):
            #Horizontal
            line_color = "black" if i % self.x_size == 0 else "gray"
            line_width = 2 if i % self.x_size == 0 else 1 # Separates the subgrids with thick lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill = line_color, width = line_width)
            
            #Vertical
            line_color = "black" if i % self.y_size == 0 else "gray"
            line_width = 2 if i % self.y_size == 0 else 1 # Separates the subgrids with thick lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill = line_color, width = line_width)

            
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.game.puzzle[i][j]
                if cell != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    text_color = "black" #if answer == original else "sea green"
                    self.canvas.create_text(x, y, text=cell, tags="numbers", fill=text_color)


class SudokuBoard(object):
    """
    Creates the board from user input and solves it
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
        self.puzzle = sudoku 
        return sudoku, gridSize, horizontalSubGridsInBoard, varticalSubGridsInBoard

    def solve_sudoku(self):
        pass


if __name__ == '__main__':
    root = Tk() # Creates a window
    SudokuUI(root) # Runs the class that creates the content
    root.resizable(width=False, height=False) # Prevents the user from resizing the window
    root.mainloop() 