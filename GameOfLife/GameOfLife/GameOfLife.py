﻿import pygame
import random

class GameOfLife(object):
    """Main class displaying board and handling events"""

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    GRID_OFFSET_X = 80
    GRID_OFFSET_Y = 150

    CELL_SIZE = 15

    BACKGROUND_COLOR = (255, 255, 255)

    ALIVE_COLOR = (255, 0, 0)
    DEAD_COLOR = (0, 0, 0)
    
    def __init__(self):
        """Initialize obligatory components"""
       
        self.cellMatrix = []
        self.nextGenerationMatrix = []
        self.clock = pygame.time.Clock()

        # Calculate rows and columns number
        self.rows = round((self.WINDOW_HEIGHT - self.GRID_OFFSET_X - self.GRID_OFFSET_Y) / (self.CELL_SIZE + 1))
        self.columns = round((self.WINDOW_WIDTH - 2 * self.GRID_OFFSET_X ) / (self.CELL_SIZE + 1))

        self.InitMatrix()

        pygame.init()
        pygame.display.set_caption("Game Of Life - Bartlomiej Buchala 2016")

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.screen.fill(self.BACKGROUND_COLOR)
        self.DrawGrid(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)

    def Start(self):
        """Game starting method."""
        
        pygame.display.flip()

        running = True
        self.SetRandomState();
        self.DrawCurrentGeneration();
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.clock.tick(1)
            self.CalculateNextGeneration()
            self.DrawCurrentGeneration()

    def InitMatrix(self):
        """Create matrices from calculated rows and colums number"""
        self.cellMatrix = [[False for i in range(self.columns)] for j in range(self.rows)]
        self.nextGenerationMatrix = [[False for i in range(self.columns)] for j in range(self.rows)]


    def DrawGrid(self, offset_x, offset_y):
        """Draws board"""
        boardWidth = self.WINDOW_WIDTH - offset_x * 2
        boardHeight = self.WINDOW_HEIGHT - offset_x - offset_y

        black = (200, 200, 200)
        gray = (120, 120, 120)
        
        # draw vertical lines
        for x in range(offset_x + 10, boardWidth + offset_x, 10):
            pygame.draw.line(self.screen, black, (x, offset_y), 
                (x, offset_y + boardHeight), 1)

        # draw horizontal lines
        for y in range(offset_y + 10, boardHeight + offset_y, 10):
            pygame.draw.line(self.screen, black, (offset_x, y), 
                (boardWidth + offset_x, y), 1)

        # draw borders
        pygame.draw.line(self.screen, gray, (offset_x - 2, offset_y - 1),
            (offset_x + boardWidth + 2, offset_y - 1), 3)
        pygame.draw.line(self.screen, gray, (offset_x - 2, offset_y + 
            boardHeight + 1), (offset_x + boardWidth + 2, offset_y + boardHeight + 1), 3)
        pygame.draw.line(self.screen, gray, (offset_x - 1, offset_y - 1), 
            (offset_x - 1, offset_y + boardHeight + 1), 3)
        pygame.draw.line(self.screen, gray, (offset_x + boardWidth + 1, 
            offset_y - 1), (offset_x + 1 + boardWidth, offset_y + boardHeight + 1), 3)

        # refresh
        pygame.display.flip()

    def DrawCurrentGeneration(self):
        """Prints current generation on grid"""
        for r in range(self.rows):
            for c in range(self.columns):

                # rectangle of cell to fill
                rect = (c * (self.CELL_SIZE + 1)  + self.GRID_OFFSET_X + 1, 
                    r * (self.CELL_SIZE + 1) + self.GRID_OFFSET_Y + 1, 
                    self.CELL_SIZE, self.CELL_SIZE)

                if self.cellMatrix[r][c] == True:
                    pygame.draw.rect(self.screen, self.ALIVE_COLOR, rect)
                elif self.cellMatrix[r][c] == False:
                    pygame.draw.rect(self.screen, self.DEAD_COLOR, rect)
        # refresh
        pygame.display.flip()

    def SetRandomState(self):
        """Randomly sets cell to be dead or alive"""
        aliveProbability = 0.2
        
        for c in range(0, self.columns):
            for r in range(0, self.rows):
                if aliveProbability > random.random():
                    self.cellMatrix[r][c] = True
                else:
                    self.cellMatrix[r][c] = False
    
    def ResetGrid(self):
        """Sets all cells to dead"""
        for r in range(self.rows):
            for c in range(self.columns):
                self.cellMatrix[r][c] = False

    def CalculateNextGeneration(self):
        """Revive or put cells to death depending on neighbour count"""
        for row in range(0, self.rows):
            for column in range(0, self.columns):

                neighbours = self.GetNeighboursCount(row, column)

                # for alive cells
                if self.cellMatrix[row][column] == True:
                    # die of under-popularion or overcrowding
                    if neighbours < 2 or neighbours > 3:
                        self.nextGenerationMatrix[row][column] = False

                # for dead cells
                else :
                    if neighbours == 3:
                        self.nextGenerationMatrix[row][column] = True

        # set the matrix to be the new state
        for row in range(self.rows):
            for column in range(self.columns):
                self.cellMatrix[row][column]  = self.nextGenerationMatrix[row][column] 
    
    def GetNeighboursCount(self, currentRow, currentColumn):
        """Calculate count of alive neighbours"""
        neigboursArray = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        aliveNeighbours = 0
		
        for x,y in neigboursArray:
            row = currentRow + x
            column = currentColumn + y
            if row >= 0 and column >= 0 and row < self.rows and column < self.columns:
                if self.cellMatrix[row][column] == True:
                    aliveNeighbours += 1

        return aliveNeighbours

    def HandleKeyboardInput(self, event):
        """Read user input and handles it"""
        if (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
            pygame.quit()
        elif event.key == pygame.K_r:
            print("Reseting grid.")
            self.ResetGrid()



    