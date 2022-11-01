import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 1000))

#rect(screen, (255, 0, 255), (100, 100, 200, 200))
#rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
#polygon(screen, (255, 255, 0), [(100,100), (200,50),
 #                              (300,100), (100,100)])
#polygon(screen, (0, 0, 255), [(100,100), (200,50),
 #                              (300,100), (100,100)], 5)
#circle(screen, (0, 255, 0), (200, 175), 50)

circle(screen, (255, 255, 0), (500, 500), 200)
polygon(screen, (0, 0, 0), [[400,600],[600,600],[600,625],[400, 625]])

polygon(screen, (0, 0, 0), [[310,340],[530,430],[520,450],[310, 370]])
polygon(screen, (0, 0, 0), [[1000-310,340],[1000-530,430],[1000-520,450],[1000-310, 370]])
circle(screen, (255, 0, 0), (450, 450), 30)
circle(screen, (255, 0, 0), (550, 460), 30)

circle(screen, (0, 0, 0), (450, 450), 20)
circle(screen, (0, 0, 0), (550, 460), 20)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()