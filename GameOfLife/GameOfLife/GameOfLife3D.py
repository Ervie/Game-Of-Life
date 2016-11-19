from visual import *

class GameOfLife3D(object):
    """Main class displaying board and handling events (3d version)"""


    def __init__(self):
        """Initialize obligatory components"""

    def Start(self):
        """Game starting method."""

        scene = display(title="Game of Life - Bartlmiej Buchala 2016", x=0, y=0, width = 800, height = 600, range = 10, background = color.black, center = (0, 5, 0))

        ball = sphere(pos = (0,0,0), radius = 2, color = color.orange)
        square = box(pos = (5,5,0), x = 1, y = 1, z = 1, color = color.blue)