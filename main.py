import pygame
import game

pygame.init()

clock = pygame.time.Clock()

size = (0, 0)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
size = screen.get_size()

game = game.Game(screen)
run = True

while run:
    clock.tick(60)

    run = game.update()
    game.draw()

game.save()
pygame.quit()
