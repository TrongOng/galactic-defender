import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Randomize dot size
        self.dot_size = random.random() * 3

        # Create a surface for the star with the random dot size
        self.image = pygame.Surface((self.dot_size, self.dot_size))
        self.image.fill((255, 255, 255))  # White color for stars

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)

    def update(self):
        # Add any movement or animation logic here
        pass

def create_star_field(ai_game, num_stars):
    stars = pygame.sprite.Group()
    for _ in range(num_stars):
        star = Star(ai_game)
        stars.add(star)
    return stars

