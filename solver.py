import sys 
import math
import numpy as np
import threading
import re
import time
from common import *

sys.setrecursionlimit(150000)
wait_milli = 10

#Codigo inspirado por http://www.norvig.com/sudoku.html
def busqueda(sudoku):
    if sudoku is False:
        return False
    if all(len(cell.posibleValues) == 1 for cell in sudoku):
        return sudoku
    #heuristica
    length, indice = min((len(sudoku[i].posibleValues), i) for i in range(len(sudoku)) if len(sudoku[i].posibleValues) > 1)
    return some(busqueda(assign(copy.deepcopy(sudoku), indice, d)) for d in sudoku[indice].posibleValues)

def assign(sudoku, indice, valor_intento):
    Celda.nodeCount += 1
    demas_valores = sudoku[indice].posibleValues.replace(valor_intento, '')
    if all(eliminate(sudoku, indice, nuevo_intento) for nuevo_intento in demas_valores):
        return sudoku
    else:
        return False

def eliminate(sudoku, indice, valor_intento):
    Celda.nodeCount += 1
    if valor_intento not in sudoku[indice].posibleValues:
        return sudoku
    sudoku[indice].posibleValues = sudoku[indice].posibleValues.replace(valor_intento, '')
    if len(sudoku[indice].posibleValues) == 0:
        return False
    elif len(sudoku[indice].posibleValues) == 1:
        sudoku[indice].val = nuevo_intento = sudoku[indice].posibleValues
        if not all(eliminate(sudoku, nuevo_i, nuevo_intento) for nuevo_i in sudoku[indice].peers):
            return False
    if isinstance(sudoku[0], PygameCell):
        sudoku[indice].draw()
        pygame.time.wait(wait_milli)
    for unit in sudoku[indice].units:
        new_tries = [i for i in unit if valor_intento in sudoku[i].posibleValues]
        if len(new_tries) == 0:
            return False
        elif len(new_tries) == 1:
            if not assign(sudoku, new_tries[0], valor_intento):
                return False
    return sudoku

def some(lista):
    for elem in lista:
        if elem is not False: 
            return elem 
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
    start_time = time.time()
    sudoku = loadSudoku(sys.argv[1], Celda)
    #sudoku = propagateConstraints(sudoku)
    for i, cell in enumerate(sudoku):
        if not cell.val is None: assign(sudoku, i, cell.val)
    sudoku = busqueda(sudoku)
    print("Time: %.4f ms" % ((time.time() - start_time) * 1000))
    print(sudoku)
    #for fila in range(Celda.tableSize):
        #for col in range(Celda.tableSize):
    

if __name__ == "__main__":
    main()
