import pygame
from random import randrange
from random import uniform

from math import *
from Utilities import *
from ObjectLists import *

class background_star(movable):
    def __init__(self, x, y, r, color, vx = -1.5, vy = 0):
        movable.__init__(self, x, y, r, r, vx)
        self.r = r
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)

class asteroid(movable):
    def __init__(self, x, y, r, color, vx = -2, vy = 0, near_ship = True):
        movable.__init__(self, x, y, r, r, vx)
        self.r = r
        self.color = color
        self.near_ship = near_ship

    def draw(self, window):
        list = []
        for i in range(6):
            list.append( (self.r * cos(i/6 * 2*pi) + self.x, self.r * sin(i/6 * 2*pi) + self.y) )
        pygame.draw.polygon(window, self.color, list)

class smoke(movable):
    def __init__(self, x, y, r, vx, vy, color, timer = 0, time_of_death = 120):
        movable.__init__(self, x, y, r, r, vx, vy)
        self.r = r
        self.color = color
        self.timer = timer
        self.time_of_death = time_of_death

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)

    def if_need_deletion(self):
        if self.timer >= self.time_of_death:
            return True
        return False

def spawn_background_star(window):
    color1 = randrange(0,100)
    color2 = randrange(0,100)
    r = randrange(2,5)
    y = randrange(10, res_y - 10)
    color = (color1, color1, color1 + color2)
    background_star_list.append( background_star(res_x + 50, y, r, color) )






def draw_explosion(x, y, r, window):
    list = []
    for i in range(20):
        rad = (i % 2 + 1) * r
        list.append( ( rad * cos(i / 20 * pi*2) + x, rad * sin(i / 20 * pi*2) + y) )
    pygame.draw.polygon(window, (200,200,0), list)

def explode_animation(x, y, window):
    frames = 30

    for i in range(frames):
        window.fill((0,0,0))

        for list in draw_list:
            for thing in list:
                thing.draw(window)
        draw_explosion(x, y, i * 2, window)

        pygame.display.update()
        pygame.time.delay(dt)

    frames = int(frames / 2)
    for i in range(frames):
        window.fill((0,0,0))

        for list in draw_list:
            for thing in list:
                thing.draw(window)
        draw_explosion(x, y, 50 - i * 2, window)

        pygame.display.update()
        pygame.time.delay(dt)

def shoot_smoke(x, y):
    r = randrange(5, 15)
    vx = uniform(0, 0.6)
    vy = uniform(0.3, 0.7)

    updown = randrange(0,2)
    updown = updown * 2 - 1
    vy *= updown

    color = randrange(100, 200)
    color = (color, color, color)
    smoke_list.append( smoke(x, y, r, vx - 1.3, vy, color) )

def shoot_sparks(x, y, r, density = 1):
    sparks = []    
    for i in range(int(r * density)):
        rad = randrange(1,5)
        center_distance = randrange(0,r)
        angle = uniform(0, 2*pi)
        x_pom = int(x + center_distance * cos(angle))
        y_pom = int(y + center_distance * sin(angle))
        vx = -2.5 + (x_pom - x) / r * 1.5
        vy = (y_pom - y) / r * 1.5
        color = (randrange(150,255), randrange(150,250), 0)
        age = randrange(20,100)

        sparks.append( smoke(x_pom, y_pom, rad, vx, vy, color, 0, age))
    for spark in sparks:
        smoke_list.append(spark)
