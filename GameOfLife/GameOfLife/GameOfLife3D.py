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
        self.columns = 10
        self.rows = 10
        self.layers = 10
        
        
        self.InitMatrix()
        self.generationCounter = 0

        self.DrawCube()

    def Start(self):
        """Game starting method."""

        #while(True):
            # TODO: Pętelka
            # self.DrawCurrentGeneration()

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

