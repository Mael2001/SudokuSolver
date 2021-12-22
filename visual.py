from solver import *
#from common import Celda
from cell import *

#const globals

def visual():
    pygame.init()
    sudoku = Tablero(sys.argv[1], PygameCell)
    PygameCell.sizeFactor = 10 * 9 / sudoku.tableSize
    PygameCell.screen = pygame.display.set_mode((sudoku.tableSize**2 * PygameCell.sizeFactor, sudoku.tableSize**2 * PygameCell.sizeFactor))
    PygameCell.size = sudoku.tableSize * PygameCell.sizeFactor
    """
    for i in range(Celda.tableSize):
        row = []
        for j in range(Celda.tableSize):
            row.append(PygameCell(None, i, j))
        sudoku.append(row)
    """
    solved = False
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    exit(0)
            elif event.type == QUIT:
                exit(0)
        if not solved:
            sudoku.draw()
            sudoku.resolver()
            solved = True

if __name__ == "__main__":
    visual()
