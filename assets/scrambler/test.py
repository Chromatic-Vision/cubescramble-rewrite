import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)

FONT_SIZE = 50
font = pygame.font.SysFont("bahnschrift", 50)

arfaere = pygame.time.Clock()
import assets.scrambler.clock as c

clock = c.Clock()

d = c.get_scramble()
print(d)

clock.convert_scramble(d)
currents = 0

while 1:

    screen.fill((0, 0, 0))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit(0)

        if ev.type == pygame.MOUSEBUTTONDOWN:

            fy = 500

            for i in range(clock.pins.__len__()):
                if fy <= ev.pos[1] <= fy + FONT_SIZE:
                    clock.pins[i] = True if not clock.pins[i] else False

                fy += FONT_SIZE

            if ev.pos[1] < 100:
                print("yes")
                if currents == 0:
                    currents = 1
                elif currents == 1:
                    currents = 0

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                clock.move(1, currents, clock.pins)
            elif ev.key == pygame.K_LEFT:
                clock.move(-1, currents, clock.pins)

    # print(currents)


    for i in range(clock.front.states.__len__()):
        pygame.draw.rect(screen, (64, 77, 255), (i % 3 * 100, i // 3 * 100, 75, 75))
        screen.blit(font.render(str(clock.front.states[i]), True, (255, 255, 255)), (i % 3 * 100 + 30, i // 3 * 100 + 30))

    for i in range(clock.back.states.__len__()):
        pygame.draw.rect(screen, (214, 77, 188), (i % 3 * 100 + 400, i // 3 * 100, 75, 75))
        screen.blit(font.render(str(clock.back.states[i]), True, (255, 255, 255)), (i % 3 * 100 + 30 + 400, i // 3 * 100 + 30))

    fy = 500

    for i in range(clock.pins.__len__()):
        screen.blit(font.render(f"Pin {i}: {clock.pins[i]}", True,(255, 255, 255)), (20, fy))
        fy += FONT_SIZE


    arfaere.tick(60)
    pygame.display.update()