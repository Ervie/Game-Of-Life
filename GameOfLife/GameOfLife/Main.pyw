import pygame
import GameOfLife as GoL


#background_color = (255, 255, 255)
#(width, height) = (1920,1080)

#screen = pygame.display.set_mode((width, height))
#pygame.display.set_caption('Game Of Life - Bartlomiej Buchala 2016')
#screen.fill(background_color)

#pygame.display.flip()


def main():
    game = GoL.GameOfLife()
    game.start()

if __name__ == "__main__":
    main()