import sys
import math
import numpy as np
import threading
import re
from common import *

sys.setrecursionlimit(150000)
wait_milli = 0

"""
class Ant():


class Board():
    def __init__(self, fileName: str, CellType = Celda):
        order = len(lines)
        self.cells = np.empty((0, order), clase)
        for i in range(len(lines)):
            fila = lines[i].replace("\n", "").split(",")
            row = []
            for j in range(len(fila)):
                numero = re.search("[0-9]+", fila[j])
                numero = None if numero is None else int(numero.string)
                self.append = np.append(self.append, [clase(numero, i, j)], axis=0)
                """
#Codigo inspirado de http://www.norvig.com/sudoku.html
def busqueda(sudoku):
    if sudoku is False:
        return False
    if all(len(cell.posibleValues) == 1 for cell in sudoku):
        return sudoku
    #heuristica
    length, indice = min((len(sudoku[i].posibleValues), i) for i in range(len(sudoku)) if len(sudoku[i].posibleValues) > 1)
    return some(busqueda(assign(copy.deepcopy(sudoku), indice, d)) for d in sudoku[indice].posibleValues)

def assign(sudoku, indice, valor_intento):
    demas_valores = sudoku[indice].posibleValues.replace(valor_intento, '')
    if all(eliminate(sudoku, indice, nuevo_intento) for nuevo_intento in demas_valores):
        return sudoku
    else:
        return False

def eliminate(sudoku, indice, valor_intento):
    if valor_intento not in sudoku[indice].posibleValues:
        return sudoku
    sudoku[indice].posibleValues = sudoku[indice].posibleValues.replace(valor_intento, '')
    if isinstance(sudoku[0], PygameCell):
        sudoku[indice].draw()
        pygame.time.wait(wait_milli)
    if len(sudoku[indice].posibleValues) == 0:
        return False
    elif len(sudoku[indice].posibleValues) == 1:
        nuevo_intento = sudoku[indice].posibleValues
        if not all([eliminate(sudoku, nuevo_i, nuevo_intento) for nuevo_i in sudoku[indice].peers]):
            return False
    for unit in sudoku[indice].units:
        new_tries = [i for i in unit if valor_intento in sudoku[i].posibleValues]
        if len(new_tries) == 0:
            return False
        elif len(new_tries) == 1:
            if not assign(copy.deepcopy(sudoku), new_tries[0], valor_intento):
                return False
    return sudoku

def some(lista):
    for elem in lista:
        if elem: return elem #retorna True o lo que sea el elemento
    return False

def loadSudoku(fileName: str, clase = Celda):
    lines = open(fileName).readlines()
    if not len(lines) == len(lines[0].replace("\n", "").split(",")):
        exit(1)
    tableSize = len(lines)
    sudoku = []
    for i in range(len(lines)):
        fila = lines[i].replace("\n", "").split(",")
        for j in range(len(fila)):
            numero = re.search("[0-9]+", fila[j])
            numero = None if numero is None else numero.string
            sudoku.append(clase(numero, i, j))
    return sudoku

def applyConstraint(sudoku: list[list[Celda]], celda: Celda):
    if celda.val is not None:
        return celda
    for col in range(Celda.tableSize):
        val = sudoku[celda.row + col * Celda.tableSize].val
        celda.discard(val)
    for row in range(Celda.tableSize):
        val = sudoku[row + celda.col * Celda.tableSize].val
        celda.discard(val)
    offset = calcSubMatrixIndexOffset()
    for i in range(offset * int(celda.col / offset), offset * int(celda.col / offset) + offset):
        for j in range(offset * int(celda.row / offset), offset * int(celda.row / offset) + offset):
            if not celda.col == i and not celda.row == i:
                celda.discard(sudoku[j + i * Celda.tableSize].val)
            if len(celda.posibleValues) == 1:
                celda.val = celda.posibleValues
    return celda

def propagateConstraints(sudoku: list[list[Celda]]):
    for fila in range(Celda.tableSize):
        for col in range(Celda.tableSize):
            sudoku[fila + col * Celda.tableSize] = applyConstraint(sudoku, sudoku[fila + col * Celda.tableSize])
            if isinstance(sudoku[0], PygameCell):
                pygame.time.wait(wait_milli)
                sudoku[fila + col * Celda.tableSize].draw()
    return sudoku

def main():
    sudoku = loadSudoku(sys.argv[1], Celda)
    sudoku = busqueda(sudoku)
    for fila in range(Celda.tableSize):
        for col in range(Celda.tableSize):
            print(sudoku[fila + col * Celda.tableSize].posibleValues)
    

if __name__ == "__main__":
    main()
