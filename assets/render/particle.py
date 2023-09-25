import math
import random
import pygame

class Particle:

    def __init__(self, screen_size: tuple):
        self.screen_size = screen_size
        self.x = random.randint(0, screen_size[0])
        self.y = random.randint(0, screen_size[1])
        self.radius = random.uniform(1.6, 2.3)
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-2.0, 2.0)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #self.color = (255, 255, 255)

    def render(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > self.screen_size[0]:
            self.vx *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if self.y < 0 or self.y > self.screen_size[1]:
            self.vy *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def distance_to(self, other_particle):
        dx = self.x - other_particle.x
        dy = self.y - other_particle.y
        return math.sqrt(dx ** 2 + dy ** 2)