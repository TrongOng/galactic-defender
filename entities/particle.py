import pygame
from pygame.sprite import Sprite
import random

class Particle(Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        # Create the particle's image with the specified color
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        
        # Set the particle's position
        self.rect = self.image.get_rect(center=(x, y))
        
        # Set the particle's velocity
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        
        # Set the particle's initial lifetime
        self.lifetime = 60

    def update(self):
        # Update the particle's position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Decrease the particle's lifetime
        self.lifetime -= 1

        # Check if the particle's lifetime has expired
        if self.lifetime <= 0:
            self.kill()



