import pygame
import random

background_color = (255, 255, 255)
(width, height) = (1920,1080)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Of Life - Bartlomiej Buchala 2016')
screen.fill(background_color)

pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False