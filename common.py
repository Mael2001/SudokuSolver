import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from pygame.locals import *
import copy

def calcSubMatrixIndexOffset():
    return int(math.sqrt(Celda.tableSize))

class Celda:
    tableSize = 9
    units = []
    nodeCount = 0
    def __init__(self, val: str, row: int, col: int, tableSize: int = None):
        self.val = val
        self.row = row
        self.col = col
        if tableSize is None:
            self.tableSize = Celda.tableSize
        #self.posibleValues = { i for i in range(1, self.tableSize + 1) } if val is None else { i for i in range(val, val+1) }
        self.posibleValues = ""
        for x in range(1, Celda.tableSize + 1):
            self.posibleValues += str(x)
        self.peers = set()
        self.units = []
        unit_col = []
        for column in range(Celda.tableSize):
            new_index = self.row + column * Celda.tableSize
            if not new_index == self.row + self.col * Celda.tableSize:
                self.peers.add(new_index)
                unit_col.append(new_index)
        self.units.append(unit_col)
        unit_row = []
        for fila in range(Celda.tableSize):
            new_index = fila + self.col * Celda.tableSize
            if not new_index == self.row + self.col * Celda.tableSize:
                self.peers.add(new_index)
                unit_row.append(new_index)
        self.units.append(unit_row)
        offset = calcSubMatrixIndexOffset()
        unit_sub_matrix = []
        for i in range(offset * int(self.col / offset), offset * int(self.col / offset) + offset):
            for j in range(offset * int(self.row / offset), offset * int(self.row / offset) + offset):
                new_index = j + i * Celda.tableSize
                if not new_index == self.row + self.col * Celda.tableSize:
                    self.peers.add(new_index)
                    unit_sub_matrix.append(new_index)
        self.units.append(unit_sub_matrix)
        

    def discard(self, v):
        if v is None:
            return
        self.posibleValues = self.posibleValues.replace(v, '')


class PygameCell(Celda):
    surfaceArray = []
    size = Celda.tableSize * 3
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
            'text': pygame.font.SysFont(None, int(Celda.tableSize * 3)),
            })

    def __getitem__(self, i):
        return type(self)

    def draw(self):
        #PygameCell.screen.blit(self.outline, (self.row * PygameCell.size, self.col * PygameCell.size))
        arr = PygameCell.surfaceArray[self.row + self.col * Celda.tableSize]
        text = arr['text']
        fill = arr['fill']
        fill.fill((255,255,255))
        PygameCell.screen.blit(fill, (self.row * (PygameCell.size) + 1, self.col * (PygameCell.size) + 1))
        num_values = math.sqrt(Celda.tableSize)
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
