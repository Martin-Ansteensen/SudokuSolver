from tkinter import *  # Python 3.x
import copy
#http://newcoder.io/gui/part-3/
"""
43123456789012123456789012123456789012123456789012123456789012123456789012123456789012123456789012123456789012123456789012123456789012123456789012
33123456789123456789123456789123456789123456789123456789123456789123456789123456789
"""
#Cleanup code, make reszing the grid the same size all the time but only with bigger cells (but not for 8*8)
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
        self.grid_size = self.x_size * self.y_size
        
        # Create empty board
        board = [self.x_size, self.y_size]
        for i in range(self.grid_size**2):
            board.append(0) 

        self.game = SudokuBoard(board)
        self.initUI()

    def initUI(self):
        self.parent.title("Sudokusolver")
        self.pack(fill=BOTH)
        number_of_buttons = 3 
        self.canvas = Canvas(self, width = WIDTH, height = HEIGHT)
        self.canvas.pack(fill = BOTH, side = TOP)
        self.winHeight = self.canvas.winfo_reqheight()

        # Inputfield were the user can type in the sudoku
        self.canvas.input_field = Entry(self)
        self.canvas.input_field.place(y=self.winHeight-131, relwidth=1)
        self.canvas.input_field.insert(END, 'Submit your sudoku')

        # Button for submiting the sudoku
        self.submit_button = Button(self, text = "Submit sudoku", command = self.submit_sudoku)
        self.submit_button.place(y=self.winHeight-103, relwidth=1)

        # Button for solving the sudoku
        self.solve_button = Button(self, text = "Solve sudoku", state=DISABLED, command = self.process_sudoku)
        self.solve_button.place(y=self.winHeight-70, relwidth=1)
        
        # Button for showing the next solution
        self.next_solution_button = Button(self, text = "Next solution", state=DISABLED, command = self.next_solution)
        self.next_solution_button.place(y=self.winHeight-37, relwidth=1)

        self.draw_grid()
        self.draw_puzzle()

    def submit_sudoku(self):
        sudoku = self.canvas.input_field.get()      #Gets the field's value
        self.canvas.input_field.delete(0, 'end')    #Clears the input field
        valid = 0  
        sudoku = sudoku.replace(".", str(0))
        self.solve_button.config(state="disabled") #Disables the button
        self.next_solution_button.config(state="disabled",text = "Next solution")

        
        if not sudoku.isdigit(): #Invalid input
            self.canvas.input_field.insert(END, 'The sudoku can only contain numbers and dots: .')
        
        else:
            self.x_size = int(sudoku[0])    #Number of rows in each subregion on the board (grid)
            self.y_size = int(sudoku[1])     #Number of columns in each subregion on the board (grid)
            self.grid_size = self.x_size*self.y_size      #The size of the board/grid
            
            
            print(len(sudoku))

            if len(sudoku) != self.grid_size*self.grid_size + 2: #Invalid inpu
                self.canvas.input_field.insert(END, 'The number of digits does not match the size of the board')


            else: #Valid input!
                sudokuArray = []
                for i in sudoku:
                    sudokuArray.append(i)
                sudoku = sudokuArray
                board = sudoku
                self.game = SudokuBoard(board)
                self.solve_button.config(state="normal")
                self.draw_grid()
                self.draw_puzzle()

    def draw_grid(self):
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * self.grid_size  # Width and height of the whole board
        self.winHeight = HEIGHT + 150
        self.canvas.config(width = WIDTH, height = HEIGHT+150)
        
        root.geometry('{}x{}'.format(WIDTH, HEIGHT+150))
        
        self.canvas.input_field.place(y=self.winHeight-131, relwidth=1)
        self.submit_button.place(y=self.winHeight-103, relwidth=1)
        self.solve_button.place(y=self.winHeight-70, relwidth=1)
        self.next_solution_button.place(y=self.winHeight-37, relwidth=1)

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

            
    def draw_puzzle(self):
        if len(self.game.puzzle) == 0:
            self.canvas.input_field.insert(END, "This board doesn't have any solutions")
        else:
            self.canvas.delete("numbers")
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    cell = self.game.puzzle[self.game.number_solution][i][j]
                    if cell != 0:
                        x = MARGIN + j * SIDE + SIDE / 2
                        y = MARGIN + i * SIDE + SIDE / 2
                        text_color = "black" #if answer == original else "sea green"
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill=text_color)
        
    def process_sudoku(self):
        boardenjenje, more_solution = self.game.solve_sudoku(self.game.board, self.grid_size, self.x_size, self.y_size) 
        if more_solution == True:
            self.next_solution_button.config(state="normal")
        else:
            self.next_solution_button.config(state="disabled")

        #self.game = SudokuBoard(board)
        self.game.number_solution = 0
        self.canvas.input_field.insert(END, 'This board has %s solutions' %(len(self.game.puzzle)))
        self.draw_grid()
        self.draw_puzzle()
        self.solve_button.config(state="disabled")
        

    def next_solution(self):
        if len(self.game.puzzle)-1 == self.game.number_solution:
            self.game.number_solution = 0
        else:
            self.game.number_solution += 1
        self.draw_grid()
        self.draw_puzzle()
        self.next_solution_button.config(text = "Next solution %s"%(self.game.number_solution +1))


class SudokuBoard(object):
    """
    Creates the board from user input and solves it
    """
    
    def __init__(self, board):
        self.board, self.lengde, self.subGridHorizontal, self.subGridVertical = self.create_board(board)
        self.number_solution = 0
#        self.puzzle = []

    def create_board(self, inputSudoku):
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
        self.puzzle = []
        self.puzzle.append(sudoku) 
        return sudoku, gridSize, horizontalSubGridsInBoard, varticalSubGridsInBoard
    
    def getSubGridBelonging(self, inputSudoku, gridSize, subGridHorizontal, subGridVertical):

        sudoku = inputSudoku
        belongsToSubGrid = {}
        gridSize = gridSize
        subGridVerticalCount = 0
        annenHverTeller = 0
        boksVannTeller = 0

        for x in sudoku: 
            belongsToSubGrid[x] = {}
            if annenHverTeller == (gridSize/subGridVertical):
                annenHverTeller = 0
                subGridVerticalCount = x           

            boksVannTeller = subGridVerticalCount
            teller = 0

            for y in sudoku[x]:
                if teller == gridSize/subGridHorizontal:
                    teller = 0
                    boksVannTeller += 1  

                belongsToSubGrid[x][y] = boksVannTeller
                teller += 1

            annenHverTeller += 1    
        
        return belongsToSubGrid


    def solve_sudoku(self, sudokuToSolve, gridSize, subGridHorizontal, subGridVertical):
        allPossible = []
        sudoku = sudokuToSolve
        allPossForCell = []
        belongsToSubGrid = self.getSubGridBelonging(sudoku, gridSize, subGridHorizontal, subGridVertical)

        for row in sudoku:
            for cell in sudoku[row]:
                if row == 0 and cell == 0:
                    ruteIndex = [row, cell] 
                    allPossForCell = self.findAllPossibilities(sudoku, gridSize, ruteIndex, belongsToSubGrid)
                    for possCell in allPossForCell:
                        sudoku[row][cell] = possCell
                        sudokuEdit = copy.deepcopy(sudoku)
                        allPossible.append(sudokuEdit)

                else:
                    copyAllPossible =  copy.deepcopy(allPossible)
                    for possSudoku in copyAllPossible:
                        sudoku = possSudoku
                        ruteIndex = [row, cell] 
                        allPossForCell = self.findAllPossibilities(sudoku, gridSize, ruteIndex, belongsToSubGrid)
                        if not allPossForCell:
                            #Det finnes ingen muligheter for ruten, og den versjonen kan derfor slettes
                            del allPossible[0]

                        else:
                            for possCell in allPossForCell:
                                sudoku[row][cell] = possCell
                                sudokuEdit = copy.deepcopy(sudoku)
                                allPossible.append(sudokuEdit)

                            del allPossible[0]
        if len(allPossible) != 1 and len(allPossible) > self.number_solution:
            more_solutions = True
        else:
            more_solutions = False
        self.puzzle = allPossible#[self.number_solution]
        return allPossible, more_solutions
        #printSolutions(allPossible)
    
    #Finds all possible values for the given cell based on the input sudoku
    def findAllPossibilities(self, inputSudoku, gridSize, ruteIndex, belongsToSubGrid):
        radForThisCell = ruteIndex[0]
        ruteForThisCell = ruteIndex[1]
        opptattIRaden = {}
        opptattIKolonnen = {}
        opptattIBoksen = {}
        belongsToSubGrid = belongsToSubGrid
        allPossible = []

        sudoku = copy.deepcopy(inputSudoku) #Lager en kopi fordi vi ikke kan endre originalen
        allPossibilities =  copy.deepcopy(inputSudoku)
        allNumbers = list(range(1, gridSize + 1))
        number = sudoku[radForThisCell][ruteForThisCell] 
        possible = []
        if number == 0:
            for x in sudoku:
                opptattIKolonnen[x] = [] #lager kolonne
                opptattIRaden[x] = []
                opptattIBoksen[x] = []

            for x in sudoku:
                for y in sudoku[x]:
                    if sudoku[x][y] != 0: 
                        opptattIRaden[x].append(sudoku[x][y])
                        opptattIKolonnen[y].append(sudoku[x][y])
                        opptattIBoksen[belongsToSubGrid[x][y]].append(sudoku[x][y])
                        
            allUnavaible = list(set(opptattIKolonnen[ruteForThisCell]) | set(opptattIRaden[radForThisCell]) | set(opptattIBoksen[belongsToSubGrid[radForThisCell][ruteForThisCell]]))
            if sudoku[radForThisCell][ruteForThisCell] == 0:
                allPossible = [e for e in allNumbers if e not in allUnavaible]
            else:
                allUnavaible = list(set(opptattIKolonnen[ruteForThisCell]) | set(opptattIRaden[radForThisCell]) | set(opptattIBoksen[belongsToSubGrid[radForThisCell][ruteForThisCell]]))
            
        else:
            if number in allNumbers:
                allPossible.append(number)
            else:
                #Throw exception
                allPossible.append("0")
        return allPossible


if __name__ == '__main__':
    root = Tk() # Creates a window
    photo = PhotoImage(file="sudoku_icon.png")
    root.iconphoto(False,photo)
    SudokuUI(root) # Runs the class that creates the content
    root.resizable(width=False, height=False) # Prevents the user from resizing the window
    root.mainloop() 