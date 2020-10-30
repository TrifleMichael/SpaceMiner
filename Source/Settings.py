from pygame import font


# game resolution (affects gameplay)
res_x = 1200
res_y = 600

# time in miliseconds per frame, default is 16 (60fps)
# game is frame locked which means that changing dt will change game speed
dt = 16


# frequency of spawning (in number of frames)
background_star_cooldown = 15
asteroid_cooldown = 20
health_pack_cooldown = 2000

# number of frames before updating possible collision list (optimalization)
check_nearby_asteroids_cooldown = 20

font.init()
font_size = 28
font = font.SysFont('Comic Sans MS', font_size)