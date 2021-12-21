import sys
import math
import numpy as np
import threading
import re
from common import *

wait_milli = 50

#class AntSystem():

#class Board():

def loadSudoku(fileName: str, clase = Celda):
    lines = open(fileName).readlines()
    if not len(lines) == len(lines[0].replace("\n", "").split(",")):
        exit(1)
    tableSize = len(lines)
    sudoku = np.empty((0, tableSize), clase)
    for i in range(len(lines)):
        fila = lines[i].replace("\n", "").split(",")
        row = []
        for j in range(len(fila)):
            numero = re.search("[0-9]+", fila[j])
            numero = None if numero is None else int(numero.string)
            row = np.append(row, [clase(numero, i, j)], axis=0)
        sudoku = np.append(sudoku, [row], axis=0)
    return sudoku

def calcSubMatrixIndexOffset(sudoku: list[list[Celda]], celda: Celda):
    return int(math.sqrt(len(sudoku)))


def applyConstraint(sudoku: list[list[Celda]], celda: Celda):
    if celda.val is not None:
        return celda
    for col in range(len(sudoku)):
        val = sudoku[celda.row][col].val
        celda.discard(val)
    for row in range(len(sudoku)):
        val = sudoku[row][celda.col].val
        celda.discard(val)
    offset = calcSubMatrixIndexOffset(sudoku, celda)
    for i in range(offset * int(celda.col / offset), offset * int(celda.col / offset) + offset):
        for j in range(offset * int(celda.row / offset), offset * int(celda.row / offset) + offset):
            if not celda.col == i and not celda.row == i:
                celda.discard(sudoku[j][i].val)
            if len(celda.posibleValues) == 1:
                for v in celda.posibleValues:
                    celda.val = v
    return celda

def propagateConstraints(sudoku: list[list[Celda]]):
    for fila in range(len(sudoku)):
        for col in range(len(sudoku)):
            sudoku[fila][col] = applyConstraint(sudoku, sudoku[fila][col])
            if isinstance(sudoku[0][0], PygameCell):
                pygame.time.wait(wait_milli)
                sudoku[fila][col].draw()
    return sudoku

def main():
    sudoku = loadSudoku(sys.argv[1], Celda)
    propagateConstraints(sudoku)
    

if __name__ == "__main__":
    main()
