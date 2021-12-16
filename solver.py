import sys
import math
import numpy as np
import threading

class Celda:
    def __init__(self, val: int, row: int, col: int, tableSize: int):
        self.val = val
        self.row = row
        self.col = col
        self.posibleValues = { i for i in range(1, tableSize + 1) } if val is None else { i for i in range(val, val+1) }

def loadSudoku(fileName: str):
    lines = open(fileName).readlines()
    if not len(lines) == len(lines[0].replace("\n", "").split(",")):
        exit(1)
    tableSize = len(lines)
    sudoku = np.empty((0, tableSize), Celda)
    for i in range(len(lines)):
        fila = lines[i].replace("\n", "").split(",")
        row = []
        for j in range(len(fila)):
            row = np.append(row, [Celda(None, i, j, tableSize) if " " in fila[j] else Celda(int(fila[j]), i, j, tableSize)], axis=0)
        sudoku = np.append(sudoku, [row], axis=0)
    return sudoku

def calcSubMatrixIndexOffset(sudoku: list[list[Celda]], celda: Celda):
    return int(math.sqrt(len(sudoku)))


def applyConstraint(sudoku: list[list[Celda]], celda: Celda):
    if celda.val is not None:
        return celda
    for col in range(len(sudoku)):
        val = sudoku[celda.row][col].val
        celda.posibleValues.discard(val)
    for row in range(len(sudoku)):
        val = sudoku[row][celda.col].val
        celda.posibleValues.discard(val)
    offset = calcSubMatrixIndexOffset(sudoku, celda)
    print(offset * int(celda.row / offset), offset * int(celda.row / offset) + offset)
    for i in range(offset * int(celda.col / offset), offset * int(celda.col / offset) + offset):
        for j in range(offset * int(celda.row / offset), offset * int(celda.row / offset) + offset):
            if not celda.col == i and not celda.row == i:
                celda.posibleValues.discard(sudoku[j][i].val)
            if len(celda.posibleValues) == 1:
                for v in celda.posibleValues:
                    celda.val = v
    return celda

def propagateConstraints(sudoku: list[list[Celda]]):
    for fila in range(len(sudoku)):
        for col in range(len(sudoku)):
            sudoku[fila][col] = applyConstraint(sudoku, sudoku[fila][col])
    for fila in range(len(sudoku)):
        for col in range(len(sudoku)):
            sudoku[fila][col] = applyConstraint(sudoku, sudoku[fila][col])
    return sudoku

def main():
    sudoku = loadSudoku(sys.argv[1])
    sudoku = propagateConstraints(sudoku)
    for i in range(len(sudoku)):
        for j in range(len(sudoku)):
            print("row: " + str(i) + " col: " + str(j) + " value: " + str(sudoku[i][j].val), sudoku[i][j].posibleValues)
        print()
    

if __name__ == "__main__":
    main()
