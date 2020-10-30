import pygame


from ObjectLists import *
from Settings import *
from Utilities import *
from Envoirment import *



    


class laser(movable):
    def __init__(self, x, y, friendly = True, vx = 5, vy = 0, height = 5, width = 20, r = 2):
        movable.__init__(self, x, y, width/2, height/2, vx, vy)
        self.height = height
        self.width = width
        self.friendly = friendly
        self.r = r
        
    def draw(self, window):
        pygame.draw.rect(window, (200,50,50), (self.x, self.y, self.width, self.height))


    def if_hit_asteroid(self, aster):
        if distance(self.x, self.y, aster.x, aster.y) < aster.r:
            return True
        return False      

class health_pack(movable):
    def __init__(self, x, y, health, width = 60, height = 60, r = 30, vx = -3.2, vy = 0):
        movable.__init__(self, x, y, width/2, height/2, vx)
        self.health = health
        self.width = width
        self.height = height
        self.r = r


    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.x + self.width / 3 - self.width/2, self.y + self.height * 0.2 - self.height/2, self.width / 3, self.height * 0.6))
        pygame.draw.rect(window, (255, 0, 0), (self.x + self.width * 0.2 - self.width/2, self.y + self.height / 3 - self.height/2, self.width * 0.6, self.height / 3))

class rocket(movable):
    def __init__(self, x, y, vx = 4, vy = 0, smoke_timer = 0, smoke_cooldown = 4, explode_radius = 200, width = 50, height = 12, point_len = 20):
        movable.__init__(self, x, y, width/2, height/2, vx)
        self.explode_radius = explode_radius
        self.smoke_timer = smoke_timer
        self.smoke_cooldown = smoke_cooldown
        self.width = width
        self.height = height
        self.point_len = point_len

    def draw(self, window):
        pygame.draw.rect(window, (200, 50, 50), (self.x, self.y, self.width, self.height))
        trojkat = [(self.x + self.width, self.y), (self.x + self.width + self.point_len, self.y + self.height / 2), (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(window, (255, 0, 0), trojkat)

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
class upgrade(movable):
    def __init__(self, x, y, type = "laser", r = 35, vx = -3, vy = 0):
        movable.__init__(self, x, y, r, r, vx)
        self.r = r
        self.type = type

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



 

def spawn_health_pack(window):
    health_boost = randrange(30, 60)
    y = randrange(100, res_y - 100)
    health_pack_list.append( health_pack(res_x + 50, y, health_boost))

def spawn_laser_upgrade(window):
    y = randrange(0 + 80, res_y - 80)
    upgrade_list.append( upgrade(res_x + 50, y) )

def spawn_asteroid(window):
    r = randrange(10, 40)
    y = randrange(0 + r, res_y - r)
    color = 220 - 5 * r + randrange(50)
    color = (color, color, color)
    asteroid_list.append( asteroid( res_x + 50, y, r, color) )




