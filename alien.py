import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''
    def __init__(self, ai_game):
        '''Initialize the alien and sets it starting position'''
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and get its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.original_image = self.image  # Store the original image for resizing

        # Resize the alien initially
        initial_size = (self.image.get_width() // 16, self.image.get_height() // 16)
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)


