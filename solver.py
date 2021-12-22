import sys
from tablero import *

def main():
    if len(sys.argv) == 1:
        print("usage: %s [--time] [-n] <sudoku_file>", file=sys.stderr)
        exit(1)
    sudoku = Tablero(sys.argv[-1])

    sudoku.resolver().toCsv()

    for i in range(len(sys.argv)):
        if "--time" == sys.argv[i]:
            print("tiempo: %.4f ms" % (sudoku.elps_time * 1000))
        if "-n" == sys.argv[i]:
            print("nodos recorridos: %i" % (sudoku.nodeCount))

if __name__ == "__main__":
    main()
