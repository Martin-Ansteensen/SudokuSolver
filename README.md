# SudokuSolver


## Use
The program has two programs of interest: gui.py and sudokuSolver.py
All square sodukus are allowed (9*9, 2*2, 20*20, etc.). 

### Format
The program only accepts sudokus in the following format: 3353..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79 (this is a 9*9 soduku). It must only contain numbers from 1-the size of the sudoku (in this case 9). Empty boxes are represented with dots. 

### sudokuSolver.py
At run the program will ask the user to input a sudoku in the terminal. The program will write all the solutions found to the terminal as well as sudoku.json

### gui.py
Input a sudoku in the "Submit sudoku" field and click "Submit sudoku". The sudoku should now be displayed in the grid. To solve the sudoku, click "Solve sudoku". If there are multiple solutions, click "Next solution" to view alternative solutions.

## Example sodukus
* 21.... (2*2 sudoku, 2 solutions)
* 22................ (4*4 sudoku, 288 solutions)
* 23..1..3..........2.26.......3..3..1.2 (6*6 sudoku, 28 solutions)
* 234.1..3..2.......6426.......3..3..1.2 (6*6 sudoku, 1 solution)
* 3353..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79 (9*9 sudoku, 1 solution)
* 33.63....85.....1......67..34..57.34..6...2...7..91.42..84..39......5.....59....36. (9*9 sudoku, 1 solution)




