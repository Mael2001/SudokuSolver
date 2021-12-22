import math
import numpy as np
import sys
import re
from utils import *
import copy
def rowToColIndex(c):
    return ord(c) - 65

def getDigits(tableSize):
    if tableSize == 4:
        return '1234'
    if tableSize == 9:
        return '123456789'
    if tableSize == 16:
        return '123456789ABCDEFX'

def getRows(tableSize):
    if tableSize == 4:
        return 'ABCD'
    if tableSize == 9:
        return 'ABCDEFGHI'
    if tableSize == 16:
        return 'ABCDEFGHIJKLMNOP'


def some(seq):
    for e in seq:
        if e: return e
    return False


def cross(A, B):
    return [a+b for a in A for b in B]

class Tablero:
    def __init__(self, fileName):
        lines = open(fileName).readlines()
        for c in lines:
            print(c)
        if not len(lines) == len(lines[0].replace("\n", "").split(",")):
            exit(1)
        self.tableSize = len(lines)
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
        self.digits   = getDigits(self.tableSize)
        self.rows     = getRows(self.tableSize)
        self.cols     = getDigits(self.tableSize)
        self.squares  = cross(self.rows, self.cols)
        x = np.array([c for c in getRows(self.tableSize)]).reshape(-1, int(math.sqrt(self.tableSize)))
        y = np.array([c for c in getDigits(self.tableSize)]).reshape(-1, int(math.sqrt(self.tableSize)))
        self.unitlist = ([cross(self.rows, c) for c in self.cols] +
                        [cross(r, self.cols) for r in self.rows] +
                        [cross(rs, cs) for rs in x for cs in y])
        self.units = dict((s, [u for u in self.unitlist if s in u]) 
                     for s in self.squares)
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s]))
                     for s in self.squares)
        chars = [d for d in sudoku]
        self.grid_values = dict(zip(self.squares, chars))

    def __assign(self, cells, s, d):
        other_values = cells[s].values.replace(d, '')
        if all(self.__eliminate(cells, s, d2) for d2 in other_values):
            return cells
        else:
            return False

    def __eliminate(self, cells, s, d):
        if d not in cells[s].values:
            return cells ## Already eliminated
        cells[s].setValues(cells[s].values.replace(d, ''))
        if len(cells[s].values) == 0:
            return False
        elif len(cells[s].values) == 1:
            d2 = cells[s].values
            if not all(self.__eliminate(cells, s2, d2) for s2 in self.peers[s]):
                return False
        for u in self.units[s]:
            dplaces = [s for s in u if d in cells[s].values]
            if len(dplaces) == 0:
                return False
            elif len(dplaces) == 1:
                if not self.__assign(cells, dplaces[0], d):
                    return False
        return cells

    def __busqueda(self, cells):
        if cells is False:
            return False 
        if all(len(cells[s].values) == 1 for s in self.squares): 
            return cells
        n,s = min((len(cells[s].values), s) for s in self.squares if len(cells[s].values) > 1)
        return some(self.__busqueda(self.__assign(copy.deepcopy(cells), s, d)) 
            for d in cells[s].values)

    def display(self, cells):
        "Display these values as a 2-D grid."
        width = 1+max(len(cells[s].values) for s in self.squares)
        line = '+'.join(['-'*(width*4)]*4)
        for r in self.rows:
            print(''.join(cells[r+c].values.center(width)+('|' if c in '48C' else '')
                          for c in self.cols))
            if r in 'DHL': print(line)

    def resolver(self):
        values = dict((s, Cell(s, self.digits)) for s in self.squares)
        for s,d in self.grid_values.items():
            if d in self.digits and not self.__assign(values, s, d):
                return False
        self.display(self.__busqueda(values))

class Cell:
    def __init__(self, square, values):
        self.row = rowToColIndex(square[0])
        self.col = hexToInt(square[1]) - 1
        self.values = values

    def setValues(self, values):
        self.values = values


    #def __init__(self, row, col, values):
        #self.row = rowToColIndex(row)
        #self.col = col
        #self.values = values

def some(seq):
    for e in seq:
        if e: return e
    return False


if __name__ == "__main__":
    t = Tablero(sys.argv[1])
    t.resolver()



#class Cell:
    #def __init__(self):

class PygameCell(Cell):
    surfaceArray = []
    size = 9 * 3
    screen = None
    #all_cells = pygame.sprite.RenderUpdates()
    def __init__(self, val: str, row: int, col: int):
        super(PygameCell, self).__init__(val, row, col)
        self.size = ((PygameCell.size - 2, PygameCell.size - 2))
        PygameCell.surfaceArray.append({
            'fill': pygame.Surface(self.size),
        #self.outline = pygame.Surface(self.size)
        #self.outline.fill((255,0,0))
            'position' :(self.row * PygameCell.size, self.col * PygameCell.size),
            'text': pygame.font.SysFont(None, int(Cell.tableSize * 3)),
            })

    def __getitem__(self, i):
        return type(self)

    def draw(self):
        #PygameCell.screen.blit(self.outline, (self.row * PygameCell.size, self.col * PygameCell.size))
        arr = PygameCell.surfaceArray[self.row + self.col * Cell.tableSize]
        text = arr['text']
        fill = arr['fill']
        fill.fill((255,255,255))
        PygameCell.screen.blit(fill, (self.row * (PygameCell.size) + 1, self.col * (PygameCell.size) + 1))
        num_values = math.sqrt(Cell.tableSize)
        square_size = PygameCell.size / num_values
        if self.val is not None:
            text = pygame.font.SysFont(None, 65)
            digit = text.render(self.val, True, (255,0,0))
            PygameCell.screen.blit(digit, (self.row * PygameCell.size + int(3/num_values) * square_size + 8, self.col * PygameCell.size + int(3/num_values) * square_size - 10))
        else:
            for v in self.posibleValues:
                val = int(v)
                digit = text.render(v, True, (0,0,0))
                PygameCell.screen.blit(digit, (self.row * PygameCell.size + ((int(val) - 1) % num_values) * square_size + 8, self.col * PygameCell.size + int((int(val) - 1) / num_values) * square_size + 3))
        pygame.display.flip()
