import sys
import re
import numpy as np
import copy
from utils import *
from cell import *

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    #for v in values.items():
        #print(v)
    return values

def loadSudoku(fileName: str):
    lines = open(fileName).readlines()
    for c in lines:
        print(c)
    if not len(lines) == len(lines[0].replace("\n", "").split(",")):
        exit(1)
    lineas = None
    for line in lines:
        if lineas is None:
            lineas = [line.replace("\n", "").split(",")]
        else:
            lineas = np.append(lineas, [line.replace("\n", "").split(",")], axis=0)
    lines = np.transpose(lineas)
    sudoku = ""
    for i in range(len(lines)):
        fila = lines[i]
        for j in range(len(fila)):
            numero = re.search("[0-9]+", fila[j])
            numero = '0' if numero is None else intToHex(int(numero.string))
            sudoku += numero
    return sudoku

def grid_values(grid):
    chars = [d for d in grid]
    return dict(zip(squares, chars))

def search(values):
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares): 
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(copy.deepcopy(values), s, d)) 
        for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def cross(A, B):
    return [a+b for a in A for b in B]

digits     = Cell.digits
rows     =  Cell.rows
cols     = digits
squares  = cross(rows, cols)
unitlist = Cell.unitlist
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*4)]*4)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '48C' else '')
                      for c in cols))
        if r in 'DHL': print(line)

if __name__ == "__main__":
    display(search(parse_grid(loadSudoku(sys.argv[1]))))
