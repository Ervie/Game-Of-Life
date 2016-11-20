import pygame
import random
import math as math

class GameOfLife2D(object):
    """Main class displaying board and handling events"""

    WINDOW_WIDTH = 1300
    WINDOW_HEIGHT = 720

    GRID_OFFSET_X = 0
    GRID_OFFSET_Y = 192

    CELL_SIZE = 30

    BACKGROUND_COLOR = (255, 255, 255)

    ALIVE_COLOR = (255, 0, 0)
    DEAD_COLOR = (0, 0, 0)
    
    def __init__(self):
        """Initialize obligatory components"""
       
        # Matrices with cells
        self.cellMatrix = []
        self.nextGenerationMatrix = []

        # Timer
        self.clock = pygame.time.Clock()
        self.speed = 3;
        self.fps = 4;

        # Border modificator
        self.bordersUp = True

        # Calculate rows and columns number
        self.rows = int(round((self.WINDOW_HEIGHT - self.GRID_OFFSET_X - self.GRID_OFFSET_Y) / (self.CELL_SIZE + 1)))
        self.columns = int(round((self.WINDOW_WIDTH - 2 * self.GRID_OFFSET_X ) / (self.CELL_SIZE + 1)))

        self.InitMatrix()
        self.generationCounter = 0

        pygame.init()
        pygame.display.set_caption("Game Of Life - Bartlomiej Buchala 2016")

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.screen.fill(self.BACKGROUND_COLOR)
        self.DrawText()
        self.DrawGrid(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)

    def Start(self):
        """Game starting method."""
        
        pygame.display.flip()
        
        self.gameUp = True
        self.paused = False
        self.SetRandomState();
        self.DrawCurrentGeneration();
        while self.gameUp == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameUp = False
                elif event.type == pygame.KEYDOWN:
                    self.HandleKeyboardInput(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.HandleMouseInput()
            
            self.DrawCurrentGeneration()
            if (self.paused == False):
                self.clock.tick(self.fps)
                self.CalculateNextGeneration()

    def InitMatrix(self):
        """Create matrices from calculated rows and colums number"""
        self.cellMatrix = [[False for i in xrange(self.columns)] for j in xrange(self.rows)]
        self.nextGenerationMatrix = [[False for i in xrange(self.columns)] for j in xrange(self.rows)]


    def DrawGrid(self, offset_x, offset_y):
        """Draws board"""
        boardWidth = self.WINDOW_WIDTH
        boardHeight = self.WINDOW_HEIGHT - offset_x - offset_y

        black = (200, 200, 200)
        gray = (120, 120, 120)


        # refresh
        pygame.display.flip()

    def DrawCurrentGeneration(self):
        """Prints current generation on grid"""
        for r in xrange(self.rows):
            for c in xrange(self.columns):

                # rectangle of cell to fill
                rect = (c * (self.CELL_SIZE + 1)  + self.GRID_OFFSET_X + 1, 
                    r * (self.CELL_SIZE + 1) + self.GRID_OFFSET_Y + 1, 
                    self.CELL_SIZE, self.CELL_SIZE)

                if self.cellMatrix[r][c] == True:
                    pygame.draw.rect(self.screen, self.ALIVE_COLOR, rect)
                elif self.cellMatrix[r][c] == False:
                    pygame.draw.rect(self.screen, self.DEAD_COLOR, rect)

        # draw updated text as well
        self.UpdateText()
        # refresh
        pygame.display.flip()

    def SetRandomState(self):
        """Randomly sets cell to be dead or alive"""
        aliveProbability = 0.2
        
        for c in xrange(0, self.columns):
            for r in xrange(0, self.rows):
                if aliveProbability > random.random():
                    self.cellMatrix[r][c] = True
                else:
                    self.cellMatrix[r][c] = False

        self.generationCounter = 0;
    
    def ResetGrid(self):
        """Sets all cells to dead"""
        for r in xrange(0, self.rows):
            for c in xrange(0, self.columns):
                self.cellMatrix[r][c] = False
                self.nextGenerationMatrix[r][c] = False
        self.generationCounter = 0;
        self.paused = True

    def ChangeSpeed(self, speedUp):
        """Speed up or slow down generation changing"""
        if speedUp == True:
            if (self.speed < 5):
                self.speed += 1
        elif speedUp == False:
            if (self.speed > 0):
                self.speed -= 1

        self.fps = pow(2, self.speed)
        print(self.speed)

    def CalculateNextGeneration(self):
        """Revive or put cells to death depending on neighbour count"""
        for row in xrange(0, self.rows):
            for column in xrange(0, self.columns):

                neighbours = self.GetNeighboursCount(row, column)

                # for alive cells
                if self.cellMatrix[row][column] == True:
                    # die of under-popularion or overcrowding
                    if neighbours < 2 or neighbours > 3:
                        self.nextGenerationMatrix[row][column] = False
                    else:
                        self.nextGenerationMatrix[row][column] = True


                # for dead cells
                else :
                    if neighbours == 3:
                        self.nextGenerationMatrix[row][column] = True

        # set the matrix to be the new state
        for row in xrange(self.rows):
            for column in xrange(self.columns):
                self.cellMatrix[row][column]  = self.nextGenerationMatrix[row][column] 

        self.generationCounter += 1;
    
    def GetNeighboursCount(self, currentRow, currentColumn):
        """Calculate count of alive neighbours"""
        neigboursArray = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        aliveNeighbours = 0
		
        if self.bordersUp == True:
            for x,y in neigboursArray:
                row = currentRow + x
                column = currentColumn + y
                if row >= 0 and column >= 0 and row < self.rows and column < self.columns:
                    if self.cellMatrix[row][column] == True:
                        aliveNeighbours += 1
        else:
            for x,y in neigboursArray:
                row = currentRow + x
                column = currentColumn + y
                
                if self.cellMatrix[row % self.rows][column % self.columns] == True:
                    aliveNeighbours += 1

        return aliveNeighbours

    def DrawText(self):
        """Write information about inpu and current modificators"""

        titleText = "Game of Life"
        controlsText = ['Sterowanie:',
            'R - resetowanie planszy', 
            'D - losowy uklad', 
            'S/Spacja - zatrzymanie/wznowienie',
            'B - aktywacja/dezaktywacja scian',
            'Up/Down - zmiana tempa, Right - przejscie o 1 generacje',
            'Q - wyjscie']
        configText = ['Obecne ustawienia:',
            'Tempo: ', 
            'Obecna generacja:',
            'Sciany:']
        
        font = pygame.font.SysFont('Harrington', 70, True)
        text = font.render(titleText, 1, (255, 0, 0))
        self.screen.blit(text, (350, 0))

        font = pygame.font.SysFont('DejaVu Sans Mono', 20)
        offset_y = 20

        for line in controlsText:
            text = font.render(line, True, (120, 155, 220))
            self.screen.blit(text, (20, offset_y))
            offset_y += 20

        offset_y = 20
        for line in configText:
            text = font.render(line, True, (120, 155, 220))
            self.screen.blit(text, (1000, offset_y))
            offset_y += 20

    def UpdateText(self):
        """Updates text which changes during game"""

        font = pygame.font.SysFont('DejaVu Sans Mono', 25)
        offset_y = 40
        
        # draw empty rectangle over old text
        rect = (1200, offset_y, 1250, offset_y + 20)
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, rect)

        # Tempo
        text = font.render(str(self.speed), True, (120, 155, 220))
        self.screen.blit(text, (1200, offset_y))
        offset_y += 20

        # Generation counter

        rect = (1200, offset_y, 1250, offset_y + 20)
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, rect)

        text = font.render(str(self.generationCounter), True, (120, 155, 220))
        self.screen.blit(text, (1200, offset_y))
        offset_y += 20

        # BorderMode

        if self.bordersUp == True:
            borderText = "Aktywne"
        else:
            borderText = "Nieaktywne"

        rect = (1200, offset_y, 1250, offset_y + 20)
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, rect)

        text = font.render(borderText, True, (120, 155, 220))
        self.screen.blit(text, (1200, offset_y))

    def HandleKeyboardInput(self, event):
        """Read user input and handles it"""
        if (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
            self.gameUp = False
        elif event.key == pygame.K_r:
            print("Reseting grid.")
            self.ResetGrid()
        elif event.key == pygame.K_d:
            print("Randomizing grid.")
            self.SetRandomState()
        elif event.key == pygame.K_b:
            if self.bordersUp == False:
                print("Borders up.")
                self.bordersUp = True
            else:
                print("Borders down.")
                self.bordersUp = False
        elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
            if self.paused == False:
                print("Game stopped.")
                self.paused = True
            else:
                print("Game resumed.")
                self.paused = False
        elif event.key == pygame.K_UP:
            print("Speed up")
            self.ChangeSpeed(True)
        elif event.key == pygame.K_DOWN:
            print("Slow down")
            self.ChangeSpeed(False)
        elif event.key == pygame.K_RIGHT:
            print("Advance 1 generation")
            self.paused = True;
            self.CalculateNextGeneration()

    def HandleMouseInput(self):
        """Handle user clicks"""

        if (not pygame.MOUSEBUTTONDOWN):
            return 0

        # mouse position when clicked
        x_mouse, y_mouse = pygame.mouse.get_pos()

        # event outside the cell borders, ignore it
        if (x_mouse > self.WINDOW_WIDTH
            or y_mouse > self.WINDOW_HEIGHT - self.GRID_OFFSET_X
            or x_mouse < self.GRID_OFFSET_X or y_mouse < self.GRID_OFFSET_Y):
            return 0

        cellWithBorderSize = self.CELL_SIZE + 1

        # calculate indexes
        index_x = int(math.floor((x_mouse - self.GRID_OFFSET_X) / cellWithBorderSize))
        index_y = int(math.floor((y_mouse - self.GRID_OFFSET_Y) / cellWithBorderSize))
        off_x = x_mouse / cellWithBorderSize * cellWithBorderSize
        off_y =  y_mouse / cellWithBorderSize * cellWithBorderSize
        rect = (off_x, off_y, self.CELL_SIZE, self.CELL_SIZE)


        if self.cellMatrix[index_y][index_x] == True:
            self.cellMatrix[index_y][index_x] = False
        else:
            self.cellMatrix[index_y][index_x] = True


    