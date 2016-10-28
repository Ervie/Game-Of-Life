import pygame
import random

class GameOfLife(object):
    """Main class displaying board and handling events"""

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    GRID_OFFSET_X = 80
    GRID_OFFSET_Y = 150

    CELL_SIZE = 15

    BACKGROUND_COLOR = (255, 255, 255)
    
    def __init__(self):
        """Initialize obligatory components"""
       
        self.cellMatrix = []
       
        # Calculate rows and columns number
        self.rows = round((self.WINDOW_HEIGHT - self.GRID_OFFSET_X - self.GRID_OFFSET_Y) / (self.CELL_SIZE + 1))
        self.columns = round((self.WINDOW_WIDTH - 2 * self.GRID_OFFSET_X ) / (self.CELL_SIZE + 1))

        self.initMatrix()

        pygame.init()
        pygame.display.set_caption("Game Of Life - Bartlomiej Buchala 2016")

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.screen.fill(self.BACKGROUND_COLOR)

        
        self.drawGrid(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)

    def start(self):
        """Game starting method."""
        
        pygame.display.flip()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def initMatrix(self):
        """Create matrix from calculated rows and colums number"""
        self.cellMatrix = [[0 for i in range(self.rows)] for j in range(self.columns)]

        #for i in range(self.rows):
        #    self.cellMatrix.append([])

        #    for j in range(self.columns):
        #        self.cellMatrix[j].append(False)

    def drawGrid(self, offset_x, offset_y):
        """Draws board"""
        boardWidth = self.WINDOW_WIDTH - offset_x * 2
        boardHeight = self.WINDOW_HEIGHT - offset_x - offset_y

        dead = (200, 200, 200)
        alive = (120, 120, 120)
        
        # draw vertical lines
        for x in range(offset_x + 10, boardWidth + offset_x, 10):
            pygame.draw.line(self.screen, dead, (x, offset_y), 
                (x, offset_y + boardHeight), 1)

        # draw horizontal lines
        for y in range(offset_y + 10, boardHeight + offset_y, 10):
            pygame.draw.line(self.screen, dead, (offset_x, y), 
                (boardWidth + offset_x, y), 1)

        # draw the thick borders of the grid: top, buttom, left, right
        pygame.draw.line(self.screen, alive, (offset_x - 2, offset_y - 1),
            (offset_x + boardWidth + 2, offset_y - 1), 3)
        pygame.draw.line(self.screen, alive, (offset_x - 2, offset_y + 
            boardHeight + 1), (offset_x + boardWidth + 2, offset_y + boardHeight + 1), 3)
        pygame.draw.line(self.screen, alive, (offset_x - 1, offset_y - 1), 
            (offset_x - 1, offset_y + boardHeight + 1), 3)
        pygame.draw.line(self.screen, alive, (offset_x + boardWidth + 1, 
            offset_y - 1), (offset_x + 1 + boardWidth, offset_y + boardHeight + 1), 3)

        # refresh
        pygame.display.flip()
                    


