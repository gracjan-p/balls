
import pygame
import time

from vector import Vector
import random
from random import randint, choice
from time import perf_counter


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Futura', 30)

# colors
BACKGROUND = '#27374D'
DARKER = '#526D82'
DARK = '#9DB2BF'
BRIGHT = '#DDE6ED'
BALL_COLOR = [
    '#b2c2cd',
    '#9DB2BF',
    '#849eae']

prev_time = perf_counter()
tick = 60 # fps lock

WIDTH, HEIGHT = (1280, 720)
window = pygame.display.set_mode((WIDTH, HEIGHT))
sim_surface = pygame.Surface((WIDTH, HEIGHT))
sim_surface.fill(BACKGROUND)
pygame.display.set_caption('Balls')

button_ico_1 = pygame.image.load('./img/grav.png')
button_ico_2 = pygame.image.load('./img/minus.png')
button_ico_3 = pygame.image.load('./img/plus.png')
button_ico_5 = pygame.image.load('./img/size-minus.png')
button_ico_6 = pygame.image.load('./img/size-plus.png')


class Ball():

    def __init__(self, x, y, acc: tuple, r, color):
        self.position = Vector((x, y))
        self.direction = Vector(acc)
        self.size = r
        self.color = color


    def draw(self):
        pygame.draw.circle(sim_surface, self.color, self.position(), self.size)

    def swap_vector(self, other):

        #while self.position.distance(other.position) > (self.size + other.size):
        #    self.position += self.direction/100

        # ball will transfer amount of energy based on it's size
        radius_multiplier = other.size / (self.size + other.size)
        collision = (self.position - other.position) * (radius_multiplier/20)
        resultant = (self.direction + collision)

        self.direction = resultant


    def move(self):

        for obj in balls:
            if obj != self:
                if (self.position + self.direction + gravity).distance(obj.position) <= (self.size+obj.size):
                    self.swap_vector(other=obj)
                    obj.swap_vector(other=self)
        # check for collisions

        # walls
        if self.position.x < (0 + self.size):
            self.position.x = (0 + self.size)
            self.direction = self.direction.neg_x()

        if self.position.x > (WIDTH - self.size):
            self.position.x = (WIDTH - self.size)
            self.direction = self.direction.neg_x()

        if self.position.y < (0 + self.size):
            self.position.y = (0 + self.size)
            self.direction = self.direction.neg_y()

        if self.position.y > (HEIGHT - self.size):
            self.position.y = (HEIGHT - self.size)
            self.direction = self.direction.neg_y()

        self.direction = self.direction + gravity
        self.position = self.position + self.direction


class Button():
    def __init__(self, x, y, width=50, height=50, type='add'):
        self.color = DARKER
        self.x, self.y = WIDTH-x, y
        self.width, self.height = width, height
        self.type = type

    def draw(self):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 0, 5)
        match self.type:
            case 'grav':
                window.blit(button_ico_1, (self.x, self.y))
            case 'remove':
                window.blit(button_ico_2, (self.x, self.y))
            case 'add':
                window.blit(button_ico_3, (self.x, self.y))
            case 'size-':
                window.blit(button_ico_5, (self.x, self.y))
            case 'size+':
                window.blit(button_ico_6, (self.x, self.y))

    def hover(self):
        mX, mY = pygame.mouse.get_pos()
        if  self.x <= mX < (self.x + self.width) and\
            self.y <= mY < (self.y + self.height):
            self.color = BRIGHT
        else:
            self.color = DARKER

    def click(self):
        global balls, ball_size
        match self.type:
            case 'add':
                balls.append(Ball(100, 100, (5,0), r=ball_size, color=choice(BALL_COLOR)))
            case 'remove':
                if len(balls) > 0:
                    balls.remove(balls[0])
            case 'grav':
                if gravity.y == 0:
                    gravity.y = 0.5
                elif gravity.y == 0.5:
                    gravity.y = 0
            case 'clear':
                balls = []
            case 'size-':
                if ball_size >= 10:
                    ball_size -= 5
                    print(ball_size)
            case 'size+':
                if ball_size <= 55:
                    ball_size += 5
                    print(ball_size)


def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(tick)
        text_fps = my_font.render(f'FPS: {int(clock.get_fps())}', False, BRIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.color == BRIGHT:
                        button.color = DARK
                        button.click()


        sim_surface.fill(BACKGROUND)

        mX, mY = pygame.mouse.get_pos()
        #mVector = Vector((mX, mY))

        for b in balls:
            b.move()
            b.draw()

        window.blit(sim_surface, (0, 0))
        for button in buttons:
            button.hover()
            button.draw()

        window.blit(text_fps, (10, 10))

        pygame.display.flip()


gravity = Vector((0, 0))
air_resistance = Vector((5, 5))

ball_size = 50
balls = []
buttons = []

balls.append(Ball(WIDTH//2, HEIGHT//2, (0, 0), r=ball_size, color=DARK))

buttons.append(Button(100, 50, type='add'))
buttons.append(Button(170, 50, type='remove'))

buttons.append(Button(100, 120, type='grav'))
buttons.append(Button(170, 120, type='clear'))

buttons.append(Button(170, 190, type='size-'))
buttons.append(Button(100, 190, type='size+'))

if __name__ == "__main__":
    main()

