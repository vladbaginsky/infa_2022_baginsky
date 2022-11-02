import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 2
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    '''рисует новый шарик '''
    global x, y, r, color
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    
speedx = randint(-50, 50)
speedy = randint(-50, 50)


def ball_go(x_pos, y_pos, speed_x, speed_y):
    x_pos += speed_x
    y_pos += speed_y
    return x_pos, y_pos

    

def click(event):
    '''возвращает координаты и радиус круга'''
    return x, y, r

def is_hit(event, circle_data):
    delta_x = event.pos[0]-circle_data[0]
    delta_y = event.pos[1]-circle_data[1]
    
    if (delta_x)**2 + (delta_y)**2<r**2:
        return True
    else:
        return False
    


#def reflection(x, y):
    
        

counter = 0

pygame.display.update()
clock = pygame.time.Clock()
finished = False

new_ball()

i = 0

while not finished:
    if i%12 ==0:
        new_ball()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_hit(event, click(event)):
                counter+=1
            print("счёт:" + str(counter))
    #reflection(x, y)
    if (y<10 or y>890):
        speedy *= -1
    if (x>1190 or x<10):
        speedx *= -1
    i+=1
    
    x, y = ball_go(x, y, speedx, speedy)       
    circle(screen, color, (x, y), r)
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()