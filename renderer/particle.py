import math
import random
import pygame


class ParticleRenderer:

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.particles = []

    def connect_lines(self, screen):
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.particles[i].distance_to(self.particles[j]) < 100:
                    # print(self.particles[i].color)
                    # pygame.draw.line(screen, self.particles[i].color, (self.particles[i].x, self.particles[i].y),
                    #                  (self.particles[j].x, self.particles[j].y), 10)
                    # TODO: pygame wiki says blend is deprecated
                    pygame.draw.aaline(screen, self.particles[i].color, (self.particles[i].x, self.particles[i].y),
                                       (self.particles[j].x, self.particles[j].y), 1)
                    # pygame.draw.aalines(screen, self.particles[i].color, False, [(self.particles[i].x, self.particles[i].y),
                                        #(self.particles[j].x, self.particles[j].y)])

    def clear(self):
        for p in self.particles:
            p.fadeout = True
        # self.particles = []

    def refresh(self, particle_amount):
        self.clear()

        for i in range(particle_amount):
            self.particles.append(ParticleRenderer.Particle(self.screen.get_size()))

    def update(self):
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        for p in self.particles:
            if p.fadeout:
                p.color = (
                    p.color[0] - 10,
                    p.color[1] - 10,
                    p.color[2] - 10,
                    p.color[3] - 10,
                )
                if min(p.color) <= 0:
                    self.particles.remove(p)
                    continue

            p.move()
            p.render(s)

        self.connect_lines(s)
        self.screen.blit(s, (0, 0))

    class Particle:

        def __init__(self, screen_size: tuple):
            self.screen_size = screen_size
            #self.x = random.randint(0, screen_size[0])
            #self.y = random.randint(0, screen_size[1])

            x_hook_range = [(0, 100), (screen_size[0] - 100, screen_size[0])]
            y_hook_range = [(0, 100), (screen_size[1] - 100, screen_size[1])]

            xv = random.choice(x_hook_range)
            yv = random.choice(y_hook_range)

            self.x = random.randint(xv[0], xv[1])
            self.y = random.randint(yv[0], yv[1])

            self.radius = random.uniform(1.6, 2.3)
            self.vx = random.uniform(-2.5, 2.5)
            self.vy = random.uniform(-2.5, 2.5)
            # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.color = (255, 255, 255, 169)
            self.fadeout = False

        def render(self, screen: pygame.surface.Surface):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        def move(self): # bounce particles
            self.x += self.vx
            self.y += self.vy

            if self.x < 0 or self.x > self.screen_size[0]:
                self.vx *= -1
                # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            if self.y < 0 or self.y > self.screen_size[1]:
                self.vy *= -1
                # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        def distance_to(self, other_particle):
            dx = self.x - other_particle.x
            dy = self.y - other_particle.y
            return math.sqrt(dx ** 2 + dy ** 2)