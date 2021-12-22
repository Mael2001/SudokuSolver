import pygame
import math
import numpy as np
import sys
import re
from utils import *
import copy

sys.setrecursionlimit(150000)

class Cell:
    def __init__(self, square, values):
        self.row = rowToColIndex(square[0])
        self.col = hexToInt(square[1]) - 1
        self.values = values

    def setValues(self, values):
        self.values = values

class PygameCell(Cell):
    tableSize = 9
    surfaceArray = []
    sizeFactor = 10
    size = tableSize * sizeFactor
    screen = None
    def __init__(self, square, values):
        super(PygameCell, self).__init__(square, values)
        self.size = ((PygameCell.size - 2, PygameCell.size - 2))
        PygameCell.surfaceArray.append({
            'fill': pygame.Surface(self.size),
        #self.outline = pygame.Surface(self.size)
        #self.outline.fill((255,0,0))
            'position' :(self.row * PygameCell.size, self.col * PygameCell.size),
            'text': pygame.font.SysFont(None, int((9/(PygameCell.size/PygameCell.sizeFactor)) * 23)),
            })

    def __getitem__(self, i):
        return type(self)

    def draw(self):
        arr = PygameCell.surfaceArray[self.row + self.col * int(PygameCell.size/PygameCell.sizeFactor)]
        text = arr['text']
        fill = arr['fill']
        fill.fill((255,255,255))
        PygameCell.screen.blit(fill, (self.row * (PygameCell.size) + 1, self.col * (PygameCell.size) + 1))
        num_values = math.sqrt(PygameCell.size/PygameCell.sizeFactor)
        square_size = PygameCell.size / num_values
        if len(self.values) == 1:
            text = pygame.font.SysFont(None, 65)
            digit = text.render(str(hexToInt(self.values)), True, (255,0,0))
            PygameCell.screen.blit(digit, (self.row * PygameCell.size + int(square_size * 5/4), self.col * PygameCell.size + int(square_size*5/6)))
        else:
            for v in self.values:
                val = hexToInt(v)
                digit = text.render(str(hexToInt(v)), True, (0,0,0))
                PygameCell.screen.blit(digit, (self.row * PygameCell.size + ((int(val) - 1) % num_values) * square_size + 8, self.col * PygameCell.size + int((int(val) - 1) / num_values) * square_size + 3))
        pygame.display.flip()
