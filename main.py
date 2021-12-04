from contextlib import redirect_stdout
from math import sqrt
from random import sample
def main():
    #while(True):
        print("Proyecto Sudoku")
        print("1.Crear problema sudoku (4x4), (9x9), (15x15)")
        print("2.Solucionador Sudoku")
        """val = int(input())
        match val:
            case 1:
                break
            case 2:
                break
            case __:
                break"""
        createSudokuPuzzle()
def createSudokuPuzzle():
    while(True):
        print("--Elegir Tamaño--")
        print("1.(9x9)")
        print("2.(16x16)")
        print("3.(25x25)")
        print("4.Salir")
        val = int(input())
        match val:
            case 1:
                createBoard(3)
                break
            case 2:
                createBoard(4)
                break
            case 3:
                createBoard(5)
                break
            case __:
                break
    
def createBoard(base):
    side  = base*base

    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    removeNumbers(side,board)

def removeNumbers(side,board):
    squares = side*side
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        board[p//side][p%side] = 0

    numSize = len(str(side))
    filename = "sudoku_"+str(side)+"x"+str(side)+".csv"
    with open(filename, 'w') as f:
        with redirect_stdout(f):
            for line in board: print(",".join(f"{n or ' ':{numSize}}" for n in line))

if __name__ == "__main__":
    main()