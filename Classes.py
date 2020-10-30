import pygame
from math import *
from random import randrange
from random import uniform

from ObjectLists import *
from Settings import *





def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # rotates point around another point
    def rotate(self, degrees, center):
        angle = degrees * pi / 180
        new_x = cos(angle) * (self.x - center.x) - sin(angle) * (self.y - center.y)
        new_y = sin(angle) * (self.x - center.x) + cos(angle) * (self.y - center.y)

        self.x = new_x + center.x
        self.y = new_y + center.y
    
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
       

class asteroid:
    def __init__(self, x, y, r, color, vx = -2, vy = 0, near_ship = True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.near_ship = near_ship

    def draw(self, window):
        list = []
        for i in range(6):
            list.append( (self.r * cos(i/6 * 2*pi) + self.x, self.r * sin(i/6 * 2*pi) + self.y) )
        pygame.draw.polygon(window, self.color, list)

    def off_map(self):
        if self.x > res_x + 100 or self.x + self.r < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False

    def move(self):
        self.x += self.vx
        self.y += self.vy

class laser:
    def __init__(self, x, y, friendly = True, vx = 5, vy = 0, height = 5, width = 20, r = 2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = height
        self.width = width
        self.friendly = friendly
        self.r = r
        
    def draw(self, window):
        pygame.draw.rect(window, (200,50,50), (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def off_map(self):
        if self.x > res_x or self.x < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False

    def if_hit_asteroid(self, aster):
        if distance(self.x, self.y, aster.x, aster.y) < aster.r:
            return True
        return False      

class health_pack:
    def __init__(self, x, y, health, width = 60, height = 60, r = 30, vx = -3.2, vy = 0):
        self.x = x
        self.y = y
        self.health = health
        self.width = width
        self.height = height
        self.r = r
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.x + self.width / 3 - self.width/2, self.y + self.height * 0.2 - self.height/2, self.width / 3, self.height * 0.6))
        pygame.draw.rect(window, (255, 0, 0), (self.x + self.width * 0.2 - self.width/2, self.y + self.height / 3 - self.height/2, self.width * 0.6, self.height / 3))

class rocket:
    def __init__(self, x, y, vx = 4, vy = 0, smoke_timer = 0, smoke_cooldown = 4, explode_radius = 200, width = 50, height = 12, point_len = 20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.explode_radius = explode_radius
        self.smoke_timer = smoke_timer
        self.smoke_cooldown = smoke_cooldown
        self.width = width
        self.height = height
        self.point_len = point_len

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, window):
        pygame.draw.rect(window, (200, 50, 50), (self.x, self.y, self.width, self.height))
        trojkat = [(self.x + self.width, self.y), (self.x + self.width + self.point_len, self.y + self.height / 2), (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(window, (255, 0, 0), trojkat)

    def off_map(self):
        if self.x > res_x or self.x < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False 

    # checks for asteroids in radius to explode
    def if_explode(self, aster):
        if distance(self.x + self.width + self.point_len, self.y + self.height / 2, aster.x, aster.y) < aster.r:
            return True
        return False

    def destroy_in_radius(self, score):

        # deleting asteroids in radius
        # removing reference from list shortens it, thus a weird implementation
        shoot_sparks(int(self.x + self.width/2), int(self.y + self.height/2), 50, 3/5)
        i = 0
        while i < len(asteroid_list):
            aster = asteroid_list[i]
            if distance(self.x + self.width / 2, self.y + self.height / 2, aster.x, aster.y) < self.explode_radius:
                shoot_sparks(aster.x, aster.y, aster.r, 1/2)    
                score[0] += int(aster.r * 3 / 4)
                del asteroid_list[i]       
            else:   
                i += 1


# general upgrade class
# can be of laser or rocket type
class upgrade:
    def __init__(self, x, y, type = "laser", r = 35, vx = -3, vy = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.type = type

    def off_map(self):
        if self.x > res_x + 100 or self.x < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False 

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, window):
        
       width = 60
       height = 60
       if self.type == "laser":
           pygame.draw.rect(window, (200, 150, 0), (self.x - width/2, self.y - height/2, width, height))

           pygame.draw.circle(window, (200,0,0), (int(self.x), int(self.y)), int(width / 3))

       if self.type == "rocket":
           pygame.draw.rect(window, (100, 75, 30), (self.x - width/2, self.y - height/2, width, height))

           pygame.draw.rect(window, (200, 50, 0), (self.x - 10, self.y - 15, 12, 30))
           triangle = [(self.x - 10, self.y - 15), (self.x - 4, self.y - 21) ,(self.x + 2, self.y - 15)]
           pygame.draw.polygon(window, (200, 0, 0), triangle)


class background_star:
    def __init__(self, x, y, r, color, vx = -1.5, vy = 0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)

    def off_map(self):
        if self.x > res_x + 100 or self.x < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False

class smoke:
    def __init__(self, x, y, r, vx, vy, color, timer = 0, time_of_death = 120):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.timer = timer
        self.time_of_death = time_of_death

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)

    def off_map(self):
        if self.x > res_x or self.x < 0:
            return True
        if self.y > res_y or self.y < 0:
            return True
        return False

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def if_need_deletion(self):
        if self.timer >= self.time_of_death:
            return True
        return False

 # shows text on screen
class text_window:
    def __init__(self, x, y, width = 200, height = 150, text_list = [], timer = 240):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_list = text_list
        self.timer = timer

    # adds text to queue
    def add_text(self, text):
        self.text_list.append( [font.render(str(text), False, (255,255,255)), self.timer, text] )

    # shows texts on screen
    def show_text(self, window):
        position_y = self.y
        for text in self.text_list:

            position_x = self.x + self.width - len(text[2]) * 10 - 20
            window.blit(text[0], (position_x, position_y))
            position_y += font_size + 5

            text[1] -= 1
            if text[1] <= 0:
                self.text_list.remove(text)

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




def spawn_background_star(window):
    color1 = randrange(0,100)
    color2 = randrange(0,100)
    r = randrange(2,5)
    y = randrange(10, res_y - 10)
    color = (color1, color1, color1 + color2)
    background_star_list.append( background_star(res_x + 50, y, r, color) )


def spawn_health_pack(window):
    health_boost = randrange(30, 60)
    y = randrange(100, res_y - 100)
    health_pack_list.append( health_pack(res_x + 50, y, health_boost))

def spawn_asteroid(window):
    r = randrange(10, 40)
    y = randrange(0 + r, res_y - r)
    color = 220 - 5 * r + randrange(50)
    color = (color, color, color)
    asteroid_list.append( asteroid( res_x + 50, y, r, color) )

def spawn_laser_upgrade(window):
    y = randrange(0 + 80, res_y - 80)
    upgrade_list.append( upgrade(res_x + 50, y) )

 
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

def which_asteroids_nearby(hero, input_list):
    max_speed = sqrt(hero.vx * hero.vx + hero.vy * hero.vy)
    for aster in input_list:
        aster.near_ship = False
        #jesli odleglosc od bohatera do asteroidy bedzie mniejsza od max odlegosci jaka przebedzie od odswiezenia
        if distance(hero.x, hero.y, aster.x, aster.y) < max_speed * check_nearby_asteroids_cooldown + 150:
            aster.near_ship = True

def pause(window):
    pygame.draw.rect(window, (250, 250, 250), (res_x / 2 - 60, res_y / 2 - 100, 50, 200))
    pygame.draw.rect(window, (250, 250, 250), (res_x / 2 + 40, res_y / 2 - 100, 50, 200))
    pygame.display.update()
    pygame.time.delay(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.time.delay(330)
                    return

def spawn_enemy(type = "regular"):
    stop_asteroids = True
    if type == "strong":
        enemy_list.append( enemy(10, 10, "strong", 0, 150) )
    else:
        enemy_list.append( enemy(10, 10) )



