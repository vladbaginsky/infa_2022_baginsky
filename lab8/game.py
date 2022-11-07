import pygame
from pygame.draw import *
from random import randint
import pandas as pd
pygame.init()


# фпс
FPS = 3
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# задаю координаты шариков
################################################
x = 0
y = 0
r = 0
color = 0
x2 = 0
y2 = 0
r2 = 0
color2 = 0
x3 = 0
y3 = 0
r3 = 0
color3 = 0
speedx = 0
speedy = 0
speedx2 = 0
speedy2 = 0
speedx3 = 0
speedy3 = 0
################################################


# functions:
################################################
def new_ball():
    '''рисует новый шарик '''
    xloc = randint(100, 1100)
    yloc = randint(100, 900)
    rloc = randint(10, 30)
    colorloc = COLORS[randint(0, 5)]
    return xloc, yloc, rloc, colorloc
################################################


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    '''выводит на экран счет'''
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))

    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    return True


################################################
def ball_go(x_pos, y_pos, speed_x, speed_y):
    '''обработка движения шарика'''
    x_pos += speed_x
    y_pos += speed_y
    return x_pos, y_pos


################################################
def click(event):
    '''возвращает координаты и радиус круга'''
    return x, y, r, x2, y2, r2, x3, y3, r3
################################################


def is_hit(event, circle_data):
    '''обработка попадания'''
    delta_x = event.pos[0]-circle_data[0]
    delta_y = event.pos[1]-circle_data[1]
    delta_x2 = event.pos[0]-circle_data[0]
    delta_y2 = event.pos[1]-circle_data[1]
    delta_x3 = event.pos[0]-circle_data[0]
    delta_y3 = event.pos[1]-circle_data[1]

    first = ((delta_x) ** 2 + (delta_y) ** 2 < r ** 2)
    second = ((delta_x2) ** 2 + (delta_y2) ** 2 < r2 ** 2)
    third = ((delta_x3) ** 2 + (delta_y3) ** 2 < r3 ** 2)

    if (first or second or third):
        return True
    else:
        return False


################################################
def reflection(x_, y_, spx, spy):
    # обработка отражения
    if (y_ < 10 or y_ > 890):
        return spx, spy*(-1)

    elif (x_ > 1190 or x_ < 10):
        return spx*(-1), spy
    else:
        return spx, spy
################################################


def write_record(name_, score):
    df2 = pd.read_csv("records.csv")
    df = pd.DataFrame({"name": [name_], "score": [score]})
    print(df.head())
    new_df = pd.concat([df, df2])
    new_df.to_csv('records.csv')


################################################
clock = pygame.time.Clock()
################################################

################################################
'''ввод имени'''

# шрифт
font = pygame.font.Font(None, 32)

# cоздаю поле для ввода
input_box = pygame.Rect(400, 500, 450, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # обработка закрытия
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # обработка поля для ввода
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            # показываю, когда активно поле а когда нет
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # записываю в переменную имя
                    name = text
                    done = True
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    # обработка удаления буквы
                    text = text[:-1]
                else:
                    # добавление соответствующей буквы после
                    # каждого нажатия клавишы
                    text += event.unicode

    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    # обновляю экран
    pygame.display.update()
    clock.tick(30)
'''ввод имени закончился'''
##############################################################


# cчётчик
counter = 0

pygame.display.update()

finished = False

new_ball()

# счетчик для контроля времени, которое шарики существуют
i = 0

while not finished:
    # обновление шарика каждые 30 тиков
    i += 1
    if i % 30 == 0:

        x, y, r, color = new_ball()
        x2, y2, r2, color2 = new_ball()
        x3, y3, r3, color3 = new_ball()

        # задаю скорости новым шарикам
        speedx = randint(20, 50)*randint(-1, 1)
        speedy = randint(20, 50)*randint(-1, 1)
        speedx2 = randint(20, 50)*randint(-1, 1)
        speedy2 = randint(20, 50)*randint(-1, 1)
        speedx3 = randint(20, 50)*randint(-1, 1)
        speedy3 = randint(20, 50)*randint(-1, 1)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            write_record(name, counter)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # обработка попадания
            if is_hit(event, click(event)):
                counter += 1
            print("счёт:" + str(counter))

    # вывод счета на экран
    draw_text(screen, "score:" + str(counter), 35, 50, 50)

    # обработка отражения
    speedx, speedy = reflection(x, y, speedx, speedy)
    speedx2, speedy2 = reflection(x2, y2, speedx2, speedy2)
    speedx3, speedy3 = reflection(x3, y3, speedx3, speedy3)

    # движение шариков
    x, y = ball_go(x, y, speedx, speedy)
    x2, y2 = ball_go(x2, y2, speedx2, speedy2)
    x3, y3 = ball_go(x3, y3, speedx3, speedy3)

    # рисую шарики
    circle(screen, color, (x, y), r)
    circle(screen, color2, (x2, y2), r2)
    circle(screen, color3, (x3, y3), r3)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
