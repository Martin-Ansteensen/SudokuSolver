#!/usr/bin/env python3
import copy
import json
import time

start_time = time.time()    #Timer to keep track of execution time

#Asks the user for a input (sudoku)
def getSudoku():
    inputData = input("Input your sudoku:")
    return inputData

#Formats the input as a nested dictionary (one dictionary for each row)
def readSudoku(inputSudoku):
    #Prints some basic info about the board to the console
    board = inputSudoku[2:]     #Removes the row and column data from the board
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
    
    for rute in board:
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

    print(str(sudoku) + "\n") #Prints the sudoku  
    return sudoku, gridSize, horizontalSubGridsInBoard, varticalSubGridsInBoard

#Creates a list where all the cells belonging subgrid is listed
def getSubGridBelonging(inputSudoku, gridSize, subGridHorizontal, subGridVertical):

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

#Uses brute force to solve the sudoku. Tries to combine every legal possibilty
def solveSudoku(sudokuToSolve, gridSize, subGridHorizontal, subGridVertical):
    allPossible = []
    sudoku = sudokuToSolve
    allPossForCell = []
    belongsToSubGrid = getSubGridBelonging(sudoku, gridSize, subGridHorizontal, subGridVertical)

    for row in sudoku:
        for cell in sudoku[row]:
            if row == 0 and cell == 0:
                ruteIndex = [row, cell] 
                allPossForCell = findAllPossibilities(sudoku, gridSize, ruteIndex, belongsToSubGrid)
                for possCell in allPossForCell:
                    sudoku[row][cell] = possCell
                    sudokuEdit = copy.deepcopy(sudoku)
                    allPossible.append(sudokuEdit)

            else:
                copyAllPossible =  copy.deepcopy(allPossible)
                for possSudoku in copyAllPossible:
                    sudoku = possSudoku
                    ruteIndex = [row, cell] 
                    allPossForCell = findAllPossibilities(sudoku, gridSize, ruteIndex, belongsToSubGrid)
                    if not allPossForCell:
                        #Det finnes ingen muligheter for ruten, og den versjonen kan derfor slettes
                        del allPossible[0]

                    else:
                        for possCell in allPossForCell:
                            sudoku[row][cell] = possCell
                            sudokuEdit = copy.deepcopy(sudoku)
                            allPossible.append(sudokuEdit)

                        del allPossible[0]
    printSolutions(allPossible)

#Finds all possible values for the given cell based on the input sudoku
def findAllPossibilities(inputSudoku, gridSize, ruteIndex, belongsToSubGrid):
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

    possible = []
    if sudoku[radForThisCell][ruteForThisCell] == 0:
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
        allPossible.append(sudoku[radForThisCell][ruteForThisCell])

    return allPossible

#Outputs the solutions to the terminal and to a .json file
def printSolutions(sudokuSolutions):
    sudokuSolutions = sudokuSolutions

    for solution in sudokuSolutions:
        for row in solution:            
            printRow = []
            for cell in solution[row]:
                printRow.append(solution[row][cell])
            print(printRow)
        
        print("")
    print("Number of solutions:", len(sudokuSolutions))
    print("Execution time: %s seconds " % (time.time() - start_time)) 

    with open("sudoku.json", "w") as outfile: #Passes the info to the .json
        json.dump(sudokuSolutions, outfile)

# Get the sudoku from the user
formatertSudoku = {} #Definer at daten fra readSudoku er en dictionary, hvis ikke tolker den det som en string
inputData = getSudoku()
formatertSudoku, lengde, subGridHorizontal, subGridVertical = readSudoku(inputData)

solveSudoku(formatertSudoku, lengde, subGridHorizontal, subGridVertical)

