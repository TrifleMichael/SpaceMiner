import pygame
from math import *


from ObjectLists import *
from Settings import *
from Active import *
from Utilities import *
from Envoirment import *



# class for handling ship statistics
class ship_states:
    def __init__(self, xkey_pressed = False, ykey_pressed = False, maxhealth = 100, health = 100):
        self.xkey_pressed = xkey_pressed
        self.ykey_pressed = ykey_pressed
        self.health = health
        self.maxhealth = maxhealth

# class for handling ship weapons statistics
class weapons:
    def __init__(self, laser_timer = 0, laser_cooldown = 60, rocket_timer = 0, rocket_cooldown = 600):
        self.laser_timer = laser_timer
        self.laser_cooldown = laser_cooldown
        self.rocket_timer = rocket_timer
        self.rocket_cooldown = rocket_cooldown
 
        
basic_state = ship_states()
basic_weapons = weapons()

# main spaceship class
class space_ship:
    def __init__(self, x, y, width, height, state = basic_state, weapons = basic_weapons, y_acc = 0.4, x_acc = 0.5, vx_max = 8, vy_max = 6, vx = 0, vy = 0, angle = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.y_acc = y_acc
        self.x_acc = x_acc
        self.vx_max = vx_max
        self.vy_max = vy_max
        self.angle = angle
        self.state = state
        self.weapons = weapons
    
    # calculates and draws next animation frame
    def draw(self, window):
        ship_model_1 = []
        ship_model_1.append( point(self.x - self.width / 2, self.y - self.height / 2) )
        ship_model_1.append( point(self.x + self.width / 2, self.y - self.height / 2) )
        ship_model_1.append( point(self.x - self.width / 2, self.y + self.height / 2) )
        ship_model_1.append( point(self.x + self.width / 2, self.y + self.height / 2) )
        
        for points in ship_model_1:
            points.rotate(self.angle, point(self.x, self.y))

        final_list = []
        for points in ship_model_1:
            final_list.append((points.x, points.y))
        pygame.draw.polygon(window, (200, 120, 0), final_list)

    def shoot_laser(self, window):
        if self.weapons.laser_timer <= 0:
            laser_list.append(laser(self.x, self.y))
            self.weapons.laser_timer = self.weapons.laser_cooldown

    def fire_rocket(self, window):
        if self.weapons.rocket_timer <= 0:
            rocket_list.append(rocket(self.x, self.y - 6))
            self.weapons.rocket_timer = self.weapons.rocket_cooldown
    
    # checks for collision with other bubbles
    def bubble_colision(self, bubble):
        bubble_1 = point ( self.x + self.width / 2 - self.height / 2, self.y)
        bubble_2 = point ( self.x - self.width / 2 + self.height / 2, self.y)
        bubble_3 = point ( self.x, self.y)

        bubble_1.rotate(self.angle, point( self.x, self.y ))
        bubble_2.rotate(self.angle, point( self.x, self.y ))

        if distance(bubble_1.x, bubble_1.y, bubble.x, bubble.y) < bubble.r + self.height / 2:
            return True
        if distance(bubble_2.x, bubble_2.y, bubble.x, bubble.y) < bubble.r + self.height / 2:
            return True
        if distance(bubble_3.x, bubble_3.y, bubble.x, bubble.y) < bubble.r + self.height / 2:
            return True
        return False

    def draw_ui(self, x, y, window):
       #healthbar
       pygame.draw.rect(window, (30, 30, 200), (x + 50, y, self.state.maxhealth, 10))
       pygame.draw.rect(window, (30, 200, 50), (x + 50, y, self.state.health, 10))

       #lazer
       if self.weapons.laser_timer <= 0:
           pygame.draw.rect(window, (250, 0, 0), (x , y - 5, 8, 20))

        #rocket
       if self.weapons.rocket_timer <= 0:
           pygame.draw.rect(window, (200, 50, 0), (x + 18, y - 10, 12, 30))
           triangle = [(x + 18, y - 10), (x + 24, y - 16) ,(x + 30, y - 10)]
           pygame.draw.polygon(window, (200, 0, 0), triangle)


    # adds health to ship
    def heal(self, health_boost):
        self.state.health += health_boost
        if self.state.health > self.state.maxhealth:
            self.state.health = self.state.maxhealth
       



# can be of regular or strong class
class enemy:
    def __init__(self, x, y, type = "regular", action_timer = 0, hp = 100, r = 28):
        self.x = x
        self.y = y
        self.action_timer = action_timer
        self.hp = hp
        self.r = r
        self.type = type

    def draw(self, window, width = 50, height = 50):

        if self.type == "regular":
            #ustawienie polozenia
            self.action_timer += 1
            cosinus = cos(self.action_timer / 400 * pi)
            cosinus = (cosinus + 1) / 2 #przedzial od 0 do 1
            self.y = int( cosinus * (res_y - 150) + 100 )
            self.x = int( res_x - width * 4 + width * cos(self.action_timer / 120 * pi) )

            #rysowanie
            pygame.draw.circle(window, (120, 100, 100), (self.x, self.y), self.r)
            pygame.draw.rect(window, (140, 120, 120), (self.x - width/2 - 15, self.y - 20, 40, 10))        
            pygame.draw.rect(window, (140, 120, 120), (self.x - width/2 - 15, self.y + 10, 40, 10))

            #strzelanie
            if self.action_timer % 50 == 0:
                enemy_laser_list.append( laser(self.x, self.y, False, -5))

            if self.action_timer % 250 == 0:
                enemy_laser_list.append( laser(self.x, self.y, False, -4.5, -1.5) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4.5, 1.5) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4, -3) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4, 3) )

        if self.type == "strong":
            #ustawienie polozenia
            self.action_timer += 1
            cosinus = cos(self.action_timer / 400 * pi)
            cosinus = (cosinus + 1) / 2 #przedzial od 0 do 1
            self.y = int( cosinus * (res_y - 150) + 100 )
            self.x = int( res_x - width * 4 + width * cos(self.action_timer / 120 * pi) )

            #rysowanie
            pygame.draw.circle(window, (150,150,250), (self.x, self.y), self.r)
            for i in range(3):
                pygame.draw.rect(window, (150,150,175), (self.x - self.r - 10, (self.y - self.r * 1/6 - 8) + i * self.r * 1/3, 50, 5))

            #strzelanie
            if self.action_timer % 40 == 0:
                enemy_laser_list.append( laser(self.x, self.y, False, -5, -0.5) )
                enemy_laser_list.append( laser(self.x, self.y, False, -5, 0.5) )
            if self.action_timer %  160 == 0:
                enemy_laser_list.append( laser(self.x, self.y, False, -4.5, -1.5) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4.5, 1.5) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4, -3) )
                enemy_laser_list.append( laser(self.x, self.y, False, -4, 3) )

            #tutaj stworzyc death laser :D
            if self.action_timer %  480 == 0:
                pass


    def bubble_colision(self, bubble):
        
        if distance(self.x, self.y, bubble.x, bubble.y) <= self.r + bubble.r:
            return True
        return False

    def hit_by_rocket(self, rocket):

        if distance(self.x, self.y, rocket.x + rocket.width, rocket.y + rocket.height/2) < rocket.point_len + self.r:
            return True
        return False




def which_asteroids_nearby(hero, input_list):
    max_speed = sqrt(hero.vx * hero.vx + hero.vy * hero.vy)
    for aster in input_list:
        aster.near_ship = False
        #jesli odleglosc od bohatera do asteroidy bedzie mniejsza od max odlegosci jaka przebedzie od odswiezenia
        if distance(hero.x, hero.y, aster.x, aster.y) < max_speed * check_nearby_asteroids_cooldown + 150:
            aster.near_ship = True



def spawn_enemy(type = "regular"):
    stop_asteroids = True
    if type == "strong":
        enemy_list.append( enemy(10, 10, "strong", 0, 150) )
    else:
        enemy_list.append( enemy(10, 10) )



