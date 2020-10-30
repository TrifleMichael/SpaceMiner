import pygame

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
