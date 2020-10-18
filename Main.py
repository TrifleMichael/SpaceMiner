import pygame
from math import *
pygame.init()
from random import randrange
from random import uniform

from Classes import *
from Settings import *
from ObjectLists import *




win = pygame.display.set_mode((res_x,res_y))
pygame.display.set_caption("Lotnik")

run = True
score = [0]
past_score = [0]
x_start = 100
y_start = 250


hero = lotnik(x_start, y_start, 100, 20)

main_text_window = text_window(res_x - 375, 55)



stop_asteroids = False

check_nearby_asteroids_timer = 0
asteroid_timer = asteroid_cooldown
background_star_timer = background_star_cooldown
health_pack_timer = health_pack_cooldown


while run:

    #pomiar czasu dla fps
    current_time = pygame.time.get_ticks()
    frame_end_time = current_time + dt

    #sprwadzania ktore asteroidy sa w poblizu
    check_nearby_asteroids_timer -= 1
    if check_nearby_asteroids_timer <= 0:
        check_nearby_asteroids_timer = check_nearby_asteroids_cooldown
        which_asteroids_nearby(hero, asteroid_list)


    #tworzenie gwiazd w tle
    background_star_timer -= 1
    if background_star_timer <= 0:
        background_star_timer = background_star_cooldown
        spawn_background_star(win)

    #spawnowanie laser upgrade
    if past_score[0] % 800 > score[0] % 800 and hero.weapons.laser_cooldown >= 22:
        spawn_laser_upgrade(win)
    #spawnowanie wrogow
    if past_score[0] % 1000 > score[0] % 1000 and hero.weapons.rocket_cooldown > 180:

        if score[0] < 6000:
            spawn_enemy()
        if score[0] >= 6000:
            spawn_enemy("strong")

    past_score[0] = score[0]

    #spawnowanie health packow
    health_pack_timer -= 1
    if health_pack_timer <= 0:
        spawn_health_pack(win)
        health_pack_timer = health_pack_cooldown

    #tworzenie asteroid
    asteroid_timer -= 1
    if asteroid_timer <= 0 and stop_asteroids == False:
        asteroid_timer = asteroid_cooldown
        spawn_asteroid(win)

    

    #wylaczanie
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #sterowanie
    hero.state.xkey_pressed = False
    hero.state.ykey_pressed = False
    keys = pygame.key.get_pressed()

    #pauza [ w trakcie tworzenia !]
    if keys[pygame.K_p]:
        pause(win)

                    
        #os x
    if keys[pygame.K_d] and hero.vx + hero.x_acc < hero.vx_max:
        hero.vx += hero.x_acc
        hero.state.xkey_pressed = True
    if keys[pygame.K_a] and abs(hero.vx - hero.x_acc) < hero.vx_max:
        hero.vx -= hero.x_acc
        hero.state.xkey_pressed = True

        #os y
    if keys[pygame.K_s] and hero.vy + hero.y_acc < hero.vy_max:
        hero.vy += hero.y_acc
        hero.state.ykey_pressed = True
    if keys[pygame.K_w] and abs(hero.vy - hero.y_acc) < hero.vy_max:
        hero.vy -= hero.y_acc
        hero.state.ykey_pressed = True

    #strzelanie
    if keys[pygame.K_f]:
        hero.shoot_laser(win)
    if hero.weapons.laser_timer > 0:
        hero.weapons.laser_timer -= 1

    if keys[pygame.K_r]:
        hero.fire_rocket(win)
    hero.weapons.rocket_timer -= 1

    #ustawienie obrotu
    hero.angle = hero.vy / hero.vy_max * hero.vx / hero.vx_max * 38

    #przesuwanie
    if hero.x + hero.vx < res_x - hero.width / 2 and hero.width / 2 < hero.x + hero.vx:
        hero.x += hero.vx
    if hero.y + hero.vy < res_y - hero.height / 2 and hero.height / 2 < hero.y + hero.vy:
        hero.y += hero.vy

    #wyhamowanie i odbicie przy zderzeniu z krawedzia
    if hero.x + hero.vx > res_x - hero.width / 2 or hero.width / 2 > hero.x + hero.vx:
        hero.vx *= -0.85
    if hero.y + hero.vy > res_y - hero.height / 2 or hero.height / 2 > hero.y + hero.vy:
        hero.vy *= -0.85

    #hamowanie
    if hero.state.xkey_pressed == False and hero.vx != 0:
        hero.vx = hero.vx * (abs(hero.vx) - hero.x_acc) / abs(hero.vx)
        if abs(hero.vx) < hero.x_acc:
            hero.vx = 0

    if hero.state.ykey_pressed == False and hero.vy != 0:
        hero.vy = hero.vy * (abs(hero.vy) - hero.y_acc) / abs(hero.vy)
        if abs(hero.vy) < hero.y_acc:
            hero.vy = 0

    #przesuwanie wszystkiego (bez statku)
    for list in movable_list:
        for thing in list:
            thing.move()



    #tworzenie dymu
    for rockets in rocket_list:
        rockets.smoke_timer += 1
        if rockets.smoke_timer >= rockets.smoke_cooldown:
            shoot_smoke(rockets.x, rockets.y)
            rockets.smoke_timer = 0

    #postarzanie dymu
    for smokes in smoke_list:
        smokes.timer += 1

    #usuwanie dymu
    for smokes in smoke_list:
        if smokes.if_need_deletion():
            smoke_list.remove(smokes)

    #usuwanie obiektow poza mapa
    for list in usuwane_za_mapa:
        for thing in list:
           if thing.off_map():
               list.remove(thing)

    #kolizja z health_packami
    for thing in health_pack_list:
        if hero.bubble_colision(thing):
            if hero.state.health < hero.state.maxhealth:
                hero.heal( thing.health )
                health_pack_list.remove( thing )
                main_text_window.add_text("Podniesiono apteczkę.")

    #kolizja z laser upgrade
    for thing in upgrade_list:
        if hero.bubble_colision(thing):

            if thing.type == "laser":
                if hero.weapons.laser_cooldown > 20:
                    hero.weapons.laser_cooldown *= 0.85
                upgrade_list.remove(thing)
                main_text_window.add_text("Czas przygotowania laserów skrócony o 15%")

            if thing.type == "rocket":
                if hero.weapons.rocket_cooldown > 180:
                    hero.weapons.rocket_cooldown *= 0.80               
                upgrade_list.remove(thing)
                main_text_window.add_text("Czas przygotowania rakiet skrócony o 20%")

    #zderzenie asteroidy ze statkiem
    for thing in asteroid_list:
        if thing.near_ship:
            if hero.bubble_colision(thing):
                hero.state.health -= thing.r * 2
                asteroid_list.remove(thing)

    #zderzenie wrogiego lasera ze statkiem
    for thing in enemy_laser_list:
        if hero.bubble_colision(thing):
            hero.state.health -= 20
            enemy_laser_list.remove(thing)


    #trafienie przeciwnika
    for enemi in enemy_list:
        for lazer in laser_list:        
            if enemi.bubble_colision( lazer ):
                enemi.hp -= 20
                shoot_sparks(lazer.x, lazer.y, 5, 2)
                laser_list.remove(lazer)
    #trafienie przeciwnika rakieta
    for enemi in enemy_list:
        for rockets in rocket_list:
            if enemi.hit_by_rocket(rockets):
                rockets.destroy_in_radius(score)
                rocket_list.remove(rockets)
                enemi.hp -= 40

    #niszczenie przeciwnikow
    for enemi in enemy_list:
        if enemi.hp <= 0:
            shoot_sparks(enemi.x, enemi.y, 40, 3)
            upgrade_list.append( upgrade(enemi.x, enemi.y, "rocket") )
            enemy_list.remove(enemi)

    if len(enemy_list) == 0:
        stop_asteroids = False
    else:
        stop_asteroids = True


            
    #niszczenie asteroid przez lasery
    for lazer in laser_list:
        for asteroida in asteroid_list:        
            if lazer.if_hit_asteroid(asteroida):

                shoot_sparks(asteroida.x, asteroida.y, asteroida.r)
                asteroid_list.remove(asteroida)
                laser_list.remove(lazer)
                score[0] += asteroida.r
                break

    #niszczenie asteroid przez wrogow
    for lazer in enemy_laser_list:
        for asteroida in asteroid_list:
            if lazer.if_hit_asteroid(asteroida):

                shoot_sparks(asteroida.x, asteroida.y, asteroida.r)
                asteroid_list.remove(asteroida)
                enemy_laser_list.remove(lazer)
                break

    #niszczenie asteroid przez rakiety
    for rockets in rocket_list:
        for asteroida in asteroid_list:        
            if rockets.if_explode(asteroida):
                rockets.destroy_in_radius(score)
                rocket_list.remove(rockets)
                break      
                     

    #zgon
    if hero.state.health <= 0:
        hero.state.health = 100

        hero.vx = 0
        hero.vy = 0

        explode_animation(hero.x, hero.y)

        hero.x = x_start
        hero.y = y_start

        score[0] = 0
        past_score[0] = 0
        hero.weapons.rocket_timer = 0
        hero.weapons.laser_cooldown = 70
        stop_asteroids = False
        enemy_list.clear()

        for list in movable_list:
            list.clear()


    #rysowanie rzeczy
    win.fill((0,0,0))

    #rysowanie obiektow
    for list in draw_list:
        for thing in list:
            thing.draw(win)

    #wyswietlanie punktow
    pointer = font.render(str(score[0]), False, (255, 255, 255))
    win.blit(pointer,(res_x - 110, 20))

    #wyswietlanie statku
    hero.draw(win)

    #okienko textowe
    main_text_window.show_text(win)

    #wyswietlanie ui
    hero.draw_ui(30, 30, win)

    pygame.display.update()

    #synchronizacja fps
    current_time = pygame.time.get_ticks()
    while current_time <= frame_end_time:
        pygame.time.delay(1)
        current_time = pygame.time.get_ticks()




