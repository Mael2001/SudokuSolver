from tablero import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse

#const globals

def visual():
    if len(sys.argv) == 1:
        print("usage: %s [--delay DELAY] <sudoku_file>", file=sys.stderr)
        exit(1)
    for i in range(len(sys.argv)):
        if "--delay" == sys.argv[i]:
            Tablero.delay = int(sys.argv[i + 1])

    pygame.init()
    sudoku = Tablero(sys.argv[-1], PygameCell)
    PygameCell.sizeFactor = 10 * 9 / sudoku.tableSize
    PygameCell.screen = pygame.display.set_mode((sudoku.tableSize**2 * PygameCell.sizeFactor, sudoku.tableSize**2 * PygameCell.sizeFactor))
    PygameCell.size = sudoku.tableSize * PygameCell.sizeFactor
    solved = False
    while True:
        if not solved:
            sudoku.draw()
            sudoku.resolver()
            solved = True

if __name__ == "__main__":
    visual()
