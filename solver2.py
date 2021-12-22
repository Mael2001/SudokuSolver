import sys
import re
import numpy as np
import copy
from utils import *

        
def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
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
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [d for d in grid]
    return dict(zip(squares, chars))

def search(values):
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares): 
        return values ## Solved!
## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(copy.deepcopy(values), s, d)) 
        for d in values[s])

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    #other_values = values[s].copy()
    #other_values.discard(d)
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d, '')
    #values[s].discard(d)
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
	    # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

#digits   = { i for i in range(1, tableSize + 1) }
digits     = '123456789ABCDEFX'
rows     = 'ABCDEFGHIJKLMNOP'
cols     = '123456789ABCDEFX'
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABCD','EFGH','IJKL', 'MNOP') for cs in ('1234','5678','9ABC', 'DEFX')])
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
