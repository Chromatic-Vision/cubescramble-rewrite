import threading
import pygame
import time
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
    print(run)

    #try:
    run = game.update()
    #except Exception as e:
        # logger.exception('while updating game', e)
        # logger.log('exiting')
        #print(str(e))
        #pygame.quit()
        #exit(1)

    game.draw()

pygame.quit()