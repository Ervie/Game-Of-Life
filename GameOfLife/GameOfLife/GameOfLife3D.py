from visual import *

class GameOfLife3D(object):
    """Main class displaying board and handling events (3d version)"""

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    def __init__(self):
        """Initialize obligatory components"""
         # Matrices with cells
        self.cellMatrix = []
        self.nextGenerationMatrix = []

        # number of elements in dimensions
        self.columns = 5
        self.rows = 5
        self.layers = 5
        
        
        self.InitMatrix()
        self.generationCounter = 0

        self.DrawCube()

    def Start(self):
        """Game starting method."""

        self.SetRandomState()
        self.gameUp = True
        self.paused = False

        while(self.gameUp):
            rate(1)
            if scene.kb.keys:
                key = scene.kb.getkey()
                HandleKeyboardInput(key)
            self.DrawCurrentGeneration()

            if (self.paused == False):
                self.CalculateNextGeneration()

    def InitMatrix(self):
        """Create matrices from calculated rows and colums number"""
        self.cellMatrix = [[[False for k in xrange(self.columns)] for j in xrange(self.rows)] for i in xrange(self.layers)]
        self.nextGenerationMatrix = [[[False for k in xrange(self.columns)] for j in xrange(self.rows)] for i in xrange(self.layers)]

    def DrawCube(self):
        """Draws board"""
        scene = display(title="Game of Life - Bartlomiej Buchala 2016", x=0, y=0, width = self.WINDOW_WIDTH, height = self.WINDOW_HEIGHT, range = 10, background = color.white, center = (0, 0, 0))

        for i in xrange(self.rows):
            for j in xrange(self.columns):
                for k in xrange(self.layers):
                    box(pos = (i * 1.3,j * 1.3,k * 1.3), length = 0.5, width = 0.5, height = 0.5, color = color.black)

    def ResetGrid(self):
        """Sets all cells to dead"""
        for r in xrange(0, self.rows):
            for c in xrange(0, self.columns):
                for l in xrange(0, self.layers):
                    self.cellMatrix[r][c][l] = False
                    self.nextGenerationMatrix[r][c][l] = False
        self.generationCounter = 0;
        self.paused = True

    def SetRandomState(self):
        """Randomly sets cell to be dead or alive"""
        aliveProbability = 0.2
        
        for c in xrange(0, self.columns):
            for r in xrange(0, self.rows):
                for l in xrange(0, self.layers):
                    if aliveProbability > random.random():
                        self.cellMatrix[r][c][l] = True
                    else:
                        self.cellMatrix[r][c][l] = False

        self.generationCounter = 0;

    def DrawCurrentGeneration(self):
        """Prints current generation on grid"""
        for r in xrange(self.rows):
            for c in xrange(self.columns):
                for l in xrange(self.layers):

                    if (self.cellMatrix[r][c][l] == False):
                        box(pos = (r * 1.3,c * 1.3,l * 1.3), length = 0.5, width = 0.5, height = 0.5, color = color.black)
                    else:
                        box(pos = (r * 1.3,c * 1.3,l * 1.3), length = 0.5, width = 0.5, height = 0.5, color = color.red)



    def CalculateNextGeneration(self):
        """Revive or put cells to death depending on neighbour count"""
        for row in xrange(0, self.rows):
            for column in xrange(0, self.columns):
                for layer in xrange(0, self.layers):

                    neighbours = self.GetNeighboursCount(row, column, layer)

                    # for alive cells
                    if self.cellMatrix[row][column][layer] == True:
                        # die of under-popularion or overcrowding
                        if neighbours < 2 or neighbours > 3:
                            self.nextGenerationMatrix[row][column][layer] = False
                        else:
                            self.nextGenerationMatrix[row][column][layer] = True


                    # for dead cells
                    else :
                        if neighbours == 3:
                            self.nextGenerationMatrix[row][column][layer] = True

        # set the matrix to be the new state
        for row in xrange(self.rows):
            for column in xrange(self.columns):
                for layer in xrange(self.layers):
                    self.cellMatrix[row][column][layer]  = self.nextGenerationMatrix[row][column][layer] 

        self.generationCounter += 1;

    def GetNeighboursCount(self, currentRow, currentColumn, currentLayer):
        """Calculate count of alive neighbours"""
        neigboursArray = [(-1,-1, -1), (-1, 0, -1), (-1, 1, -1), (0, -1, -1), (0, 1, -1), (1, -1, -1), (1, 0, -1), (1, 1, -1), (0, 0, -1),
                          (-1,-1,0), (-1, 0,0), (-1, 1,0), (0, -1,0), (0, 1,0), (1, -1,0), (1, 0,0), (1, 1,0),
                          (-1,-1, 1), (-1, 0, 1), (-1, 1, 1), (0, -1, 1), (0, 1, 1), (1, -1, 1), (1, 0, 1), (1, 1, 1), (0, 0, 1)]

        aliveNeighbours = 0
		
        for x,y,z in neigboursArray:
            row = currentRow + x
            column = currentColumn + y
            layer = currentLayer + z
            if row >= 0 and column >= 0 and layer > 0 and row < self.rows and column < self.columns and layer < self.layers:
                if self.cellMatrix[row][column][layer] == True:
                    aliveNeighbours += 1

        return aliveNeighbours

    def HandleKeyboardInput(self, key):
        """Read user input and handles it"""
        if (key == 'q'):
            self.gameUp = False
        elif event.key == pygame.K_r:
            self.ResetGrid()
        elif event.key == pygame.K_d:
            self.SetRandomState()
        elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
            if self.paused == False:
                self.paused = True
            else:
                self.paused = False
        elif event.key == pygame.K_RIGHT:
            self.paused = True;
            self.CalculateNextGeneration()
