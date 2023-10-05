import pygame
import game

pygame.init()

clock = pygame.time.Clock()

game = game.Game()
run = True

while run:
    clock.tick(60)

    run = game.update()
    game.draw()

    print(clock.get_fps())

game.save()
pygame.quit()
