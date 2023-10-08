import pygame
import game

pygame.init()

clock = pygame.time.Clock()

game = game.Game()
run = True

while run:
    clock.tick(60)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.QUIT:
            run = False

    game.update(events)
    game.draw()

    print(clock.get_fps())

game.save()
pygame.quit()
