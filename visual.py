from solver import *
from common import Celda

#const globals

def visual():
    pygame.init()
    Celda.tableSize = 9
    PygameCell.size = Celda.tableSize * 10
    PygameCell.screen = pygame.display.set_mode((PygameCell.size * Celda.tableSize, PygameCell.size * Celda.tableSize))
    sudoku = loadSudoku(sys.argv[1], PygameCell)
    """
    for i in range(Celda.tableSize):
        row = []
        for j in range(Celda.tableSize):
            row.append(PygameCell(None, i, j))
        sudoku.append(row)
    """
    i = 1
    propagated = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                exit(0)
            if event.key == K_r:
                sudoku[0].discard(i)
                i += 1
                if len(sudoku[0].posibleValues) == 1:
                    sudoku[0].val = i
        elif event.type == QUIT:
            exit(0)
        for c in sudoku:
            c.draw()
        if not propagated:
            for i, cell in enumerate(copy.deepcopy(sudoku)):
                if cell.val is not None: assign(sudoku, i, cell.val)
            #propagateConstraints(sudoku)
            propagated = True
            busqueda(sudoku)
    print(Celda.nodeCount)

if __name__ == "__main__":
    visual()
