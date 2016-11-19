import pygame
import GameOfLife2D as GoL2D
import GameOfLife3D as GoL3d
import sys

def main():
    if (len(sys.argv) < 1 or sys.argv[1] == '2'):
        game = GoL2D.GameOfLife2D()
        game.Start()
    else:
        game = GoL3d.GameOfLife3D()
        game.Start()

if __name__ == "__main__":
    main()