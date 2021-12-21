import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from pygame.locals import *

class Celda:
    tableSize = 9
    def __init__(self, val: int, row: int, col: int, tableSize: int = None):
        self.val = val
        self.row = row
        self.col = col
        if tableSize is None:
            self.tableSize = Celda.tableSize
        self.posibleValues = { i for i in range(1, self.tableSize + 1) } if val is None else { i for i in range(val, val+1) }
    def discard(self, v):
        self.posibleValues.discard(v)


class PygameCell(Celda):
    size = Celda.tableSize * 3
    screen = None
    #all_cells = pygame.sprite.RenderUpdates()
    def __init__(self, val: int, row: int, col: int):
        super(PygameCell, self).__init__(val, row, col)
        self.size = (PygameCell.size - 2, PygameCell.size - 2)
        self.fill = pygame.Surface(self.size)
        self.fill.fill((255,255,255))
        self.outline = pygame.Surface(self.size)
        self.outline.fill((255,0,0))
        self.position = (self.row * PygameCell.size, self.col * PygameCell.size)
        self.text = pygame.font.SysFont(None, int(Celda.tableSize * 3))

    def __getitem__(self, i):
        return type(self)

    def draw(self):
        #PygameCell.screen.blit(self.outline, (self.row * PygameCell.size, self.col * PygameCell.size))
        PygameCell.screen.blit(self.fill, (self.row * (PygameCell.size) + 1, self.col * (PygameCell.size) + 1))
        num_values = math.sqrt(Celda.tableSize)
        square_size = PygameCell.size / num_values
        if self.val is not None:
            self.text = pygame.font.SysFont(None, 65)
            digit = self.text.render(str(self.val), True, (255,0,0))
            PygameCell.screen.blit(digit, (self.row * PygameCell.size + int(3/num_values) * square_size + 8, self.col * PygameCell.size + int(3/num_values) * square_size - 10))
        else:
            for val in self.posibleValues:
                digit = self.text.render(str(val), True, (0,0,0))
                PygameCell.screen.blit(digit, (self.row * PygameCell.size + ((val - 1) % num_values) * square_size + 8, self.col * PygameCell.size + int((val - 1) / num_values) * square_size + 3))
        pygame.display.flip()
