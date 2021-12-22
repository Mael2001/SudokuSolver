from cell import *

wait_milli = 0

class Tablero:
    def __init__(self, fileName, CellType=Cell):
        self.solved = False
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
        self.cells = dict((s, CellType(s, self.digits if self.grid_values[s] == '0' else self.grid_values[s])) for s in self.squares)
        #self.cells = dict((s, CellType(s, self.digits)) for s in self.squares)

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
        if isinstance(cells[s], PygameCell):
            cells[s].draw()
            pygame.time.wait(wait_milli)
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

    def __display(self, cells):
        width = 1+max(len(cells[s].values) for s in self.squares)
        line = '+'.join(['-'*(width*4)]*4)
        for r in self.rows:
            print(''.join(cells[r+c].values.center(width)+('|' if c in '48C' else '')
                          for c in self.cols))
            if r in 'DHL': print(line)

    def draw(self):
        for cell in self.cells.items():
            cell[1].draw()


    def resolver(self):
        if self.solved:
            return True
        for s,d in self.grid_values.items():
            if d in self.digits and not self.__assign(self.cells, s, d):
                return False
        self.solved = not self.__busqueda(self.cells) is False
