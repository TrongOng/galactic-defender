import pygame
from pygame.sprite import Sprite
import random

class Particle(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))  # Red color for particles
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.lifetime = 60

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()

