import math
from random import choice
from random import randint as rnd

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии
        единицы времени.

        Метод описывает
        перемещение мяча за один
        кадр перерисовки. То есть,
        обновляет значения
        self.x и self.y с учетом
        скоростей self.vx и self.vy,
        силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.y < 5 or self.y > 570:
            self.vy *= -1
        if self.x < 5 or self.x > 790:
            self.vx *= -1
        if self.y > 570:
            self.vy *= 0.8
            self.vx *= 0.95
        else:
            self.vy -= 1

        self.x += self.vx
        self.y -= self.vy 
        self.vx *= 0.99
        self.vy *= 0.8

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкиваетсяли
        данный обьект с целью,
        описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым
            проверяется столкновение.
        Returns:
            Возвращает True в случае
            столкновения мяча и цели.
            В противном случае возвращает False.
        """

        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (obj.r) ** 2 + (self.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.y = 450
        self.x = 40

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент
        скорости мяча vx и vy зависят от
        положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y),
                             (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от
        положения мыши."""
        if event:
            self.an = math.atan(
                (event.pos[1] - self.y) / (event.pos[0] - self.x)
                )
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            BLACK,
            (self.x, self.y),
            (self.x + self.f2_power / 1.5 * math.cos(self.an),
             self.y + self.f2_power / 1.5 * math.sin(self.an)),
            10
            )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self, x_, y_):
        self.x += 10*x_
        self.y += 10*y_


class Target:

    def __init__(self, screen, points = 0):
        self.screen = screen
        self.points = points
        self.new_target()
        self.vx = rnd(2, 5)
        self.vy = rnd(2, 10)
        self.motionflag = 0

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(30, 50)
        # x=
        # y=
        # z= was
        self.color = RED
        # color=
        self.live = 1
        targets.append(self)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        global balls
        balls = []

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        if self.y < 5 or self.y > 570:
            self.vy *= -1
        if self.x < 5 or self.x > 790:
            self.vx *= -1
        self.x += self.vx
        self.y -= self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)

target = Target(screen)
target1 = Target(screen)

finished = False


while not finished:
    screen.fill(WHITE)
    gun.draw()

    for t in targets:
        t.draw()

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        for t in targets:
            t.move()
            t.motionflag = 1
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gun.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                gun.move(1, 0)
            elif event.key == pygame.K_UP:
                gun.move(0, -1)
            elif event.key == pygame.K_DOWN:
                gun.move(0, 1)

    for t in targets:
        if t.motionflag == 1:
            t.motionflag = 0
            break
        else:
            t.move()

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                t.new_target()

    gun.power_up()

pygame.quit()
